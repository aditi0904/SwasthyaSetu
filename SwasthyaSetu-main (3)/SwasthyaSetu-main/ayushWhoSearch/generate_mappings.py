import os
import csv
import psycopg2
import psycopg2.extras
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuration ---
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

OUTPUT_CSV_PATH = "candidate_mappings_semantic_v2.csv"

# Suggested models:
# "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb" (biomedical focus)
# "ai4bharat/indic-bert" (multilingual, useful for Sanskrit/Hindi/Tamil terms)
MODEL_NAME = "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"

SIMILARITY_THRESHOLD = 0.5
TOP_N_MATCHES = 3


def fetch_codes_from_db(query, table_name):
    """Fetches records from the database as a list of dictionaries."""
    print(f"📖 Fetching records from '{table_name}'...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        records = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        print(f"✅ Found {len(records)} records in {table_name}.")
        return records
    except Exception as e:
        print(f"❌ Failed to fetch from '{table_name}': {e}")
        return []


def classify_relationship(score: float) -> str:
    """Classify mapping relationship strength based on similarity score."""
    if score >= 0.85:
        return "equivalent"
    elif score >= 0.6:
        return "narrower-than"
    else:
        return "related-to"


def generate_semantic_mappings():
    """Generates mappings using Sentence Transformers with enriched data."""
    print(f"🧠 Loading the Sentence Transformer model: '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)

    # 1. Fetch data from all three tables
    ayush_codes = fetch_codes_from_db(
        "SELECT code, display, definition FROM codes", "codes"
    )
    tm2_codes = fetch_codes_from_db(
        "SELECT code, title, index_terms FROM who_tm2_codes", "who_tm2_codes"
    )
    biomed_codes = fetch_codes_from_db(
        "SELECT code, title, definition FROM biomedicine_codes",
        "biomedicine_codes",
    )

    if not ayush_codes:
        print("❌ Critical Error: Could not fetch AYUSH codes. Aborting.")
        return

    # 2. Prepare text for embedding
    ayush_texts = [
        f"{rec['display']}. {rec.get('definition') or ''}" for rec in ayush_codes
    ]
    tm2_texts = [
        f"{rec['title']}. {rec.get('index_terms') or ''}" for rec in tm2_codes
    ]
    biomed_texts = [
        f"{rec['title']}. {rec.get('definition') or ''}" for rec in biomed_codes
    ]

    # 3. Generate embeddings
    print("⏳ Generating embeddings for AYUSH codes...")
    ayush_embeddings = model.encode(ayush_texts, show_progress_bar=True)

    similarity_matrix_tm2 = None
    similarity_matrix_biomed = None

    if tm2_codes:
        print("⏳ Generating embeddings for TM2 codes (with index terms)...")
        tm2_embeddings = model.encode(tm2_texts, show_progress_bar=True)
        similarity_matrix_tm2 = cosine_similarity(ayush_embeddings, tm2_embeddings)

    if biomed_codes:
        print("⏳ Generating embeddings for Biomedicine codes...")
        biomed_embeddings = model.encode(biomed_texts, show_progress_bar=True)
        similarity_matrix_biomed = cosine_similarity(
            ayush_embeddings, biomed_embeddings
        )

    # 4. Calculate similarities and find top matches
    print("🤖 Calculating similarities and selecting top candidates...")
    all_candidates = []

    for i, ayush in enumerate(ayush_codes):
        # Process TM2 matches
        if similarity_matrix_tm2 is not None:
            tm2_scores = similarity_matrix_tm2[i]
            top_tm2_indices = np.argsort(tm2_scores)[-TOP_N_MATCHES:][::-1]
            for index in top_tm2_indices:
                score = float(tm2_scores[index])
                if score >= SIMILARITY_THRESHOLD:
                    all_candidates.append(
                        {
                            "AYUSH_Code": ayush["code"],
                            "AYUSH_Term": ayush["display"],
                            "Target_System": "TM2",
                            "WHO_Code_Candidate": tm2_codes[index]["code"],
                            "WHO_Term_Candidate": tm2_codes[index]["title"],
                            "Similarity_Score": round(score, 4),
                            "Suggested_Relationship": classify_relationship(score),
                        }
                    )

        # Process Biomedicine matches
        if similarity_matrix_biomed is not None:
            biomed_scores = similarity_matrix_biomed[i]
            top_biomed_indices = np.argsort(biomed_scores)[-TOP_N_MATCHES:][::-1]
            for index in top_biomed_indices:
                score = float(biomed_scores[index])
                if score >= SIMILARITY_THRESHOLD:
                    all_candidates.append(
                        {
                            "AYUSH_Code": ayush["code"],
                            "AYUSH_Term": ayush["display"],
                            "Target_System": "Biomedicine",
                            "WHO_Code_Candidate": biomed_codes[index]["code"],
                            "WHO_Term_Candidate": biomed_codes[index]["title"],
                            "Similarity_Score": round(score, 4),
                            "Suggested_Relationship": classify_relationship(
                                score
                            ),
                        }
                    )

    # 5. Write results to a new CSV
    print(f"\n✍️  Writing {len(all_candidates)} mappings to '{OUTPUT_CSV_PATH}'...")
    headers = [
        "AYUSH_Code",
        "AYUSH_Term",
        "Target_System",
        "WHO_Code_Candidate",
        "WHO_Term_Candidate",
        "Similarity_Score",
        "Suggested_Relationship",
    ]
    with open(OUTPUT_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_candidates)

    print(f"✅ Successfully created '{OUTPUT_CSV_PATH}'.")


if __name__ == "__main__":
    generate_semantic_mappings()
    print("\n🎉 Semantic mapping phase (V2) is complete!")
