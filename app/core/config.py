from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Scholarship AI System"
    VERSION: str = "1.0.0"

    # Database - PostgreSQL Configuration
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/scholarship_db"

    # Heavy Server (GPU) - RAG & AI Processing
    HEAVY_SERVER_URL: str = "http://localhost:8001"

    # Gemini API
    GOOGLE_API_KEY: Optional[str] = None

    # Chroma DB Path - separate paths for different embedding models
    CHROMA_DB_PATH: str = "./data/embeddings/chroma_db"
    CHROMA_HF_DB_PATH: str = "./data/embeddings/chroma_db_hf"  # For HuggingFace (384-dim)
    CHROMA_GEMINI_DB_PATH: str = (
        "./data/embeddings/chroma_db_gemini"  # For Gemini (768-dim)
    )

    # Server Config
    NORMAL_SERVER_HOST: str = "0.0.0.0"
    NORMAL_SERVER_PORT: int = 8000
    HEAVY_SERVER_HOST: str = "0.0.0.0"
    HEAVY_SERVER_PORT: int = 8001

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # HuggingFace API Key (optional)
    HUGGINGFACE_API_KEY: Optional[str] = None
    ANONYMIZED_TELEMETRY: Optional[str] = "False"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
