from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class DiagnosisBase(BaseModel):
    primary_condition: str = Field(..., min_length=1)
    secondary_conditions: List[str] = Field(default_factory=list)
    
class DiagnosisCreate(DiagnosisBase):
    patient_id: str
    diagnosed_by: str
    notes: Optional[str] = None

class DiagnosisResponse(DiagnosisBase):
    id: int
    patient_id: str
    namaste_codes: Dict[str, Any] = Field(default_factory=dict)
    icd11_codes: Dict[str, Any] = Field(default_factory=dict)
    tm2_codes: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float
    diagnosis_date: datetime
    diagnosed_by: str
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True