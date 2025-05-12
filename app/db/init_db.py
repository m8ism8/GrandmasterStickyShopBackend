from sqlalchemy.orm import Session
from sqlalchemy import text
from . import get_db
from ..models.category import Category
from ..models.product import Product
from app.db import engine, Base
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_categories(db: Session):
    try:
        logger.info("Initializing categories...")
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
        logger.info("Categories initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing categories: {str(e)}")
        raise

def init_db():
    try:
        logger.info("Starting database initialization...")
        
        # Test database connection
        with engine.connect() as conn:
            logger.info("Database connection successful")
            
            # Check if users table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'users'
                );
            """))
            table_exists = result.scalar()
            logger.info(f"Users table exists: {table_exists}")
        
        # Create all tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully")
        
        # Modify schema
        logger.info("Modifying database schema...")
        with engine.begin() as conn:
            conn.execute(text("""
                DO $$ 
                BEGIN 
                    -- Add is_seller column if it doesn't exist
                    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                                WHERE table_name = 'users' AND column_name = 'is_seller') THEN
                        ALTER TABLE users ADD COLUMN is_seller BOOLEAN NOT NULL DEFAULT false;
                        RAISE NOTICE 'Added is_seller column';
                    END IF;
                    
                    -- Drop role column if it exists
                    IF EXISTS (SELECT 1 FROM information_schema.columns 
                            WHERE table_name = 'users' AND column_name = 'role') THEN
                        ALTER TABLE users DROP COLUMN role;
                        RAISE NOTICE 'Dropped role column';
                    END IF;
                    
                    -- Make username unique if it's not already
                    IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints 
                                WHERE table_name = 'users' AND constraint_name = 'users_username_key') THEN
                        ALTER TABLE users ADD CONSTRAINT users_username_key UNIQUE (username);
                        RAISE NOTICE 'Added username unique constraint';
                    END IF;
                END $$;
            """))
        logger.info("Schema modifications completed")
        
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        raise

if __name__ == "__main__":
    init_db() 