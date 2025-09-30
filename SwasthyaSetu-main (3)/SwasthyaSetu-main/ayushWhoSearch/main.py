# from fastapi import FastAPI, HTTPException, Header, Depends, Query
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# import pandas as pd
# from rapidfuzz import fuzz
# from datetime import datetime, timedelta
# import jwt
# import requests
# import json
# from typing import Optional, Dict, Any
# import uuid
# import os

# app = FastAPI(title="AYUSH ↔ WHO Semantic Search API with ABHA Integration")

# # ABHA Configuration - Update these when you get real credentials
# ABHA_CONFIG = {
#     "client_id": os.getenv("ABHA_CLIENT_ID", ""),
#     "client_secret": os.getenv("ABHA_CLIENT_SECRET", ""),
#     "base_url": "https://abhasbx.abdm.gov.in/gateway",  # Sandbox URL
#     "production_url": "https://abha.abdm.gov.in/gateway",  # Production URL
#     "auth_url": "https://abhasbx.abdm.gov.in/gateway/v0.5/sessions",
#     "token_url": "https://abhasbx.abdm.gov.in/gateway/v0.5/auth/authConfirm"
# }

# # Security scheme for ABHA token
# security = HTTPBearer()

# # Load CSV
# BASE_DIR = os.path.dirname(__file__)
# CSV_PATH = os.path.join(BASE_DIR, "candidate_mappings_semantic_v2.csv")

# try:
#     df = pd.read_csv(CSV_PATH)
#     # Preprocess lowercase columns
#     df["AYUSH_Term_lower"] = df["AYUSH_Term"].str.lower()
#     df["WHO_Term_lower"] = df["WHO_Term_Candidate"].str.lower()
#     print(f"✅ Loaded {len(df)} mappings from CSV")
# except Exception as e:
#     print(f"❌ Error loading CSV: {e}")
#     df = pd.DataFrame()

# def fuzzy_match(term: str, candidates: pd.Series, threshold: int = 80) -> pd.Series:
#     """Return boolean mask where term matches candidate fuzzily above threshold."""
#     return candidates.apply(lambda x: fuzz.partial_ratio(str(x).lower(), term.lower()) >= threshold)

# class ABHAAuthManager:
#     """Handles ABHA OAuth authentication and token management"""
    
#     def __init__(self):
#         self.access_token = None
#         self.token_expires_at = None
#         self.session_token = None
    
#     async def get_session_token(self) -> str:
#         """Get initial session token from ABHA gateway"""
#         if not ABHA_CONFIG["client_id"] or not ABHA_CONFIG["client_secret"]:
#             raise HTTPException(
#                 status_code=503, 
#                 detail="ABHA credentials not configured. Please set ABHA_CLIENT_ID and ABHA_CLIENT_SECRET environment variables."
#             )
        
#         try:
#             headers = {
#                 "Content-Type": "application/json",
#                 "Accept": "application/json"
#             }
            
#             payload = {
#                 "clientId": ABHA_CONFIG["client_id"],
#                 "clientSecret": ABHA_CONFIG["client_secret"]
#             }
            
#             response = requests.post(
#                 ABHA_CONFIG["auth_url"],
#                 headers=headers,
#                 json=payload,
#                 timeout=30
#             )
            
#             if response.status_code == 200:
#                 data = response.json()
#                 self.session_token = data.get("accessToken")
#                 return self.session_token
#             else:
#                 raise HTTPException(status_code=401, detail=f"ABHA session failed: {response.text}")
                
#         except requests.exceptions.RequestException as e:
#             raise HTTPException(status_code=503, detail=f"ABHA service unavailable: {str(e)}")
    
#     async def validate_user_token(self, token: str) -> Dict[str, Any]:
#         """Validate user's ABHA token and extract user info"""
#         if not token:
#             raise HTTPException(status_code=401, detail="Missing ABHA token")
        
#         # If no credentials configured, use dummy validation
#         if not ABHA_CONFIG["client_id"] or not ABHA_CONFIG["client_secret"]:
#             return self._dummy_token_validation(token)
        
#         try:
#             # Real ABHA token validation would go here
#             # For now, using dummy validation until credentials are available
#             return self._dummy_token_validation(token)
            
