import uuid
from datetime import datetime
from typing import Dict, List

def validate_dual_coding(bundle: Dict) -> bool:
    has_dual = False
    for e in bundle.get("entry", []):
        r = e.get("resource", {})
        if r.get("resourceType") == "Condition":
            codings = r.get("code", {}).get("coding", [])
            systems = [c.get("system", "").lower() for c in codings]
            if any("namaste" in s for s in systems) and any("icd" in s or "who.int" in s for s in systems):
                has_dual = True
    return has_dual

def add_provenance(bundle: Dict, user_id: str) -> Dict:
    bundle_id = bundle.get("id") or str(uuid.uuid4())
    bundle["id"] = bundle_id
    bundle["meta"] = {"provenance": {"user": user_id, "timestamp": datetime.utcnow().isoformat()}}
    return bundle
