from fastapi import FastAPI
from app.db import engine, Base
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API działa"}