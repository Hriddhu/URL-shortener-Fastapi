import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, status
from typing import Optional
from repositories.base import IURLRepository

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
    url_repo:IURLRepository,
    long_url: str,
    custom_slug: Optional[str] = None,
    expires_in_days: Optional[int] = None,
    user_id: Optional[int] = None
):
    if custom_slug:
        existing = url_repo.get_by_slug(custom_slug)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug already taken")

    expires_at = None
    if expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    url_obj= url_repo.create(long_url=long_url, user_id=user_id, expires_at=expires_at)
    
    object_id = url_obj.id
    if not object_id:
        raise HTTPException(status_code=500, detail="Database failed to generate an ID")
        
    slug = custom_slug if custom_slug else encode(object_id)
    
    url_obj= url_repo.set_slug(url_obj, slug) 

    return url_obj


def resolve(url_repo:IURLRepository, slug: str):
    url_obj = url_repo.get_by_slug(slug)
    
    if not url_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    
    is_active = cast(bool, url_obj.is_active)
    if not is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link is deactivated")
    
    expires_at = Optional[datetime], url_obj.expires_at
    if expires_at is not None and expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link expired")
    
    url_obj= url_repo.increment_clicks(url_obj)
    return url_obj.long_url