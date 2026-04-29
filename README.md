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
