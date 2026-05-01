# RAG-COMPLY

A Retrieval-Augmented Generation (RAG) based web application that combines semantic search with Large Language Models (LLMs) to deliver document-grounded startup compliance guidance. By utilizing verified regulatory sources across multiple sectors, RAG-COMPLY provides accurate, explainable, and trustworthy responses for informed decision-making.

## 🚀 Features

*   **RAG Assistant:** Ask compliance-related questions across various sectors and receive precise, AI-generated answers grounded in uploaded documents.
*   **Sector-Specific Knowledge Bases:** Separate FAISS vector stores for distinct sectors: Legal, Workforce, Branding, Promotion, Property Dealing, and Infrastructure.
*   **User Authentication:** Secure user registration, login, and session management using Werkzeug password hashing.
*   **Admin Dashboard:**
    *   Upload new `.pdf`, `.docx`, or `.txt` documents to specific sectors to continuously update the knowledge base.
    *   Monitor and review unanswered questions from the RAG assistant.
    *   Review and manage contact inquiries from users.
*   **Contact Form:** Allow users to submit inquiries or feedback.
*   **Question History:** Retains user questions and queries for later review and system improvement.

## 💻 Tech Stack

*   **Backend:** Flask (Python)
*   **Database:** SQLite (via SQLAlchemy ORM)
*   **RAG Pipeline:**
    *   **LLM Integration:** Google GenAI (`google-genai`)
    *   **Vector Database:** FAISS (`faiss-cpu`)
    *   **Embeddings:** Sentence Transformers
    *   **Document Parsers:** `pypdf` (for PDFs), `python-docx` (for Word documents)
*   **Frontend:** HTML, CSS, JavaScript (Jinja2 templates)

## 📁 Project Structure

```
RAG-COMPLY/
│
├── app.py                  # Main Flask application and routes
├── config.py               # Application configurations
├── database.py             # Database initialization (SQLAlchemy)
├── index_documents.py      # Script to chunk documents and build FAISS indexes
├── models.py               # SQLAlchemy database models
├── requirements.txt        # Python dependencies
│
├── data/                   # Raw documents categorized by sector
│   ├── branding/
│   ├── infrastructure/
│   ├── legal/
│   ├── promotion/
│   ├── property_dealing/
│   └── workforce/
│
├── vector_store/           # Generated FAISS indexes for each sector
├── utils/                  # Utility scripts (chunker, document loader, embedding, FAISS indexer)
├── templates/              # HTML Jinja2 templates (index, login, admin, assistant, etc.)
└── static/                 # Static assets (CSS, JS, images)
```

## 🛠️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd RAG-COMPLY
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   Windows: `venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up Environment Variables:**
    Create a `.env` file in the root directory and add your necessary API keys (e.g., Google Gemini API key if required by your `config.py` / `google-genai`).

6.  **Initialize the database and vector stores:**
    The SQLite database (`database.db`) is automatically initialized when `app.py` is run. 
    To populate the vector database with existing documents in the `data/` folder, run:
    ```bash
    python index_documents.py
    ```

7.  **Run the application:**
    ```bash
    python app.py
    ```
    The server will start at `http://127.0.0.1:5000/`.

## 🛡️ Admin Access

To access the admin dashboard (`/admin`), you must be logged in with the designated admin email address. By default, this is set in `app.py` as:
*   **Email:** `email address as email in which you created account`
*(To change this, update the admin email check within the `/signin` route in `app.py`)*

Admins have the exclusive ability to view unanswered queries, read user feedback, and upload new reference documents directly from the interface.

## Project Screenshots

Below are the screenshots of the working project:
### Landing Page
<img width="49%" alt="Screenshot (394)" src="https://github.com/user-attachments/assets/879891ec-81c9-4314-8a13-7cac89dc8c1b" />
<img width="49%" alt="Screenshot (396)" src="https://github.com/user-attachments/assets/ccd7f316-28c7-47f4-a6cc-97579a5af6ca" />
<img width="49%" alt="Screenshot (397)" src="https://github.com/user-attachments/assets/a1c87bf3-686f-4c05-99fb-2ba64e3eb186" />
<img width="49%" alt="Screenshot (398)" src="https://github.com/user-attachments/assets/c7efcdc1-ffd0-481c-838e-6c4b4975fd64" />

### About Page
<img width="49%" alt="Screenshot (399)" src="https://github.com/user-attachments/assets/d92677b7-19b6-4d30-a9fe-6c4b38338226" />
<img width="49%" alt="Screenshot (400)" src="https://github.com/user-attachments/assets/7345cd2d-c150-4673-9d7e-be7c0302d85d" />
<img width="49%" alt="Screenshot (401)" src="https://github.com/user-attachments/assets/38c06673-43a4-4272-8e95-6a3a9c42ac24" />

### Contact Page
<img width="49%" alt="Screenshot (402)" src="https://github.com/user-attachments/assets/d8047f8b-8756-4342-bbe2-285a2dbe66c6" />

### SignUp Page
<img width="49%" alt="Screenshot (404)" src="https://github.com/user-attachments/assets/9a466b5a-8cd5-40aa-91b7-3b0e16e98588" />

### SignIn Page
<img width="49%" alt="Screenshot (403)" src="https://github.com/user-attachments/assets/cae61cd4-9f00-41ef-b3f1-80d4358eeeb8" />

### Admin Page
<img width="49%" alt="Screenshot (405)" src="https://github.com/user-attachments/assets/0d7157ce-8b39-46dd-af54-737068927403" />
<img width="49%" alt="Screenshot (406)" src="https://github.com/user-attachments/assets/82e46de4-4ba9-42ff-8ad7-dc793fbdb1e8" />

### RAG Assistant Page 
<img width="49%" alt="Screenshot (395)" src="https://github.com/user-attachments/assets/b831e3eb-7145-47b0-bf64-a5268f6f3cc3" />












