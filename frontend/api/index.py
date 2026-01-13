"""
Vercel Serverless Function wrapper for FastAPI backend
This file serves as the main entry point for all API routes
"""
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '../../backend')
sys.path.insert(0, backend_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.test_session import router

# Create database tables (only if not exists)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database initialization note: {e}")

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
# Vercel Python runtime expects a handler function
from mangum import Mangum

# Create Mangum adapter for FastAPI (ASGI to AWS Lambda/Vercel format)
handler = Mangum(app, lifespan="off")

