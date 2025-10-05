from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Dict, Any
from app.models.patient import PatientCreate, PatientData
from app.models.diagnosis import DiagnosisCreate, DiagnosisData
from app.models.treatment import TreatmentPlan
from app.services.real_namaste_service import NAMASTEService
from app.services.real_icd11_service import ICD11Service
from app.services.treatment_recommender import TreatmentRecommender

router = APIRouter()

@router.post("/patients", response_model=Dict[str, Any])
async def create_patient(patient: PatientCreate):
    """Create a new patient record"""
    # Generate patient ID
    patient_id = f"PAT_{hash(patient.name + str(patient.age)) % 100000:05d}"
    
    patient_data = PatientData(
        patient_id=patient_id,
        **patient.dict()
    )
    
    # Store in database (implementation needed)
    return {
        "status": "success",
        "patient_id": patient_id,
        "message": "Patient created successfully"
    }

@router.post("/diagnosis", response_model=Dict[str, Any])
async def create_diagnosis(
    diagnosis: DiagnosisCreate,
    request: Request
):
    """Create diagnosis with code mapping"""
    try:
        # Get services from app state
        namaste_service = NAMASTEService()
        icd11_service = ICD11Service()
        
        # Map codes
        namaste_codes = await namaste_service.map_condition_to_codes(
            diagnosis.primary_condition
        )
        
        icd11_codes = await icd11_service.map_to_icd11_tm2(
            diagnosis.primary_condition
        )
        
        # Create diagnosis record
        diagnosis_data = DiagnosisData(
            patient_id=diagnosis.patient_id,
            primary_condition=diagnosis.primary_condition,
            secondary_conditions=diagnosis.secondary_conditions,
            namaste_codes=namaste_codes,
            icd11_codes=icd11_codes,
            diagnosed_by=diagnosis.diagnosed_by,
            notes=diagnosis.notes,
            confidence_score=0.85  # Calculate based on mapping quality
        )
        
        return {
            "status": "success",
            "diagnosis_id": f"DIAG_{hash(diagnosis.patient_id) % 100000:05d}",
            "mapped_codes": {
                "namaste": namaste_codes,
                "icd11": icd11_codes
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/treatment/recommend", response_model=Dict[str, Any])
async def get_treatment_recommendations(
    patient_id: str,
    diagnosis_id: int,
    request: Request
):
    """Get integrative treatment recommendations"""
    try:
        # Get services from app state
        google_ai = request.app.state.google_ai
        treatment_recommender = TreatmentRecommender(google_ai)
        
        # Get patient and diagnosis data (mock implementation)
        patient_data = {
            "age": 45,
            "gender": "female",
            "primary_condition": "hypertension",
            "secondary_conditions": ["diabetes"],
            "current_medications": ["metformin"],
            "allergies": [],
            "constitution_type": "vata-pitta"
        }
        
        # Generate recommendations
        recommendations = await treatment_recommender.get_recommendations(
            patient_data, {"primary_condition": "hypertension"}
        )
        
        return {
            "status": "success",
            "patient_id": patient_id,
            "diagnosis_id": diagnosis_id,
            "recommendations": [rec.dict() for rec in recommendations],
            "integrated_approach": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mapping/{ayush_code}")
async def get_code_mapping(ayush_code: str):
    """Get code mapping for AYUSH code"""
    # Load mapping data (implementation needed)
    return {
        "ayush_code": ayush_code,
        "mappings": [
            {
                "target_system": "TM2",
                "who_code": "SS50",
                "who_term": "Vata constitution pattern (TM2)",
                "similarity_score": 0.5378,
                "relationship": "related-to"
            }
        ]
    }