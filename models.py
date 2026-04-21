import string

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class QuestionHistory(Base):
    __tablename__ = "question_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'),nullable=True)
    question = Column(String(500))
    sector = Column(String(50))
    timestamp = Column(String)

class UnansweredQuestion(Base):
    __tablename__ = "unanswered_questions"

    id = Column(Integer, primary_key=True,index=True)
    question = Column(String(500))
    sector = Column(String(50))
    timestamp = Column(String)

class User(Base):
    __tablename__="user"

    id = Column(Integer, primary_key=True,index=True)
    fullname = Column(String(100))
    email = Column(String(100))
    username = Column(String(100))
    password = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    