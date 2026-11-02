from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
import hashlib
import secrets
from fastapi import Response
from schemas import Token, UserBase, UserRank
from fastapi.security import OAuth2PasswordBearer
from redis_client import password_hash, oauth2_scheme
from datetime import datetime, timedelta, timezone
import os
import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from routers.common import get_db
import models
from fastapi import FastAPI, Depends, HTTPException, status, Cookie, Response

router = APIRouter()
refresh_tokens: dict[str, dict] = {}

SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "15"))
REFRESH_TOKEN_DAYS = int(os.getenv("REFRESH_TOKEN_DAYS", "7"))
REFRESH_COOKIE = "refresh_token"
REFRESH_COOKIE_PATH = "/api/auth"

def is_expired(expiration_time: datetime | None) -> bool:
    if expiration_time is None:
        return False
    if expiration_time.date() == datetime(1970, 1, 1).date():
        return False
    if expiration_time.tzinfo is None:
        expiration_time = expiration_time.replace(tzinfo=timezone.utc)
    return expiration_time <= datetime.now(timezone.utc)

def create_access_token(sub: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    return jwt.encode({"sub": sub, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def _hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def issue_refresh_token(username: str) -> str:
    token = secrets.token_urlsafe(48)
    refresh_tokens[_hash(token)] = {
        "username": username,
        "expires": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_DAYS),
        "revoked": False,
    }
    return token

def set_refresh_cookie(response: Response, token: str):
    response.set_cookie(
        REFRESH_COOKIE, token,
        max_age=REFRESH_TOKEN_DAYS * 24 * 3600,
        httponly=True,
        secure=False,
        samesite="lax",
        path=REFRESH_COOKIE_PATH,
    )

def require_role(*ranks: UserRank):
    def checker(user: UserBase = Depends(get_current_user)) -> UserBase:
        if user.rank not in ranks:
            raise HTTPException(status_code=403, detail={
                "error_code": "INSUFFICIENT_ROLE",
                "message": "No sufficient role"
            })
        return user
    return checker

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> UserBase:
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "error_code": "INVALID_TOKEN",
            "message": "Invalid token"
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except jwt.InvalidTokenError:
        raise exc
    if not isinstance(username, str):
        raise exc
    user = await db.scalar(select(models.User).where(models.User.username == username).limit(1))
    if user is None or is_expired(user.expiration_time):
        raise exc
    return UserBase(username = user.username, 
                    rank = UserRank(user.rank.value), 
                    expiration_time = user.expiration_time,
                    created_at = user.created_at)

@router.post("/auth/login", response_model=Token)
async def login(
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await db.scalar(select(models.User).where(models.User.username == form.username).limit(1))
    if user is None:
        raise HTTPException(status_code=401, detail={
            "error_code": "INVALID_CREDENTIALS",
            "message": "Invalid username or password"
        })
    hashed_password = getattr(user, "hashed_password", None) or getattr(user, "password", None)
    if not isinstance(hashed_password, str) or not hashed_password:
        raise HTTPException(status_code=401, detail={
            "error_code": "INVALID_CREDENTIALS",
            "message": "Invalid username or password"
        })
    password_matches = await db.scalar(
        select(func.crypt(form.password, hashed_password) == hashed_password)
    )
    if not password_matches:
        raise HTTPException(status_code=401, detail={
            "error_code": "INVALID_CREDENTIALS",
            "message": "Invalid username or password"
        })
    if is_expired(user.expiration_time):
        raise HTTPException(status_code=401, detail={
            "error_code": "ACCOUNT_EXPIRED",
            "message": "Account expired"
        })
    set_refresh_cookie(response, issue_refresh_token(user.username))
    return Token(access_token=create_access_token(user.username))

@router.post("/auth/refresh", response_model=Token)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Brak ciasteczka")

    stored = refresh_tokens.get(_hash(refresh_token))
    if stored is None:
        raise HTTPException(status_code=401, detail="Nieznany token")
    if stored["revoked"]:
        for t in refresh_tokens.values():
            if t["username"] == stored["username"]:
                t["revoked"] = True
        raise HTTPException(status_code=401, detail="Token już użyty")
    now = datetime.now(timezone.utc)
    if stored["expires"] < now:
        raise HTTPException(status_code=401, detail="Token wygasł")
    user = await db.scalar(
        select(models.User).where(models.User.username == stored["username"]).limit(1)
    )
    if user is None or is_expired(user.expiration_time):
        raise HTTPException(status_code=401, detail="Sesja wygasła")

    stored["revoked"] = True                                   # rotacja
    set_refresh_cookie(response, issue_refresh_token(stored["username"]))
    
    return Token(access_token=create_access_token(stored["username"]))

@router.post("/auth/logout", status_code=204)
async def logout(response: Response, refresh_token: str | None = Cookie(default=None)):
    if refresh_token and (stored := refresh_tokens.get(_hash(refresh_token))):
        stored["revoked"] = True
    response.delete_cookie(REFRESH_COOKIE, path=REFRESH_COOKIE_PATH)

@router.get("/auth/me", response_model=UserBase)
async def me(user: UserBase = Depends(get_current_user)):
    print(user)
    return user

@router.get("/secret")
async def secret(user: UserBase = Depends(require_role(UserRank.ADMIN))):
    return {"msg": f"Cześć {user.username}, to chroniony endpoint"}