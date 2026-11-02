import redis
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer

r = redis.Redis(host='redis', port=6379, db=0)
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")