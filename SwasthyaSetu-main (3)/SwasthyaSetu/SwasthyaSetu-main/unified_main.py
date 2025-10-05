"""
SwasthyaSetu Unified Platform - Fixed Version
Run: uvicorn unified_main:app --host 0.0.0.0 --port 8000 --reload
"""
import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Optional, Dict, Any
import importlib.util
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("swasthyasetu")

BASE_DIR = Path(__file__).parent

# Verify required environment variables
required_vars = ["DATABASE_URL", "SECRET_KEY", "GOOGLE_AI_API_KEY", "GOOGLE_PROJECT_ID"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
    logger.warning("Create a .env file with: DATABASE_URL, SECRET_KEY, GOOGLE_AI_API_KEY, GOOGLE_PROJECT_ID")

def load_module(module_name: str, file_path: Path):
    """Safely load a module from file path"""
    try:
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
            
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec or not spec.loader:
            logger.error(f"Failed to create spec for {module_name}")
            return None
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        if hasattr(module, 'app'):
            logger.info(f"✅ Loaded {module_name}")
            return module.app
        else:
            logger.error(f"❌ {module_name} has no 'app' attribute")
            return None
    except Exception as e:
        logger.error(f"❌ Failed to load {module_name}: {e}")
        return None

# Store loaded services
services = {}

# 1. Load Allergy Mapper
allergy_path = BASE_DIR / "allergymapper" / "main.py"
allergy_app = load_module("allergy_service", allergy_path)
if allergy_app:
    services['allergy'] = allergy_app

# 2. Load AYUSH-WHO Search
ayush_path = BASE_DIR / "ayushWhoSearch" / "main.py"
ayush_app = load_module("ayush_service", ayush_path)
if ayush_app:
    services['ayush'] = ayush_app

# 3. Load Predictive Analytics
predictive_dir = BASE_DIR / "predictive_analytics_sih"
if predictive_dir.exists():
    # Create .env if needed
    env_file = predictive_dir / ".env"
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
    
    # Add to path
    if str(predictive_dir) not in sys.path:
        sys.path.insert(0, str(predictive_dir))
    
    try:
        from app.main import app as predictive_app
        
        # CRITICAL: Initialize AI for mounted app
        try:
            import google.generativeai as genai
            api_key = os.getenv("GOOGLE_AI_API_KEY")
            if api_key and api_key.strip():
                logger.info("Initializing Google AI for predictive service...")
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
                
                # Test the model
                test_response = model.generate_content(
                    "Hello",
                    generation_config=genai.GenerationConfig(temperature=0.5, max_output_tokens=10)
                )
                
                if test_response and getattr(test_response, "text", None):
                    predictive_app.state.ai_model = model
                    predictive_app.state.ai_available = True
                    logger.info("✅ Google AI initialized for predictive service")
                else:
                    logger.warning("⚠️ AI test failed - using fallback mode")
            else:
                logger.warning("⚠️ No Google AI API key - using fallback mode")
        except Exception as ai_error:
            logger.warning(f"⚠️ AI initialization failed: {ai_error} - using fallback mode")
        
        services['predictive'] = predictive_app
        logger.info("✅ Predictive Analytics loaded")
    except Exception as e:
        logger.error(f"❌ Predictive Analytics: {e}")

# 4. Load Claim Validator
claim_paths = [
    BASE_DIR / "Claim_Validator" / "claim" / "main.py",
    BASE_DIR / "Claim_Validator" / "main.py"
]

for claim_path in claim_paths:
    if claim_path.exists():
        claim_app = load_module("claim_service", claim_path)
        if claim_app:
            services['claims'] = claim_app
            break

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    logger.info("🚀 Starting SwasthyaSetu Unified Platform")
    logger.info(f"✅ Loaded {len(services)} services: {', '.join(services.keys())}")
    yield
    logger.info("Shutting down SwasthyaSetu")

# Create main app
app = FastAPI(
    title="SwasthyaSetu - Unified Healthcare Platform",
    description="Integrated platform for all healthcare services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
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
for name, service_app in services.items():
    try:
        app.mount(f"/api/{name}", service_app)
        logger.info(f"Mounted: /api/{name}")
    except Exception as e:
        logger.error(f"Failed to mount {name}: {e}")

# ============= ROOT ENDPOINTS =============

@app.get("/")
async def root():
    service_info = []
    
    if 'allergy' in services:
        service_info.append({
            "name": "Allergy Mapper",
            "path": "/api/allergy",
            "status": "operational",
            "endpoints": {
                "health": "/api/allergy/health",
                "map_drug": "/api/allergy/map (POST)"
            }
        })
    
    if 'ayush' in services:
        service_info.append({
            "name": "AYUSH-WHO Search",
            "path": "/api/ayush",
            "status": "operational",
            "endpoints": {
                "search": "/api/ayush/search/{term}",
                "demo_passport": "/api/ayush/demo/health-passport"
            }
        })
    
    if 'predictive' in services:
        service_info.append({
            "name": "Predictive Analytics",
            "path": "/api/predictive",
            "status": "operational",
            "endpoints": {
                "assessment": "/api/predictive/hybrid-assessment (POST)",
                "health": "/api/predictive/health"
            }
        })
    
    if 'claims' in services:
        service_info.append({
            "name": "Claim Validator",
            "path": "/api/claims",
            "status": "operational",
            "endpoints": {
                "validate": "/api/claims/validate_claim (POST)",
                "plans": "/api/claims/meta/plans"
            }
        })
    
    return {
        "message": "SwasthyaSetu - Unified Healthcare Platform",
        "version": "1.0.0",
        "status": "operational",
        "services": service_info,
        "total_services": len(services),
        "documentation": "/docs",
        "quick_tests": {
            "ayush_search": 'curl "http://localhost:8000/api/ayush/search/Diabetes"',
            "demo_passport": 'curl http://localhost:8000/api/ayush/demo/health-passport',
            "insurance_plans": 'curl http://localhost:8000/api/claims/meta/plans',
            "allergy_health": 'curl http://localhost:8000/api/allergy/health'
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "platform": "SwasthyaSetu",
        "version": "1.0.0",
        "services": {
            "allergy_mapper": "operational" if 'allergy' in services else "unavailable",
            "ayush_who_search": "operational" if 'ayush' in services else "unavailable",
            "predictive_analytics": "operational" if 'predictive' in services else "unavailable",
            "claim_validator": "operational" if 'claims' in services else "unavailable"
        },
        "total_loaded": len(services)
    }

# ============= CONVENIENCE ENDPOINTS (from your original design) =============

@app.get("/search/{term}")
async def convenience_search(term: str, threshold: int = Query(default=80, ge=50, le=100)):
    """AYUSH search without /api/ayush prefix - forwards to mounted service"""
    if 'ayush' not in services:
        raise HTTPException(status_code=503, detail="AYUSH Search service unavailable")
    
    # Forward to the mounted service
    import httpx
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://localhost:8000/api/ayush/search/{term}",
                params={"threshold": threshold},
                timeout=30.0
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/demo/health-passport")
async def convenience_demo_passport():
    """Demo health passport without /api/ayush prefix"""
    if 'ayush' not in services:
        raise HTTPException(status_code=503, detail="AYUSH Search service unavailable")
    
    import httpx
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "http://localhost:8000/api/ayush/demo/health-passport",
                timeout=30.0
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

@app.get("/meta/plans")
async def convenience_plans():
    """Insurance plans without /api/claims prefix"""
    if 'claims' not in services:
        raise HTTPException(status_code=503, detail="Claims service unavailable")
    
    import httpx
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "http://localhost:8000/api/claims/meta/plans",
                timeout=30.0
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

@app.get("/meta/packages")
async def convenience_packages(icd_code: Optional[str] = None, limit: int = 100):
    """HBP packages without /api/claims prefix"""
    if 'claims' not in services:
        raise HTTPException(status_code=503, detail="Claims service unavailable")
    
    import httpx
    async with httpx.AsyncClient() as client:
        try:
            params = {}
            if icd_code:
                params["icd_code"] = icd_code
            if limit != 100:
                params["limit"] = limit
                
            response = await client.get(
                "http://localhost:8000/api/claims/meta/packages",
                params=params,
                timeout=30.0
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

@app.post("/validate_claim")
async def convenience_validate_claim(claim_data: dict = Body(...)):
    """Validate claim without /api/claims prefix"""
    if 'claims' not in services:
        raise HTTPException(status_code=503, detail="Claims service unavailable")
    
    import httpx
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
            raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@app.post("/map")
async def convenience_allergy_map(request: dict = Body(...)):
    """Allergy mapping without /api/allergy prefix"""
    if 'allergy' not in services:
        raise HTTPException(status_code=503, detail="Allergy service unavailable")
    
    import httpx
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/api/allergy/map",
                json=request,
                timeout=30.0
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Mapping failed: {str(e)}")

@app.post("/hybrid-assessment")
async def convenience_hybrid_assessment(data: dict = Body(...)):
    """Hybrid assessment without /api/predictive prefix"""
    if 'predictive' not in services:
        raise HTTPException(status_code=503, detail="Predictive service unavailable")
    
    import httpx
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/api/predictive/hybrid-assessment",
                json=data,
                timeout=30.0
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "path": str(request.url.path),
            "hint": "Try /api/ayush/search/Diabetes or /search/Diabetes",
            "available_services": list(services.keys()),
            "documentation": "/docs"
        }
    )

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("🚀 SwasthyaSetu Unified Platform")
    print("="*80)
    print(f"\n✅ Loaded Services: {', '.join(services.keys()) if services else 'None'}")
    print(f"📊 Total Services: {len(services)}/4")
    print("\n📝 API Documentation: http://localhost:8000/docs")
    print("🔍 Service Status: http://localhost:8000/health")
    print("\n💡 Quick Tests:")
    if 'ayush' in services:
        print('   curl "http://localhost:8000/api/ayush/search/Diabetes"')
    if 'allergy' in services:
        print('   curl http://localhost:8000/api/allergy/health')
    print("\n" + "="*80 + "\n")
    
    uvicorn.run(
        "unified_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )