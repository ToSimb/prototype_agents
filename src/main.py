from fastapi import FastAPI, HTTPException
import sqlite3
import os

from logger.log_meddlewary import LogMiddleware
from logger.logger import logger

app = FastAPI()
app.add_middleware(LogMiddleware)

# @app.on_event("startup")
# async def startup():
#     db_path = "mydatabase.db"
#     if not os.path.exists(db_path):
#         logger.error(f"База данных '{db_path}' не найдена. Закрытие приложения.")
#         os._exit(1)
#     logger.info("Подключение к БД")
#     app.state.db_connection = sqlite3.connect(db_path)
#
# @app.on_event("shutdown")
# async def shutdown():
#     logger.info("разрыв соединения")
#     app.state.db_connection.close()

@app.get("/")
async def root():
    try:
        return {"Hello": "World"}
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
