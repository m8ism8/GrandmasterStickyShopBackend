from sqlalchemy.orm import Session
from sqlalchemy import text
from . import get_db
from ..models.category import Category
from ..models.product import Product

def init_categories(db: Session):
    db.execute(text("SET client_encoding TO 'UTF8'"))
    db.execute(text("DROP TABLE IF EXISTS categories CASCADE"))
    db.commit()
    
    categories = [
        Category(
            name_en="Electronics",
            name_ru="Электроника",
            slug="electronics",
            image_url="https://placehold.co/600x400?text=Electronics"
        ),
        Category(
            name_en="Clothing",
            name_ru="Одежда",
            slug="clothing",
            image_url="https://placehold.co/600x400?text=Clothing"
        ),
        Category(
            name_en="Books",
            name_ru="Книги",
            slug="books",
            image_url="https://placehold.co/600x400?text=Books"
        ),
        Category(
            name_en="Home & Garden",
            name_ru="Дом и Сад",
            slug="home-garden",
            image_url="https://placehold.co/600x400?text=Home+%26+Garden"
        ),
        Category(
            name_en="Sports",
            name_ru="Спорт",
            slug="sports",
            image_url="https://placehold.co/600x400?text=Sports"
        )
    ]
    
    for category in categories:
        db.add(category)
    
    db.commit()

def init_db():
    db = next(get_db())
    init_categories(db)

if __name__ == "__main__":
    init_db() 