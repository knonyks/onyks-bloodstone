from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
import hashlib
import secrets
from schemas import Token, UserBase, UserRank
from redis_client import oauth2_scheme
from datetime import datetime, timedelta, timezone
import os
import jwt
from redis.asyncio import Redis
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from routers.common import get_db
import models

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise RuntimeError("Set SECRET_KEY to a random value of at least 32 characters")
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "15"))
REFRESH_TOKEN_DAYS = int(os.getenv("REFRESH_TOKEN_DAYS", "7"))
REFRESH_TTL = REFRESH_TOKEN_DAYS * 24 * 3600
REFRESH_COOKIE = "refresh_token"
REFRESH_COOKIE_PATH = "/api/auth"
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true").lower() == "true"


LOGIN_MAX_FAILS_PER_USER = int(os.getenv("LOGIN_MAX_FAILS_PER_USER", "5"))
LOGIN_MAX_FAILS_PER_IP = int(os.getenv("LOGIN_MAX_FAILS_PER_IP", "20"))
LOGIN_LOCK_SECONDS = int(os.getenv("LOGIN_LOCK_SECONDS", "900"))


from redis_client import oauth2_scheme, ar as redis


def _k_token(h: str) -> str:      return f"rt:{h}"
def _k_used(h: str) -> str:       return f"rt_used:{h}"
def _k_user_set(u: str) -> str:   return f"rt_user:{u}"
def _k_fail_user(u: str) -> str:  return f"login_fail:user:{u.lower()}"
def _k_fail_ip(ip: str) -> str:   return f"login_fail:ip:{ip}"

def _error(code: int, error_code: str, message: str, headers: dict | None = None) -> HTTPException:
    return HTTPException(status_code=code, detail={"error_code": error_code, "message": message}, headers=headers)

def is_expired(expiration_time: datetime | None) -> bool:
    if expiration_time is None:
        return False
    if expiration_time.date() == datetime(1970, 1, 1).date():
        return False
    if expiration_time.tzinfo is None:
        expiration_time = expiration_time.replace(tzinfo=timezone.utc)
    return expiration_time <= datetime.now(timezone.utc)


