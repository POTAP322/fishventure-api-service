from pydantic import BaseModel, Field
from typing import List, Optional
from api.v1.utils.time_tracker import get_moscow_time

from datetime import date, datetime


class RegisterRequest(BaseModel):
    login: str
    password: str
    birth_date: date

class LoginRequest(BaseModel):
    login: str
    password: str


class PlayerLogCreateRequest(BaseModel):
    auth_token: str
    login: str
    entered_at: datetime = Field(
        default_factory=get_moscow_time(),
        example=get_moscow_time().isoformat()
    )
    exit_at: datetime = Field(
        default_factory=get_moscow_time(),
        example=get_moscow_time().isoformat()
    )

class PlayerLogResponse(BaseModel):
    id: int
    entered_at: datetime = Field(
        default_factory=get_moscow_time(),
    )
    exit_at: datetime = Field(
        default_factory=get_moscow_time(),
    )


class LogCreateRequest(BaseModel):
    auth_token: str
    login: str
    log_text: str

class LogCreateResponse(BaseModel):
    id: int
    log_text: str
    created_at: str


class TokenResponse(BaseModel):
    auth_token: str


class RefreshRequest(BaseModel):
    auth_token: str
    login: str


class QwenGenerateRequest(BaseModel):
    auth_token: str
    login: str
    prompt: str
    max_tokens: int = 600