import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql
from datetime import datetime, timedelta

# Устанавливаем переменную окружения перед импортом app
os.environ["TESTING"] = "1"

from api.v1.main import app
from api.v1.database import Base, get_db
from api.v1.config import settings
from api.v1.models import Player

@pytest.fixture(scope="session", autouse=True)
def prepare_test_environment():
    """Подготовка тестового окружения"""
    # 1. Создаём тестовую БД
    try:
        conn = pymysql.connect(
            host="5.35.89.153",
            user="admin",
            password="ker555!Rss",
            autocommit=True
        )
        with conn.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS fishventure_test_db")
            cursor.execute("CREATE DATABASE fishventure_test_db")
    except Exception as e:
        pytest.fail(f"Ошибка создания БД: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

    # 2. Создаём таблицы
    engine = create_engine(settings.TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    engine.dispose()

    yield

    # 3. Очистка после тестов (опционально)
    engine = create_engine(settings.TEST_DATABASE_URL)
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

# ----- Основные фикстуры ----- #

@pytest.fixture(scope="session")
def engine():
    """Фикстура подключения к тестовой БД"""
    engine = create_engine(
        settings.TEST_DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    yield engine
    engine.dispose()

@pytest.fixture()
def db_session(engine):
    """Фикстура сессии БД с откатом транзакций"""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    # Очищаем основные таблицы перед тестом
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

    yield session

    # Откатываем изменения после теста
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db_session):
    """Фикстура тестового клиента FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

# ----- Фикстуры тестовых данных ----- #

@pytest.fixture()
def test_user(db_session):
    """Фикстура тестового пользователя"""
    user = Player(
        username="test_user",
        hash_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        auth_token="test_token",
        birth_date=datetime.now() - timedelta(days=365*20))
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture()
def auth_token(client, test_user):
    """Фикстура для получения валидного токена"""
    # Обновляем токен через API
    response = client.post("/auth/login", json={
        "login": "test_user",
        "password": "secret"
    })
    return response.json()["auth_token"]

@pytest.fixture()
def test_log(db_session, test_user):
    """Фикстура тестового лога"""
    from api.v1.models import Logs
    log = Logs(log_text="Test log message")
    db_session.add(log)
    db_session.commit()
    return log

@pytest.fixture()
def test_player_log(db_session, test_user):
    """Фикстура тестового лога игрока"""
    from api.v1.models import PlayerLogs
    log = PlayerLogs(
        player_id=test_user.id,
        entered_at=datetime.now(),
        exit_at=datetime.now() + timedelta(hours=2))
    db_session.add(log)
    db_session.commit()
    return log