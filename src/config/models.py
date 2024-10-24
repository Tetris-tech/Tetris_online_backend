from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rating = Column(Integer, default=0)
