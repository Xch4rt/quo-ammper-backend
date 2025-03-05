from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import UserCreate, Token, User as UserSchema
from auth import get_current_user, create_access_token, verify_password, get_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy import or_

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(or_(UserModel.email == user.email, UserModel.name == user.name)).first()
    
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    hashed_password = get_password_hash(user.password)
    new_user = UserModel(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token({"sub": new_user.email})
    refresh_token = create_access_token({"sub": new_user.email}, expires_delta=timedelta(days=7))
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_access_token({"sub": user.email}, expires_delta=timedelta(days=7))
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh(current_user: UserModel = Depends(get_current_user)):
    access_token = create_access_token({"sub": current_user.email})
    refresh_token = create_access_token({"sub": current_user.email}, expires_delta=timedelta(days=7))

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


