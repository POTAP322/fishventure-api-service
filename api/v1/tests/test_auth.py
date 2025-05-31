import time
from datetime import date, timedelta
from fastapi import status

def test_register_user(client):
    # Успешная регистрация
    response = client.post("/auth/register", json={
        "login": "testuser",
        "password": "testpass",
        "birth_date": str(date.today() - timedelta(days=365*13))  # 13 лет
    })
    assert response.status_code == status.HTTP_200_OK

    # Попытка повторной регистрации
    response = client.post("/auth/register", json={
        "login": "testuser",
        "password": "testpass",
        "birth_date": "2000-01-01"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_refresh_token(client):
    """Обновление токена"""
    # Регистрация и логин
    client.post("/auth/register", json={
        "login": "refresh_user",
        "password": "pass123",
        "birth_date": "2000-01-01"
    })
    login_res = client.post("/auth/login", json={
        "login": "refresh_user",
        "password": "pass123"
    })
    token = login_res.json()["auth_token"]

    # Небольшая задержка
    time.sleep(1)

    # Обновление токена
    response = client.post("/auth/refresh", json={
        "auth_token": token,
        "login": "refresh_user"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "auth_token" in response.json()
    assert response.json()["auth_token"] != token  # Проверяем, что токен изменился