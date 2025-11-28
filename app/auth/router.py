from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth.schemas import SignUpSchema, LoginSchema, TokenResponse
from app.auth.models import User
from app.auth.utils import hash_password, verify_password, create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(payload: SignUpSchema, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})

    user_payload = {"id": user.id, "name": user.name, "email": user.email}

    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        user=user_payload,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})

    user_payload = {"id": user.id, "name": user.name, "email": user.email}

    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        user=user_payload,
    )
