import os
from typing import List, Dict, Optional, Any
from app.core.config import settings
from app.services.faiss_db import FaissDB

import requests


class RAGService:
    def __init__(self):
        self.faiss_db = FaissDB(settings.FAISS_DB_PATH, dim=384)
        self.hf_api_key = settings.HUGGINGFACE_API_KEY
        self.embed_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"

        # Configure Gemini if API key is available (for response generation)
        self.client = None
        if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY.startswith("AIza"):
            from google import genai

            self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings from HuggingFace API"""
        if not self.hf_api_key:
            raise Exception("HuggingFace API key not configured")

        headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        response = requests.post(
            self.embed_url, headers=headers, json={"inputs": texts}, timeout=30
        )

        if response.status_code == 403:
            raise Exception("Invalid HuggingFace API key")
        if response.status_code == 503:
            raise Exception("Model is loading. Please try again in a few seconds.")

        response.raise_for_status()
        result = response.json()

        # Handle both single and batch responses
        if isinstance(result, list):
            if len(result) == 1:
                return [result[0]] if isinstance(result[0], list) else result
            return result
        return result

    def add_documents(self, documents: List[Dict[str, str]]):
        """Add documents to the vector database"""
        if not documents:
            return

        texts = [doc["content"] for doc in documents]

        try:
            embeddings = self.get_embeddings(texts)
        except Exception as e:
            print(f"Failed to embed documents: {e}")
            return

        metadatas = [
            {
                "source": doc.get("source", "unknown"),
                "scholarship_name": doc.get("scholarship_name", ""),
                "doc_type": doc.get("doc_type", "general"),
            }
            for doc in documents
        ]

        self.faiss_db.add(embeddings=embeddings, documents=texts, metadatas=metadatas)

    def query(self, query_text: str, n_results: int = 5) -> Dict[str, Any]:
        """Query the vector database"""
        try:
            embeddings = self.get_embeddings([query_text])
            q_emb = embeddings[0]
        except Exception as e:
            print(f"Failed to embed query: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        return self.faiss_db.query([q_emb], n_results=n_results)

    def get_relevant_context(self, query: str, max_docs: int = 5) -> str:
        """Get relevant context from vector DB for a query"""
        results = self.query(query, n_results=max_docs)

        if not results or not results.get("documents") or not results["documents"][0]:
            return ""

        documents = results["documents"][0]
        metadatas = results.get("metadatas", [[]])[0]

        context_parts = []
        for doc, meta in zip(documents, metadatas):
            source = meta.get("source", "Unknown") if meta else "Unknown"
            doc_type = meta.get("doc_type", "general") if meta else "general"
            context_parts.append(f"[Source: {source} ({doc_type})]\n{doc}")

        return "\n\n---\n\n".join(context_parts)

    def generate_response(
        self, query: str, context: str, conversation_history: List[Dict] = None
    ) -> str:
        """Generate response using Gemini with RAG context"""
        if context and self.client:
            return self._generate_with_context(query, context, conversation_history)
        else:
            return self._generate_without_context(query, conversation_history)

    def _generate_with_context(
        self, query: str, context: str, conversation_history: List[Dict] = None
    ) -> str:
        """Generate response using Gemini with context"""
        if not self.client:
            return self._generate_without_context(query, conversation_history)

        history_prompt = ""
        if conversation_history:
            for msg in conversation_history[-5:]:
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_prompt += f"{role}: {msg.get('content', '')}\n"

        prompt = f"""You are a helpful scholarship advisor assistant for a college. Use the following context to answer the user's question accurately.

Context from scholarship documents:
{context}

{history_prompt}
User: {query}

Format your response like this (use line breaks for readability):

**Scholarship Name:** [name]
**Description:** [brief description]
**Eligibility Criteria:** [list each criterion on a new line with bullet points]
**Documents Required:** [list each document on a new line with bullet points]
**Application Procedure:** [step by step procedure]
**Amount:** [scholarship amount if available]
**Provider:** [who provides this scholarship]

If information is not available, write "Not specified" for that field."""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            return response.text
        except Exception as e:
            return self._generate_without_context(query, conversation_history)

    def _generate_without_context(
        self, query: str, conversation_history: List[Dict] = None
    ) -> str:
        """Generate response without external API (fallback)"""
        query_lower = query.lower()

        if any(
            word in query_lower
            for word in ["eligible", "qualify", "can i apply", "check eligibility"]
        ):
            return """Based on your query, I recommend using the **Check Eligibility** tab on this portal.

