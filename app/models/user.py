from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP
from app.db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_seller = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)