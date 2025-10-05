# sih/ayush/semantic_routes.py
import pandas as pd
from rapidfuzz import fuzz
from fastapi import APIRouter

router = APIRouter(prefix="/semantic", tags=["Semantic Search"])

# Load CSV once at startup
df = pd.read_csv("candidate_mappings_semantic_v2.csv")
df["AYUSH_Term_lower"] = df["AYUSH_Term"].str.lower()
df["WHO_Term_lower"] = df["WHO_Term_Candidate"].str.lower()

def fuzzy_match(term: str, candidates: pd.Series, threshold: int = 80) -> pd.Series:
    return candidates.apply(lambda x: fuzz.partial_ratio(str(x).lower(), term.lower()) >= threshold)

@router.get("/search/{term}")
def search(term: str):
    term_words = term.lower().split()
    mask = pd.Series(False, index=df.index)
    
    for word in term_words:
        mask |= fuzzy_match(word, df["AYUSH_Term_lower"])
        mask |= fuzzy_match(word, df["WHO_Term_lower"])
    
    semantic_mask = (df["Similarity_Score"] >= 0.5) & mask
    results = df[mask | semantic_mask].copy()
    
    if results.empty:
        return {"message": f"No matches found for '{term}'"}
    
    results["rank_score"] = results["Similarity_Score"].fillna(0)
    results = results.sort_values(by="rank_score", ascending=False)
    
    return results[[
        "AYUSH_Code", "AYUSH_Term", "Target_System",
        "WHO_Code_Candidate", "WHO_Term_Candidate",
        "Similarity_Score", "Suggested_Relationship"
    ]].to_dict(orient="records")
