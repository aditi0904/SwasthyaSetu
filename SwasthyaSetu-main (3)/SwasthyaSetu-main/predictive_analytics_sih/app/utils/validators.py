import re
from typing import Any, List, Dict
from pydantic import validator

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate Indian phone number"""
    pattern = r'^[6-9]\d{9}
    return bool(re.match(pattern, phone))

def validate_ayush_code(code: str) -> bool:
    """Validate AYUSH code format"""
    pattern = r'^(AYURVEDA|YOGA|UNANI|SIDDHA|HOMEOPATHY)-[A-Z]{3}-\d{3}
    return bool(re.match(pattern, code))

def sanitize_medical_text(text: str) -> str:
    """Sanitize medical text input"""
    # Remove potentially harmful characters
    text = re.sub(r'[<>"\']', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text.strip()

class MedicalDataValidator:
    """Validator for medical data"""
    
    @staticmethod
    def validate_vital_signs(vital_signs: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate vital signs data"""
        errors = {}
        
        # Temperature validation (Celsius)
        if 'temperature' in vital_signs:
            temp = vital_signs['temperature']
            if not (35.0 <= temp <= 42.0):
                errors.setdefault('temperature', []).append('Temperature must be between 35-42°C')
        
        # Blood pressure validation
        if 'systolic' in vital_signs and 'diastolic' in vital_signs:
            sys = vital_signs['systolic']
            dia = vital_signs['diastolic']
            if not (70 <= sys <= 250) or not (40 <= dia <= 150):
                errors.setdefault('blood_pressure', []).append('Invalid blood pressure range')
            if sys <= dia:
                errors.setdefault('blood_pressure', []).append('Systolic must be higher than diastolic')
        
        # Heart rate validation
        if 'heart_rate' in vital_signs:
            hr = vital_signs['heart_rate']
            if not (30 <= hr <= 220):
                errors.setdefault('heart_rate', []).append('Heart rate must be between 30-220 bpm')
        
        return errors