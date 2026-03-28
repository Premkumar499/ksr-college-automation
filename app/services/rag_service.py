from typing import List, Dict
from app.services.search_service import search_service


class RAGService:
    def __init__(self):
        self.client = None
        self.search = search_service

        from app.core.config import settings

        if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY.startswith("AIza"):
            from google import genai

            self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
            print("Gemini client loaded successfully")

    def get_relevant_context(self, query: str) -> str:
        """Get relevant context using keyword search"""
        return self.search.get_context(query)

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
        if not self.client:
            return context

        history_prompt = ""
        if conversation_history:
            for msg in conversation_history[-3:]:
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_prompt += f"{role}: {msg.get('content', '')}\n"

        prompt = f"""You are a helpful scholarship advisor. Answer the user's question using ONLY the provided scholarship information.

IMPORTANT RULES:
1. Answer based ONLY on the scholarship information provided
2. Provide detailed information about ONLY the scholarship mentioned
3. Do NOT add information not in the context
4. Format your response clearly with bullet points
5. Include the scholarship name as heading

{history_prompt}
User Question: {query}

=== SCHOLARSHIP INFORMATION ===
{context}
=== END ===

Your Answer:"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return context

    def _generate_no_context_response(self, query: str) -> str:
        """Response when no context is available"""
        names = self.search.get_all_names()

        return f"""I couldn't find specific information about that scholarship.

Available Scholarships:
{chr(10).join(f"• {name}" for name in names)}

Try asking:
• "Tell me about BC scholarship"
• "Infosys STEM Stars eligibility"
• "What documents needed for SC scholarship\""""

    def index_scholarship_data(self):
        """Load scholarships"""
        print(f"Loaded {len(self.search.scholarships)} scholarships")


rag_service = RAGService()
