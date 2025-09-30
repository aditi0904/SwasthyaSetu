"""Patient data schemas"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class PatientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    gender: str = Field(..., regex="^(male|female|other)$")
    contact_info: Dict[str, Any] = Field(default_factory=dict)

class PatientCreate(PatientBase):
    medical_history: List[str] = Field(default_factory=list)
    current_medications: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    lifestyle_factors: Dict[str, Any] = Field(default_factory=dict)

class PatientResponse(PatientBase):
    patient_id: str
    constitution_type: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True