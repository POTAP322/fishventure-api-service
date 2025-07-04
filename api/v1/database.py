from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from api.v1.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"init_command": "SET SESSION time_zone='+03:00';"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()