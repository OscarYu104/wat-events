from fastapi import FastAPI
from sqlalchemy import text

from app.api import events, admin
from app.core.database import engine

app = FastAPI(title="UW Events Aggregator")

app.include_router(events.router)
app.include_router(admin.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/health/db")
def health_check_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
