import os, requests
from dotenv import load_dotenv
load_dotenv()

TOKEN_URL = os.getenv("WHO_ICD_TOKEN_URL")
CLIENT_ID = os.getenv("WHO_ICD_CLIENT_ID")
CLIENT_SECRET = os.getenv("WHO_ICD_CLIENT_SECRET")
API_BASE = os.getenv("WHO_ICD_API_BASE", "https://id.who.int")
PAGE_SIZE = int(os.getenv("WHO_ICD_PAGE_SIZE", "50"))

_token_cache = {"access_token": None, "expires_at": 0}

def fetch_token():
    import time
    global _token_cache
    if _token_cache["access_token"] and _token_cache["expires_at"] > time.time() + 30:
        return _token_cache["access_token"]
    if not TOKEN_URL or not CLIENT_ID or not CLIENT_SECRET:
        # no token config — work in unauthenticated mode (some endpoints may still work)
        return None
    data = {"grant_type":"client_credentials"}
    resp = requests.post(TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET), timeout=10)
    resp.raise_for_status()
    j = resp.json()
    token = j.get("access_token")
    exp = time.time() + int(j.get("expires_in",3600))
    _token_cache = {"access_token": token, "expires_at": exp}
    return token

def icd_search(query, page=1):
    token = fetch_token()
    headers = {"Accept":"application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    # WHO search path (mms linearization)
    url = f"{API_BASE}/icd/release/11/mms/search"
    params = {"q": query, "page": page, "pageSize": PAGE_SIZE}
    r = requests.get(url, params=params, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()
