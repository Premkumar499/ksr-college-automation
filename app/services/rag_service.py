from typing import List, Dict, Any
from app.services.chroma_db import ChromaWrapper
from app.core.config import settings
import google.generativeai as genai


class RAGService:
    def __init__(self):
        self.client = True
        self.vector_db = ChromaWrapper(path=settings.CHROMA_GEMINI_DB_PATH)

        if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY.startswith("AIza"):
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
            print("Gemini client loaded successfully")
        else:
            self.model = None

    def get_relevant_context(self, query: str) -> str:
        """Get relevant context using vector search"""
        res = self.vector_db.query(query_texts=[query], n_results=3)
        if not res or not res.get("documents") or not res["documents"][0]:
            return ""
        return "\n\n".join(res["documents"][0])

    def generate_response(
        self, query: str, context: str, conversation_history: List[Dict] = None
    ) -> str:
        """Generate response using Gemini with context"""
        if context and self.client:
            return self._generate_with_context(query, context, conversation_history)
        else:
            return self._generate_no_context_response(query)

    def _generate_with_context(
        self, query: str, context: str, conversation_history: List[Dict] = None
    ) -> str:
        """Generate response using Gemini with context"""
        if not self.model:
            return self._generate_no_context_response(query)

        history_prompt = ""
        if conversation_history:
            for msg in conversation_history[-3:]:
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_prompt += f"{role}: {msg.get('content', '')}\n"

        prompt = f"""You are a helpful scholarship advisor. Answer the user's question using ONLY the provided scholarship information below.

IMPORTANT RULES:
1. Answer based ONLY on the scholarship information provided in the Context section
2. If the user asks about a specific scholarship, provide detailed information about ONLY that scholarship
3. Do NOT make up or add information that is not in the context
4. Format your response clearly with bullet points
5. Always include the scholarship name as the heading

{history_prompt}
User Question: {query}

=== SCHOLARSHIP INFORMATION (Use ONLY this) ===
{context}
=== END OF INFORMATION ===

Your Answer:"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._generate_no_context_response(query)

    def _generate_no_context_response(self, query: str) -> str:
        """Response when no context is available"""
        names = ["SC | SCA | ST | SCC Scholarships", "BC | MBC | DNC Scholarships", "Pudhumai Penn & Tamil Puthalvan Scheme"]

        return f"""I couldn't find specific information about that in my database.

Available Scholarships:
{chr(10).join(f"• {name}" for name in names)}

Try asking:
• "Tell me about BC scholarship"
• "Infosys STEM Stars eligibility"
• "What documents needed for SC scholarship?"
• "How to apply for Pudhumai scheme\""""

    def index_scholarship_data(self):
        """Load scholarships (already done in __init__)"""
        print(f"Loaded scholarships into vector DB")


# Global instance
rag_service = RAGService()
