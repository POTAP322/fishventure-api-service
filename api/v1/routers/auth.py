from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.v1.database import get_db
from ..services import AuthService
from ..schemas import RegisterRequest, LoginRequest, TokenResponse, PlayerResponse, RefreshRequest
from ..security import verify_token

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()

@router.post("/register", response_model = PlayerResponse)
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    try:
        new_user = auth_service.register_user(db, user)
        return {"id": new_user.id, "login": new_user.username, "birth_date": new_user.birth_date}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/login", response_model=TokenResponse)
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = auth_service.authenticate_user(db, user_data.login, user_data.password)
        return {"auth_token": user.auth_token}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/refresh", response_model=TokenResponse)
def refresh(user_data: RefreshRequest, db: Session = Depends(get_db)):
    try:
        #verify_token(user_data.auth_token, user_data.login, db)
        user = auth_service.refresh_token(db, user_data)
        return {"auth_token": user.auth_token}
    except ValueError as e:
        raise HTTPException(400, str(e))