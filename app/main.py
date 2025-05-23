from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, Base, get_db
from sqlalchemy.orm import Session
from app.models import user, category, product, order
from typing import List, Any
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from app.routes import auth
from app.db.init_db import init_db as initialize_database
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db_user = db.query(user.User).filter(user.User.id == user_id).first()
    if db_user is None:
        raise credentials_exception
    return db_user

app = FastAPI(
    title="Marketplace API",
    description="API for the Grandmaster Sticky Shop",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=JSONResponse,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*", "Authorization", "Content-Type"],
    expose_headers=["*"],
    max_age=600,
)

# Import your models
from app.models import user, category, product, order

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    try:
        initialize_database()
    except Exception as e:
        print(f"Failed to initialize database: {str(e)}")
        raise

Base.metadata.create_all(bind=engine)

class CategoryResponse(BaseModel):
    id: int
    name_en: str
    name_ru: str
    slug: str
    image_url: str | None = None

    class Config:
        from_attributes = True
        json_encoders = {
            str: lambda v: v.encode('utf-8').decode('utf-8')
        }

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    img: str | None = None
    owner_id: int
    category_id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    price: int
    img: str | None = None
    category_id: int

class OrderProduct(BaseModel):
    id: int
    name: str
    amount: int
    seller_id: int

class OrderCreate(BaseModel):
    products: list[OrderProduct]

class OrderResponse(BaseModel):
    id: int
    buyer_id: int
    buyer_username: str
    products: list[Any]
    created_at: datetime

    class Config:
        from_attributes = True

class OrderMineResponse(BaseModel):
    id: int
    products: list[Any]
    created_at: datetime

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "Welcome to the Marketplace API"}

@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(category.Category).all()
    return categories

@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(product.Product).all()
    return products

@app.post("/products", response_model=ProductResponse)
def create_product(product_data: ProductCreate, current_user: user.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_seller:
        raise HTTPException(status_code=403, detail="Only sellers can create products")
    
    # Create new product
    new_product = product.Product(
        name=product_data.name,
        price=product_data.price,
        img=product_data.img,
        owner_id=current_user.id,
        category_id=product_data.category_id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product

@app.post("/orders")
def create_order(order_data: OrderCreate, current_user: user.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_order = order.Order(
        buyer_id=current_user.id,
        products=[product.dict() for product in order_data.products]
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Order created successfully", "order_id": new_order.id}

@app.get("/orders/mine", response_model=list[OrderMineResponse], status_code=status.HTTP_200_OK)
def get_my_orders(current_user: user.User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(order.Order).filter(order.Order.buyer_id == current_user.id).all()
    return orders

@app.get("/orders/for-my-products", response_model=list[OrderResponse], status_code=status.HTTP_200_OK)
def get_orders_for_my_products(current_user: user.User = Depends(get_current_user), db: Session = Depends(get_db)):
    all_orders = db.query(order.Order).all()
    result = []
    for o in all_orders:
        my_products = [p for p in o.products if p.get('seller_id') == current_user.id]
        if my_products:
            buyer = db.query(user.User).filter(user.User.id == o.buyer_id).first()
            buyer_username = buyer.username if buyer else "?"
            result.append(OrderResponse(
                id=o.id,
                buyer_id=o.buyer_id,
                buyer_username=buyer_username,
                products=my_products,
                created_at=o.created_at
            ))
    return result
