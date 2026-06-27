import os
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from models import User
from repositories.base import IUserRepository, IURLRepository

JWT_SECRET = os.getenv("JWT_SECRET", "changemeinproduction")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def create_user(user_repo: IUserRepository, email: str, password: str) -> User:
    existing = user_repo.get_by_email(email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return user_repo.create(email= email, hashed_pwd= hash_password(password))

def authenticate_user(user_repo:IUserRepository, email: str, password: str) -> User:
    user = user_repo.get_by_email(email)
    if not user or not verify_password(password, str(user.hashed_pwd)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user