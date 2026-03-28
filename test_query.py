import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app.core.config import settings
from app.services.chroma_db import ChromaWrapper

vector_db = ChromaWrapper(path=settings.CHROMA_GEMINI_DB_PATH)
query = "What is the scholarship for ST?"
res = vector_db.query(query_texts=[query], n_results=1)

if res and res.get("documents") and res["documents"][0]:
    print("VERIFICATION SUCCESS!")
    print("Query:", query)
    print("Result:", res["documents"][0][0])
else:
    print("VERIFICATION FAILED! No documents returned.")
