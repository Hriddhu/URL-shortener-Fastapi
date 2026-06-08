from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from schemas.url import ShortenRequest, ShortResponse
from services.url import create, resolve
from deps import get_db
import os
from datetime import datetime

router = APIRouter()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

@router.post("/shorten", response_model=ShortResponse, status_code=201)
def shorten_url(body: ShortenRequest, db: Session = Depends(get_db)):
    url_obj = create(
        db=db,
        long_url=str(body.long_url),
        custom_slug=body.custom_slug,
        expires_in_days=body.expires_in_days
    )
    return ShortResponse(
        short_url=f"{BASE_URL}/{str(url_obj.slug)}",
        slug=str(url_obj.slug),
        created_at=url_obj.created_at if url_obj.created_at else datetime.utcnow(),
        expires_at=url_obj.expires_at if url_obj.expires_at else None
        )

@router.get("/{slug}")
def redirect_url(slug: str, db: Session = Depends(get_db)):
    long_url = str(resolve(db, slug))
    return RedirectResponse(url=long_url, status_code=302)