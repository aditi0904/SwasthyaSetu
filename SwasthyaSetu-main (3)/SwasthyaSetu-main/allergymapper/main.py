# # app/main.py
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Optional, List, Dict, Any, Tuple
# import asyncio
# import httpx
# import asyncpg  # NEW


# app = FastAPI(title="Ayur Allergy Mapper API", version="0.5.0")

# # ---------- System check ----------
# @app.get("/health")
# def health_check():
#     return {"status": "ok"}

# # ---------- Request model ----------
# class MapRequest(BaseModel):
#     drug: str

# # ---------- Endpoints & settings ----------
# RXNAV_BASE   = "https://rxnav.nlm.nih.gov/REST"
# RXCLASS_BASE = "https://rxnav.nlm.nih.gov/REST"
# PUBMED_EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
# HTTP_TIMEOUT = 30.0
# RETRIES = 3
# RETRY_BACKOFF = 1.5  # seconds

# # ---------- Neon Postgres (Option B: hardcoded DSN) ----------
# DATABASE_URL = (
#     "postgresql://neondb_owner:npg_kKMf0RBTxs4Q@ep-hidden-cake-a1rylakb-pooler.ap-southeast-1.aws.neon.tech/"
#     "neondb?sslmode=require&channel_binding=require"
# )

# # ---------- HTTP helper with retries ----------
# async def _fetch_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
#     last_err: Optional[Exception] = None
#     for attempt in range(1, RETRIES + 1):
#         try:
#             async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
#                 resp = await client.get(url, params=params)
#                 resp.raise_for_status()
#                 return resp.json()
#         except (httpx.TimeoutException, httpx.ConnectTimeout) as e:
#             last_err = e
#             if attempt < RETRIES:
#                 await asyncio.sleep(RETRY_BACKOFF * attempt)
#                 continue
#             raise HTTPException(status_code=504, detail=f"Upstream timeout calling {url}")
#         except httpx.HTTPError as e:
#             raise HTTPException(status_code=502, detail=f"Upstream HTTP error: {e}")
#     raise HTTPException(status_code=502, detail=str(last_err) if last_err else "Unknown upstream error")

# # ---------- RxNav: name -> RxCUI ----------
# async def get_rxcui(drug_name: str) -> Optional[str]:
#     data = await _fetch_json(f"{RXNAV_BASE}/rxcui.json", params={"name": drug_name})
#     rxids = (data.get("idGroup") or {}).get("rxnormId")
#     return rxids[0] if rxids else None

# # ---------- RxNav: properties ----------
# async def get_properties(rxcui: str) -> Dict[str, Any]:
#     data = await _fetch_json(f"{RXNAV_BASE}/rxcui/{rxcui}/properties.json")
#     props = data.get("properties") or {}
#     return {
#         "rxcui": props.get("rxcui"),
#         "name": props.get("name"),
#         "synonym": props.get("synonym"),
#         "tty": props.get("tty"),
#         "language": props.get("language"),
#     }

# # ---------- RxClass: therapeutic classes ----------
# async def get_therapeutic_classes(rxcui: str) -> List[Dict[str, Any]]:
#     data = await _fetch_json(f"{RXCLASS_BASE}/rxclass/class/byRxcui.json", params={"rxcui": rxcui})
#     rels = (data.get("rxclassDrugInfoList") or {}).get("rxclassDrugInfo") or []
#     out: List[Dict[str, Any]] = []
#     for item in rels:
#         cls = (item.get("rxclassMinConceptItem") or {})
#         out.append({
#             "className": cls.get("className"),
#             "classType": cls.get("classType"),
#             "classId":   cls.get("classId"),
#             "source":    cls.get("classType")
#         })
#     return out

# # ---------- Deduplicate classes ----------
# def dedupe_classes(classes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#     seen = set()
#     out: List[Dict[str, Any]] = []
#     for c in classes:
#         key = (c.get("classType"), c.get("classId"))
#         if key in seen:
#             continue
#         seen.add(key)
#         out.append(c)
#     return out

