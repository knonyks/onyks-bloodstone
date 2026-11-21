import redis
import redis.asyncio as aioredis
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer

r = redis.Redis(host='redis', port=6379, db=0)
ar = aioredis.Redis(host='redis', port=6379, db=0, decode_responses=True)
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")