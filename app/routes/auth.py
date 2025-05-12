from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
import os

router = APIRouter()

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    access_token: str
    token_type: str = "bearer"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user
    new_user = User(
        username=user_data.username,
        password=user_data.password,  # In production, hash this password!
        is_seller=user_data.is_seller,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": str(new_user.id)})
    
    return UserResponse(
        username=new_user.username,
        is_seller=new_user.is_seller,
        access_token=access_token
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
    
    # Create access token
    access_token = create_access_token(data={"sub": str(db_user.id)})
    
    # Return user info with token
    return UserResponse(
        username=db_user.username,
        is_seller=db_user.is_seller,
        access_token=access_token
    )

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out"} 