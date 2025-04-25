from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fishventure API"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    DATABASE_URL: str = "mysql+pymysql://root:gh245hyt@localhost/fishventure_db"

    class Config:
        env_file = ".env"

settings = Settings()