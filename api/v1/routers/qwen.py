from fastapi import APIRouter, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import QwenGenerateRequest
from ..services import QwenService
from ..security import verify_token

router = APIRouter(prefix="/qwen", tags=["Qwen"])
qwen_service = QwenService()


@router.post("/generate")
def generate_text(request: QwenGenerateRequest, db: Session = Depends(get_db)):
    #проверяем аутентификацию пользователя
    verify_token(request.auth_token, request.login, db)

    try:
        #вызываем Qwen API через сервис
        generated_text = qwen_service.generate_text(
            prompt=request.prompt,
            max_tokens=request.max_tokens
        )
        return {"text": generated_text}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Qwen API error")