# # ---------- Map class names -> indication keywords ----------
# def derive_indication_keywords(classes: List[Dict[str, Any]]) -> List[str]:
#     keywords: set = set()
#     for c in classes:
#         name = (c.get("className") or "").lower()
#         if any(tok in name for tok in ["antibiotic", "antibacterial", "penicillin", "beta-lactam", "cephalosporin"]):
#             keywords.update(["antibacterial", "antimicrobial", "infection"])
#         if any(tok in name for tok in ["nsaid", "anti-inflammatory", "cox"]):
#             keywords.update(["anti-inflammatory", "analgesic", "pain"])
#         if "antihistamine" in name:
#             keywords.update(["allergy", "h1 antihistamine"])
#         if any(tok in name for tok in ["proton pump", "ppi", "prazole"]):
#             keywords.update(["acid reflux", "gastroprotective", "ulcer"])
#         if any(tok in name for tok in ["corticosteroid", "glucocorticoid"]):
#             keywords.update(["anti-inflammatory", "immunomodulatory"])
#         if "anti-infective" in name:
#             keywords.update(["antimicrobial", "infection"])
#     return sorted(list(keywords))

# # ---------- PubMed evidence ----------
# async def pubmed_search_links(query: str, max_links: int = 2) -> List[str]:
#     term = f'{query} AND (allergy OR hypersensitivity OR dermatitis OR safety OR adverse)'
#     params = {"db": "pubmed", "retmode": "json", "retmax": str(max_links), "term": term, "sort": "relevance"}
#     data = await _fetch_json(f"{PUBMED_EUTILS}/esearch.fcgi", params=params)
#     idlist = ((data.get("esearchresult") or {}).get("idlist")) or []
#     return [f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" for pmid in idlist[:max_links]]

# # ---------- Scoring ----------
# def score_candidate(herb: Dict[str, Any], keyword: str) -> Tuple[int, str]:
#     score = 0
#     strong = {"antibacterial", "anti-inflammatory"}
#     if keyword in strong:
#         score += 2
#     links = herb.get("evidence_links", []) or []
#     if len(links) >= 1:
#         score += 1
#     if len(links) >= 2:
#         score += 1
#     if herb.get("botanical"):
#         score += 1
#     if score >= 5:
#         conf = "High"
#     elif score >= 3:
#         conf = "Medium"
#     else:
#         conf = "Low"
#     return score, conf

# # ---------- DB: fetch herbs for keywords (replaces AYURVEDA_SEED) ----------
# async def fetch_herbs_for_keywords(keywords: List[str]) -> List[Dict[str, Any]]:
#     """
#     Reads from Neon tables we created earlier:
#       herbs, functions, herb_functions, risks, refs
#     Returns a list of herb dicts shaped like your old seed items:
#       {herb_id, common, sanskrit, botanical, risk, refs}
#     """
#     if not keywords:
#         return []

#     conn = await asyncpg.connect(DATABASE_URL)
#     try:
#         rows = await conn.fetch(
#             """
#             SELECT
#                 h.herb_id,
#                 h.common_name       AS common,
#                 h.sanskrit          AS sanskrit,
#                 h.botanical_name    AS botanical,
#                 r.risk_level        AS risk_label,
#                 r.notes             AS risk_notes,
#                 COALESCE(array_agg(DISTINCT ref.reference)
#                          FILTER (WHERE ref.reference IS NOT NULL), '{}') AS refs
#             FROM herbs h
#             JOIN herb_functions hf ON hf.herb_id = h.herb_id
#             JOIN functions f       ON f.function_id = hf.function_id
#             LEFT JOIN risks r      ON r.herb_id = h.herb_id
#             LEFT JOIN refs  ref    ON ref.herb_id = h.herb_id
#             WHERE f.function_name = ANY($1::text[])
#             GROUP BY h.herb_id, h.common_name, h.sanskrit, h.botanical_name, r.risk_level, r.notes
#             ORDER BY h.common_name;
#             """,
#             keywords
#         )
#         herbs = []
#         for r in rows:
#             herbs.append({
#                 "herb_id": r["herb_id"],
#                 "common": r["common"],
#                 "sanskrit": r["sanskrit"],
#                 "botanical": r["botanical"],
#                 "risk": {
#                     "label": r["risk_label"] or "Unknown",
#                     "notes": [r["risk_notes"]] if r["risk_notes"] else []
#                 },
#                 "refs": list(r["refs"] or []),
#             })
#         return herbs
#     finally:
#         await conn.close()

