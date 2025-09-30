from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class Treatment(Base):
    __tablename__ = "treatments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"))
    modality = Column(String)  # allopathy, ayurveda, etc.
    treatment_plan = Column(JSON)
    confidence_score = Column(Float)
    status = Column(String, default="recommended")  # recommended, active, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    prescribed_by = Column(String)
    notes = Column(String)

class TreatmentRecommendation(BaseModel):
    """Pydantic model for treatment recommendations"""
    modality: str
    treatment: str
    dosage: Optional[str] = None
    duration: Optional[str] = None
    frequency: Optional[str] = None
    confidence: float
    rationale: str
    contraindications: List[str] = []
    monitoring_required: bool = True
    expected_outcomes: List[str] = []
    side_effects: List[str] = []
    cost_estimate: Optional[float] = None

class TreatmentPlan(BaseModel):
    """Complete treatment plan"""
    patient_id: str
    diagnosis_id: int
    recommendations: List[TreatmentRecommendation]
    integrated_approach: bool = True
    total_confidence: float
    created_by: str
    notes: Optional[str] = None