#         except Exception as e:
#             raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")
    
#     def _dummy_token_validation(self, token: str) -> Dict[str, Any]:
#         """Dummy token validation for testing without real ABHA credentials"""
#         # Accept specific test tokens for different user types
#         test_tokens = {
#             "test_patient_001": {
#                 "abha_id": "12-3456-7890-1234", 
#                 "name": "Test Patient",
#                 "mobile": "+91-98765-43210"
#             },
#             "test_doctor_001": {
#                 "abha_id": "98-7654-3210-9876", 
#                 "name": "Dr. Test Physician",
#                 "mobile": "+91-87654-32109",
#                 "role": "doctor"
#             },
#             "demo_user": {
#                 "abha_id": "11-1111-1111-1111", 
#                 "name": "Demo User",
#                 "mobile": "+91-99999-99999"
#             }
#         }
        
#         if token in test_tokens:
#             return test_tokens[token]
#         elif len(token) >= 8:  # Accept any token with 8+ characters for demo
#             return {
#                 "abha_id": f"00-0000-0000-{token[-4:].zfill(4)}", 
#                 "name": f"User {token[-4:]}",
#                 "mobile": "+91-XXXX-XXXXX"
#             }
#         else:
#             raise HTTPException(status_code=401, detail="Invalid token format")

# # Initialize ABHA auth manager
# abha_auth = ABHAAuthManager()

# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     """Dependency to get current authenticated user"""
#     return await abha_auth.validate_user_token(credentials.credentials)

# # Dummy Health Passport Data Generator
# def generate_dummy_health_passport(abha_id: str, user_name: str = "Unknown User") -> Dict[str, Any]:
#     """Generate comprehensive dummy health passport data"""
    
#     # Sample conditions mapped to AYUSH and WHO codes
#     sample_conditions = [
#         {
#             "condition": "Hypertension",
#             "ayush_term": "Rakta Gata Vata",
#             "ayush_code": "AY-CVS-001",
#             "who_code": "I10",
#             "system": "Ayurveda",
#             "severity": "Mild",
#             "diagnosed_date": "2024-01-15"
#         },
#         {
#             "condition": "Type 2 Diabetes", 
#             "ayush_term": "Madhumeha",
#             "ayush_code": "AY-END-002",
#             "who_code": "E11.9",
#             "system": "Ayurveda",
#             "severity": "Moderate", 
#             "diagnosed_date": "2023-08-20"
#         },
#         {
#             "condition": "Arthritis",
#             "ayush_term": "Amavata",
#             "ayush_code": "AY-MSK-003", 
#             "who_code": "M79.3",
#             "system": "Ayurveda",
#             "severity": "Mild",
#             "diagnosed_date": "2024-03-10"
#         }
#     ]
    
#     sample_medications = [
#         {
#             "medicine": "Ashwagandha Churna",
#             "dosage": "5g twice daily",
#             "system": "Ayurveda",
#             "prescribed_date": "2024-01-15",
#             "prescribed_by": "Dr. Ayurvedic Practitioner"
#         },
#         {
#             "medicine": "Jamun Seed Powder",
#             "dosage": "2g daily with water",
#             "system": "Ayurveda",
#             "prescribed_date": "2023-08-20", 
#             "prescribed_by": "Dr. Ayurvedic Practitioner"
#         }
#     ]
    
#     return {
#         "abha_id": abha_id,
#         "generated_at": datetime.now().isoformat(),
#         "patient_demographics": {
#             "name": user_name,
#             "age": 45,
#             "gender": "Male",
#             "blood_group": "O+",
#             "phone": "+91-XXXX-XXXXX",
#             "address": {
#                 "city": "Pune",
#                 "state": "Maharashtra", 
#                 "country": "India",
#                 "pincode": "411001"
#             }
#         },
#         "medical_history": sample_conditions,
#         "current_medications": sample_medications,
#         "vital_signs": {
#             "last_recorded": "2024-09-15",
#             "blood_pressure": "130/85 mmHg",
#             "heart_rate": "72 bpm", 
#             "weight": "75 kg",
#             "height": "175 cm",
#             "bmi": 24.5,
#             "temperature": "98.6°F"
#         },
#         "allergies": ["Peanuts", "Shellfish"],
#         "emergency_contact": {
#             "name": "Emergency Contact",
#             "relationship": "Family",
#             "phone": "+91-YYYY-YYYYY"
#         },
#         "healthcare_providers": [
#             {
#                 "name": "Dr. Ayurvedic Practitioner",
#                 "system": "Ayurveda", 
#                 "contact": "+91-ZZZZ-ZZZZZ",
#                 "last_visit": "2024-09-10"
#             }
#         ]
#     }

