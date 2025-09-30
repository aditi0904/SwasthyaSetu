#!/usr/bin/env bash
set -e

# Export WHO API key (replace with real one or keep placeholder for SIH demo)
export WHO_ICD_API_KEY="your-api-key-here"

# Run the sync (fetch WHO ICD data)
python3 -m fetch_who_data

# Generate final FHIR resources
python -m generate_fhir

echo "✅ Sync + FHIR generation completed. Check outputs in project root."
# Run locally
python -m venv venv
source venv/bin/activate (or venv\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env   # edit .env
python -m app.init_db
uvicorn app:app --reload --port 8000
