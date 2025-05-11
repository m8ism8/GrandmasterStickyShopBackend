from sqlalchemy import Column, Integer, ForeignKey, ARRAY
from app.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    buyer_user_id = Column(Integer, ForeignKey("users.id"))
    seller_user_id = Column(Integer, ForeignKey("users.id"))
    products_sold = Column(ARRAY(Integer))