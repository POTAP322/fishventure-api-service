from sqlalchemy.orm import Session
from .models import Player, PlayerLogs,Logs
from .schemas import RegisterRequest, LogCreateRequest, PlayerLogCreateRequest
from .security import hash_password, verify_password, create_access_token
from datetime import datetime
from api.utils.time_tracker import get_moscow_time

class AuthService:
    def register_user(self, db: Session, user_data: RegisterRequest) -> Player:
        existing_user = db.query(Player).filter_by(username=user_data.login).first()
        if existing_user:
            raise ValueError("User already exists")

        hashed_password = hash_password(user_data.password)
        new_user = Player(username=user_data.login, hash_password=hashed_password, birth_date=user_data.birth_date)
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


class LogsService:
    def save_log(self, db: Session, log_data: LogCreateRequest) -> Logs:
        new_log = Logs(log_text=log_data.log_text)
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log

class PlayerLogsService:
    def save_player_log(self, db: Session, player_log_data: PlayerLogCreateRequest) -> PlayerLogs:
        new_log = PlayerLogs(
            player_id=player_log_data.player_id,
            entered_at=player_log_data.entered_at,
            exit_at=player_log_data.exit_at
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log