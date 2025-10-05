import json, os

def icd_to_ayush(icd_code: str):
    cm_path = "./data/namaste-combined-conceptmap.json"
    if not os.path.exists(cm_path):
        return []
    cm = json.load(open(cm_path))
    results = []
    for el in cm.get("group", [{}])[0].get("element", []):
        for t in el.get("target", []):
            if t.get("code") == icd_code:
                results.append({"AYUSH_Code": el.get("code"), "AYUSH_Term": el.get("display")})
    return results