# @app.get("/")
# def root():
#     return {
#         "message": "AYUSH ↔ WHO Semantic Search API with ABHA Integration",
#         "version": "2.0",
#         "features": ["semantic_search", "abha_integration", "health_passport"],
#         "status": "operational",
#         "endpoints": {
#             "search_mappings": "/search/{term}",
#             "health_passport": "/health-passport (requires auth)",
#             "demo_passport": "/demo/health-passport (no auth required)",
#             "test_tokens": "/test-auth",
#             "abha_status": "/abha/status",
#             "health_check": "/health"
#         }
#     }

# @app.get("/search/{term}")
# def search_mappings(term: str, threshold: int = Query(default=80, ge=50, le=100)):
#     """Search for AYUSH-WHO mappings using fuzzy matching"""
#     if df.empty:
#         raise HTTPException(status_code=503, detail="Mapping database not available")
    
#     term_words = term.lower().split()
#     mask = pd.Series(False, index=df.index)
    
#     # Check each word against AYUSH and WHO terms
#     for word in term_words:
#         mask |= fuzzy_match(word, df["AYUSH_Term_lower"], threshold)
#         mask |= fuzzy_match(word, df["WHO_Term_lower"], threshold)
    
#     # Include semantic matches (Similarity_Score >= 0.5)
#     semantic_mask = (df["Similarity_Score"] >= 0.5) & mask
#     results = df[mask | semantic_mask].copy()
    
#     if results.empty:
#         return {
#             "query": term,
#             "threshold": threshold,
#             "message": f"No matches found for '{term}' with threshold {threshold}%",
#             "suggestion": "Try lowering the threshold or using different search terms"
#         }
    
#     # Rank by similarity score
#     results["rank_score"] = results["Similarity_Score"].fillna(0)
#     results = results.sort_values(by="rank_score", ascending=False)
    
#     return {
#         "query": term,
#         "threshold": threshold,
#         "total_results": len(results),
#         "mappings": results[[
#             "AYUSH_Code", "AYUSH_Term", "Target_System",
#             "WHO_Code_Candidate", "WHO_Term_Candidate",
#             "Similarity_Score", "Suggested_Relationship"
#         ]].to_dict(orient="records")
#     }

# @app.get("/demo/health-passport")
# def get_demo_health_passport():
#     """Get demo health passport without authentication - for testing purposes"""
    
#     try:
#         # Generate dummy health passport data with demo user
#         demo_user = {
#             "abha_id": "12-3456-7890-1234", 
#             "name": "Demo Patient",
#             "mobile": "+91-98765-43210"
#         }
        
#         health_passport = generate_dummy_health_passport(
#             demo_user["abha_id"], 
#             demo_user["name"]
#         )
        
#         # Enhance conditions with semantic mappings from our database
#         enhanced_conditions = []
#         for condition in health_passport["medical_history"]:
#             # Search for related terms in mapping database
#             related_mappings = []
#             if not df.empty:
#                 term_words = condition["condition"].lower().split()
#                 mask = pd.Series(False, index=df.index)
                
#                 for word in term_words:
#                     mask |= fuzzy_match(word, df["AYUSH_Term_lower"], 70)
#                     mask |= fuzzy_match(word, df["WHO_Term_lower"], 70)
                
#                 results = df[mask].copy()
#                 if not results.empty:
#                     related_mappings = results[[
#                         "AYUSH_Code", "AYUSH_Term", "WHO_Code_Candidate",
#                         "WHO_Term_Candidate", "Similarity_Score"
#                     ]].head(3).to_dict(orient="records")
            
