from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from services.auth import decode_token
from repositories.base import IUserRepository, IURLRepository
from repositories.user_repository import SQLAlchemyUserRepository
from repositories.url_repository import SQLAlchemyURLRepository
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    # Takes: db session from get_db
    #constructs SQLAlchemyUserRepository with that session
    user_repo_obj = SQLAlchemyUserRepository(db)
    return user_repo_obj
    

def get_url_repository(db: Session = Depends(get_db)) -> IURLRepository:
    # Takes: db session from get_db
    # constructs SQLAlchemyURLRepository with that session
    url_repo_obj = SQLAlchemyURLRepository(db)
    return url_repo_obj
    
    

def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: IUserRepository = Depends(get_user_repository)
) -> User:
    user_id = decode_token(token)
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

async def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    user_repo: IUserRepository = Depends(get_user_repository)
) -> Optional[User]:
    if token is None:
        return None
    user_id = decode_token(token)
    return user_repo.get_by_id(user_id)