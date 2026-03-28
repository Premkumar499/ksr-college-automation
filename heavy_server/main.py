"""
Heavy Server - GPU-accelerated processing for RAG and AI inference
Runs on GPU for faster embeddings and AI processing
"""

import os
from typing import List, Dict, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import pdfplumber
from google import genai

# Use path trick to import ChromaWrapper from the app folder
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.config import settings
from app.services.chroma_db import ChromaWrapper

app = FastAPI(title="Heavy Server - GPU Processing")

# Initialize Chroma - Gemini text embedding
vector_db = ChromaWrapper(path=settings.CHROMA_GEMINI_DB_PATH)

# Configure Gemini
client = genai.Client(api_key=settings.GOOGLE_API_KEY)


class DocumentInput(BaseModel):
    content: str
    source: str
    scholarship_name: str
    doc_type: str = "general"


class QueryInput(BaseModel):
    query: str
    n_results: int = 5
    conversation_history: Optional[List[Dict[str, str]]] = None


@app.post("/index/documents")
async def index_documents(documents: List[DocumentInput]):
    """Index documents into the vector database"""
    try:
        texts = [doc.content for doc in documents]

        metadatas = [
            {
                "source": doc.source,
                "scholarship_name": doc.scholarship_name,
                "doc_type": doc.doc_type,
            }
            for doc in documents
        ]
        vector_db.add(documents=texts, metadatas=metadatas)
        return {"status": "success", "indexed": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/index/pdf")
async def index_pdf(file: UploadFile = File(...), scholarship_name: str = "Unknown"):
    """Extract text from PDF and index it"""
    try:
        content = await file.read()
        tmp_path = f"/tmp/{file.filename}"
        os.makedirs("/tmp", exist_ok=True)
        with open(tmp_path, "wb") as f:
            f.write(content)

        text_content = []
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)

        full_text = "\n\n".join(text_content)

        vector_db.add(
            documents=[full_text],
            metadatas=[
                {
                    "source": file.filename,
                    "scholarship_name": scholarship_name,
                    "doc_type": "pdf",
                }
            ],
        )

        os.remove(tmp_path)

        return {
            "status": "success",
            "pages_processed": len(text_content),
            "characters": len(full_text),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/index/excel")
async def index_excel(file: UploadFile = File(...)):
    """Index structured data from Excel/CSV files"""
    import pandas as pd

    try:
        content = await file.read()
        filename = file.filename.lower()

        tmp_path = f"/tmp/{file.filename}"
        os.makedirs("/tmp", exist_ok=True)
        with open(tmp_path, "wb") as f:
            f.write(content)

        if filename.endswith(".csv"):
            df = pd.read_csv(tmp_path)
        else:
            df = pd.read_excel(tmp_path)

        documents = []
        for _, row in df.iterrows():
            row_text = " | ".join(
                [f"{col}: {val}" for col, val in row.items() if pd.notna(val)]
            )
            documents.append(
                {
                    "content": row_text,
                    "source": filename,
                    "scholarship_name": str(
                        row.get("name", row.get("scholarship_name", "Unknown"))
                    ),
                    "doc_type": "structured_data",
                }
            )

        if documents:
            texts = [doc["content"] for doc in documents]
            metadatas = [
                {
                    "source": doc["source"],
                    "scholarship_name": doc["scholarship_name"],
                    "doc_type": doc["doc_type"],
                }
                for doc in documents
            ]
            vector_db.add(documents=texts, metadatas=metadatas)

        os.remove(tmp_path)

        return {"status": "success", "rows_indexed": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query_vector_db(query_input: QueryInput):
    """Query the vector database"""
    try:
        res = vector_db.query(query_texts=[query_input.query], n_results=query_input.n_results)
        return {
            "query": query_input.query,
            "results": [
                {
                    "content": doc,
                    "metadata": meta,
                    "relevance_score": 1 - dist if dist else 1,
                }
                for doc, meta, dist in zip(
                    res["documents"][0], res["metadatas"][0], res["distances"][0]
                )
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate")
async def generate_response(query_input: QueryInput):
    """Generate response using Gemini with RAG context"""
    if not settings.GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API not configured")

    try:
        res = vector_db.query(query_texts=[query_input.query], n_results=5)

        context = "\n\n".join(res["documents"][0])

        history_prompt = ""
        if query_input.conversation_history:
            for msg in query_input.conversation_history[-5:]:
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_prompt += f"{role}: {msg.get('content', '')}\n"

        prompt = f"""You are a helpful scholarship advisor assistant for a college. Use the following context to answer the user's question accurately.

Context from scholarship documents:
{context}

{history_prompt}
User: {query_input.query}

Format your response like this (use line breaks for readability, NOT paragraphs):

**Scholarship Name:** [name]
**Description:** [brief description]
**Eligibility Criteria:** [list each criterion on a new line with bullet points]
**Documents Required:** [list each document on a new line with bullet points]
**Application Procedure:** [step by step procedure]
**Amount:** [scholarship amount if available]
**Provider:** [who provides this scholarship]

If information is not available, write "Not specified" for that field."""

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
        except Exception as e:
            error_msg = str(e)
            if "image" in error_msg.lower() and "does not support" in error_msg.lower():
                return {
                    "response": "I can only process text questions. Please type your question instead of uploading an image.",
                    "sources": [],
                }
            raise HTTPException(status_code=500, detail=str(e))

        sources = []
        for meta in res["metadatas"][0]:
            if meta and "scholarship_name" in meta:
                sources.append(meta["scholarship_name"])

        return {"response": response.text, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/collection/stats")
def get_collection_stats():
    """Get statistics about the indexed collection"""
    try:
        return {
            "total_documents": vector_db.count(),
            "collection_name": vector_db.get_name(),
            "metadata": {},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/collection/reset")
def reset_collection():
    """Reset the entire collection"""
    global vector_db
    import shutil

    try:
        if os.path.exists(settings.CHROMA_GEMINI_DB_PATH):
            shutil.rmtree(settings.CHROMA_GEMINI_DB_PATH)
        vector_db = ChromaWrapper(path=settings.CHROMA_GEMINI_DB_PATH)
        return {"status": "Collection reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "gpu_available": True,
        "embedding_model": "embedding-001",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HEAVY_SERVER_HOST, port=settings.HEAVY_SERVER_PORT)
