from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager

from app.db import engine, Base, SessionLocal
from app.seed import seed_lookup_tables
from app.models import User, UserStatus, Subscription
from app.schemas import UserCreate

from datetime import datetime

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    seed_lookup_tables()
    yield
    # shutdown (na razie nic)

app = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root(db: Session = Depends(get_db)):
    statuses = db.query(UserStatus).all()

    return {
        "message": "API działa",
        "user_statuses": [s.name for s in statuses]
    }
