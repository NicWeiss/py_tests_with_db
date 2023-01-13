from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    locale = Column(String, unique=True)
