from fastapi import status
import pytest

def test_generate_text_success(client, auth_token):
    """Успешная генерация текста"""
    response = client.post("/qwen/generate", json={
        "auth_token": auth_token,
        "login": "test_user",
        "prompt": "say hello",
        "max_tokens": 50
    })
    assert response.status_code == status.HTTP_200_OK
    assert "text" in response.json()

def test_generate_text_unauthorized(client):
    """Неавторизованный доступ"""
    response = client.post("/qwen/generate", json={
        "auth_token": "invalid_token",
        "login": "nonexistent",
        "prompt": "Test prompt",
        "max_tokens": 50
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
