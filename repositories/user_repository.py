from typing import Optional
from sqlalchemy.orm import Session
from models import User
from repositories.base import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):

    def __init__(self, db: Session):
        # Takes: a SQLAlchemy Session object
        # Does: stores it as self.db so all methods can use it
        self.db= db
        # This is constructor injection — the session comes from outside,
        # not created here. That's what makes this class testable/swappable.
        ...

    def get_by_id(self, user_id: int) -> Optional[User]:
        self.user_id= db.query(User).filter(User.id == user_id).first()


    def get_by_email(self, email: str) -> Optional[User]:
        # hint: same pattern, filter on User.email
        self.email= db.query(User).filter(User.email==email).first()
        ...

    def create(self, email: str, hashed_pwd: str) -> User:
        # hint: build User(...), db.add, db.commit, db.refresh, return it
        # these lines currently live in services/auth.py inside create_user()
        # you are moving them here
        ...