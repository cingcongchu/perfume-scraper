from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./perfumes.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Perfume(Base):
    __tablename__ = "perfumes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String, index=True)
    designer = Column(String, index=True)
    price = Column(Float)
    size = Column(String)
    description = Column(Text)
    notes = Column(Text)
    image_url = Column(String)
    source_url = Column(String)
    # Fragrantica-specific fields
    rating = Column(Float)
    gender = Column(String)
    year = Column(Integer)
    top_notes = Column(Text)
    middle_notes = Column(Text)
    base_notes = Column(Text)
    longevity = Column(String)
    sillage = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()