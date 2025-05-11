from app.db import SessionLocal
from app.db.init_db import init_categories

def init():
    db = SessionLocal()
    try:
        init_categories(db)
    finally:
        db.close()

if __name__ == "__main__":
    init() 