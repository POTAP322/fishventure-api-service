from sqlalchemy.orm import Session
from .models import Player, PlayerLogs
from .schemas import RegisterRequest
from .security import hash_password, verify_password, create_access_token
from datetime import datetime
from app.utils.time_tracker import get_moscow_time

class AuthService:
    def register_user(self, db: Session, user_data: RegisterRequest) -> Player:
        existing_user = db.query(Player).filter_by(username=user_data.login).first()
        if existing_user:
            raise ValueError("User already exists")

        hashed_password = hash_password(user_data.hash_password)
        new_user = Player(username=user_data.login, hash_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def authenticate_user(self, db: Session, username: str, password: str) -> Player:
        user = db.query(Player).filter_by(username=username).first()
        if not user or not verify_password(password, user.hash_password):
            raise ValueError("Invalid credentials")

        # Генерация нового токена
        access_token = create_access_token(data={"sub": str(user.id)})

        # Обновление поля auth_token в базе данных
        user.auth_token = access_token
        db.commit()
        db.refresh(user)

        return user

    def generate_token(self, user_id: int) -> str:
        return create_access_token(data={"sub": str(user_id)})


class PlayerLogsService:
    def save_player_logs(self, db: Session, user_id: int, data: list[dict]) -> None:
        for entry in data:
            log_entry = PlayerLogs(
                Players_id=user_id,
                log_text=entry.get("log_text"),
                created_at=get_moscow_time(),
                entered_at=get_moscow_time(),
                exit_at=get_moscow_time()
            )
            db.add(log_entry)
        db.commit()