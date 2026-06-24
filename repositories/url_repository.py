from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from models import URL
from repositories.base import IURLRepository


class SQLAlchemyURLRepository(IURLRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_by_slug(self, slug: str) -> Optional[URL]:
        return self.db.query(URL).filter(URL.slug == slug).first()

    def create(self, long_url: str, user_id: Optional[int], expires_at: Optional[datetime]) -> URL:
        
        url_obj = URL(long_url=long_url, user_id=user_id, expires_at=expires_at)
        self.db.add(url_obj)
        self.db.commit()
        self.db.refresh(url_obj)
    
        return url_obj

    def set_slug(self, url_obj: URL, slug: str) -> URL:
        url_obj.slug= slug
        self.db.commit()
        self.db.refresh(url_obj)
        return url_obj
        

    def increment_clicks(self, url_obj: URL) -> URL:
        current_clicks = url_obj.clicks
        if current_clicks is None:
            url_obj.clicks = 1
        else:
            url_obj.clicks += 1
        self.db.commit()
        return url_obj