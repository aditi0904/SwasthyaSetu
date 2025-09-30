from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class TreatmentBase(BaseModel):
    modality: str = Field(..., min_length=1)
    treatment: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str = Field(..., min_length=1)

class TreatmentCreate(TreatmentBase):
    patient_id: str
    diagnosis_id: int
    prescribed_by: str
    
class TreatmentResponse(TreatmentBase):
    id: int
    patient_id: str
    diagnosis_id: int
    status: str
    contraindications: List[str] = Field(default_factory=list)
    monitoring_required: bool = True
    created_at: datetime
    prescribed_by: str
    
    class Config:
        from_attributes = True