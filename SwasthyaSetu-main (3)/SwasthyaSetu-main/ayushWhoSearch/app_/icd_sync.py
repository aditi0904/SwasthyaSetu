from .who_client import icd_search
from .database import SessionLocal
from .models import IcdEntity
from sqlalchemy.exc import IntegrityError

def sync_terms_to_db(term_list, limit_per_term=3):
    db = SessionLocal()
    added = 0
    for term in term_list:
        for page in range(1, limit_per_term+1):
            resp = icd_search(term, page=page)
            entities = resp.get("destinationEntities") or resp.get("items") or []
            for e in entities:
                icd_uri = e.get("id") or e.get("@id") or e.get("uri")
                icd_code = e.get("mms") or e.get("code") or ''
                label = e.get("title", {}).get("@value") if isinstance(e.get("title"), dict) else e.get("title") or ''
                raw = e
                existing = db.query(IcdEntity).filter(IcdEntity.icd_uri==icd_uri).first()
                if not existing:
                    ent = IcdEntity(icd_uri=icd_uri, icd_code=icd_code, label=label, definition=e.get("definition",""), source_query=term, raw_json=raw)
                    db.add(ent)
                    try:
                        db.commit()
                        added += 1
                    except IntegrityError:
                        db.rollback()
    db.close()
    return added