# # ---------- Enrich herb ----------
# async def enrich_with_pubmed(herb: Dict[str, Any], keyword: str) -> Dict[str, Any]:
#     q = f'{herb["botanical"]} {keyword}'
#     links = await pubmed_search_links(q, max_links=2)
#     enriched = dict(herb)
#     enriched["evidence_links"] = links
#     enriched["why"] = [
#         f"Candidate for '{keyword}' based on traditional/known use; evidence links are PubMed search results for '{herb['botanical']} {keyword}'."
#     ]
#     # keep DB risk if present; otherwise minimal default
#     if "risk" not in enriched:
#         enriched["risk"] = {"label": "Unknown–Low", "notes": ["Always check patient-specific allergies."]}
#     s, conf = score_candidate(enriched, keyword)
#     enriched["score"] = s
#     enriched["confidence"] = conf
#     return enriched

# # ---------- Build candidates (now uses DB) ----------
# def _expand_keywords(indications: List[str]) -> List[str]:
#     expanded = []
#     for kw in indications:
#         if kw in ("antimicrobial", "infection"):
#             expanded.append("antibacterial")
#         expanded.append(kw)
#     seen = set()
#     out = []
#     for k in expanded:
#         if k not in seen:
#             seen.add(k)
#             out.append(k)
#     return out

# async def build_candidates_from_indications(indications: List[str]) -> List[Dict[str, Any]]:
#     keywords = _expand_keywords(indications)

#     # NEW: fetch possible herbs from Neon
#     base_herbs = await fetch_herbs_for_keywords(keywords)

#     # same enrichment + scoring as before
#     merged: Dict[str, Dict[str, Any]] = {}
#     for kw in keywords:
#         tasks = [enrich_with_pubmed(h, kw) for h in base_herbs]
#         results = await asyncio.gather(*tasks, return_exceptions=True)
#         for res in results:
#             if isinstance(res, Exception):
#                 continue
#             hid = res.get("herb_id")
#             if hid and hid not in merged:
#                 merged[hid] = res

#     out = list(merged.values())
#     out.sort(key=lambda h: (-h.get("score", 0), (h.get("common") or "")))
#     return out[:3]

# # ---------- /map ----------
# @app.post("/map")
# async def map_drug(req: MapRequest):
#     rxcui = await get_rxcui(req.drug)
#     if not rxcui:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Could not normalize '{req.drug}'. Try specific names (e.g., 'Penicillin G', 'Penicillin VK', 'Ibuprofen')."
#         )

#     props = await get_properties(rxcui)
#     classes = dedupe_classes(await get_therapeutic_classes(rxcui))
#     indications = derive_indication_keywords(classes)
#     candidates = await build_candidates_from_indications(indications)

#     return {
#         "input_drug": req.drug,
#         "normalized": props,
#         "therapeutic_classes": classes,
#         "indication_keywords": indications,
#         "candidates": candidates,
#         "disclaimer": "This is a research aid, not medical advice. Always consult a clinician."
#     }


# app/main.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Tuple
import asyncio
import httpx
import asyncpg
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# App initialization
app = FastAPI(title="Ayur Allergy Mapper API", version="0.5.0")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8501", # Streamlit's default port
    "http://127.0.0.1:8001", # Uvicorn's default port
    "http://localhost:3001", # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods, including POST, PUT, and OPTIONS
    allow_headers=["*"],  # Allows all headers
)

# ---------- System check ----------
@app.get("/health")
def health_check():
    """Returns the API status."""
    return {"status": "ok"}

# ---------- Request model ----------
class MapRequest(BaseModel):
    drug: str

# ---------- Endpoints & settings ----------
RXNAV_BASE = "https://rxnav.nlm.nih.gov/REST"
PUBMED_EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
HTTP_TIMEOUT = 30.0
RETRIES = 3
RETRY_BACKOFF = 1.5  # seconds

# ---------- Neon Postgres (Option B: hardcoded DSN) ----------
# WARNING: Storing credentials in code is a security risk. Use environment variables in production.
DATABASE_URL = (
    "postgresql://neondb_owner:npg_kKMf0RBTxs4Q@ep-hidden-cake-a1rylakb-pooler.ap-southeast-1.aws.neon.tech/"
    "neondb?sslmode=require&channel_binding=require"
)

