from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from src.models.database import get_db
from src.models.perfume import PerfumeResponse, ScrapingRequest
from src.scrapers.fragrantica_scraper import FragranticaScraper
from src.scrapers.perfume_scraper import PerfumeScraper as LegacyScraper
from src.models.database import Perfume

router = APIRouter()

@router.post("/scrape", response_model=List[PerfumeResponse])
async def scrape_perfumes(
    request: ScrapingRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Scrape perfumes for a specific brand from multiple sources"""
    try:
        all_perfumes_data = []
        
        # Scrape from Fragrantica (primary source)
        if request.source in ["all", "fragrantica"]:
            print(f"Scraping from Fragrantica: {request.brand}")
            fragrantica_scraper = FragranticaScraper()
            fragrantica_data = fragrantica_scraper.scrape_all_sources(request.brand, request.max_items)
            all_perfumes_data.extend(fragrantica_data)
        
        # Scrape from legacy sources (Sephora, FragranceX)
        if request.source in ["all", "sephora", "fragrancex"]:
            print(f"Scraping from legacy sources: {request.brand}")
            legacy_scraper = LegacyScraper()
            legacy_limit = request.max_items if request.source != "all" else max(1, request.max_items // 2)
            legacy_data = legacy_scraper.scrape_all_sources(request.brand, legacy_limit)
            all_perfumes_data.extend(legacy_data)
        
        saved_perfumes = []
        for perfume_data in all_perfumes_data:
            # Check if perfume already exists
            existing = db.query(Perfume).filter(
                Perfume.name == perfume_data["name"],
                Perfume.brand == perfume_data["brand"]
            ).first()
            
            if not existing:
                db_perfume = Perfume(**perfume_data)
                db.add(db_perfume)
                db.commit()
                db.refresh(db_perfume)
                saved_perfumes.append(db_perfume)
            else:
                # Update existing record with new data if available
                if perfume_data.get("rating") and not existing.rating:
                    existing.rating = perfume_data.get("rating")
                if perfume_data.get("notes") and not existing.notes:
                    existing.notes = perfume_data.get("notes")
                if perfume_data.get("description") and not existing.description:
                    existing.description = perfume_data.get("description")
                db.commit()
                saved_perfumes.append(existing)
        
        return saved_perfumes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@router.get("/", response_model=List[PerfumeResponse])
async def get_perfumes(
    brand: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all perfumes, optionally filtered by brand"""
    query = db.query(Perfume)
    
    if brand:
        query = query.filter(Perfume.brand.ilike(f"%{brand}%"))
    
    perfumes = query.offset(skip).limit(limit).all()
    return perfumes

@router.get("/{perfume_id}", response_model=PerfumeResponse)
async def get_perfume(perfume_id: int, db: Session = Depends(get_db)):
    """Get a specific perfume by ID"""
    perfume = db.query(Perfume).filter(Perfume.id == perfume_id).first()
    if not perfume:
        raise HTTPException(status_code=404, detail="Perfume not found")
    return perfume

@router.delete("/{perfume_id}")
async def delete_perfume(perfume_id: int, db: Session = Depends(get_db)):
    """Delete a perfume by ID"""
    perfume = db.query(Perfume).filter(Perfume.id == perfume_id).first()
    if not perfume:
        raise HTTPException(status_code=404, detail="Perfume not found")
    
    db.delete(perfume)
    db.commit()
    return {"message": "Perfume deleted successfully"}

@router.get("/brands/list")
async def get_brands(db: Session = Depends(get_db)):
    """Get list of all available brands"""
    brands = db.query(Perfume.brand).distinct().all()
    return {"brands": [brand[0] for brand in brands if brand[0]]}