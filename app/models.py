from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from .database import Base
from app.utils.time_tracker import get_moscow_time

class Player(Base):
    __tablename__ = "Players"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    hash_password = Column(String(100), nullable=False)
    auth_token = Column(String(500), nullable=True)
    created_at = Column(TIMESTAMP, default=get_moscow_time)

class Logs(Base):
    __tablename__ = "Logs"
    id = Column(Integer, primary_key=True)
    log_text = Column(String(400))
    created_at = Column(TIMESTAMP, default=get_moscow_time)

class PlayerLog(Base):
    __tablename__ = "PlayerLogs"
    id = Column(Integer, primary_key=True)
    Players_id = Column(Integer, ForeignKey("Players.id", ondelete="CASCADE"))
    log_text = Column(String(400))
    created_at = Column(TIMESTAMP, default=get_moscow_time)
    entered_at = Column(TIMESTAMP, default=get_moscow_time)
    exit_at = Column(TIMESTAMP, default=get_moscow_time)