from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fishventure API"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000
    DATABASE_URL: str = "mysql+pymysql://root:gh245hyt@localhost/fishventure_db"
    QWEN_API_KEY: str = "key"
    QWEN_API_URL: str = "https://openrouter.ai/api/v1"
    QWEN_MODEL: str = "qwen/qwen3-235b-a22b:free"


    class Config:
        env_file = ".env"

settings = Settings()