To check your scholarship eligibility:
1. Go to the **Check Eligibility** tab
2. Fill in your details (GPA, category, income, etc.)
3. Click **Check Eligibility** to see scholarships you qualify for

This will give you personalized results based on your academic profile."""

        elif any(
            word in query_lower for word in ["document", "required", "need to submit"]
        ):
            return """Common documents required for scholarships:

• Community Certificate
• Income Certificate  
• Previous Year Marksheet
• Aadhar Card
• Bank Account Details
• Passport Size Photos
• Caste Certificate (if applicable)

Note: Specific requirements vary by scholarship. Please check individual scholarship details."""

        elif any(
            word in query_lower for word in ["apply", "application", "how to apply"]
        ):
            return """To apply for scholarships:

1. **National Scholarship Portal (NSP):** Visit https://scholarships.gov.in/
2. **State Scholarship Portals:** Check your state's scholarship website
3. **College Scholarships:** Contact your college scholarship cell

Steps:
• Register on the portal
• Fill in your details
• Upload required documents
• Submit before the deadline"""

        elif any(
            word in query_lower
            for word in ["sc", "st", "scc", "bc", "mbc", "dnc", "category"]
        ):
            return """**Government of Tamil Nadu Scholarships:**

**SC | SCA | ST | SCC Scholarships:**
• Annual Family Income: Below ₹2.5 Lakhs
• Quota: Government & Management Quota
• Required: Community Certificate, Income Certificate, Aadhaar

**BC | MBC | DNC Scholarships:**
• Annual Family Income: Below ₹2.5 Lakhs
• Quota: Government Quota Only (7.5 Category Not Eligible)
• Required: Community Certificate, Income Certificate, First Graduation Certificate

**Pudhumai Penn & Tamil Puthalvan Scheme:**
• For students from 6th to 12th Government School
• Bank Seeding Active required

