# framework: bridge between frontend and backend. also called UI library
# stramlit(small projects:easy to use and understand, lesser number of components that can't be customized) and flask(web apps)[UI from scratch,]

# main server file :typos leads to issues in running server

# code to start main server: currently not in root directory rather it's in flask sub-folder
import os
from flask import Flask, render_template, request, redirect, url_for,jsonify,Blueprint,flash,session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash 
from werkzeug.utils import secure_filename
from datetime import datetime
from utils.rag_pipeline import rag_answer
from database import init_db, SessionLocal
from models import QuestionHistory,UnansweredQuestion,User,ContactInquiry

app= Flask(__name__)

app.secret_key ='supersecretkey' # secret key for session management and flash messages

print(" init db created")
init_db()

admin_bp=Blueprint('admin',__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # use session.get for clarity and allow redirect back after login
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            # include next so user returns to original page after signing in
            return redirect(url_for('login',next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# you need to route between pages to view them
@app.route('/') # default page i.e. home page
def home():
    return render_template("index.html")

@app.route('/aboutUs') # overview page
def aboutUs():
    return render_template("aboutUs.html")

@app.route('/signup', methods=['GET', 'POST']) # register page
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not fullname or len(fullname.strip()) < 2:
            flash('Full name must be at least 2 characters long', 'error')
            return redirect(url_for('login'))

        if not username or len(username.strip()) < 6:
            flash('Username must be at least 6 characters long', 'error')
            return redirect(url_for('login'))

        if not email or '@' not in email:
            flash('Please enter a valid email', 'error')
            return redirect(url_for('login'))

        if (
            len(password) < 8
            or not any(c.isalpha() for c in password)
            or not any(c.isdigit() for c in password)
            or not any(not c.isalnum() for c in password)
        ):
            flash('Password must be at least 8 characters and include letters, numbers & special characters', 'error')
            return redirect(url_for('login'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('login'))

        db = SessionLocal()
        existing_user_email = db.query(User).filter(User.email == email).first()
        existing_user_username = db.query(User).filter(User.username == username).first()

        if existing_user_email:
            db.close()
            flash('Email already registered. Please login.', 'error')
            return redirect(url_for('login'))

        if existing_user_username:
            db.close()
            flash('Username already taken. Please choose another.', 'error')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)

        new_user = User(
            fullname=fullname.strip(),
            username=username.strip(),
            email=email.strip(),
            password=hashed_password,
            created_at=datetime.utcnow()
        )

        try:
            db.add(new_user)
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception:
            db.rollback()
            flash('Registration failed. Try again.', 'error')
            return redirect(url_for('login'))
        finally:
            db.close()
    return render_template("login.html")
                
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        if not (email and username and password):
            flash('Please provide email, username, and password.', 'error')
            return redirect(url_for('login'))

        db = SessionLocal()
        user = db.query(User).filter(User.email == email, User.username == username).first()
        db.close()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.username
            
            # Check if user is admin (example condition)
            if user.email == 'srivastavaurvashi933@gmail.com' and user.username == 'Spongebob':
                session["is_admin"] = True
                flash('Welcome back, Admin!', 'success')
                return redirect('/admin')
            
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.', 'error')
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template("login.html")
    

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        message = request.form.get('message')
        inquiry_type = request.form.get('inquiry_type')

        db = SessionLocal()
        new_inquiry = ContactInquiry(
            fullname=fullname,
            email=email,
            message=message,
            inquiry_type=inquiry_type,
            timestamp=datetime.utcnow(),
            status="Pending"
        )
        try:
            db.add(new_inquiry)
            db.commit()
            flash('Message sent successfully 🚀', 'success')
        except Exception as e:
            db.rollback()
            flash('Error sending message. Please try again.', 'error')
        finally:
            db.close()
            
        return redirect(url_for('contact'))
        
    return render_template("contact.html")

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
        result = rag_answer(query, sector, user_id)
        answer = result["answer"]
        sources = result["sources"]

    return render_template(
        "assistant.html",
        answer=answer,
        sources=sources
    )
# ---------------- ADMIN ----------------
def get_local_documents(base_dir="data"):
    """Scans the data directory and returns just the filenames and sectors."""
    documents = []
    sectors = ["legal", "workforce","branding","infrastructure","promotion","property_dealing"]
    
    for sector in sectors:
        folder_path = os.path.join(base_dir, sector)
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                # Only grab supported files
                if filename.endswith((".pdf", ".docx", ".txt")):
                    documents.append({
                        "name": filename,
                        "sector": sector.capitalize()
                    })
    return documents

@admin_bp.route("/admin")
@login_required
def view_unanswered():
    if not session.get('is_admin'):
        flash('Unauthorized access. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    db = SessionLocal()
    questions = (
        db.query(UnansweredQuestion)
        .order_by(UnansweredQuestion.timestamp.desc())
        .all()
    )
    # Fetch the recent contact inquiries
    inquiries = (
        db.query(ContactInquiry)
        .order_by(ContactInquiry.timestamp.desc())
        .limit(10) # Get the 10 most recent inquiries
        .all()
    )
    db.close()

    # 3. Fetch the documents from the local folder
    local_docs = get_local_documents("data")

    # 4. Pass the 'local_docs' list to your HTML template
    return render_template("admin.html", questions=questions, documents=local_docs, inquiries=inquiries)

@admin_bp.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('admin.view_unanswered'))
    
    file = request.files['file']
    sector = request.form.get('sector')

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('admin.view_unanswered'))
    
    if file and sector:
        filename = secure_filename(file.filename)
        # Ensure the sector folder exists
        folder_path = os.path.join("data", sector)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        file.save(os.path.join(folder_path, filename))
        flash(f'File "{filename}" uploaded successfully to {sector}!', 'success')
        return redirect(url_for('admin.view_unanswered'))
    
    flash('Upload failed', 'error')
    return redirect(url_for('admin.view_unanswered'))

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
    app.run(debug=True,port=5000)

# in terminal type : 1) cd flask 2)python app.py --> in the http link provided-> follow link--> web page gets opened
# make a sub-folder with name exactly as : templates
