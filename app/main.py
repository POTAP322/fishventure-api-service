from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, metrics,logs

app = FastAPI(title="Fishventure API")

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(logs.router)
app.include_router(metrics.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)