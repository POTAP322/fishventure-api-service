from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import AuthService
from ..schemas import RegisterRequest, LoginRequest, TokenResponse, PlayerResponse

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()

@router.post("/register", response_model = PlayerResponse)
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    try:
        new_user = auth_service.register_user(db, user)
        return {"id": new_user.id, "username": new_user.username}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/login", response_model=TokenResponse)
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = auth_service.authenticate_user(db, user_data.login, user_data.password)
        token = auth_service.generate_token(user.id)
        return {"auth_token": token}
    except ValueError as e:
        raise HTTPException(400, str(e))