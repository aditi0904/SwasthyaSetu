from pathlib import Path
import shutil, json
CONCEPTMAP_PATH = Path("namaste-combined-conceptmap.json")
BACKUP_DIR = Path("./backups"); BACKUP_DIR.mkdir(exist_ok=True)

def merge_entities_into_conceptmap(entities):
    cm = json.loads(CONCEPTMAP_PATH.read_text())
    # assume one group, source = namaste codesystem
    group = cm['group'][0]
    element_map = {el['code']: el for el in group.get('element', [])}
    added = 0
    for ent in entities:
        # ent['id'] might be an absolute URI or short id, normalise
        icd_code = str(ent.get('id') or ent.get('mms') or ent.get('label'))
        icd_uri = icd_code
        if icd_code.startswith("http"):
            # keep
            pass
        else:
            icd_uri = f"http://id.who.int/icd/entity/{icd_code}"
        # naive mapping strategy: find best namaste source using ent['source_query'] or fallback: use candidate_mappings_semantic_v2
        # for demo: map every entity to a 'source' equal to ent.get('source_query')
        # In your implementation, resolve source to NAMASTE code (NOT display)
        src_display = ent.get('source_query')
        # find src code by display
        src_code = None
        # search in CodeSystem
        codesystem = json.loads(Path('namaste-combined-codesystem.json').read_text())
        for c in codesystem.get('concept', []):
            if c.get('display') and src_display and c.get('display').lower() == src_display.lower():
                src_code = c.get('code'); break
        if not src_code:
            continue
        # append mapping
        el = element_map.get(src_code)
        if not el:
            el = {'code': src_code, 'target': []}
            group.setdefault('element', []).append(el)
            element_map[src_code] = el
        # check duplicate target
        if not any(t.get('code') == icd_uri for t in el.get('target', [])):
            el.setdefault('target', []).append({'code': icd_uri, 'display': ent.get('label',''), 'equivalence': 'relatedTo'})
            added += 1
    # backup
    shutil.copy(CONCEPTMAP_PATH, BACKUP_DIR / f"conceptmap_backup_{int(time.time())}.json")
    Path(CONCEPTMAP_PATH).write_text(json.dumps(cm, ensure_ascii=False, indent=2))
    return added
