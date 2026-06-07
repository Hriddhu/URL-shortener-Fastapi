import os
from datetime import datetime, timedelta
from typing import Optional, cast  # Added cast here
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import URL

load_dotenv()

SECRET_KEY_RAW = os.getenv("SECRET_KEY")
if not SECRET_KEY_RAW:
    raise RuntimeError("SECRET_KEY is missing from environment variables!")

SECRET_KEY = int(SECRET_KEY_RAW)
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode(id: int) -> str:
    id = id ^ SECRET_KEY
    result = []
    if id == 0:
        return ALPHABET[0]
    
    while id > 0:
        remainder = id % 62
        result.append(ALPHABET[remainder])
        id = id // 62

    return "".join(reversed(result))

def create(
    db: Session,
    long_url: str,
    custom_slug: Optional[str] = None,
    expires_in_days: Optional[int] = None,
    user_id: Optional[int] = None
):
    if custom_slug:
        does_it_exist = db.query(URL).filter(URL.slug == custom_slug).first()
        if does_it_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug already taken")

    expires_at = None
    if expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    url_obj = URL(long_url=long_url, user_id=user_id, expires_at=expires_at)
    db.add(url_obj)
    db.commit()
    db.refresh(url_obj)
    
    # FIX: Cast url_obj.id to int so Pylance knows it's not a 'Column' object
    object_id = cast(int, url_obj.id)
    if not object_id:
        raise HTTPException(status_code=500, detail="Database failed to generate an ID")
        
    slug = custom_slug if custom_slug else encode(object_id)
    
    # FIX: Cast the slug setting to Any or bypass strict linting using an explicit assignment
    url_obj.slug = slug  # type: ignore
    db.commit()
    db.refresh(url_obj)
    
    return url_obj

def resolve(db: Session, slug: str):
    url_obj = db.query(URL).filter(URL.slug == slug).first()
    
    if not url_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    
    # FIX: Cast conditions to bool so Pylance knows they resolve safely in the 'if' checks
    is_active = cast(bool, url_obj.is_active)
    if not is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link is deactivated")
    
    expires_at = cast(Optional[datetime], url_obj.expires_at)
    if expires_at is not None and expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link expired")
    
    # FIX: Use type: ignore for mutations on old-style SQLAlchemy columns 
    # to silence the Pylance type-checking proxy mismatch
    current_clicks = cast(Optional[int], url_obj.clicks)
    if current_clicks is None:
        url_obj.clicks = 0  # type: ignore
    else:
        url_obj.clicks = current_clicks + 1  # type: ignore
    
    db.commit()
    return url_obj.long_url