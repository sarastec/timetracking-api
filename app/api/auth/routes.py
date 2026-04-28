from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from passlib.context import CryptContext

from app.deps import get_db, create_access_token, get_current_user
from app.api.auth.schemas import UserCreate, UserLogin
from app.models import User


router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=pwd_context.hash(user.password),
        created_dt=datetime.now(timezone.utc)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }


@router.post("/login", status_code=200)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Find user
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Check password
    if not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Generate JWT
    access_token = create_access_token({
        "sub": str(db_user.id)
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", status_code=200)
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }
