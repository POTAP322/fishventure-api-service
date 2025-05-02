from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Logs
from ..schemas import LogCreateRequest, LogCreateResponse
from ..security import verify_token
from ..services import LogsService
from datetime import datetime

router = APIRouter(prefix="/logs", tags=["Logs"])
log_service = LogsService()
@router.post("/", response_model=LogCreateResponse)
def create_log(log: LogCreateRequest, db: Session = Depends(get_db)):
    verify_token(log.auth_token, log.login, db)
    try:
        new_log = log_service.save_log(db, log)
        created_at_str = new_log.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return {"id": new_log.id, "log_text": new_log.log_text, "created_at": created_at_str}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/{log_id}", response_model=LogCreateResponse)
def get_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(Logs).filter(Logs.id == log_id).first()
    created_at_str = log.created_at.strftime('%Y-%m-%d %H:%M:%S')
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"id": log.id, "log_text": log.log_text, "created_at": created_at_str}

@router.get("/", response_model=List[LogCreateResponse])
def list_logs(db: Session = Depends(get_db)):
    logs = db.query(Logs).all()
    # Формирование списка ответов
    response = []
    for log in logs:
        created_at_str = log.created_at.strftime('%Y-%m-%d %H:%M:%S')
        response.append({
            "id": log.id,
            "log_text": log.log_text,
            "created_at": created_at_str
        })

    return response