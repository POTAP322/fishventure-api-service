import requests
from sqlalchemy.orm import Session
from .models import Player, PlayerLogs,Logs
from .schemas import RegisterRequest, LogCreateRequest, PlayerLogCreateRequest, RefreshRequest
from .security import hash_password, verify_password, create_access_token
from .config import settings

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

    def refresh_token(self, db: Session, user_data: RefreshRequest) -> Player:
        user = db.query(Player).filter_by(username=user_data.login).first()
        if not user:
            raise ValueError("User not found")
        #проверяем, совпадает ли переданный токен с текущим токеном пользователя
        if user.auth_token != user_data.auth_token:
            raise ValueError("Invalid token")

        # Генерация нового токена
        access_token = create_access_token(data={"sub": str(user.id)})
        # Обновление поля auth_token в базе данных
        user.auth_token = access_token
        db.commit()
        db.refresh(user)
        return user




class LogsService:
    def save_log(self, db: Session, log_data: LogCreateRequest) -> Logs:
        new_log = Logs(log_text=log_data.log_text)
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log

class PlayerLogsService:
    def save_player_log(self, db: Session, player_log_data: PlayerLogCreateRequest) -> PlayerLogs:
        player = db.query(Player).filter_by(username=player_log_data.login).first()
        if not player:
            raise ValueError("User with this login does not exist")
        new_log = PlayerLogs(
            player_id=player.id,
            entered_at=player_log_data.entered_at,
            exit_at=player_log_data.exit_at
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log


class QwenService:
    def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        headers = {
            "Authorization": f"Bearer {settings.QWEN_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": settings.QWEN_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }
        response = requests.post(
            f"{settings.QWEN_API_URL}/chat/completions",
            json=data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

