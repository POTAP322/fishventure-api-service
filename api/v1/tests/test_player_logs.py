from fastapi import status
from datetime import datetime, timedelta

def test_create_player_log(client, auth_token):
    """Создание лога игрока"""
    entered_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    exit_at = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')

    response = client.post("/player_logs/", json={
        "auth_token": auth_token,
        "login": "test_user",
        "entered_at": entered_at,
        "exit_at": exit_at
    })
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()

def test_invalid_player_log_time(client, auth_token):
    """Неверное время (выход раньше входа)"""
    response = client.post("/player_logs/", json={
        "auth_token": auth_token,
        "login": "test_user",
        "entered_at": "2023-01-01 12:00:00",
        "exit_at": "2023-01-01 10:00:00"  # Раньше входа
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "cannot be after" in response.text