def create_access_token(sub: str) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {"sub": sub, "iat": now, "exp": now + timedelta(minutes=ACCESS_TOKEN_MINUTES), "type": "access"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


async def issue_refresh_token(username: str) -> str:
    token = secrets.token_urlsafe(48)
    h = _hash(token)
    async with redis.pipeline(transaction=True) as p:
        p.set(_k_token(h), username, ex=REFRESH_TTL)
        p.sadd(_k_user_set(username), h)
        p.expire(_k_user_set(username), REFRESH_TTL)
        await p.execute()
    return token


async def revoke_all_refresh_tokens(username: str) -> None:
    """Logs the user out on all devices.
    Also call this when changing/resetting the password or locking the account."""
    hashes = await redis.smembers(_k_user_set(username))
    async with redis.pipeline(transaction=True) as p:
        for h in hashes:
            p.delete(_k_token(h))
        p.delete(_k_user_set(username))
        await p.execute()


def set_refresh_cookie(response: Response, token: str):
    response.set_cookie(
        REFRESH_COOKIE, token,
        max_age=REFRESH_TTL,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path=REFRESH_COOKIE_PATH,
    )


def clear_refresh_cookie(response: Response):
    response.delete_cookie(
        REFRESH_COOKIE,
        path=REFRESH_COOKIE_PATH,
        secure=COOKIE_SECURE,
        httponly=True,
        samesite="lax",
    )


_dummy_hash: str | None = None

async def _get_dummy_hash(db: AsyncSession) -> str:
    global _dummy_hash
    if _dummy_hash is None:
        _dummy_hash = await db.scalar(text("SELECT crypt('dummy-password', gen_salt('bf', 10))"))
    return _dummy_hash


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"

def require_role(*ranks: UserRank):
    def checker(user: UserBase = Depends(get_current_user)) -> UserBase:
        if user.rank not in ranks:
            raise _error(403, "INSUFFICIENT_ROLE", "No sufficient role")
        return user
    return checker


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> UserBase:
    exc = _error(status.HTTP_401_UNAUTHORIZED, "INVALID_TOKEN", "Invalid token", {"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM],
            options={"require": ["exp", "sub", "iat"]},
        )
    except jwt.InvalidTokenError:
        raise exc
    username = payload.get("sub")
    if not isinstance(username, str) or payload.get("type") != "access":
        raise exc
    user = await db.scalar(select(models.User).where(models.User.username == username).limit(1))
    if user is None or is_expired(user.expiration_time):
        raise exc
    return UserBase(username=user.username,
                    rank=UserRank(user.rank.value),
                    expiration_time=user.expiration_time,
                    created_at=user.created_at)

@router.post("/auth/login", response_model=Token)
async def login(
    request: Request,
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    ip = _client_ip(request)
    fail_user_key = _k_fail_user(form.username)
    fail_ip_key = _k_fail_ip(ip)

    user_fails, ip_fails = await redis.mget(fail_user_key, fail_ip_key)
    if int(user_fails or 0) >= LOGIN_MAX_FAILS_PER_USER or int(ip_fails or 0) >= LOGIN_MAX_FAILS_PER_IP:
        raise _error(429, "TOO_MANY_ATTEMPTS", "Too many login attempts, try again later",
                     {"Retry-After": str(LOGIN_LOCK_SECONDS)})

    user = await db.scalar(select(models.User).where(models.User.username == form.username).limit(1))
    stored_hash = None
    if user is not None:
        stored_hash = getattr(user, "hashed_password", None) or getattr(user, "password", None)
    hash_valid = isinstance(stored_hash, str) and len(stored_hash) > 0
    hash_to_check = stored_hash if hash_valid else await _get_dummy_hash(db)

    password_matches = await db.scalar(
        select(func.crypt(form.password, hash_to_check) == hash_to_check)
    )

    if user is None or not hash_valid or not password_matches:
        async with redis.pipeline(transaction=True) as p:
            p.incr(fail_user_key)
            p.expire(fail_user_key, LOGIN_LOCK_SECONDS)
            p.incr(fail_ip_key)
            p.expire(fail_ip_key, LOGIN_LOCK_SECONDS)
            await p.execute()
        raise _error(401, "INVALID_CREDENTIALS", "Invalid username or password")

    await redis.delete(fail_user_key)

    if is_expired(user.expiration_time):
        raise _error(401, "ACCOUNT_EXPIRED", "Account expired")

    set_refresh_cookie(response, await issue_refresh_token(user.username))
    return Token(access_token=create_access_token(user.username))


@router.post("/auth/refresh", response_model=Token)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    if not refresh_token:
        raise _error(401, "NO_REFRESH_TOKEN", "Refresh cookie is missing")

    h = _hash(refresh_token)

    username = await redis.getdel(_k_token(h))

    if username is None:
        reused_by = await redis.get(_k_used(h))
        if reused_by is not None:
            await revoke_all_refresh_tokens(reused_by)
            clear_refresh_cookie(response)
            raise _error(401, "TOKEN_REUSED", "Token has already been used")
        clear_refresh_cookie(response)
        raise _error(401, "INVALID_REFRESH_TOKEN", "Unknown or expired token")

    async with redis.pipeline(transaction=True) as p:
        p.set(_k_used(h), username, ex=REFRESH_TTL)
        p.srem(_k_user_set(username), h)
        await p.execute()

    user = await db.scalar(select(models.User).where(models.User.username == username).limit(1))
    if user is None or is_expired(user.expiration_time):
        await revoke_all_refresh_tokens(username)
        clear_refresh_cookie(response)
        raise _error(401, "SESSION_EXPIRED", "Session expired")

    set_refresh_cookie(response, await issue_refresh_token(username))
    return Token(access_token=create_access_token(username))


@router.post("/auth/logout", status_code=204)
async def logout(response: Response, refresh_token: str | None = Cookie(default=None)):
    if refresh_token:
        h = _hash(refresh_token)
        username = await redis.getdel(_k_token(h))
        if username is not None:
            await redis.srem(_k_user_set(username), h)
    clear_refresh_cookie(response)


@router.post("/auth/logout-all", status_code=204)
async def logout_all(response: Response, user: UserBase = Depends(get_current_user)):
    await revoke_all_refresh_tokens(user.username)
    clear_refresh_cookie(response)


@router.get("/auth/me", response_model=UserBase)
async def me(user: UserBase = Depends(get_current_user)):
    return user