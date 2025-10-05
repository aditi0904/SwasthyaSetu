"""Treatment Recommendation Service"""

from typing import Dict, List, Any
import structlog
from app.services.google_ai_service import GoogleAIService, TreatmentContext
from app.models.treatment import TreatmentRecommendation

logger = structlog.get_logger(__name__)

class TreatmentRecommender:
    """Service for generating integrative treatment recommendations"""
    
    def __init__(self, google_ai_service: GoogleAIService):
        self.google_ai = google_ai_service
    
    async def get_recommendations(
        self,
        patient_data: Dict[str, Any],
        diagnosis_data: Dict[str, Any]
    ) -> List[TreatmentRecommendation]:
        """Get comprehensive treatment recommendations"""
        
        # Create treatment context
        context = TreatmentContext(
            patient_age=patient_data.get("age", 0),
            patient_gender=patient_data.get("gender", "unknown"),
            primary_condition=diagnosis_data.get("primary_condition", ""),
            secondary_conditions=patient_data.get("secondary_conditions", []),
            current_medications=patient_data.get("current_medications", []),
            allergies=patient_data.get("allergies", []),
            lifestyle_factors=patient_data.get("lifestyle_factors", {}),
            constitution_type=patient_data.get("constitution_type"),
            severity=diagnosis_data.get("severity", "moderate")
        )
        
        # Get AI-powered recommendations
        ai_recommendations = await self.google_ai.get_integrative_treatment_recommendations(
            context, diagnosis_data
        )
        
        # Enhance with rule-based recommendations
        enhanced_recommendations = await self._enhance_with_rules(
            ai_recommendations, context
        )
        
        return enhanced_recommendations
    
    async def _enhance_with_rules(
        self,
        ai_recommendations: List[TreatmentRecommendation],
        context: TreatmentContext
    ) -> List[TreatmentRecommendation]:
        """Enhance AI recommendations with rule-based logic"""
        
        enhanced = []
        
        for rec in ai_recommendations:
            # Apply safety rules
            if await self._is_safe_recommendation(rec, context):
                # Adjust based on patient constitution (Ayurvedic)
                if context.constitution_type:
                    rec = self._adjust_for_constitution(rec, context.constitution_type)
                
                # Add monitoring requirements
                rec.monitoring_required = self._requires_monitoring(rec, context)
                
                enhanced.append(rec)
        
        # Add lifestyle recommendations
        lifestyle_recs = self._get_lifestyle_recommendations(context)
        enhanced.extend(lifestyle_recs)
        
        return enhanced
    
    async def _is_safe_recommendation(
        self,
        recommendation: TreatmentRecommendation,
        context: TreatmentContext
    ) -> bool:
        """Check if recommendation is safe for patient"""
        
        # Check allergies
        for allergy in context.allergies:
            if allergy.lower() in recommendation.treatment.lower():
                return False
        
        # Age-based safety checks
        if context.patient_age < 18:
            unsafe_for_children = ["aspirin", "certain herbs"]
            if any(unsafe in recommendation.treatment.lower() for unsafe in unsafe_for_children):
                return False
        
        return True
    
    def _adjust_for_constitution(
        self,
        recommendation: TreatmentRecommendation,
        constitution: str
    ) -> TreatmentRecommendation:
        """Adjust recommendation based on Ayurvedic constitution"""
        
        constitution_adjustments = {
            "vata": {
                "emphasis": "warmth, regularity, grounding",
                "avoid": "cold, dry, irregular"
            },
            "pitta": {
                "emphasis": "cooling, calming, moderate",
                "avoid": "hot, spicy, excessive"
            },
            "kapha": {
                "emphasis": "stimulating, warming, energizing",
                "avoid": "heavy, cold, excessive"
            }
        }
        
        if constitution in constitution_adjustments:
            adjustment = constitution_adjustments[constitution]
            recommendation.rationale += f" (Adjusted for {constitution} constitution: {adjustment['emphasis']})"
        
        return recommendation
    
    def _requires_monitoring(
        self,
        recommendation: TreatmentRecommendation,
        context: TreatmentContext
    ) -> bool:
        """Determine if recommendation requires monitoring"""
        
        high_monitoring_treatments = [
            "medication", "surgery", "invasive", "prescription"
        ]
        
        return any(term in recommendation.treatment.lower() for term in high_monitoring_treatments)
    
    def _get_lifestyle_recommendations(
        self,
        context: TreatmentContext
    ) -> List[TreatmentRecommendation]:
        """Get lifestyle-based recommendations"""
        
        lifestyle_recs = []
        
        # Diet recommendations
        if context.primary_condition in ["diabetes", "hypertension", "obesity"]:
            lifestyle_recs.append(TreatmentRecommendation(
                modality="lifestyle",
                treatment="Adopt heart-healthy diet with reduced sodium and processed foods",
                confidence=0.9,
                rationale="Diet modification is crucial for cardiovascular and metabolic health",
                contraindications=[],
                monitoring_required=False
            ))
        
        # Exercise recommendations
        lifestyle_recs.append(TreatmentRecommendation(
            modality="lifestyle",
            treatment="Regular moderate exercise 30 minutes daily",
            confidence=0.85,
            rationale="Physical activity improves overall health outcomes",
            contraindications=["severe joint problems", "cardiac restrictions"],
            monitoring_required=False
        ))
        
        # Stress management
        lifestyle_recs.append(TreatmentRecommendation(
            modality="lifestyle",
            treatment="Stress reduction through meditation or yoga",
            confidence=0.8,
            rationale="Stress management supports healing and prevents complications",
            contraindications=[],
            monitoring_required=False
        ))
        
        return lifestyle_recs