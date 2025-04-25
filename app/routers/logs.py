from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Logs
from ..schemas import LogCreate, LogResponse
from datetime import datetime

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.post("/", response_model=LogResponse)
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    db_log = Logs(
        log_text=log.log_text,
        created_at=log.created_at or datetime.utcnow().isoformat()
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/{log_id}", response_model=LogResponse)
def get_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(Logs).filter(Logs.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

@router.get("/", response_model=List[LogResponse])
def list_logs(db: Session = Depends(get_db)):
    logs = db.query(Logs).all()
    return logs