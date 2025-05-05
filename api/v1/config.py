from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fishventure API"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000
    DATABASE_URL: str = "mysql+pymysql://root:gh245hyt@localhost/fishventure_db"
    QWEN_API_KEY: str = "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"
    QWEN_API_URL: str = "https://openrouter.ai/api/v1"
    QWEN_MODEL: str = "qwen/qwen3-235b-a22b:free"


    class Config:
        env_file = ".env"

settings = Settings()