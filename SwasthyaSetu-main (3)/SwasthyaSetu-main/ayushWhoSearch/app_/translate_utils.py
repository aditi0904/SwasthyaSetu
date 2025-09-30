import pandas as pd
from googletrans import Translator

# Load CSV once
CSV = "./data/candidate_mappings_semantic_v2.csv"
df = pd.read_csv(CSV, dtype=str).fillna("")

translator = Translator()

# Optional: manual mapping for AYUSH terms
MANUAL_AYUSH_MAP = {
    "vyAnavAtakopaH": "व्यानवातकोप",
    "vAtaprakopaH": "वातप्रकोप",
    # add more Sanskrit -> Hindi mappings here
}

def translate_term(term: str, target_lang: str = "hi") -> str:
    """
    Translate a term using Google Translate.
    Falls back to original if translation fails.
    """
    try:
        return translator.translate(term, dest=target_lang).text
    except Exception:
        return term

def clean_term(term: str) -> str:
    # Remove leading dashes and extra spaces
    return term.replace("-", "").strip()

def translate_ayush_code(ayush_code: str, target_lang: str = "hi") -> dict:
    row = df[df["AYUSH_Code"] == ayush_code]
    if row.empty:
        return {"AYUSH_Code": ayush_code, "AYUSH_Term": "", "AYUSH_Term_Translated": "", "targets": []}

    ayush_term = row.iloc[0]["AYUSH_Term"]
    ayush_translated = MANUAL_AYUSH_MAP.get(ayush_term, ayush_term)

    targets = []
    for _, r in row.iterrows():
        who_term = r["WHO_Term_Candidate"]
        # preserve (TM2) tag
        tag = ""
        if "(" in who_term and ")" in who_term:
            parts = who_term.split("(")
            base_term = parts[0].strip()
            tag = "(" + parts[1]
        else:
            base_term = who_term

        base_term_clean = clean_term(base_term)
        translated_base = translate_term(base_term_clean, target_lang)
        who_term_translated = f"{translated_base} {tag}".strip()

        targets.append({
            "WHO_Code": r["WHO_Code_Candidate"],
            "WHO_Term": who_term,
            "WHO_Term_Translated": who_term_translated,
            "Similarity_Score": r["Similarity_Score"],
            "Suggested_Relationship": r["Suggested_Relationship"]
        })

    return {
        "AYUSH_Code": ayush_code,
        "AYUSH_Term": ayush_term,
        "AYUSH_Term_Translated": ayush_translated,
        "targets": targets
    }
