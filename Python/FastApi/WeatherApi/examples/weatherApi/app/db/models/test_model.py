from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Test(Base):
    __tablename__ = "k_area_data"

    id = Column(Integer, primary_key=True, index=True)
