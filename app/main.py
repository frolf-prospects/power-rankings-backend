from fastapi import FastAPI
from .db import create_db_and_tables, seed_database
from .api.routes import api_router

app = FastAPI(title="Power Rankings Backend")


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()
    seed_database()

app.include_router(api_router)
