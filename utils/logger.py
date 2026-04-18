from datetime import datetime 
from database import SessionLocal 
from models import QuestionHistory, UnansweredQuestion 
 
def log_question(question, sector, user_id, answer=""): 
    db = SessionLocal() 

    entry = QuestionHistory( 
        user_id=user_id, 
        query=question, 
        # answer=answer, 
        timestamp=datetime.now().isoformat(),
        sector=sector 
    ) 
    db.add(entry) 
    db.commit() 
    db.close() 
 
def log_unanswered(question, sector): 
    db = SessionLocal() 

    entry = UnansweredQuestion(
        query=question, 
        sector=sector, 
        timestamp=datetime.now().isoformat()) 
    
    db.add(entry) 
    db.commit() 
    db.close()