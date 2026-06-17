from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import RegisterRequest, LoginRequest, UserResponse, TokenResponse
from services.auth import create_user, authenticate_user, create_token
from deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    user = create_user(db, body.email, body.password)
    return UserResponse(
        id=int(user.id),
        email=str(user.email),
        created_at=user.created_at
    )

@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, body.email, body.password)
    token = create_token(int(user.id))
    return TokenResponse(access_token=token, token_type="bearer")