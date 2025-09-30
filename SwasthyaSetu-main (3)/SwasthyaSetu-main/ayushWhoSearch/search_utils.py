import pandas as pd
from rapidfuzz import fuzz
from functools import lru_cache

CSV = "./data/candidate_mappings_semantic_v2.csv"
df = pd.read_csv(CSV, dtype=str).fillna("")
df["AYUSH_Term_lower"] = df["AYUSH_Term"].str.lower()
df["WHO_Term_lower"] = df["WHO_Term_Candidate"].str.lower()
df["Similarity_Score"] = pd.to_numeric(df.get("Similarity_Score", 0), errors="coerce").fillna(0)

def get_confidence_label(score: float) -> str:
    if score >= 0.8: return "High Match"
    elif score >= 0.6: return "Medium Match"
    return "Low Match"

@lru_cache(maxsize=1024)
def cached_search(query: str, top_k: int = 20, min_similarity: float = 0.5):
    return fuzzy_search_with_explain(query, top_k, min_similarity)

def fuzzy_search_with_explain(query, top_k=20, min_similarity=0.5):
    q = query.lower()
    results = []
    for i, row in df.iterrows():
        ayush = row["AYUSH_Term_lower"]
        who = row["WHO_Term_lower"]
        score_fuzzy_ayush = fuzz.partial_ratio(q, ayush)/100
        score_fuzzy_who = fuzz.partial_ratio(q, who)/100
        sim = float(row.get("Similarity_Score", 0))
        combined = max(score_fuzzy_ayush, score_fuzzy_who) * 0.6 + sim * 0.4
        if combined >= min_similarity:
            results.append({
                "AYUSH_Code": row.get("AYUSH_Code"),
                "AYUSH_Term": row.get("AYUSH_Term"),
                "WHO_Code": row.get("WHO_Code_Candidate"),
                "WHO_Term": row.get("WHO_Term_Candidate"),
                "similarity": sim,
                "fuzzy_ayush": score_fuzzy_ayush,
                "fuzzy_who": score_fuzzy_who,
                "combined": combined,
                "confidence": get_confidence_label(combined),
                "relationship": row.get("Suggested_Relationship"),
                "explain": {"fuzzy_ayush": score_fuzzy_ayush, "fuzzy_who": score_fuzzy_who, "semantic": sim}
            })
    results = sorted(results, key=lambda x: x["combined"], reverse=True)[:top_k]
    return results
