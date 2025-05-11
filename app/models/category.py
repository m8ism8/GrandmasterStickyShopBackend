from sqlalchemy import Column, Integer, String, JSON
from app.db import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String, unique=True)
    name_ru = Column(String, unique=True)
    slug = Column(String, unique=True)
    image_url = Column(String)