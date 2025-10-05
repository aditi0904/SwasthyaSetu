import os
import psycopg2
import psycopg2.extras
import pandas as pd
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# IMPORTANT: Update this to the name of the CSV you created from the Excel file
# The preprocess script named it 'icd11_processed.csv'
BIOMEDICINE_CSV_PATH = "icd11_processed.csv"

# IMPORTANT: Update these with the actual column headers from your CSV file.
# We now only expect the Code and the Title.
CSV_CODE_COLUMN = "Code"  # Or whatever the code column is named
CSV_TITLE_COLUMN = "Title" # Or whatever the title column is named

def setup_biomedicine_table():
    """Creates or clears the 'biomedicine_codes' table."""
    print("⚙️  Setting up 'biomedicine_codes' table in the database...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS biomedicine_codes (
                id SERIAL PRIMARY KEY,
                code TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                definition TEXT
            )
        ''')
        cursor.execute("TRUNCATE TABLE biomedicine_codes RESTART IDENTITY")
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ 'biomedicine_codes' table is ready.")
        return True
    except Exception as e:
        print(f"❌ Failed to create table: {e}")
        return False

def populate_biomedicine_table_fast():
    """Reads the biomedicine CSV (with only Code and Title) and uses a fast bulk insert."""
    print(f"📖 Reading terms from '{BIOMEDICINE_CSV_PATH}'...")
    try:
        df = pd.read_csv(BIOMEDICINE_CSV_PATH, dtype=str).fillna('')
        print(f"✅ Found {len(df)} records in the CSV file.")
    except FileNotFoundError:
        print(f"❌ ERROR: '{BIOMEDICINE_CSV_PATH}' not found. Did you run the preprocess script?")
        return
    except KeyError:
        print(f"❌ ERROR: A column was not found. Please make sure the CSV_CODE_COLUMN ('{CSV_CODE_COLUMN}') and CSV_TITLE_COLUMN ('{CSV_TITLE_COLUMN}') variables in the script match your CSV headers exactly.")
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    # Prepare the data for insertion (Code, Title, and an empty string for Definition)
    data_to_insert = [
        (row[CSV_CODE_COLUMN], row[CSV_TITLE_COLUMN], "") # We add an empty string for the definition
        for index, row in df.iterrows() if CSV_CODE_COLUMN in row and CSV_TITLE_COLUMN in row
    ]

    print(f"🚀 Prepared {len(data_to_insert)} records for fast bulk insert.")

    # Use execute_batch for a single, fast transaction
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        insert_query = """
            INSERT INTO biomedicine_codes (code, title, definition)
            VALUES (%s, %s, %s)
            ON CONFLICT (code) DO NOTHING
        """
        
        psycopg2.extras.execute_batch(cursor, insert_query, data_to_insert)
        
        conn.commit()
        print(f"✅ Successfully inserted {len(data_to_insert)} biomedicine terms.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Database population failed: {e}")

if __name__ == "__main__":
    if not DATABASE_URL:
        print("❌ ERROR: DATABASE_URL not found in .env file.")
    else:
        if setup_biomedicine_table():
            populate_biomedicine_table_fast()
            print("\n🎉 Biomedicine codes have been successfully loaded into your database!")