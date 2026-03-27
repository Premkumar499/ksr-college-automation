from typing import List, Dict, Optional
from app.services.rag_service import rag_service
from app.models.database import ChatHistory
from sqlalchemy.orm import Session
import uuid


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def chat(
        self,
        query: str,
        student_id: Optional[int] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict:
        """Process a chat query using RAG"""

        # Determine intent and route appropriately
        query_lower = query.lower()

        # Check for image content
        if (
            "pasted-image" in query_lower
            or ".png" in query_lower
            or ".jpg" in query_lower
            or "data:image" in query_lower
        ):
            return {
                "response": "I can only process text questions. Please type your question instead of uploading an image.",
                "sources": [],
                "conversation_id": str(uuid.uuid4()),
            }

        # Get relevant context from RAG
        context = rag_service.get_relevant_context(query)

        # Generate response using Gemini
        response = rag_service.generate_response(
            query=query, context=context, conversation_history=conversation_history
        )

        # Extract sources
        sources = []
        if context:
            lines = context.split("\n---\n")
            for line in lines:
                if "[Source:" in line:
                    start = line.find("[Source:") + 9
                    end = line.find("]", start)
                    if end > start:
                        sources.append(line[start:end])

        # Generate conversation ID
        conversation_id = str(uuid.uuid4())

        # Save to chat history
        chat_record = ChatHistory(
            student_id=student_id,
            query=query,
            response=response,
            context_used={"sources": sources, "intent": self._detect_intent(query)},
        )
        self.db.add(chat_record)
        self.db.commit()

        return {
            "response": response,
            "sources": sources,
            "conversation_id": conversation_id,
        }

    def _detect_intent(self, query: str) -> str:
        """Simple intent detection"""
        query_lower = query.lower()

        if any(
            word in query_lower
            for word in ["eligible", "qualify", "can i apply", "am i eligible"]
        ):
            return "eligibility_check"
        elif any(
            word in query_lower for word in ["document", "required", "need to submit"]
        ):
            return "document_inquiry"
        elif any(
            word in query_lower
            for word in ["apply", "application", "how to apply", "procedure"]
        ):
            return "application_procedure"
        elif any(
            word in query_lower
            for word in ["list", "all scholarships", "available scholarships"]
        ):
            return "list_scholarships"
        elif any(word in query_lower for word in ["deadline", "last date", "due date"]):
            return "deadline_inquiry"
        else:
            return "general_inquiry"

    def get_conversation_context(self, student_id: int, limit: int = 5) -> List[Dict]:
        """Get recent conversation history for context"""
        history = (
            self.db.query(ChatHistory)
            .filter(ChatHistory.student_id == student_id)
            .order_by(ChatHistory.created_at.desc())
            .limit(limit)
            .all()
        )

        return [{"role": "user", "content": h.query} for h in reversed(history)]
