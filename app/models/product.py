from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from app.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    seller_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP)