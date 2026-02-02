from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PerfumeBase(BaseModel):
    name: str
    brand: str
    designer: str
    price: Optional[float] = None
    size: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    # Fragrantica-specific fields
    rating: Optional[float] = None
    gender: Optional[str] = None
    year: Optional[int] = None
    top_notes: Optional[str] = None
    middle_notes: Optional[str] = None
    base_notes: Optional[str] = None
    longevity: Optional[str] = None
    sillage: Optional[str] = None

class PerfumeCreate(PerfumeBase):
    pass

class PerfumeResponse(PerfumeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ScrapingRequest(BaseModel):
    brand: str
    max_items: Optional[int] = 50
    source: Optional[str] = "all"  # "all", "fragrantica", "sephora", "fragrancex"