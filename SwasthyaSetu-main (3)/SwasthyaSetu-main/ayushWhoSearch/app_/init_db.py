import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .database import engine, Base
from . import models

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ DB tables created")

if __name__ == "__main__":
    init_db()
