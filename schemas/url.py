from pydantic import HttpUrl, BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta, timezone

class ShortenRequest(BaseModel):
    long_url: HttpUrl
    custom_slug: Optional[str]=Field(default=None, description="If you have a custom slug", min_length=1, max_length=30)
    expires_in_days: Optional[int]= Field(default=None, le=1, gt=365)
    
    model_config={'from_attributes': True}
    
class ShortResponse(BaseModel):
    long_url: Optional[str]=Field(description="The long url that needs to be shortened")
    slug: str
    created_at: datetime
    expires_at: Optional[datetime]= None
   
    
    model_config={'from_attributes': True}
    
    
    