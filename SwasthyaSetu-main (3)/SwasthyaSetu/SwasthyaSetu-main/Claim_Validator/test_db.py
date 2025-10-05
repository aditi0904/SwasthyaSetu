import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()  # load .env file
engine = create_engine(os.getenv("DATABASE_URL"), future=True)

with engine.connect() as conn:
    result = conn.execute(text("SELECT now()"))
    print("DB Time:", result.scalar())