#             enhanced_conditions.append({
#                 **condition,
#                 "semantic_mappings": related_mappings
#             })
        
#         return {
#             "status": "success",
#             "message": "Demo health passport - no authentication required",
#             "user": demo_user,
#             "health_passport": {
#                 **health_passport,
#                 "medical_history": enhanced_conditions
#             },
#             "integration_info": {
#                 "mapping_database": "loaded" if not df.empty else "unavailable",
#                 "semantic_search": "enabled",
#                 "data_source": "dummy_generated",
#                 "last_updated": datetime.now().isoformat(),
#                 "note": "This is demo data for testing purposes"
#             }
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error generating demo health passport: {str(e)}")

# @app.get("/health-passport")
# async def get_health_passport(current_user: dict = Depends(get_current_user)):
#     """Get health passport for authenticated user (dummy data for now)"""
    
#     try:
#         # Generate dummy health passport data
#         health_passport = generate_dummy_health_passport(
#             current_user["abha_id"], 
#             current_user.get("name", "Unknown User")
#         )
        
#         # Enhance conditions with semantic mappings from our database
#         enhanced_conditions = []
#         for condition in health_passport["medical_history"]:
#             # Search for related terms in mapping database
#             related_mappings = []
#             if not df.empty:
#                 term_words = condition["condition"].lower().split()
#                 mask = pd.Series(False, index=df.index)
                
#                 for word in term_words:
#                     mask |= fuzzy_match(word, df["AYUSH_Term_lower"], 70)
#                     mask |= fuzzy_match(word, df["WHO_Term_lower"], 70)
                
#                 results = df[mask].copy()
#                 if not results.empty:
#                     related_mappings = results[[
#                         "AYUSH_Code", "AYUSH_Term", "WHO_Code_Candidate",
#                         "WHO_Term_Candidate", "Similarity_Score"
#                     ]].head(3).to_dict(orient="records")
            
#             enhanced_conditions.append({
#                 **condition,
#                 "semantic_mappings": related_mappings
#             })
        
#         return {
#             "status": "success",
#             "user": current_user,
#             "health_passport": {
#                 **health_passport,
#                 "medical_history": enhanced_conditions
#             },
#             "integration_info": {
#                 "mapping_database": "loaded" if not df.empty else "unavailable",
#                 "semantic_search": "enabled",
#                 "data_source": "dummy_generated",
#                 "last_updated": datetime.now().isoformat()
#             }
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error generating health passport: {str(e)}")

# @app.get("/abha/status")
# def get_abha_status():
#     """Get ABHA integration status and configuration"""
#     credentials_configured = bool(ABHA_CONFIG["client_id"] and ABHA_CONFIG["client_secret"])
    
#     return {
#         "abha_integration": {
#             "credentials_configured": credentials_configured,
#             "environment": "sandbox" if "sbx" in ABHA_CONFIG["base_url"] else "production", 
#             "base_url": ABHA_CONFIG["base_url"],
#             "auth_mode": "oauth2" if credentials_configured else "dummy_tokens",
#             "ready_for_production": credentials_configured
#         },
#         "mapping_database": {
#             "loaded": not df.empty,
#             "total_mappings": len(df) if not df.empty else 0,
#             "status": "operational" if not df.empty else "unavailable"
#         },
#         "api_endpoints": {
#             "semantic_search": "/search/{term}",
#             "health_passport": "/health-passport",
#             "demo_passport": "/demo/health-passport",
#             "abha_status": "/abha/status"
#         }
#     }

# @app.get("/test-auth")
# async def test_authentication():
#     """Test endpoint to get valid test tokens"""
#     return {
#         "message": "Use these test tokens in Authorization header as 'Bearer {token}'",
#         "test_tokens": {
#             "patient": "test_patient_001",
#             "doctor": "test_doctor_001", 
#             "demo": "demo_user",
#             "custom": "any_string_8chars_or_longer"
#         },
#         "example_usage": {
#             "curl": "curl -H 'Authorization: Bearer test_patient_001' http://localhost:8000/health-passport",
#             "demo_endpoint": "GET /demo/health-passport (no auth required)",
#             "note": "Replace 'test_patient_001' with any of the test tokens above"
#         }
#     }

