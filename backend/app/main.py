from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.test_session import router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IELTS Test API",
    description="API for IELTS Test with Gemini AI",
    version="1.0.0",
)

# CORS middleware
import os

allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    # Railway frontend domain
    "https://test-production-73f1.up.railway.app",
]

# Add frontend domain from environment variable (for Railway deployment)
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

# Allow all origins in production (for Railway deployment)
# Railway sets RAILWAY_ENVIRONMENT automatically
if (
    os.getenv("RAILWAY_ENVIRONMENT") == "production"
    or os.getenv("ENVIRONMENT") == "production"
    or os.getenv("RENDER") == "true"
):
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api", tags=["test-session"])


@app.get("/")
def read_root():
    return {"message": "IELTS Test API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
