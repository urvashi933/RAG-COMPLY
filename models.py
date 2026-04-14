from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(200)) # Hashed password
    created_at = Column(DateTime, default=datetime.utcnow)

class QuestionHistory(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'),nullable=True)
    query = Column(String(500))
    answer = Column(String(2000))
    sector = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)

class UnansweredQuestion(Base):
    __tablename__ = "unanswered"
    id = Column(Integer, primary_key=True)
    query = Column(String(500))
    sector = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)