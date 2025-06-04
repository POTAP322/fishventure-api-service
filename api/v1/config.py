from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fishventure API"
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000

    DATABASE_URL: str
    TEST_DATABASE_URL: str

    QWEN_API_KEY: str
    QWEN_API_URL: str
    QWEN_MODEL: str


    class Config:
        env_file = ".env"

settings = Settings()
