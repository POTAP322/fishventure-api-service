from pydantic import BaseModel
from typing import List, Optional


class RegisterRequest(BaseModel):
    login: str
    hash_password: str

class LoginRequest(BaseModel):
    login: str
    hash_password: str

class TokenResponse(BaseModel):
    auth_token: str

class MetricsRequest(BaseModel):
    auth_token: str
    data: List[dict]

class LogCreate(BaseModel):
    log_text: str
    created_at: Optional[str] = None

class LogResponse(BaseModel):
    id: int
    log_text: str
    created_at: str