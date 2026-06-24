from typing import Optional
from sqlalchemy.orm import Session
from models import User
from repositories.base import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):

    def __init__(self, db: Session):
        # Does: stores it as self.db so all methods can use it
        self.db= db
      

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()


    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email==email).first()
        

    def create(self, email: str, hashed_pwd: str) -> User:

        user = User(email=email, hashed_pwd= hashed_pwd)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
        
    
        