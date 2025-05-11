from sqlalchemy.orm import Session
from app.models.category import Category
from sqlalchemy import text

def init_categories(db: Session):
    # First, ensure the database is using UTF-8
    db.execute(text("SET client_encoding TO 'UTF8'"))
    
    # Add image_url column if it doesn't exist
    try:
        db.execute(text("ALTER TABLE categories ADD COLUMN IF NOT EXISTS image_url VARCHAR"))
        db.commit()
    except Exception as e:
        print(f"Error adding image_url column: {e}")
    
    # Drop existing categories
    db.query(Category).delete()
    db.commit()
    
    categories = [
        {
            "name_en": "Smartphones and Gadgets",
            "name_ru": "Смартфоны и гаджеты",
            "slug": "smartphones",
            "image_url": "https://placehold.co/400x300?text=Smartphones"
        },
        {
            "name_en": "Appliances",
            "name_ru": "Бытовая техника",
            "slug": "appliances",
            "image_url": "https://placehold.co/400x300?text=Appliances"
        },
        {
            "name_en": "Tv, Audio, Video",
            "name_ru": "ТВ, Аудио, Видео",
            "slug": "tv-audio-video",
            "image_url": "https://placehold.co/400x300?text=TV+Audio"
        },
        {
            "name_en": "Computers",
            "name_ru": "Компьютеры",
            "slug": "computers",
            "image_url": "https://placehold.co/400x300?text=Computers"
        },
        {
            "name_en": "Furniture",
            "name_ru": "Мебель",
            "slug": "furniture",
            "image_url": "https://placehold.co/400x300?text=Furniture"
        },
        {
            "name_en": "Beauty",
            "name_ru": "Красота",
            "slug": "beauty",
            "image_url": "https://placehold.co/400x300?text=Beauty"
        },
        {
            "name_en": "For children",
            "name_ru": "Для детей",
            "slug": "children",
            "image_url": "https://placehold.co/400x300?text=Children"
        },
        {
            "name_en": "Pharmacy",
            "name_ru": "Аптека",
            "slug": "pharmacy",
            "image_url": "https://placehold.co/400x300?text=Pharmacy"
        }
    ]

    for category_data in categories:
        db_category = Category(**category_data)
        db.add(db_category)
    
    db.commit() 