from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True
    id           = Column(Integer, primary_key=True)
    email        = Column(String, unique=True, nullable=False)
    hashed_pwd   = Column(String, nullable=False)
    created_at   = Column(DateTime, server_default=func.now())

class URL(Base):
    __tablename__ = "urls"
    __allow_unmapped__ = True
    id         = Column(Integer, primary_key=True, index=True)
    slug       = Column(String, unique=True, index=True)   # indexed — this gets queried on EVERY redirect
    long_url   = Column(Text, nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=True)
    is_active  = Column(Boolean, default=True)
    clicks     = Column(Integer, default=0)