from sqlalchemy import Column, Integer, String

from database.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    seq = Column(Integer)