"""
SwasthyaSetu Unified Platform - All Services with Original Endpoints
Run with: uvicorn unified_main:app --host 0.0.0.0 --port 8000 --reload
"""
import sys
import os
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException, Request, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging
from typing import Optional, Dict, Any, List
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("swasthyasetu")

BASE_DIR = Path(__file__).parent

# Set environment variables
os.environ.setdefault("DATABASE_URL", "sqlite:///./swasthyasetu.db")
os.environ.setdefault("SECRET_KEY", "swasthyasetu-secret-key-change-in-production")
os.environ.setdefault("GOOGLE_AI_API_KEY", "AIzaSyDjo7b2-eW5Rfigq4fqv8rivfCiI9B6Oig")
os.environ.setdefault("GOOGLE_PROJECT_ID", "namaste-472613")
os.environ.setdefault("PROJECT_ID", "namaste-472613")

# Add service directories to Python path
service_paths = [
    BASE_DIR / "allergymapper",
    BASE_DIR / "ayushWhoSearch",
    BASE_DIR / "predictive_analytics_sih",
    BASE_DIR / "Claim_Validator",
]

for path in service_paths:
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

# Load services
allergy_app = None
ayush_app = None
predictive_app = None
claim_app = None

# Load Allergy Mapper
try:
    from main import app as allergy_app
    logger.info("✅ Allergy Mapper loaded")
except Exception as e:
    logger.error(f"❌ Allergy Mapper: {e}")

# Load AYUSH-WHO Search
try:
    import importlib.util
    ayush_path = BASE_DIR / "ayushWhoSearch" / "main.py"
    if not ayush_path.exists():
        ayush_path = BASE_DIR / "ayushWhoSearch" / "app.py"
    
    spec = importlib.util.spec_from_file_location("ayush_search", ayush_path)
    ayush_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ayush_module)
    ayush_app = ayush_module.app
    logger.info("✅ AYUSH-WHO Search loaded")
except Exception as e:
    logger.error(f"❌ AYUSH-WHO Search: {e}")

# Load Predictive Analytics
try:
    env_file = BASE_DIR / "predictive_analytics_sih" / ".env"
    if not env_file.exists():
        env_content = f"""SECRET_KEY={os.getenv('SECRET_KEY')}
DATABASE_URL={os.getenv('DATABASE_URL')}
GOOGLE_AI_API_KEY={os.getenv('GOOGLE_AI_API_KEY')}
GOOGLE_PROJECT_ID={os.getenv('GOOGLE_PROJECT_ID')}
PROJECT_ID={os.getenv('GOOGLE_PROJECT_ID')}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL_ASYNC=sqlite+aiosqlite:///./swasthyasetu.db
ENABLE_PREDICTIVE_ANALYTICS=True"""
        env_file.write_text(env_content)
    
    from app.main import app as predictive_app
    logger.info("✅ Predictive Analytics loaded")
except Exception as e:
    logger.error(f"❌ Predictive Analytics: {e}")

# Load Claim Validator
try:
    claim_path = BASE_DIR / "Claim_Validator" / "main.py"
    if not claim_path.exists():
        claim_path = BASE_DIR / "Claim_Validator" / "claim" / "main.py"
    
    spec = importlib.util.spec_from_file_location("claim_main", claim_path)
    claim_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(claim_module)
    claim_app = claim_module.app
    logger.info("✅ Claim Validator loaded")
except Exception as e:
    logger.error(f"❌ Claim Validator: {e}")