# # Health check endpoint
# @app.get("/health")
# def health_check():
#     return {
#         "status": "healthy",
#         "timestamp": datetime.now().isoformat(),
#         "services": {
#             "api": "operational",
#             "semantic_search": "operational" if not df.empty else "degraded", 
#             "abha_integration": "demo_mode" if not (ABHA_CONFIG["client_id"] and ABHA_CONFIG["client_secret"]) else "configured",
#             "database": "loaded" if not df.empty else "error"
#         },
#         "environment": "sandbox" if "sbx" in ABHA_CONFIG["base_url"] else "production"
#     }


# sih/ayush/app.py  (full file)
import os, json, uuid, logging
from fastapi import FastAPI, Body, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import pandas as pd
from rapidfuzz import fuzz
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import jwt
import requests

# local imports from your project structure
# from app_.database import SessionLocal
# from app_ import models
# from app_.security import oauth2_scheme, validate_abha_token
# from app_.icd_sync import sync_terms_to_db
# from app_ import who_client
# from search_utils import fuzzy_search_with_explain
# from app_.translate_utils import translate_ayush_code

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ayush-api")

# The main FastAPI application
app = FastAPI(title="AYUSH ↔ WHO Semantic Search API with ABHA Integration")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8501", # Streamlit's default port
    "http://127.0.0.1:8000", # Uvicorn's default port
    "http://localhost:3001", # React dev server
]
# ADDED: CORS middleware to allow cross-origin requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allows all origins. Change in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# ABHA Configuration - Update these when you get real credentials
ABHA_CONFIG = {
    "client_id": os.getenv("ABHA_CLIENT_ID", ""),
    "client_secret": os.getenv("ABHA_CLIENT_SECRET", ""),
    "base_url": "https://abhasbx.abdm.gov.in/gateway",  # Sandbox URL
    "production_url": "https://abha.abdm.gov.in/gateway",  # Production URL
    "auth_url": "https://abhasbx.abdm.gov.in/gateway/v0.5/sessions",
    "token_url": "https://abhasbx.abdm.gov.in/gateway/v0.5/auth/authConfirm"
}

# Security scheme for ABHA token
security = HTTPBearer()

# Load CSV data for semantic search
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "candidate_mappings_semantic_v2.csv")

try:
    df = pd.read_csv(CSV_PATH)
    # Preprocess lowercase columns for fuzzy matching
    df["AYUSH_Term_lower"] = df["AYUSH_Term"].str.lower()
    df["WHO_Term_lower"] = df["WHO_Term_Candidate"].str.lower()
    print(f"✅ Loaded {len(df)} mappings from CSV")
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    df = pd.DataFrame()

def fuzzy_match(term: str, candidates: pd.Series, threshold: int = 80) -> pd.Series:
    """Return boolean mask where term matches candidate fuzzily above threshold."""
    return candidates.apply(lambda x: fuzz.partial_ratio(str(x).lower(), term.lower()) >= threshold)

