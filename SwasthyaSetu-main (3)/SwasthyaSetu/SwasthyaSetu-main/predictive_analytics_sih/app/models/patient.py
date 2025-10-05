from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.core.database import Base
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    contact_info = Column(JSON)
    medical_history = Column(JSON)
    current_medications = Column(JSON)
    allergies = Column(JSON)
    lifestyle_factors = Column(JSON)
    constitution_type = Column(String)  # Ayurvedic constitution
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PatientData(BaseModel):
    """Pydantic model for patient data"""
    patient_id: str
    name: str
    age: int
    gender: str
    contact_info: Dict[str, Any]
    medical_history: List[str] = []
    current_medications: List[str] = []
    allergies: List[str] = []
    lifestyle_factors: Dict[str, Any] = {}
    constitution_type: Optional[str] = None

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    contact_info: Dict[str, Any]
    medical_history: List[str] = []
    current_medications: List[str] = []
    allergies: List[str] = []
    lifestyle_factors: Dict[str, Any] = {}