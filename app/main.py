from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.database import engine, Base
from app.api import scholarships, chat, eligibility, dashboard, students
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Agentic AI System for Scholarship Management",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scholarships.router)
app.include_router(chat.router)
app.include_router(eligibility.router)
app.include_router(dashboard.router)
app.include_router(students.router)


@app.on_event("startup")
async def startup_event():
    from app.services.rag_service import rag_service

    try:
        rag_service.index_scholarship_data()
        print("Scholarship data indexed successfully!")
    except Exception as e:
        print(f"Warning: Could not index scholarship data: {e}")


@app.get("/")
def root():
    return {
        "message": "Scholarship AI System API",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/frontend")
def serve_frontend():
    return FileResponse(
        os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.NORMAL_SERVER_HOST,
        port=settings.NORMAL_SERVER_PORT,
        reload=True,
    )
