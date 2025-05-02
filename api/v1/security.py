from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from .config import settings
from sqlalchemy.orm import Session
from api.v1.database import get_db
from api.v1.models import Player
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str, login: str, db: Session) -> int:
    try:
        # декодируем токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # проверка времени истечения
        exp = payload.get("exp")
        if exp is None or datetime.utcnow() > datetime.utcfromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token expired")

        #находим пользователя по логину
        user = db.query(Player).filter_by(username=login).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # проверяем, что user_id из токена совпадает с ID пользователя в базе данных
        if int(user_id) != user.id:
            raise HTTPException(status_code=401, detail="Token does not match the user")

        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")