class ABHAAuthManager:
    """Handles ABHA OAuth authentication and token management"""
    
    def __init__(self):
        self.access_token = None
        self.token_expires_at = None
        self.session_token = None
    
    async def get_session_token(self) -> str:
        """Get initial session token from ABHA gateway"""
        if not ABHA_CONFIG["client_id"] or not ABHA_CONFIG["client_secret"]:
            raise HTTPException(
                status_code=503, 
                detail="ABHA credentials not configured. Please set ABHA_CLIENT_ID and ABHA_CLIENT_SECRET environment variables."
            )
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            payload = {
                "clientId": ABHA_CONFIG["client_id"],
                "clientSecret": ABHA_CONFIG["client_secret"]
            }
            
            response = requests.post(
                ABHA_CONFIG["auth_url"],
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.session_token = data.get("accessToken")
                return self.session_token
            else:
                raise HTTPException(status_code=401, detail=f"ABHA session failed: {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=503, detail=f"ABHA service unavailable: {str(e)}")
    
    async def validate_user_token(self, token: str) -> Dict[str, Any]:
        """Validate user's ABHA token and extract user info"""
        if not token:
            raise HTTPException(status_code=401, detail="Missing ABHA token")
        
        # If no credentials configured, use dummy validation
        if not ABHA_CONFIG["client_id"] or not ABHA_CONFIG["client_secret"]:
            return self._dummy_token_validation(token)
        
        try:
            # Real ABHA token validation would go here
            # For now, using dummy validation until credentials are available
            return self._dummy_token_validation(token)
            
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")
    
    def _dummy_token_validation(self, token: str) -> Dict[str, Any]:
        """Dummy token validation for testing without real ABHA credentials"""
        # Accept specific test tokens for different user types
        test_tokens = {
            "test_patient_001": {
                "abha_id": "12-3456-7890-1234", 
                "name": "Test Patient",
                "mobile": "+91-98765-43210"
            },
            "test_doctor_001": {
                "abha_id": "98-7654-3210-9876", 
                "name": "Dr. Test Physician",
                "mobile": "+91-87654-32109",
                "role": "doctor"
            },
            "demo_user": {
                "abha_id": "11-1111-1111-1111", 
                "name": "Demo User",
                "mobile": "+91-99999-99999"
            }
        }
        
        if token in test_tokens:
            return test_tokens[token]
        elif len(token) >= 8:  # Accept any token with 8+ characters for demo
            return {
                "abha_id": f"00-0000-0000-{token[-4:].zfill(4)}", 
                "name": f"User {token[-4:]}",
                "mobile": "+91-XXXX-XXXXX"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid token format")

# Initialize ABHA auth manager
abha_auth = ABHAAuthManager()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current authenticated user"""
    return await abha_auth.validate_user_token(credentials.credentials)

# Dummy Health Passport Data Generator
def generate_dummy_health_passport(abha_id: str, user_name: str = "Unknown User") -> Dict[str, Any]:
    """Generate comprehensive dummy health passport data"""
    
    # Sample conditions mapped to AYUSH and WHO codes
    sample_conditions = [
        {
            "condition": "Hypertension",
            "ayush_term": "Rakta Gata Vata",
            "ayush_code": "AY-CVS-001",
            "who_code": "I10",
            "system": "Ayurveda",
            "severity": "Mild",
            "diagnosed_date": "2024-01-15"
        },
        {
            "condition": "Type 2 Diabetes", 
            "ayush_term": "Madhumeha",
            "ayush_code": "AY-END-002",
            "who_code": "E11.9",
            "system": "Ayurveda",
            "severity": "Moderate", 
            "diagnosed_date": "2023-08-20"
        },
        {
            "condition": "Arthritis",
            "ayush_term": "Amavata",
            "ayush_code": "AY-MSK-003", 
            "who_code": "M79.3",
            "system": "Ayurveda",
            "severity": "Mild",
            "diagnosed_date": "2024-03-10"
        }
    ]
    
    sample_medications = [
        {
            "medicine": "Ashwagandha Churna",
            "dosage": "5g twice daily",
            "system": "Ayurveda",
            "prescribed_date": "2024-01-15",
            "prescribed_by": "Dr. Ayurvedic Practitioner"
        },
        {
            "medicine": "Jamun Seed Powder",
            "dosage": "2g daily with water",
            "system": "Ayurveda",
            "prescribed_date": "2023-08-20", 
            "prescribed_by": "Dr. Ayurvedic Practitioner"
        }
    ]
    
    return {
        "abha_id": abha_id,
        "generated_at": datetime.now().isoformat(),
        "patient_demographics": {
            "name": user_name,
            "age": 45,
            "gender": "Male",
            "blood_group": "O+",
            "phone": "+91-XXXX-XXXXX",
            "address": {
                "city": "Pune",
                "state": "Maharashtra", 
                "country": "India",
                "pincode": "411001"
            }
        },
        "medical_history": sample_conditions,
        "current_medications": sample_medications,
        "vital_signs": {
            "last_recorded": "2024-09-15",
            "blood_pressure": "130/85 mmHg",
            "heart_rate": "72 bpm", 
            "weight": "75 kg",
            "height": "175 cm",
            "bmi": 24.5,
            "temperature": "98.6°F"
        },
        "allergies": ["Peanuts", "Shellfish"],
        "emergency_contact": {
            "name": "Emergency Contact",
            "relationship": "Family",
            "phone": "+91-YYYY-YYYYY"
        },
        "healthcare_providers": [
            {
                "name": "Dr. Ayurvedic Practitioner",
                "system": "Ayurveda", 
                "contact": "+91-ZZZZ-ZZZZZ",
                "last_visit": "2024-09-10"
            }
        ]
    }

# Main root endpoint, provides API info
@app.get("/")
def root():
    return {
        "message": "AYUSH ↔ WHO Semantic Search API with ABHA Integration",
        "version": "2.0",
        "features": ["semantic_search", "abha_integration", "health_passport"],
        "status": "operational",
        "endpoints": {
            "search_mappings": "/search/{term}",
            "health_passport": "/health-passport (requires auth)",
            "demo_passport": "/demo/health-passport (no auth required)",
            "test_tokens": "/test-auth",
            "abha_status": "/abha/status",
            "health_check": "/health"
        }
    }

# Search endpoint, finds mappings using fuzzy matching
@app.get("/search/{term}")
def search_mappings(term: str, threshold: int = Query(default=80, ge=50, le=100)):
    """Search for AYUSH-WHO mappings using fuzzy matching"""
    if df.empty:
        raise HTTPException(status_code=503, detail="Mapping database not available")
    
    term_words = term.lower().split()
    mask = pd.Series(False, index=df.index)
    
    # Check each word against AYUSH and WHO terms
    for word in term_words:
        mask |= fuzzy_match(word, df["AYUSH_Term_lower"], threshold)
        mask |= fuzzy_match(word, df["WHO_Term_lower"], threshold)
    
    # Include semantic matches (Similarity_Score >= 0.5)
    semantic_mask = (df["Similarity_Score"] >= 0.5) & mask
    results = df[mask | semantic_mask].copy()
    
    if results.empty:
        return {
            "query": term,
            "threshold": threshold,
            "message": f"No matches found for '{term}' with threshold {threshold}%",
            "suggestion": "Try lowering the threshold or using different search terms"
        }
    
    # Rank by similarity score
    results["rank_score"] = results["Similarity_Score"].fillna(0)
    results = results.sort_values(by="rank_score", ascending=False)
    
    return {
        "query": term,
        "threshold": threshold,
        "total_results": len(results),
        "mappings": results[[
            "AYUSH_Code", "AYUSH_Term", "Target_System",
            "WHO_Code_Candidate", "WHO_Term_Candidate",
            "Similarity_Score", "Suggested_Relationship"
        ]].to_dict(orient="records")
    }

# Endpoint to get a demo health passport (no authentication)
@app.get("/demo/health-passport")
def get_demo_health_passport():
    """Get demo health passport without authentication - for testing purposes"""
    
    try:
        # Generate dummy health passport data with demo user
        demo_user = {
            "abha_id": "12-3456-7890-1234", 
            "name": "Demo Patient",
            "mobile": "+91-98765-43210"
        }
        
        health_passport = generate_dummy_health_passport(
            demo_user["abha_id"], 
            demo_user["name"]
        )
        
        # Enhance conditions with semantic mappings from our database
        enhanced_conditions = []
        for condition in health_passport["medical_history"]:
            # Search for related terms in mapping database
            related_mappings = []
            if not df.empty:
                term_words = condition["condition"].lower().split()
                mask = pd.Series(False, index=df.index)
                
                for word in term_words:
                    mask |= fuzzy_match(word, df["AYUSH_Term_lower"], 70)
                    mask |= fuzzy_match(word, df["WHO_Term_lower"], 70)
                
                results = df[mask].copy()
                if not results.empty:
                    related_mappings = results[[
                        "AYUSH_Code", "AYUSH_Term", "WHO_Code_Candidate",
                        "WHO_Term_Candidate", "Similarity_Score"
                    ]].head(3).to_dict(orient="records")
            
            enhanced_conditions.append({
                **condition,
                "semantic_mappings": related_mappings
            })
        
        return {
            "status": "success",
            "message": "Demo health passport - no authentication required",
            "user": demo_user,
            "health_passport": {
                **health_passport,
                "medical_history": enhanced_conditions
            },
            "integration_info": {
                "mapping_database": "loaded" if not df.empty else "unavailable",
                "semantic_search": "enabled",
                "data_source": "dummy_generated",
                "last_updated": datetime.now().isoformat(),
                "note": "This is demo data for testing purposes"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating demo health passport: {str(e)}")

# Endpoint to get an authenticated user's health passport
@app.get("/health-passport")
async def get_health_passport(current_user: dict = Depends(get_current_user)):
    """Get health passport for authenticated user (dummy data for now)"""
    
    try:
        # Generate dummy health passport data
        health_passport = generate_dummy_health_passport(
            current_user["abha_id"], 
            current_user.get("name", "Unknown User")
        )
        
        # Enhance conditions with semantic mappings from our database
        enhanced_conditions = []
        for condition in health_passport["medical_history"]:
            # Search for related terms in mapping database
            related_mappings = []
            if not df.empty:
                term_words = condition["condition"].lower().split()
                mask = pd.Series(False, index=df.index)
                
                for word in term_words:
                    mask |= fuzzy_match(word, df["AYUSH_Term_lower"], 70)
                    mask |= fuzzy_match(word, df["WHO_Term_lower"], 70)
                
                results = df[mask].copy()
                if not results.empty:
                    related_mappings = results[[
                        "AYUSH_Code", "AYUSH_Term", "WHO_Code_Candidate",
                        "WHO_Term_Candidate", "Similarity_Score"
                    ]].head(3).to_dict(orient="records")
            
            enhanced_conditions.append({
                **condition,
                "semantic_mappings": related_mappings
            })
        
        return {
            "status": "success",
            "user": current_user,
            "health_passport": {
                **health_passport,
                "medical_history": enhanced_conditions
            },
            "integration_info": {
                "mapping_database": "loaded" if not df.empty else "unavailable",
                "semantic_search": "enabled",
                "data_source": "dummy_generated",
                "last_updated": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating health passport: {str(e)}")

# Endpoint to check ABHA integration status
@app.get("/abha/status")
def get_abha_status():
    """Get ABHA integration status and configuration"""
    credentials_configured = bool(ABHA_CONFIG["client_id"] and ABHA_CONFIG["client_secret"])
    
    return {
        "abha_integration": {
            "credentials_configured": credentials_configured,
            "environment": "sandbox" if "sbx" in ABHA_CONFIG["base_url"] else "production", 
            "base_url": ABHA_CONFIG["base_url"],
            "auth_mode": "oauth2" if credentials_configured else "dummy_tokens",
            "ready_for_production": credentials_configured
        },
        "mapping_database": {
            "loaded": not df.empty,
            "total_mappings": len(df) if not df.empty else 0,
            "status": "operational" if not df.empty else "unavailable"
        },
        "api_endpoints": {
            "semantic_search": "/search/{term}",
            "health_passport": "/health-passport",
            "demo_passport": "/demo/health-passport",
            "abha_status": "/abha/status"
        }
    }

# Endpoint to get valid test tokens for authentication
@app.get("/test-auth")
async def test_authentication():
    """Test endpoint to get valid test tokens"""
    return {
        "message": "Use these test tokens in Authorization header as 'Bearer {token}'",
        "test_tokens": {
            "patient": "test_patient_001",
            "doctor": "test_doctor_001", 
            "demo": "demo_user",
            "custom": "any_string_8chars_or_longer"
        },
        "example_usage": {
            "curl": "curl -H 'Authorization: Bearer test_patient_001' http://localhost:8000/health-passport",
            "demo_endpoint": "GET /demo/health-passport (no auth required)",
            "note": "Replace 'test_patient_001' with any of the test tokens above"
        }
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "operational",
            "semantic_search": "operational" if not df.empty else "degraded", 
            "abha_integration": "demo_mode" if not (ABHA_CONFIG["client_id"] and ABHA_CONFIG["client_secret"]) else "configured",
            "database": "loaded" if not df.empty else "error"
        },
        "environment": "sandbox" if "sbx" in ABHA_CONFIG["base_url"] else "production"
    }