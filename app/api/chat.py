from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.scholarship import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post("/", response_model=ChatResponse)
def chat(query: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat with the scholarship AI assistant.

    The chatbot can help with:
    - Scholarship details and eligibility
    - Application procedures
    - Required documents
    - General scholarship queries
    """
    # Check if query contains pasted image content (only specific browser paste patterns)
    query_lower = query.query.lower()
    # Only block actual pasted image filenames from browser, not general text
    if (
        "pasted-image-" in query_lower
        or "data:image" in query_lower
        or "blob:" in query_lower
    ):
        raise HTTPException(
            status_code=400,
            detail="I can only process text questions. Please type your question instead of uploading an image.",
        )

    chat_service = ChatService(db)

    try:
        result = chat_service.chat(
            query=query.query,
            student_id=query.student_id,
            conversation_history=query.conversation_history,
        )

        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            conversation_id=result["conversation_id"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{student_id}")
def get_chat_history(student_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get chat history for a student"""
    chat_service = ChatService(db)
    history = chat_service.get_conversation_context(student_id, limit=limit)
    return {"history": history}



