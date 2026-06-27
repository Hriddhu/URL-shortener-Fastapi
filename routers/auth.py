from fastapi import APIRouter, Depends
from schemas.user import RegisterRequest, LoginRequest, UserResponse, TokenResponse
from services.auth import create_user, authenticate_user, create_token
from deps import get_user_repository
from repositories.base import IUserRepository


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(body: RegisterRequest, user_repo: IUserRepository = Depends(get_user_repository)):
    user = create_user(user_repo, email=body.email, password=body.password)
    return UserResponse(
        id=int(user.id),
        email=str(user.email),
        created_at=user.created_at
    )

@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, user_repo: IUserRepository = Depends(get_user_repository)):
    user = authenticate_user(user_repo, body.email, body.password)
    token = create_token(int(user.id))
    return TokenResponse(access_token=token, token_type="bearer")