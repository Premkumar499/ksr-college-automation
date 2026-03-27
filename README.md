# Scholarship AI - Agentic AI System for College Scholarship Management

An intelligent web-based application that automates scholarship management using RAG (Retrieval-Augmented Generation) powered by Google Gemini.

## Features

### 1. Chatbot Section
- AI-powered chatbot for scholarship queries
- Answers questions about eligibility, documents, procedures
- Uses RAG to provide accurate responses based on scholarship data
- Maintains conversation history

### 2. Eligibility Section
- Students input their details
- AI analyzes eligibility across all scholarships
- Shows detailed eligibility score and reasons
- Saves eligibility check history

### 3. Dashboard Section
- Overview statistics (total scholarships, students, disbursed amount)
- Scholarship-wise breakdown with recipient counts
- Recent scholarship recipients list

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (HTML/JS)                    │
│                    localhost:3000                       │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP
┌─────────────────────▼───────────────────────────────────┐
│              Normal Server (CPU)                         │
│              FastAPI - Port 8000                         │
│  - API Endpoints                                         │
│  - Database (PostgreSQL)                                 │
│  - Request Routing                                       │
└─────────────────────┬───────────────────────────────────┘
                      │ Internal
┌─────────────────────▼───────────────────────────────────┐
│              Heavy Server (GPU)                         │
│              FastAPI - Port 8001                        │
│  - RAG Processing                                        │
│  - Vector DB (ChromaDB)                                  │
│  - Embedding Generation                                  │
│  - AI Inference (Gemini)                                 │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **AI/ML**: Google Gemini, ChromaDB, Sentence Transformers
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **RAG**: Custom implementation with ChromaDB

## Setup Instructions

### Prerequisites

1. Python 3.9+
2. PostgreSQL 13+
3. (Optional) GPU with CUDA for heavy server

### Step 1: Clone and Setup Environment

```bash
cd scholarship-ai
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure PostgreSQL

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE scholarship_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE scholarship_db TO postgres;
```

3. Copy `.env.example` to `.env` and update settings

### Step 3: Initialize Database

```bash
python setup.py
```

### Step 4: Run the Servers

**Terminal 1 - Normal Server (CPU):**
```bash
python -m app.main
```

**Terminal 2 - Heavy Server (GPU):**
```bash
python heavy_server/main.py
```

### Step 5: Open Frontend

Open `frontend/index.html` in your browser.

## API Endpoints

### Scholarships
- `GET /scholarships/` - List all scholarships
- `GET /scholarships/{id}` - Get scholarship details
- `POST /scholarships/` - Create scholarship
- `PUT /scholarships/{id}` - Update scholarship
- `DELETE /scholarships/{id}` - Delete scholarship

### Chat
- `POST /chat/` - Chat with AI assistant
- `GET /chat/history/{student_id}` - Get chat history

### Eligibility
- `POST /eligibility/check` - Check eligibility
- `GET /eligibility/history/{student_id}` - Get eligibility history

### Dashboard
- `GET /dashboard/` - Get dashboard statistics
- `GET /dashboard/scholarship/{id}/recipients` - Get recipients by scholarship

### Students
- `GET /students/` - List all students
- `GET /students/{id}` - Get student details
- `POST /students/` - Register student

## Adding Scholarship Data

### Option 1: Through API
```python
import requests

scholarship = {
    "name": "Merit Scholarship",
    "provider": "College Trust",
    "description": "Scholarship for top performers",
    "eligibility_criteria": {
        "min_gpa": 8.0,
        "max_income": 300000
    },
    "documents_required": ["Marksheet", "Income Certificate"],
    "application_procedure": "Apply through college portal",
    "amount": 40000
}

requests.post("http://localhost:8000/scholarships/", json=scholarship)
```

### Option 2: Upload PDF/Excel
Use the Heavy Server endpoints:
- `POST /heavy_server/index/pdf` - Upload scholarship PDF
- `POST /heavy_server/index/excel` - Upload Excel/CSV data

## Configuration

Edit `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/scholarship_db
GOOGLE_API_KEY=your-gemini-api-key
HEAVY_SERVER_URL=http://localhost:8001
```

## Project Structure

```
scholarship-ai/
├── app/
│   ├── api/           # API routes
│   ├── core/          # Configuration, database
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   ├── utils/         # Utilities
│   └── main.py        # Normal server entry
├── heavy_server/
│   └── main.py        # Heavy server entry (RAG)
├── frontend/
│   └── index.html     # Web interface
├── data/
│   ├── scholarships/  # Scholarship documents
│   └── embeddings/    # ChromaDB storage
├── requirements.txt
├── setup.py
└── README.md
```

## License

This is a college project. Feel free to use and modify.

## Authors

College Students - 2026
# ksr-college-automation
