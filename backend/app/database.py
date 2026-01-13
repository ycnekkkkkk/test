from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_session.db")

# Use SQLite for development, PostgreSQL for production (Vercel/Render)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
elif DATABASE_URL.startswith("postgresql"):
    # PostgreSQL connection with pooling for serverless
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=300,    # Recycle connections after 5 minutes
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
