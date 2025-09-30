import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, List
import pandas as pd

def generate_patient_id(name: str, dob: str = None) -> str:
    """Generate unique patient ID"""
    data = f"{name}_{dob or datetime.now().isoformat()}"
    hash_object = hashlib.md5(data.encode())
    return f"PAT_{hash_object.hexdigest()[:8].upper()}"

def generate_diagnosis_id(patient_id: str, condition: str) -> str:
    """Generate unique diagnosis ID"""
    data = f"{patient_id}_{condition}_{datetime.now().isoformat()}"
    hash_object = hashlib.md5(data.encode())
    return f"DIAG_{hash_object.hexdigest()[:8].upper()}"

def format_medical_condition(condition: str) -> str:
    """Format medical condition name"""
    # Remove extra spaces and capitalize properly
    formatted = ' '.join(condition.strip().split())
    return formatted.title()

def calculate_age_group(age: int) -> str:
    """Calculate age group category"""
    if age < 13:
        return "pediatric"
    elif age < 18:
        return "adolescent"
    elif age < 65:
        return "adult"
    else:
        return "geriatric"

def load_mapping_data(csv_path: str) -> pd.DataFrame:
    """Load code mapping data from CSV"""
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"Error loading mapping data: {e}")
        return pd.DataFrame()

class DataProcessor:
    """Data processing utilities"""
    
    @staticmethod
    def normalize_symptom_text(text: str) -> str:
        """Normalize symptom text for better matching"""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = ''.join(c for c in text if c.isalnum() or c.isspace())
        # Normalize whitespace
        text = ' '.join(text.split())
        return text
    
    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        """Extract medical keywords from text"""
        # Simple keyword extraction
        common_medical_terms = [
            'pain', 'fever', 'headache', 'cough', 'fatigue',
            'nausea', 'dizziness', 'shortness', 'breath',
            'chest', 'back', 'joint', 'muscle', 'stomach'
        ]
        
        words = text.lower().split()
        keywords = [word for word in words if word in common_medical_terms]
        return list(set(keywords))