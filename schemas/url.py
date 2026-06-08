from pydantic import HttpUrl, BaseModel, Field
from typing import Optional
from datetime import datetime

class ShortenRequest(BaseModel):
    long_url: HttpUrl
    custom_slug: Optional[str] = Field(default=None, min_length=1, max_length=30)
    expires_in_days: Optional[int] = Field(default=None, ge=1, le=365)

class ShortResponse(BaseModel):
    short_url: str
    slug: str
    created_at: datetime
    expires_at: Optional[datetime] = None

    model_config = {"from_attributes": True}