import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app.services.rag_service import rag_service

query = "tell about bc scholorschips"
print("Fetching context...")
context = rag_service.get_relevant_context(query)
print("CONTEXT RETRIEVED:")
print(context)
print("---")
print("Generating response...")
response = rag_service.generate_response(query=query, context=context)
print("RESPONSE GENERATED:")
print(response)
