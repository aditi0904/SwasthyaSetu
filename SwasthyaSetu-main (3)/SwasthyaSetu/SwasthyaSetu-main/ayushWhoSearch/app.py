# sih/ayush/app.py  (full file)
import os, json, uuid, logging
from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
# local imports
from app_.database import SessionLocal
from app_ import models
from app_.security import oauth2_scheme, validate_abha_token
from app_.icd_sync import sync_terms_to_db
from app_ import who_client
from search_utils import fuzzy_search_with_explain
from app_.translate_utils import translate_ayush_code

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ayush-api")

app = FastAPI(title="AYUSH <-> WHO Terminology API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SearchRequest(BaseModel):
    query: str
    top_k: int = 20
    min_similarity: float = 0.5

class TranslateRequest(BaseModel):
    system: str
    code: str

# health & version
@app.get("/health")
def health():
    return {"status":"ok", "time": datetime.utcnow().isoformat()}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse({"error":"validation_error","detail": exc.errors()}, status_code=422)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception("Unhandled exception")
    return JSONResponse({"error":"server_error","detail": str(exc)}, status_code=500)
    
@app.get("/version")
def version():
    return {"who_release": os.getenv("WHO_ICD_RELEASE","11"), "app_version": "0.2.0"}

# semantic search: uses CSV (rapidfuzz route - you already have main.py code)
@app.post("/search", tags=["Search"])
def search(req: SearchRequest):
    # reuse your Pandas rapidfuzz logic (imported or embedded)
   
    results = fuzzy_search_with_explain(req.query, top_k=req.top_k, min_similarity=req.min_similarity)
    return {"query": req.query, "results": results}

# ICD sync trigger
@app.post("/sync/icd", tags=["Sync"])
def sync_icd(token: str = Depends(oauth2_scheme)):
    user = validate_abha_token(token)
    # load NAMASTE terms to query
    codes = None
    cs_path = "./data/namaste-combined-codesystem.json"
    if os.path.exists(cs_path):
        codes = json.load(open(cs_path)).get("concept",[])
    term_list = [c.get("display") for c in codes if c.get("display")] if codes else ["fever","cough"]
    added = sync_terms_to_db(term_list[:50], limit_per_term=2)
    # audit log
    db = SessionLocal(); 
    db.add(models.AuditLog(action="sync_icd", by_user=user.get("sub","system"), details={"added": added}))
    db.commit(); db.close()
    return {"status":"ok", "added": added}

# FHIR CodeSystem & ConceptMap endpoints (serve generated files)
@app.get("/fhir/CodeSystem/namaste")
def get_codesystem():
    path = "./data/namaste-combined-codesystem.json"
    if not os.path.exists(path):
        raise HTTPException(404, "CodeSystem not found; run generator")
    cs = json.load(open(path, encoding="utf-8"))
    return cs

@app.get("/fhir/ConceptMap/namaste-to-icd11")
def get_conceptmap():
    path = "./data/namaste-combined-conceptmap.json"
    if not os.path.exists(path):
        raise HTTPException(404, "ConceptMap not found; run generator")
    cm = json.load(open(path, encoding="utf-8"))
    return cm

# Translate operation (NAMASTE -> ICD)
class TranslateRequest(BaseModel):
    system: str
    code: str
    target_lang: str = "hi"

@app.post("/translate")
def translate(req: TranslateRequest):
    if req.system.upper() != "NAMASTE":
        return {"error": "unsupported_system"}
    
    result = translate_ayush_code(req.code, req.target_lang)
    
    return {
        "source": {"system": req.system, "code": req.code},
        "AYUSH_Term": result["AYUSH_Term"],
        "AYUSH_Term_Translated": result["AYUSH_Term_Translated"],
        "targets": result["targets"]
    }



# Bundle ingestion (FHIR Bundle)
@app.post("/fhir/Bundle", tags=["FHIR"])
def ingest_bundle(bundle: Dict = Body(...), token: str = Depends(oauth2_scheme)):
    user = validate_abha_token(token)
    if bundle.get("resourceType")!="Bundle":
        raise HTTPException(400, "Not a FHIR Bundle")
    # validate dual codes in Conditions
    has_dual=False
    for e in bundle.get("entry", []):
        r = e.get("resource",{})
        if r.get("resourceType")=="Condition":
            codings = r.get("code",{}).get("coding",[])
            systems = [c.get("system","") for c in codings]
            if any("namaste" in s.lower() for s in systems) and any("icd" in s.lower() or "who.int" in s.lower() for s in systems):
                has_dual=True
    # save with provenance
    bid = bundle.get("id") or str(uuid.uuid4())
    out = {"bundle": bundle, "provenance":{"who": user.get("sub"), "when": datetime.utcnow().isoformat()}}
    os.makedirs("./data/bundles", exist_ok=True)
    json.dump(out, open(f"./data/bundles/{bid}.json","w", encoding="utf-8"), indent=2, ensure_ascii=False)
    # audit
    db = SessionLocal(); db.add(models.AuditLog(action="bundle_upload", by_user=user.get("sub"), details={"bundle_id": bid, "has_dual": has_dual})); db.commit(); db.close()
    return {"status": "stored", "bundle_id": bid, "has_dual": has_dual}
