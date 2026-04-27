from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from app.db import engine, Base
from app.seed import seed_lookup_tables
from app.deps import get_db
from app.models import UserStatus
from app.api.auth import routes as auth

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    seed_lookup_tables()
    yield
    # shutdown

app = FastAPI(lifespan=lifespan)


@app.get("/")
def root(db: Session = Depends(get_db)):
    statuses = db.query(UserStatus).all()

    return {
        "message": "API działa",
        "user_statuses": [s.name for s in statuses]
    }


app.include_router(auth.router)
