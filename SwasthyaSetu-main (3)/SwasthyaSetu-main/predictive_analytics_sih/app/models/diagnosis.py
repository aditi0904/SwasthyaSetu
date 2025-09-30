from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class Diagnosis(Base):
    __tablename__ = "diagnoses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    primary_condition = Column(String)
    secondary_conditions = Column(JSON)
    namaste_codes = Column(JSON)
    icd11_codes = Column(JSON)
    tm2_codes = Column(JSON)
    confidence_score = Column(Float)
    diagnosis_date = Column(DateTime(timezone=True), server_default=func.now())
    diagnosed_by = Column(String)
    notes = Column(String)

class DiagnosisData(BaseModel):
    """Pydantic model for diagnosis data"""
    patient_id: str
    primary_condition: str
    secondary_conditions: List[str] = []
    namaste_codes: Dict[str, Any] = {}
    icd11_codes: Dict[str, Any] = {}
    tm2_codes: Dict[str, Any] = {}
    confidence_score: float = 0.0
    diagnosed_by: str
    notes: Optional[str] = None

class DiagnosisCreate(BaseModel):
    patient_id: str
    primary_condition: str
    secondary_conditions: List[str] = []
    diagnosed_by: str
    notes: Optional[str] = None