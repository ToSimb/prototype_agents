from fastapi import FastAPI, HTTPException
import sqlite3
import os

app = FastAPI()


@app.on_event("startup")
async def startup():
    db_path = "mydatabase.db"
    if not os.path.exists(db_path):
        print(f"База данных '{db_path}' не найдена. Закрытие приложения.")
        os._exit(1)
    print("Подключение к БД")
    app.state.db_connection = sqlite3.connect(db_path)

@app.on_event("shutdown")
async def shutdown():
    print("разрыв соединения")
    app.state.db_connection.close()

@app.get("/")
async def root():
    try:
        return {"Hello": "World"}
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
