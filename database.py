from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///data/incubator.db", echo=False)
SessionLocal = sessionmaker(bind=engine) # Create a session factory bound to the engine done to manage database sessions
Base = declarative_base()

def init_db():
	from models import User, QuestionHistory, UnansweredQuestion
	Base.metadata.create_all(bind=engine)