Visit https://scholarships.gov.in/ for applications."""

        elif any(
            word in query_lower for word in ["aicte", "swanath", "saksham", "pragati"]
        ):
            return """**AICTE Scholarships on National Scholarship Portal:**

**1. Swanath Scholarship:**
• For Orphan students / Wards of Armed Forces martyred in action
• Income: ≤ ₹8,00,000
• Technical Diploma/Degree students

**2. Saksham Scholarship:**
• For Specially Abled Students (≥40% disability)
• Income: ≤ ₹8,00,000
• First year Technical Degree/Diploma

**3. Pragati Scholarship:**
• For Girl Students only
• Income: ≤ ₹8,00,000
• 1st year or 2nd year (lateral entry)

Apply at: https://scholarships.gov.in/"""

        elif any(
            word in query_lower for word in ["private", "reliance", "aspire", "infosys"]
        ):
            return """**Private Scholarships:**

**Aspire - Harihara Subramanian Scholarship:**
• 70%+ in 10th & 12th
• First-Year: CSE/IT/ECE/EEE/VLSI/AI & DS/AIML
• Income: ≤ ₹3 Lakhs
• Link: https://pearltrifoundation.org/form/

**Reliance Foundation Undergraduate Scholarship:**
• 60%+ in 12th
• 1st year regular UG degree
• Income: < ₹15 Lakhs (preference < ₹2.5 Lakhs)

**Reliance Foundation Postgraduate Scholarship:**
• GATE score 550-1000 OR 7.5+ CGPA
• Engineering/Technology/Life Sciences
• Link: Reliance Foundation site

**Infosys STEM Stars Scholarship:**
• Indian female students only
• 1st year STEM courses at NIRF institutions
• Income: ≤ ₹8 Lakhs
• Link: https://www.buddy4study.com/page/infosys-stem-stars-scholarship"""

        elif any(word in query_lower for word in ["deadline", "last date", "due date"]):
            return """Scholarship deadlines vary by scheme:

• **SC/SCA/ST/SCC Scholarships:** June 30
• **BC/MBC/DNC Scholarships:** July 15
• **Pudhumai Penn Scheme:** August 31
• **NSP Scholarships:** August 31

Please check https://scholarships.gov.in/ for exact dates."""

        elif any(
            word in query_lower for word in ["list", "all scholarships", "available"]
        ):
            return """**Available Scholarships:**

**Government (Tamil Nadu):**
• SC | SCA | ST | SCC Scholarships
• BC | MBC | DNC Scholarships
• Pudhumai Penn & Tamil Puthalvan Scheme

**National Scholarship Portal (NSP):**
• AICTE – Swanath Scholarship
• AICTE – Saksham Scholarship
• AICTE – Pragati Scholarship
• PM-USP Special Scholarship (J&K students)
• AICTE – GATE/CEED Scholarship

**Private:**
• Aspire - Harihara Subramanian Scholarship
• Reliance Foundation Scholarships
• Infosys STEM Stars Scholarship

Visit **Dashboard** tab for more details!"""

        else:
            return """I'm here to help with scholarship information!

I can assist with:
• Checking your eligibility
• Required documents
• Application procedures
• Scholarship deadlines
• List of available scholarships
• Category-specific scholarships (SC/ST/BC/OBC)

Try asking:
• "Am I eligible for SC scholarship?"
• "What documents do I need?"
• "How to apply for AICTE scholarships?"
• "List private scholarships"

Or use the **Check Eligibility** tab for personalized results!"""

    def index_scholarship_data(self):
        """Index all scholarship data from add_data.py format"""
        documents = [
            # SC | SCA | ST | SCC Scholarships
            {
                "content": """SC | SCA | ST | SCC Scholarships - Government of Tamil Nadu
Eligibility Criteria:
- Government Quota & Management Quota (7.5 Category Not Eligible)
- Annual Family Income Below ₹2.5 Lakhs
- Bank Seeding Active with Individual Bank Account

Required Documents:
- Community Certificate
- Income Certificate
- Allotment Order (Government Quota Counselling Students Only)
- Aadhaar Xerox
- Aadhar Linked Mobile Number & Phone

Application: Apply through Tamil Nadu scholarship portal""",
                "source": "Government of Tamil Nadu",
                "scholarship_name": "SC | SCA | ST | SCC Scholarships",
                "doc_type": "government_scholarship",
            },
            # BC | MBC | DNC Scholarships
            {
                "content": """BC | MBC | DNC Scholarships - Government of Tamil Nadu
Eligibility Criteria:
- Government Quota Only (7.5 Category & Management Quota Students Not Eligible)
- Annual Family Income Below ₹2.5 Lakhs
- Bank Seeding Active with Individual Bank Account

Required Documents:
- Community Certificate
- Income Certificate
- First Graduation Certificate
- Provisional Allotment Order (DoTE)
- Aadhaar Xerox
- Aadhar Linked Mobile Number & Phone

Application: Apply through Tamil Nadu scholarship portal""",
                "source": "Government of Tamil Nadu",
                "scholarship_name": "BC | MBC | DNC Scholarships",
                "doc_type": "government_scholarship",
            },
            # Pudhumai Penn
            {
                "content": """Pudhumai Penn & Tamil Puthalvan Scheme - Government of Tamil Nadu
Eligibility Criteria:
- 6th to 12th Government School (Tamil & English Medium)
- 6th to 12th Government Fully Aided School (Tamil Medium Only)
- Bank Seeding Active with Individual Bank Account

Required Documents:
- 10th & 12th Marksheet & TC
- Aadhar Linked Mobile Number & Phone

Application: Apply through Tamil Nadu scholarship portal""",
                "source": "Government of Tamil Nadu",
                "scholarship_name": "Pudhumai Penn & Tamil Puthalvan Scheme",
                "doc_type": "government_scholarship",
            },
            # AICTE Swanath
            {
                "content": """AICTE – Swanath Scholarship Scheme
For Technical Diploma and Technical Degree
Eligibility:
- Orphan students who lost one or both parents due to COVID-19
- Wards of Armed Forces/Central Paramilitary Forces martyred in action
- Annual family income ≤ ₹8,00,000
- Must be enrolled in AICTE-approved regular diploma/degree programs

Application: https://scholarships.gov.in/""",
                "source": "National Scholarship Portal",
                "scholarship_name": "AICTE – Swanath Scholarship",
                "doc_type": "aicte_scholarship",
            },
            # AICTE Saksham
            {
                "content": """AICTE – Saksham Scholarship Scheme
For Specially Abled Students – Technical Degree/Diploma
Eligibility:
- Open to students with ≥40% disability
- Annual family income ≤ ₹8,00,000
- Admitted to first year of AICTE-approved technical degree/diploma course

Application: https://scholarships.gov.in/""",
                "source": "National Scholarship Portal",
                "scholarship_name": "AICTE – Saksham Scholarship",
                "doc_type": "aicte_scholarship",
            },
            # AICTE Pragati
            {
                "content": """AICTE – Pragati Scholarship Scheme
For Girl Students – Technical Degree/Diploma
Eligibility:
- Admitted in 1st year or 2nd year (lateral entry) of AICTE-approved institution
- Maximum 2 girl students per family can apply
- Annual family income ≤ ₹8,00,000
- For married applicants, higher income of parents or in-laws will be considered

Application: https://scholarships.gov.in/""",
                "source": "National Scholarship Portal",
                "scholarship_name": "AICTE – Pragati Scholarship",
                "doc_type": "aicte_scholarship",
            },
            # PM-USP
            {
                "content": """PM-USP Special Scholarship Scheme
For Students from Jammu & Kashmir and Ladakh
Eligibility:
- Domicile of Jammu & Kashmir or Ladakh
- Passed Class 12 from JKBOSE or CBSE in 2021–22 or 2022–23
- Diploma holders from UT polytechnics eligible for 2nd-year admission
- Annual family income < ₹8,00,000

Application: https://scholarships.gov.in/""",
                "source": "National Scholarship Portal",
                "scholarship_name": "PM-USP Special Scholarship",
                "doc_type": "aicte_scholarship",
            },
            # GATE Scholarship
            {
                "content": """AICTE – GATE/CEED Scholarship
For full-time AICTE-approved PG programs
Eligibility:
- Must have a valid GATE/CEED 2025 score at the time of admission
- Only for students in full-time AICTE-approved PG programs
- Not eligible: Foreign students, sponsored/management quota, or part-time students
- Must have an Aadhar-linked savings bank account (not joint or Jan-Dhan)
- Must upload valid SC/ST/OBC (NCL)/PH certificates if applicable
- Available for up to 24 months or until course completion/thesis submission

Application: https://scholarships.gov.in/""",
                "source": "National Scholarship Portal",
                "scholarship_name": "AICTE – GATE/CEED Scholarship",
                "doc_type": "aicte_scholarship",
            },
            # Aspire Scholarship
            {
                "content": """Aspire - Harihara Subramanian Scholarship
Provider: Pearl Tri Foundation
Eligibility:
- Students must have scored 70% or above in both 10th and 12th standard examinations
- Open to First-Year students from: CSE / IT / ECE / EEE / VLSI / AI & DS / AIML
- Both Counselling and Management quota students are eligible to apply
- Annual family income should be ₹3.0 lakhs or below

Application: https://pearltrifoundation.org/form/""",
                "source": "Private - Pearl Tri Foundation",
                "scholarship_name": "Aspire - Harihara Subramanian Scholarship",
                "doc_type": "private_scholarship",
            },
            # Reliance Foundation UG
            {
                "content": """Reliance Foundation Undergraduate Scholarship
Eligibility:
- Be a resident citizen of India
- Students who have passed std. 12th with a minimum of 60% marks
- Enrolled in 1st year regular full-time UG degree in any stream
- Students having House Hold income < Rs. 15 lakhs (preference given to <Rs.2.5 lakhs)

Application: Undergraduate Scholarship Details & Application on Reliance Foundation site""",
                "source": "Private - Reliance Foundation",
                "scholarship_name": "Reliance Foundation Undergraduate Scholarship",
                "doc_type": "private_scholarship",
            },
            # Reliance Foundation PG
            {
                "content": """Reliance Foundation Postgraduate Scholarships
Eligibility:
- Resident of India
- First year regular full time PG Students
- Score of 550 - 1,000 in the GATE Examination OR
- Students who have scored 7.5 or above in their Undergraduate CGPA
- Eligible degree programmes – Engineering, Technology, Energy and Life-Sciences

Application: Postgraduate Scholarship Details & Application on Reliance Foundation site""",
                "source": "Private - Reliance Foundation",
                "scholarship_name": "Reliance Foundation Postgraduate Scholarships",
                "doc_type": "private_scholarship",
            },
            # Infosys STEM Stars
            {
                "content": """Infosys Foundation STEM Stars Scholarship Program
Eligibility:
- Candidates must be Indian female students
- Candidates must have completed Class 12
- Students must be enrolled in first-year undergraduate courses at NIRF-accredited institutions in STEM-related courses
- Also eligible: second-year B.Arch or five-year Integrated/Dual Degree courses
- Annual family income ≤ ₹8,00,000

Application: https://www.buddy4study.com/page/infosys-stem-stars-scholarship""",
                "source": "Private - Infosys Foundation",
                "scholarship_name": "Infosys Foundation STEM Stars Scholarship",
                "doc_type": "private_scholarship",
            },
        ]

        self.add_documents(documents)
        print(f"Indexed {len(documents)} scholarship documents to FAISS")


rag_service = RAGService()
