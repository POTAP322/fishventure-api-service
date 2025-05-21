from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import PlayerLogs
from ..schemas import PlayerLogCreateRequest, PlayerLogResponse
from ..security import verify_token
from ..services import PlayerLogsService
from datetime import datetime

router = APIRouter(prefix="/player_logs", tags=["PlayerLogs"])
player_logs_service = PlayerLogsService()

@router.post("/", response_model=PlayerLogResponse)
def create_player_log(player_log: PlayerLogCreateRequest, db: Session = Depends(get_db)):
    verify_token(player_log.auth_token, player_log.login, db)
    try:
        new_player_log = player_logs_service.save_player_log(db, player_log)
        return {
            "id": new_player_log.id,
            "player_id": new_player_log.player_id,
            "entered_at": new_player_log.entered_at,
            "exit_at": new_player_log.exit_at
        }
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/{log_id}", response_model=PlayerLogResponse)
def get_player_log(log_id: int, db: Session = Depends(get_db)):
    player_log = db.query(PlayerLogs).filter(PlayerLogs.id == log_id).first()
    if not player_log:
        raise HTTPException(status_code=404, detail="Player log not found")
    entered_at_str = player_log.entered_at.strftime('%Y-%m-%d')
    exit_at_str = player_log.exit_at.strftime('%Y-%m-%d')
    return {
        "id": player_log.id,
        "player_id": player_log.player_id,
        "entered_at": entered_at_str,
        "exit_at": exit_at_str
    }

@router.get("/", response_model=List[PlayerLogResponse])
def list_player_logs(db: Session = Depends(get_db)):
    player_logs = db.query(PlayerLogs).all()
    return [log.__dict__ for log in player_logs]