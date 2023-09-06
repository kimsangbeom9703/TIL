from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.connection import get_db

from app.apis import test # main logic

test_router = APIRouter(
    prefix="/items",  # url 앞에 고정적으로 붙는 경로추가
    tags=["health Check"],
)  # Route 분리


@test_router.get("/test_route")  # Route Path
def test_index(db: Session = Depends(get_db)):
    res = test.test_index(db=db)  # apis 호출

    return {
        "res": res,
    }  # 결과