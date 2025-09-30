import os
import psycopg2
import psycopg2.extras
import pandas as pd
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
TM2_CSV_PATH = "icd11_tm2_data.csv"  # <-- Make sure this filename is correct

CSV_CODE_COLUMN = "Code"
CSV_TITLE_COLUMN = "Title"
CSV_INDEX_TERMS_COLUMN = "Index_Terms"

def setup_tm2_table():
    """Creates a new, correctly structured table for the TM2 codes."""
    print("⚙️  Setting up the corrected 'who_tm2_codes' table...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        # Drop the old 'who_codes' table if it exists to avoid confusion
        cursor.execute("DROP TABLE IF EXISTS who_codes;")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS who_tm2_codes (
                id SERIAL PRIMARY KEY,
                code TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                index_terms TEXT
            )
        ''')
        cursor.execute("TRUNCATE TABLE who_tm2_codes RESTART IDENTITY")
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ 'who_tm2_codes' table is ready.")
        return True
    except Exception as e:
        print(f"❌ Failed to set up table: {e}")
        return False

def populate_tm2_table_fast():
    """Reads the TM2 CSV and populates the new table."""
    print(f"📖 Reading terms from '{TM2_CSV_PATH}'...")
    try:
        df = pd.read_csv(TM2_CSV_PATH, dtype=str).fillna('')
        print(f"✅ Found {len(df)} records in the CSV file.")
    except FileNotFoundError:
        print(f"❌ ERROR: '{TM2_CSV_PATH}' not found.")
        return
    
    # Prepare data for insertion into the new table structure
    data_to_insert = [
        (row[CSV_CODE_COLUMN], row[CSV_TITLE_COLUMN], row[CSV_INDEX_TERMS_COLUMN])
        for index, row in df.iterrows()
    ]

    print(f"🚀 Prepared {len(data_to_insert)} records for bulk insert.")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO who_tm2_codes (code, title, index_terms)
            VALUES (%s, %s, %s)
            ON CONFLICT (code) DO NOTHING
        """
        psycopg2.extras.execute_batch(cursor, insert_query, data_to_insert)
        conn.commit()
        print(f"✅ Successfully inserted {len(data_to_insert)} TM2 terms.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Database population failed: {e}")

if __name__ == "__main__":
    if setup_tm2_table():
        populate_tm2_table_fast()
        print("\n🎉 TM2 codes have been loaded correctly into the new table!")