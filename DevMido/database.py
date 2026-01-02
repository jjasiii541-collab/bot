from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)  # Changed to String for BigInt safety
    is_vip = Column(Boolean, default=False)
    has_paid = Column(Boolean, default=False)
    star_count = Column(Integer, default=100) # Added to store custom star count
    groups = Column(Text, default="") # Added to store group links

class TelegramSession(Base):
    __tablename__ = "telegram_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # Changed to String for BigInt safety
    session_string = Column(Text, unique=True)
    is_active = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
