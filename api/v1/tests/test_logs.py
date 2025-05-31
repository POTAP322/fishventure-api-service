from fastapi import status
from datetime import datetime

def test_create_log_unauthorized(client):
    """Создание лога без авторизации"""
    response = client.post("/logs/", json={
        "auth_token": "invalid_token",
        "login": "nonexistent",
        "log_text": "Test log"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_and_get_log(client, auth_token):
    """Полный цикл создания и получения лога"""
    # Создание
    response = client.post("/logs/", json={
        "auth_token": auth_token,
        "login": "test_user",
        "log_text": "Sample log message"
    })
    assert response.status_code == status.HTTP_200_OK
    log_id = response.json()["id"]

    # Получение
    response = client.get(f"/logs/{log_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["log_text"] == "Sample log message"
    # Проверяем формат даты
    assert isinstance(response.json()["created_at"], str)
    datetime.strptime(response.json()["created_at"], '%Y-%m-%d %H:%M:%S')

def test_get_nonexistent_log(client):
    """Получение несуществующего лога"""
    response = client.get("/logs/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_logs(client, auth_token):
    """Тестирование списка логов"""
    # Создаем несколько логов
    for i in range(3):
        client.post("/logs/", json={
            "auth_token": auth_token,
            "login": "test_user",
            "log_text": f"Log {i}"
        })

    # Получаем список
    response = client.get("/logs/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 3
    # Проверяем формат дат в списке
    for log in response.json():
        datetime.strptime(log["created_at"], '%Y-%m-%d %H:%M:%S')