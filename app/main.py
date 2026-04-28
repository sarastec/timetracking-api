from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db import engine, Base
from app.seed import seed_lookup_tables
from app.api.auth import routes as auth
from app.api.folders import routes as folders

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    seed_lookup_tables()
    yield
    # shutdown

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(folders.router)
