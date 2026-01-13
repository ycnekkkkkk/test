"""
Vercel Serverless Function wrapper for FastAPI backend
This file serves as the main entry point for all API routes
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.routes.test_session import router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IELTS Test API",
    description="API for IELTS Test with Gemini AI",
    version="1.0.0",
)

# CORS middleware - allow all origins for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


# Vercel serverless function handler
def handler(request):
    """
    Vercel serverless function handler
    This wraps FastAPI app to work with Vercel's serverless functions
    """
    from mangum import Mangum
    
    # Create Mangum adapter for FastAPI
    handler = Mangum(app, lifespan="off")
    
    # Convert Vercel request to ASGI
    return handler(request)


# For Vercel Python runtime
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)

