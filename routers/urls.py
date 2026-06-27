from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from schemas.url import ShortenRequest, ShortResponse
from services.url import create, resolve
from deps import IURLRepository, get_url_repository, get_optional_user
import os
from typing import Optional
from models import User
from datetime import datetime

router = APIRouter()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

@router.post("/shorten", response_model=ShortResponse, status_code=201)
def shorten_url(
    body: ShortenRequest,
    url_repo: IURLRepository = Depends(get_url_repository),
    current_user: Optional[User] = Depends(get_optional_user)  # optional auth
):
    url_obj = create(
        url_repo,
        long_url=str(body.long_url),
        custom_slug=body.custom_slug,
        expires_in_days=body.expires_in_days,
        user_id=current_user.id if current_user else None 
    )
    return ShortResponse(
        short_url=f"{BASE_URL}/{str(url_obj.slug)}",
        slug=str(url_obj.slug),
        created_at=url_obj.created_at if url_obj.created_at else datetime.utcnow(),
        expires_at=url_obj.expires_at if url_obj.expires_at else None
     )

@router.get("/{slug}")
def redirect_url(slug: str, url_repo: IURLRepository = Depends(get_url_repository)):
    long_url = str(resolve(url_repo, slug))
    return RedirectResponse(url=long_url, status_code=302)