# ---------- HTTP helper with retries ----------
async def _fetch_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    last_err: Optional[Exception] = None
    for attempt in range(1, RETRIES + 1):
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                return resp.json()
        except (httpx.TimeoutException, httpx.ConnectTimeout) as e:
            last_err = e
            if attempt < RETRIES:
                await asyncio.sleep(RETRY_BACKOFF * attempt)
                continue
            raise HTTPException(status_code=504, detail=f"Upstream timeout calling {url}")
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Upstream HTTP error: {e}")
    raise HTTPException(status_code=502, detail=str(last_err) if last_err else "Unknown upstream error")

# ---------- RxNav: name -> RxCUI ----------
async def get_rxcui(drug_name: str) -> Optional[str]:
    data = await _fetch_json(f"{RXNAV_BASE}/rxcui.json", params={"name": drug_name})
    rxids = (data.get("idGroup") or {}).get("rxnormId")
    return rxids[0] if rxids else None

# ---------- RxNav: properties ----------
async def get_properties(rxcui: str) -> Dict[str, Any]:
    data = await _fetch_json(f"{RXNAV_BASE}/rxcui/{rxcui}/properties.json")
    props = data.get("properties") or {}
    return {
        "rxcui": props.get("rxcui"),
        "name": props.get("name"),
        "synonym": props.get("synonym"),
        "tty": props.get("tty"),
        "language": props.get("language"),
    }

# ---------- RxClass: therapeutic classes ----------
async def get_therapeutic_classes(rxcui: str) -> List[Dict[str, Any]]:
    data = await _fetch_json(f"{RXNAV_BASE}/rxclass/class/byRxcui.json", params={"rxcui": rxcui})
    rels = (data.get("rxclassDrugInfoList") or {}).get("rxclassDrugInfo") or []
    out: List[Dict[str, Any]] = []
    for item in rels:
        cls = (item.get("rxclassMinConceptItem") or {})
        out.append({
            "className": cls.get("className"),
            "classType": cls.get("classType"),
            "classId":   cls.get("classId"),
            "source":    cls.get("classType")
        })
    return out

