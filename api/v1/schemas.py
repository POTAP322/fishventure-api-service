from pydantic import BaseModel
from typing import List, Optional

from datetime import date



class RegisterRequest(BaseModel):
    login: str
    password: str
    birth_date: date

class LoginRequest(BaseModel):
    login: str
    password: str


class PlayerLogCreateRequest(BaseModel):
    auth_token: str
    player_id: int
    entered_at: date
    exit_at: date

class PlayerLogResponse(BaseModel):
    id: int
    entered_at: date
    exit_at: date


class LogCreateRequest(BaseModel):
    log_text: str

class LogCreateResponse(BaseModel):
    id: int
    log_text: str
    created_at: str


class TokenResponse(BaseModel):
    auth_token: str
class PlayerResponse(BaseModel):
    id: int
    username: str
    birth_date: date