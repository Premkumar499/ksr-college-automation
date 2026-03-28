# Scholarship AI - Agentic AI System for College Scholarship Management

An intelligent web-based application that automates scholarship management using RAG powered by HuggingFace embeddings and intelligent chatbots.

## Features

### 1. Chatbot Section
- AI-powered chatbot for scholarship queries
- Answers questions about eligibility, documents, procedures
- Image rejection for text-only queries
- Maintains conversation history

### 2. Eligibility Section
- Students input their details (GPA, category, income, etc.)
- AI analyzes eligibility across all scholarships
- Shows detailed eligibility score and reasons
- Supports Tamil Nadu, AICTE, and Private scholarships

### 3. Dashboard Section
- Overview statistics (total scholarships, students, disbursed amount)
- Scholarship-wise breakdown with recipient counts
- Recent scholarship recipients list

## Tech Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Vector DB**: FAISS
- **Embeddings**: HuggingFace Sentence Transformers
- **Frontend**: Vanilla HTML/CSS/JavaScript

## PostgreSQL Setup with pgAdmin

### Step 1: Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**Start PostgreSQL:**
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 2: Create Database and User

```bash
sudo -u postgres psql
```

Then run:
```sql
CREATE DATABASE scholarship_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE scholarship_db TO postgres;
\q
```

### Step 3: Connect pgAdmin

1. Open pgAdmin (http://localhost:5050 or install from https://www.pgadmin.org/)
2. Right-click on "Servers" → "Create" → "Server"
3. Fill in details:
   - **Name**: Scholarship AI
   - **Host**: localhost
   - **Port**: 5432
   - **Database**: scholarship_db
   - **Username**: postgres
   - **Password**: postgres

4. Click "Save" to connect

### Step 4: View Tables in pgAdmin

After connecting:
1. Expand "Scholarship AI" → "Databases" → "scholarship_db"
2. Expand "Schemas" → "Tables"
3. You'll see all tables:
   - scholarships
   - students
   - eligibility_checks
   - scholarship_applications
   - scholarship_recipients
   - chat_history

4. Right-click on any table → "View/Edit Data" → "All Rows" to see data

## Setup Instructions

### Step 1: Clone and Setup Environment

```bash
cd scholarship-ai
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure .env

Update `.env` file:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/scholarship_db
HUGGINGFACE_API_KEY=your_huggingface_api_key
GOOGLE_API_KEY=your_google_api_key
```

### Step 3: Initialize Database

```bash
python setup_postgres.py
```

This will:
- Create the database if it doesn't exist
- Create all required tables
- Seed 12 scholarships automatically

### Step 4: Run the Servers

**Terminal 1 - Backend API:**
```bash
source venv/bin/activate
PYTHONPATH=. python3 app/main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python3 -m http.server 8080
```

### Step 5: Open in Browser

- **Frontend**: http://127.0.0.1:8080/
- **API Docs**: http://127.0.0.1:8000/docs
- **pgAdmin**: http://localhost:5050/

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /scholarships/ | List all scholarships |
| GET | /scholarships/{id} | Get scholarship details |
| POST | /scholarships/ | Create scholarship |
| PUT | /scholarships/{id} | Update scholarship |
| DELETE | /scholarships/{id} | Delete scholarship |
| POST | /chat/ | Chat with AI assistant |
| GET | /chat/history/{student_id} | Get chat history |
| POST | /eligibility/check | Check eligibility |
| GET | /eligibility/history/{student_id} | Get eligibility history |
| GET | /dashboard/ | Get dashboard statistics |
| GET | /students/ | List all students |
| POST | /students/ | Register student |

## Scholarship Data

The system includes 12 pre-configured scholarships:

**Government of Tamil Nadu:**
- SC | SCA | ST | SCC Scholarships
- BC | MBC | DNC Scholarships
- Pudhumai Penn & Tamil Puthalvan Scheme

**National Scholarship Portal (AICTE):**
- Swanath Scholarship
- Saksham Scholarship
- Pragati Scholarship
- PM-USP Special Scholarship
- GATE/CEED Scholarship

**Private Scholarships:**
- Aspire - Harihara Subramanian Scholarship
- Reliance Foundation Undergraduate Scholarship
- Reliance Foundation Postgraduate Scholarship
- Infosys Foundation STEM Stars Scholarship

## Project Structure

```
scholarship-ai/
├── app/
│   ├── api/           # API routes (chat, scholarships, eligibility, etc.)
│   ├── core/          # Configuration, database connection
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic (RAG, eligibility, chat)
│   └── main.py       # FastAPI application
├── frontend/
│   └── index.html     # Web interface
├── data/
│   └── embeddings/    # FAISS vector database
├── bin/               # Unused/test files
├── setup_postgres.py  # PostgreSQL setup script
├── add_scholarships.py
├── add_user_data.py
├── requirements.txt
└── README.md
```

## Adding Test Data

```bash
# Add scholarships
python add_scholarships.py

# Index scholarship data for RAG
python add_user_data.py
```

## License

This is a college project for KSR College Automation - 2026
