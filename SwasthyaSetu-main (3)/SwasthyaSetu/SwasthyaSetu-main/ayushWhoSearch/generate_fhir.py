import csv
import json
import os   # for WHO release version from env
import uuid
from datetime import datetime
import pandas as pd

# --- Input Config ---
INPUT_FILES_CONFIG = [
    {
        "path": "ayurveda_processed.csv",
        "system": "Ayurveda",
        "columns": {
            "id": "NAMC_CODE",
            "display": "NAMC_term",
            "definition": "Long_definition"
        }
    },
    {
        "path": "siddha_processed.csv",
        "system": "Siddha",
        "columns": {
            "id": "NAMC_CODE",
            "display": "NAMC_TERM",
            "definition": "Long_definition"
        }
    },
    {
        "path": "unani_processed.csv",
        "system": "Unani",
        "columns": {
            "id": "NUMC_CODE",
            "display": "NUMC_TERM",
            "definition": "Long_definition"
        }
    }
]

AI_MAPPINGS_CSV = "candidate_mappings_semantic_v2.csv"

CODESYSTEM_OUTPUT_PATH = 'namaste-combined-codesystem.json'
CONCEPTMAP_OUTPUT_PATH = 'namaste-combined-conceptmap.json'

NAMASTE_CODESYSTEM_URL = "http://your-domain.org/fhir/CodeSystem/namaste-combined"
ICD11_URL = "http://id.who.int/icd/entity"


def create_fhir_resources():
    print("🚀 Starting FHIR resource generation from NAMASTE files + AI mappings...")

    who_release = os.getenv("WHO_ICD_RELEASE", "11")
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

    # --- CodeSystem (combined AYUSH terms) ---
    code_system = {
        "resourceType": "CodeSystem",
        "id": f"namaste-combined-{uuid.uuid4()}",
        "url": NAMASTE_CODESYSTEM_URL,
        "version": f"who-{who_release}-{timestamp}",
        "meta": {
            "lastSync": datetime.utcnow().isoformat() + "Z",
            "whoRelease": who_release
        },
        "name": "NAMASTE_Combined_AYUSH_Terminology",
        "title": "NAMASTE Combined (Ayurveda, Siddha, Unani) Terminology",
        "status": "active",
        "experimental": False,
        "date": datetime.now().isoformat(),
        "publisher": "Your Organization Name",
        "description": "A combined FHIR CodeSystem representing standardized terms from the NAMASTE portal for Ayurveda, Siddha, and Unani.",
        "caseSensitive": True,
        "content": "complete",
        "concept": []
    }

    total_concepts = 0

    # Load each AYUSH system file
    for config in INPUT_FILES_CONFIG:
        file_path = config["path"]
        system_name = config["system"]
        cols = config["columns"]

        print(f"\nProcessing {system_name} file: {file_path}...")

        try:
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                print(f"DEBUG: Found headers: {csv_reader.fieldnames}")

                file_concepts_count = 0
                for row in csv_reader:
                    term_id = row.get(cols["id"], "").strip()
                    term_name = row.get(cols["display"], "").strip()
                    term_def = row.get(cols["definition"], "").strip()

                    if not term_id or not term_name:
                        continue

                    concept_entry = {
                        "code": f"{system_name.upper()}-{term_id}",
                        "display": term_name,
                        "definition": term_def
                    }
                    code_system['concept'].append(concept_entry)
                    file_concepts_count += 1

                print(f"✅ Successfully processed {file_concepts_count} terms from {system_name}.")
                total_concepts += file_concepts_count

        except FileNotFoundError:
            print(f"❌ ERROR: The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

    # Save CodeSystem
    with open(CODESYSTEM_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(code_system, f, indent=4)
    print(f"\n✅ Combined FHIR CodeSystem with {total_concepts} total terms saved to: {CODESYSTEM_OUTPUT_PATH}")

    # --- ConceptMap with AI mappings ---
    concept_map = {
        "resourceType": "ConceptMap",
        "id": f"namaste-combined-to-icd11-{uuid.uuid4()}",
        "url": "http://your-domain.org/fhir/ConceptMap/namaste-combined-to-icd11",
        "version": f"who-{who_release}-{timestamp}",
        "meta": {
            "lastSync": datetime.utcnow().isoformat(),
            "whoRelease": who_release
        },
        "name": "NAMASTE_Combined_to_ICD11_Mapping",
        "title": "Mapping from Combined AYUSH to ICD-11",
        "status": "draft",
        "experimental": True,
        "date": datetime.now().isoformat(),
        "publisher": "Your Organization Name",
        "description": "Maps concepts from the combined NAMASTE AYUSH CodeSystem to WHO ICD-11, enriched by AI semantic similarity.",
        "sourceUri": NAMASTE_CODESYSTEM_URL,
        "targetUri": ICD11_URL,
        "group": [
            {
                "source": NAMASTE_CODESYSTEM_URL,
                "target": ICD11_URL,
                "element": []
            }
        ]
    }

    # Load AI mappings CSV
    try:
        df = pd.read_csv(AI_MAPPINGS_CSV, dtype=str).fillna("")
        print(f"📖 Loaded {len(df)} AI-suggested mappings from {AI_MAPPINGS_CSV}.")

        for _, row in df.iterrows():
            ayush_code = row.get("AYUSH_Code", "").strip()
            who_code = row.get("WHO_Code_Candidate", "").strip()
            who_term = row.get("WHO_Term_Candidate", "").strip()
            relationship = row.get("Suggested_Relationship", "related-to").strip()

            if not ayush_code or not who_code:
                continue

            element_entry = {
                "code": ayush_code,
                "target": [
                    {
                        "code": who_code,
                        "display": who_term,
                        "equivalence": relationship
                    }
                ]
            }
            concept_map["group"][0]["element"].append(element_entry)

        print(f"✅ Added {len(concept_map['group'][0]['element'])} mappings into ConceptMap.")

    except FileNotFoundError:
        print(f"⚠️ AI mappings file {AI_MAPPINGS_CSV} not found. ConceptMap will only be a stub.")

    # Save ConceptMap
    with open(CONCEPTMAP_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(concept_map, f, indent=4)
    print(f"✅ FHIR ConceptMap saved to: {CONCEPTMAP_OUTPUT_PATH}")

    if total_concepts > 0:
        print("\n🎉 Phase 1 + AI integration completed successfully!")
    else:
        print("\n⚠️ Finished, but no CodeSystem data was processed. Please check CSV column names.")


if __name__ == "__main__":
    create_fhir_resources()
