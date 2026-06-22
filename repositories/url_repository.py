from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from models import URL
from repositories.base import IURLRepository


class SQLAlchemyURLRepository(IURLRepository):

    def __init__(self, db: Session):
        # same idea as user repository — store db as self.db
        ...

    def get_by_slug(self, slug: str) -> Optional[URL]:
        # hint: db.query(URL).filter(URL.slug == slug).first()
        ...

    def create(self, long_url: str, user_id: Optional[int], expires_at: Optional[datetime]) -> URL:
        # hint: these lines currently live in services/url.py inside create()
        # URL(...), db.add, db.commit, db.refresh, return url_obj
        # do NOT set slug here — it will be None after this call, that's fine
        ...

    def set_slug(self, url: URL, slug: str) -> URL:
        # hint: url.slug = slug, db.commit, db.refresh, return url
        # this handles the second commit currently in services/url.py
        ...

    def increment_clicks(self, url: URL) -> URL:
        # hint: read url.clicks, handle None, add 1, db.commit, return url
        # these lines currently live in services/url.py inside resolve()
        ...