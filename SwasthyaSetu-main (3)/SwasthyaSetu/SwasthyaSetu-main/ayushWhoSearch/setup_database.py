import os
import psycopg2
import psycopg2.extras  # Needed for batch insert
import json
from dotenv import load_dotenv

# --- Config ---
CODESYSTEM_JSON_PATH = "namaste-combined-codesystem.json"

# Load secrets
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def initialize_database():
    """
    Connects to Neon (PostgreSQL) and creates base tables if missing.
    """
    if not DATABASE_URL:
        print("❌ ERROR: DATABASE_URL not found. Did you create the .env file?")
        return False

    print("⚙️  Connecting to the Neon PostgreSQL database...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # --- Codes table ---
        cur.execute("""
            CREATE TABLE IF NOT EXISTS codes (
                id SERIAL PRIMARY KEY,
                code_system TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                display TEXT NOT NULL,
                definition TEXT
            )
        """)

        # --- Mappings table ---
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mappings (
                id SERIAL PRIMARY KEY,
                source_code_id INTEGER NOT NULL,
                target_code_system TEXT NOT NULL,
                target_code TEXT NOT NULL,
                target_display TEXT,
                relationship TEXT NOT NULL,
                FOREIGN KEY (source_code_id) REFERENCES codes (id)
            )
        """)

        # --- ICD entities (WHO ICD sync) ---
        cur.execute("""
            CREATE TABLE IF NOT EXISTS icd_entities (
                id SERIAL PRIMARY KEY,
                icd_uri TEXT UNIQUE,
                icd_code TEXT,
                label TEXT,
                definition TEXT,
                source_query TEXT,
                raw_json JSONB,
                created_at TIMESTAMPTZ DEFAULT now(),
                updated_at TIMESTAMPTZ DEFAULT now()
            )
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database tables are ready.")
        return True
    except Exception as e:
        print(f"❌ Database connection or setup failed: {e}")
        return False


def clear_codes_table():
    """
    Clears all data from 'codes' (fresh start).
    """
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("TRUNCATE TABLE codes RESTART IDENTITY CASCADE")
        conn.commit()
        cur.close()
        conn.close()
        print("🧹 'codes' table cleared.")
    except Exception as e:
        print(f"⚠️ Could not clear table: {e}")


def populate_database_fast():
    """
    Bulk insert FHIR CodeSystem JSON into Neon DB.
    """
    print(f"📖 Reading terms from '{CODESYSTEM_JSON_PATH}'...")
    try:
        with open(CODESYSTEM_JSON_PATH, "r", encoding="utf-8") as f:
            code_system = json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: '{CODESYSTEM_JSON_PATH}' not found.")
        return

    concepts = code_system.get("concept", [])
    if not concepts:
        print("⚠️ No concepts found in JSON.")
        return

    data_to_insert = []
    for concept in concepts:
        code = concept.get("code")
        display = concept.get("display")
        definition = concept.get("definition")
        code_system_name = code.split("-")[0] if code else "unknown"
        data_to_insert.append((code_system_name, code, display, definition))

    print(f"🚀 Prepared {len(data_to_insert)} records for bulk insert...")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        insert_query = """
            INSERT INTO codes (code_system, code, display, definition)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (code) DO NOTHING
        """

        psycopg2.extras.execute_batch(cur, insert_query, data_to_insert)

        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Inserted {len(data_to_insert)} codes.")
    except Exception as e:
        print(f"❌ Bulk insert failed: {e}")


if __name__ == "__main__":
    if initialize_database():
        clear_codes_table()
        populate_database_fast()
        print("\n🎉 Neon DB setup + population complete!")
