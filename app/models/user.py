from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

from app.db.base_class import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    country_id = Column(Integer, ForeignKey("country.id"))
    city_id = Column(Integer, ForeignKey("city.id"))
