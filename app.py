# framework: bridge between frontend and backend. also called UI library
# stramlit(small projects:easy to use and understand, lesser number of components that can't be customized) and flask(web apps)[UI from scratch,]

# main server file :typos leads to issues in running server

# code to start main server: currently not in root directory rather it's in flask sub-folder
from flask import Flask, render_template, request, redirect, url_for,jsonify,Blueprint,flash,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash 
from functools import wraps

from datetime import datetime
from utils.rag_pipeline import multi_agent_rag

from database import init_db, SessionLocal
from models import QuestionHistory,UnansweredQuestion,User

app= Flask(__name__)

app.secret_key ='supersecretkey' # secret key for session management and flash messages

print(" init db created")
init_db()

admin_bp=Blueprint('admin',__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #initializing database

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

with app.app_context():
    db.create_all() # creates the database and tables based on the defined models. It ensures that the database is set up before any operations are performed on it. This is necessary because SQLAlchemy needs to know about the application context to create the tables correctly.

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # use session.get for clarity and allow redirect back after login
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            # include next so user returns to original page after signing in
            return redirect(url_for('signup',next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# you need to route between pages to view them
@app.route('/') # default page i.e. home page
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST']) # register page
def signup():
    if request.method == 'POST':
        # Determine whether this POST is a registration (has fullname) or a login
        if request.form.get('fullname'):
            fullname = request.form.get('fullname', '').strip()
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password')

            # Basic validation
            if not (fullname and username and email and password):
                flash('Please fill all required fields for registration.', 'error')
                return redirect(url_for('signup'))
            
             #password must be at least 8 characters long and a combination of letters and numbers and special characters
            if len(password)<8 or not any(char.isdigit() for char in password)\
              or not any(char.isalpha() for char in password) or not any(not char.isalnum()\
                                                                          for char in password):
                flash('Password must be at least 8 characters long and contain letters, \
                  numbers, and special characters.', 'error')
                return redirect(url_for('signup'))
        
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return redirect(url_for('signup'))

            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists!', 'error')
                return redirect(url_for('signup'))

            # Hash the password
            password_hash = generate_password_hash(password)

            # Create new user
            new_user = User(
                fullname=fullname,
                username=username,
                email=email,
                password_hash=password_hash
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please sign in.', 'success')
                # Redirect back to the same login page so the sign-in form is shown
                return redirect(url_for('signup'))

            except Exception:
                db.session.rollback()
                flash('Registration failed!', 'error')
                return redirect(url_for('signup'))

        else:
            # Login flow
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            if not (username and password):
                flash('Please provide username and password.', 'error')
                return redirect(url_for('signup'))

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session["user_id"]=user.id
                session["user_name"]=user.username
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials.', 'error')
                return redirect(url_for('signup'))

    return render_template("login.html")


@app.route('/assistant') # assistant page
@login_required
def assistant():
    return render_template("assistant.html")

@app.route('/aboutUs') # overview page
def aboutUs():
    return render_template("aboutUs.html")

# ---------------- SIGNOUT ----------------
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Logged out successfully','success')
    return redirect(url_for('signup'))
# ---------------- RAG ----------------
@app.route('/rag', methods=['GET', 'POST'])
@login_required
def rag_assistant():
    answer = None
    sources = []
    if request.method == "POST":
        query = request.form.get("query")
        sector = request.form.get("sector")
        # pass the current logged-in user's id into the RAG pipeline
        user_id = session.get('user_id')
        result = multi_agent_rag(query, sector)
        answer = result["answer"]
        sources = result["sources"]
    return render_template(
        "rag_assistant.html",
        answer=answer,
        sources=sources
    )
# ---------------- ADMIN ----------------
@admin_bp.route("/admin")
@login_required
def view_unanswered():
    db = SessionLocal()
    questions = (
        db.query(UnansweredQuestion)
        .order_by(UnansweredQuestion.timestamp.desc())
        .all()
    )
    db.close()
    return render_template("admin.html", questions=questions)
app.register_blueprint(admin_bp)
# ---------------- HISTORY API ----------------
@app.route("/history", methods=["GET"])
@login_required
def get_question_history():
    db = SessionLocal()
    questions = (
        db.query(QuestionHistory)
        .order_by(QuestionHistory.id.desc())
        .limit(20)
        .all()
    )
    db.close()
    return jsonify([
        {
            "id": q.id,
            "question": q.question,
            "sector": q.sector,
            "timestamp": q.timestamp
        }
        for q in questions
    ])
# ---------------- RUN ----------------

if __name__=='__main__':
    app.run(debug=True)

# in terminal type : 1) cd flask 2)python app.py --> in the http link provided-> follow link--> web page gets opened
# make a sub-folder with name exactly as : templates
