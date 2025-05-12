from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, Base, get_db
from sqlalchemy.orm import Session
from app.models import user, category, product, order
from typing import List
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from app.routes import auth
from app.db.init_db import init_db as initialize_database

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
    allow_headers=["*"],
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
    name_en: str
    name_ru: str
    description_en: str
    description_ru: str
    price: float
    category_id: int
    image_url: str | None = None

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