# Create main app
app = FastAPI(
    title="SwasthyaSetu - Unified Healthcare Platform",
    description="Integrated platform combining all healthcare services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount sub-applications
if allergy_app:
    app.mount("/api/allergy", allergy_app)
    logger.info("Mounted: /api/allergy")

if ayush_app:
    app.mount("/api/ayush", ayush_app)
    logger.info("Mounted: /api/ayush")

if predictive_app:
    app.mount("/api/predictive", predictive_app)
    logger.info("Mounted: /api/predictive")

if claim_app:
    app.mount("/api/claims", claim_app)
    logger.info("Mounted: /api/claims")

# ============= CONVENIENCE ENDPOINTS (Your Original Design) =============

@app.get("/search/{term}")
async def convenience_search(term: str, threshold: int = Query(default=80, ge=50, le=100)):
    """AYUSH search without /api/ayush prefix"""
    if not ayush_app:
        raise HTTPException(status_code=503, detail="AYUSH Search service unavailable")
    return RedirectResponse(url=f"/api/ayush/search/{term}?threshold={threshold}")

@app.get("/demo/health-passport")
async def convenience_demo_passport():
    """Demo health passport without /api/ayush prefix"""
    if not ayush_app:
        raise HTTPException(status_code=503, detail="AYUSH Search service unavailable")
    return RedirectResponse(url="/api/ayush/demo/health-passport")

@app.get("/meta/plans")
async def convenience_plans():
    """Insurance plans without /api/claims prefix"""
    if not claim_app:
        raise HTTPException(status_code=503, detail="Claims service unavailable")
    return RedirectResponse(url="/api/claims/meta/plans")

@app.get("/meta/packages")
async def convenience_packages(icd_code: Optional[str] = None, limit: int = 100):
    """HBP packages without /api/claims prefix"""
    if not claim_app:
        raise HTTPException(status_code=503, detail="Claims service unavailable")
    
    url = "/api/claims/meta/packages"
    params = []
    if icd_code:
        params.append(f"icd_code={icd_code}")
    if limit != 100:
        params.append(f"limit={limit}")
    if params:
        url += "?" + "&".join(params)
    
    return RedirectResponse(url=url)

@app.post("/validate_claim")
async def convenience_validate_claim(claim_data: dict = Body(...)):
    """Validate claim without /api/claims prefix"""
    if not claim_app:
        raise HTTPException(status_code=503, detail="Claims service unavailable")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/api/claims/validate_claim",
                json=claim_data,
                timeout=30.0
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============= ROOT ENDPOINTS =============

@app.get("/")
async def root():
    services = []
    
    if allergy_app:
        services.append({
            "name": "Allergy Mapper",
            "base_path": "/api/allergy",
            "status": "operational",
            "endpoints": {
                "health": "/api/allergy/health",
                "map_drug": "/api/allergy/map (POST)"
            }
        })
    
    if ayush_app:
        services.append({
            "name": "AYUSH-WHO Search",
            "base_path": "/api/ayush",
            "status": "operational",
            "endpoints": {
                "search": "/api/ayush/search/{term}",
                "demo_passport": "/api/ayush/demo/health-passport",
                "convenience_search": "/search/{term}",
                "convenience_demo": "/demo/health-passport"
            }
        })
    
    if predictive_app:
        services.append({
            "name": "Predictive Analytics",
            "base_path": "/api/predictive",
            "status": "operational",
            "endpoints": {
                "assessment": "/api/predictive/hybrid-assessment (POST)",
                "health": "/api/predictive/health"
            }
        })
    
    if claim_app:
        services.append({
            "name": "Claim Validator",
            "base_path": "/api/claims",
            "status": "operational",
            "endpoints": {
                "validate": "/api/claims/validate_claim (POST)",
                "plans": "/api/claims/meta/plans",
                "packages": "/api/claims/meta/packages",
                "convenience_validate": "/validate_claim (POST)",
                "convenience_plans": "/meta/plans",
                "convenience_packages": "/meta/packages"
            }
        })
    
    return {
        "message": "SwasthyaSetu - Unified Healthcare Platform",
        "version": "1.0.0",
        "status": "operational",
        "services": services,
        "total_services": len(services),
        "quick_tests": [
            'curl "http://localhost:8000/search/Diabetes"',
            'curl http://localhost:8000/demo/health-passport',
            'curl http://localhost:8000/meta/plans',
            'curl http://localhost:8000/api/allergy/health',
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "allergy_mapper": "operational" if allergy_app else "unavailable",
            "ayush_who_search": "operational" if ayush_app else "unavailable",
            "predictive_analytics": "operational" if predictive_app else "unavailable",
            "claim_validator": "operational" if claim_app else "unavailable",
        }
    }

@app.get("/api")
async def api_overview():
    return {
        "message": "SwasthyaSetu API Gateway",
        "available_apis": {
            "allergy_mapping": {"path": "/api/allergy", "status": "available" if allergy_app else "unavailable"},
            "ayush_search": {"path": "/api/ayush", "convenience": "/search/{term}", "status": "available" if ayush_app else "unavailable"},
            "predictive_analytics": {"path": "/api/predictive", "status": "available" if predictive_app else "unavailable"},
            "claim_validation": {"path": "/api/claims", "convenience": "/validate_claim", "status": "available" if claim_app else "unavailable"}
        }
    }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    path = request.url.path
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "path": path,
            "available_endpoints": [
                "/",
                "/health",
                "/search/{term}",
                "/demo/health-passport",
                "/meta/plans",
                "/meta/packages",
                "/validate_claim (POST)",
                "/api/allergy/*",
                "/api/ayush/*",
                "/api/predictive/*",
                "/api/claims/*"
            ]
        }
    )

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("🚀 SwasthyaSetu Unified Platform Starting...")
    print("="*80)
    print("\n📝 API Documentation: http://localhost:8000/docs")
    print("🔍 Service Discovery: http://localhost:8000/")
    print("\n💡 Quick Tests:")
    print('   curl "http://localhost:8000/search/Diabetes"')
    print('   curl http://localhost:8000/demo/health-passport')
    print('   curl http://localhost:8000/meta/plans')
    print("\n" + "="*80 + "\n")
    
    uvicorn.run(
        "unified_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )