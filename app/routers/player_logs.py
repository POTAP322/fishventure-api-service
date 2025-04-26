from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import PlayerLogsService
from ..schemas import PlayerLogRequest
from ..security import verify_token

router = APIRouter(prefix="/player_logs", tags=["Player_logs"])
player_logs_service = PlayerLogsService()

@router.post("")
def save_player_logs(
    player_logs: PlayerLogRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    try:
        player_logs_service.save_player_logs(db, user_id, player_logs.data)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(500, str(e))

