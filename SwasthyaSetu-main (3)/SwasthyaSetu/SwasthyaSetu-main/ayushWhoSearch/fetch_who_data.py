import os, time, json, logging, requests
from pathlib import Path
from urllib.parse import urljoin
import psycopg2
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parents[0]
ICD_TM2_CSV = DATA_DIR / "icd11_tm2_data.csv"
ICD_PROCESSED_CSV = DATA_DIR / "icd11_processed.csv"
ICD_SYNC_META = DATA_DIR / "icd_sync_meta.json"

WHO_BASE = os.getenv("WHO_ICD_API_BASE", "https://id.who.int")
WHO_SEARCH_PATH = "/icd/release/11/mms/search"   # common WHO search path (adjust if docs differ)
PAGE_SIZE = int(os.getenv("WHO_ICD_PAGE_SIZE", "50"))
API_KEY = os.getenv("WHO_ICD_API_KEY", None)
RATE_LIMIT_SLEEP = 0.15

logger = logging.getLogger(__name__)

def _request_search(q, page=1):
    url = urljoin(WHO_BASE, WHO_SEARCH_PATH)
    headers = {"Accept": "application/json"}
    params = {"q": q, "page": page, "pageSize": PAGE_SIZE}
    if API_KEY:
        headers["Api-Key"] = API_KEY
    resp = requests.get(url, params=params, headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.json()

def _extract_entities_from_search(json_resp):
    """
    Generic extractor: WHO JSON-LD formats vary; we look for recognizable keys.
    Return list of dicts: { 'id':..., 'label':..., 'definition':..., 'mms':... }
    """
    entities = []
    # Many WHO responses have 'destination'/'result' or '@graph' or 'titleSet' — try a few patterns
    if isinstance(json_resp, dict):
        # heuristic #1: if 'destination' or 'titleSet' or 'result' exist
        for key in ("destination","titleSet","result","results","entities","items"):
            arr = json_resp.get(key)
            if isinstance(arr, list):
                for it in arr:
                    ent = {}
                    ent['id'] = it.get('id') or it.get('@id') or it.get('entity') or it.get('uri')
                    ent['label'] = it.get('title') or it.get('label') or it.get('displayName') or it.get('name')
                    ent['definition'] = it.get('definition') or it.get('definitionSet') or it.get('desc')
                    # try to find MMS code if present
                    ent['mms'] = it.get('mms') or it.get('code') or None
                    if ent['id'] or ent['label']:
                        entities.append(ent)
                if entities:
                    return entities
    # fallback: traverse top-level lists/dicts for objects that look like entities
    def walk(o):
        if isinstance(o, dict):
            if ('title' in o or 'label' in o) and ('id' in o or '@id' in o or 'uri' in o):
                yield {
                    'id': o.get('id') or o.get('@id') or o.get('uri'),
                    'label': o.get('title') or o.get('label'),
                    'definition': o.get('definition', '')
                }
            for v in o.values():
                yield from walk(v)
        elif isinstance(o, list):
            for x in o:
                yield from walk(x)
    for x in walk(json_resp):
        entities.append(x)
    return entities

def sync_terms(term_list, save_csv=True):
    """Sync a list of search terms -> returns list of found entities"""
    collected = []
    for term in term_list:
        page = 1
        while True:
            try:
                resp = _request_search(term, page=page)
            except Exception as e:
                logger.exception("WHO search failed for %s: %s", term, e)
                break
            ents = _extract_entities_from_search(resp)
            if not ents:
                break
            for e in ents:
                e['source_query'] = term
                collected.append(e)
            # basic pagination heuristics: stop if fewer than PAGE_SIZE returned
            if len(ents) < PAGE_SIZE:
                break
            page += 1
            time.sleep(RATE_LIMIT_SLEEP)
    # optionally dedupe by id or label
    dedup = {}
    for e in collected:
        key = e.get('id') or e.get('label')
        if not key: continue
        if key not in dedup:
            dedup[key] = e
    entities = list(dedup.values())
    # write outputs (CSV/JSON) for later steps
    if save_csv:
        out_json = (DATA_DIR / "icd11_sync_results.json")
        out_json.write_text(json.dumps(entities, ensure_ascii=False, indent=2))
        meta = {"last_sync": __import__("datetime").datetime.utcnow().isoformat(), "count": len(entities)}
        ICD_SYNC_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    return entities
def save_icd_entities_to_db(conn, entities):
    cur = conn.cursor()
    for ent in entities:
        cur.execute("""
            INSERT INTO icd_entities (icd_uri, icd_code, label, definition, source_query, raw_json, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (icd_uri)
            DO UPDATE SET icd_code = EXCLUDED.icd_code,
                          label = EXCLUDED.label,
                          definition = EXCLUDED.definition,
                          source_query = EXCLUDED.source_query,
                          raw_json = EXCLUDED.raw_json,
                          updated_at = EXCLUDED.updated_at
        """, (
            ent["uri"],
            ent.get("code"),
            ent.get("label"),
            ent.get("definition"),
            ent.get("source_query"),
            json.dumps(ent),
            datetime.utcnow()
        ))
    conn.commit()
    cur.close()
