import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app.core.config import settings
import google.generativeai as genai

genai.configure(api_key=settings.GOOGLE_API_KEY)
models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
print("AVAILABLE GENERATION MODELS:", models)
