from sqlalchemy import Column, Integer, String,ForeignKey
from database import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer,primary_key=True)
    japanese = Column(String,nullable=False)
    reading = Column(String,nullable=False)
    meaning = Column(String,nullable=False)
    status = Column(String, default="learning")

    owner_id = Column(Integer,ForeignKey("users.id"))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    username = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)