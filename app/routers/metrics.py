from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import MetricsService
from ..schemas import MetricsRequest
from ..security import verify_token

router = APIRouter(prefix="/metrics", tags=["Metrics"])
metrics_service = MetricsService()

@router.post("")
def save_metrics(
    metrics: MetricsRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    try:
        metrics_service.save_metrics(db, user_id, metrics.data)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(500, str(e))