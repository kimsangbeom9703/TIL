from sqlalchemy.orm import Session
from app.crud import crud_test

def test_index(db):
    something = crud_test.get_items(db)
    return something