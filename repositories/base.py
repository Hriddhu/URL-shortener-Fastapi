from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from models import URL, User


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch a user by primary key. Return None if not found —
        do NOT raise an exception here. Repositories report absence,
        services decide whether absence is an error."""
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Used by both registration (check for duplicates) and login
        (find the account to verify password against)."""
        ...

    @abstractmethod
    def create(self, email: str, hashed_pwd: str) -> User:
        """Persist a new user row and return the created object
        (with its DB-assigned id populated)."""
        ...


class IURLRepository(ABC):
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[URL]:
        """Used by both collision-checking (does this custom slug
        already exist?) and redirect resolution (find the target URL)."""
        ...

    @abstractmethod
    def create(self, long_url: str, user_id: Optional[int], expires_at: Optional[datetime]) -> URL:
        """Insert a new URL row WITHOUT a slug yet — slug generation
        depends on the auto-incremented id, which only exists after
        this insert. This is why create and set_slug are separate."""
        ...

    @abstractmethod
    def set_slug(self, url: URL, slug: str) -> URL:
        """Second step of creation — write the computed slug onto
        an already-persisted row."""
        ...

    @abstractmethod
    def increment_clicks(self, url: URL) -> URL:
        """Bump the click counter. Kept as its own method (not buried
        inside get_by_slug) because incrementing clicks is a WRITE,
        and a repository method's name should tell you whether it
        mutates the database."""
        ...