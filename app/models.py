from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from .database import Base

class Player(Base):
    __tablename__ = "Players"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    hash_password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP)

class Logs(Base):
    __tablename__ = "Logs"
    id = Column(Integer, primary_key=True)
    log_text = Column(String(400))
    created_at = Column(TIMESTAMP)

class PlayerLog(Base):
    __tablename__ = "PlayerLogs"
    id = Column(Integer, primary_key=True)
    Players_id = Column(Integer, ForeignKey("Players.id", ondelete="CASCADE"))
    log_text = Column(String(400))
    created_at = Column(TIMESTAMP)
    entered_at = Column(TIMESTAMP)
    exit_at = Column(TIMESTAMP)