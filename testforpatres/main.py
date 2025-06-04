from fastapi import FastAPI
from endpoints import auth as endpoints_auth  # Импорт роутера

app = FastAPI()

# Подключаем роутер
# app.include_router(endpoints_auth.router)