# ---------- Deduplicate classes ----------
def dedupe_classes(classes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out: List[Dict[str, Any]] = []
    for c in classes:
        key = (c.get("classType"), c.get("classId"))
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out

# ---------- Map class names -> indication keywords ----------
def derive_indication_keywords(classes: List[Dict[str, Any]]) -> List[str]:
    keywords: set = set()
    for c in classes:
        name = (c.get("className") or "").lower()
        if any(tok in name for tok in ["antibiotic", "antibacterial", "penicillin", "beta-lactam", "cephalosporin"]):
            keywords.update(["antibacterial", "antimicrobial", "infection"])
        if any(tok in name for tok in ["nsaid", "anti-inflammatory", "cox"]):
            keywords.update(["anti-inflammatory", "analgesic", "pain"])
        if "antihistamine" in name:
            keywords.update(["allergy", "h1 antihistamine"])
        if any(tok in name for tok in ["proton pump", "ppi", "prazole"]):
            keywords.update(["acid reflux", "gastroprotective", "ulcer"])
        if any(tok in name for tok in ["corticosteroid", "glucocorticoid"]):
            keywords.update(["anti-inflammatory", "immunomodulatory"])
        if "anti-infective" in name:
            keywords.update(["antimicrobial", "infection"])
    return sorted(list(keywords))

# ---------- PubMed evidence ----------
async def pubmed_search_links(query: str, max_links: int = 2) -> List[str]:
    term = f'{query} AND (allergy OR hypersensitivity OR dermatitis OR safety OR adverse)'
    params = {"db": "pubmed", "retmode": "json", "retmax": str(max_links), "term": term, "sort": "relevance"}
    data = await _fetch_json(f"{PUBMED_EUTILS}/esearch.fcgi", params=params)
    idlist = ((data.get("esearchresult") or {}).get("idlist")) or []
    return [f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" for pmid in idlist[:max_links]]

# ---------- Scoring ----------
def score_candidate(herb: Dict[str, Any], keyword: str) -> Tuple[int, str]:
    score = 0
    strong = {"antibacterial", "anti-inflammatory"}
    if keyword in strong:
        score += 2
    links = herb.get("evidence_links", []) or []
    if len(links) >= 1:
        score += 1
    if len(links) >= 2:
        score += 1
    if herb.get("botanical"):
        score += 1
    if score >= 5:
        conf = "High"
    elif score >= 3:
        conf = "Medium"
    else:
        conf = "Low"
    return score, conf

# ---------- DB: fetch herbs for keywords ----------
async def fetch_herbs_for_keywords(keywords: List[str]) -> List[Dict[str, Any]]:
    if not keywords:
        return []

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch(
            """
            SELECT
                h.herb_id,
                h.common_name AS common,
                h.sanskrit AS sanskrit,
                h.botanical_name AS botanical,
                r.risk_level AS risk_label,
                r.notes AS risk_notes,
                COALESCE(array_agg(DISTINCT ref.reference)
                         FILTER (WHERE ref.reference IS NOT NULL), '{}') AS refs
            FROM herbs h
            JOIN herb_functions hf ON hf.herb_id = h.herb_id
            JOIN functions f ON f.function_id = hf.function_id
            LEFT JOIN risks r ON r.herb_id = h.herb_id
            LEFT JOIN refs ref ON ref.herb_id = h.herb_id
            WHERE f.function_name = ANY($1::text[])
            GROUP BY h.herb_id, h.common_name, h.sanskrit, h.botanical_name, r.risk_level, r.notes
            ORDER BY h.common_name;
            """,
            keywords
        )
        herbs = []
        for r in rows:
            herbs.append({
                "herb_id": r["herb_id"],
                "common": r["common"],
                "sanskrit": r["sanskrit"],
                "botanical": r["botanical"],
                "risk": {
                    "label": r["risk_label"] or "Unknown",
                    "notes": [r["risk_notes"]] if r["risk_notes"] else []
                },
                "refs": list(r["refs"] or []),
            })
        return herbs
    finally:
        await conn.close()

# ---------- Enrich herb ----------
async def enrich_with_pubmed(herb: Dict[str, Any], keyword: str) -> Dict[str, Any]:
    q = f'{herb["botanical"]} {keyword}'
    links = await pubmed_search_links(q, max_links=2)
    enriched = dict(herb)
    enriched["evidence_links"] = links
    enriched["why"] = [
        f"Candidate for '{keyword}' based on traditional/known use; evidence links are PubMed search results for '{herb['botanical']} {keyword}'."
    ]
    if "risk" not in enriched:
        enriched["risk"] = {"label": "Unknown–Low", "notes": ["Always check patient-specific allergies."]}
    s, conf = score_candidate(enriched, keyword)
    enriched["score"] = s
    enriched["confidence"] = conf
    return enriched

# ---------- Build candidates (now uses DB) ----------
def _expand_keywords(indications: List[str]) -> List[str]:
    expanded = []
    for kw in indications:
        if kw in ("antimicrobial", "infection"):
            expanded.append("antibacterial")
        expanded.append(kw)
    seen = set()
    out = []
    for k in expanded:
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out

async def build_candidates_from_indications(indications: List[str]) -> List[Dict[str, Any]]:
    keywords = _expand_keywords(indications)
    base_herbs = await fetch_herbs_for_keywords(keywords)
    merged: Dict[str, Dict[str, Any]] = {}
    for kw in keywords:
        tasks = [enrich_with_pubmed(h, kw) for h in base_herbs]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, Exception):
                continue
            hid = res.get("herb_id")
            if hid and hid not in merged:
                merged[hid] = res
    out = list(merged.values())
    out.sort(key=lambda h: (-h.get("score", 0), (h.get("common") or "")))
    return out[:3]

# ---------- /map endpoints (POST and PUT) ----------
@app.post("/map")
@app.put("/map")
async def map_drug(req: MapRequest):
    rxcui = await get_rxcui(req.drug)
    if not rxcui:
        raise HTTPException(
            status_code=404,
            detail=f"Could not normalize '{req.drug}'. Try specific names (e.g., 'Penicillin G', 'Penicillin VK', 'Ibuprofen')."
        )

    props = await get_properties(rxcui)
    classes = dedupe_classes(await get_therapeutic_classes(rxcui))
    indications = derive_indication_keywords(classes)
    candidates = await build_candidates_from_indications(indications)

    return {
        "input_drug": req.drug,
        "normalized": props,
        "therapeutic_classes": classes,
        "indication_keywords": indications,
        "candidates": candidates,
        "disclaimer": "This is a research aid, not medical advice. Always consult a clinician."
    }