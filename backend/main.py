from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.routes.perfume import router as perfume_router
from src.models.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Perfume Web Scraper API",
    description="API for scraping designer perfume data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local frontend
        "http://localhost:3001",  # Alternative local port
        "http://localhost:3002",  # Alternative local port
        "https://*.vercel.app",   # Vercel deployment
        "https://*.netlify.app",  # Netlify deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(perfume_router, prefix="/api/perfumes", tags=["perfumes"])

@app.get("/")
async def root():
    return {"message": "Perfume Web Scraper API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)