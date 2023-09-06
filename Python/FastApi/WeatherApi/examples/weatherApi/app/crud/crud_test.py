from sqlalchemy.orm import Session
from app.db.models.test_model import Test

def get_items(db: Session):
    return db.query(Test).all()