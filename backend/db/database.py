from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import Generator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in environment")

# Optional: enable pool_pre_ping to avoid stale connections; set echo via env
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=(os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"),
)

# expire_on_commit=False keeps objects usable after commit (choose based on app needs)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()