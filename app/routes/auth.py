from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str
    is_seller: bool = False

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    is_seller: bool

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user
    new_user = User(
        username=user.username,
        password=user.password,  # In production, hash this password!
        is_seller=user.is_seller,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        username=new_user.username,
        is_seller=new_user.is_seller
    )

@router.post("/login", response_model=UserResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user by username
    db_user = db.query(User).filter(User.username == credentials.username).first()
    
    # Check if user exists and password matches
    if not db_user or db_user.password != credentials.password:  # In production, use proper password verification!
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    # Return user info
    return UserResponse(
        username=db_user.username,
        is_seller=db_user.is_seller
    )

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out"} 