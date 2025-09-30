"""Real NAMASTE API Integration Service"""

import httpx
import pandas as pd
from typing import Dict, List, Any, Optional
import structlog
from datetime import datetime, timedelta
import asyncio

from app.core.config import get_settings

logger = structlog.get_logger(__name__)

class RealNAMASTEService:
    """Real NAMASTE API integration service"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.NAMASTE_API_BASE_URL
        self.api_key = self.settings.NAMASTE_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.mapping_cache = {}
        self.cache_expiry = timedelta(hours=24)
        
        # Load local mapping data as fallback
        self.local_mappings = self._load_local_mappings()
    
    def _load_local_mappings(self) -> pd.DataFrame:
        """Load local mapping data from CSV"""
        try:
            df = pd.read_csv(self.settings.MAPPING_DATA_PATH)
            logger.info(f"Loaded {len(df)} mapping entries from local CSV")
            return df
        except Exception as e:
            logger.error("Failed to load local mapping data", error=str(e))
            return pd.DataFrame()
    
    async def get_ayush_code_mapping(self, condition: str) -> Dict[str, Any]:
        """Get AYUSH code mapping for a medical condition"""
        try:
            # Check cache first
            cache_key = f"condition_{condition.lower()}"
            if cache_key in self.mapping_cache:
                cached_data, timestamp = self.mapping_cache[cache_key]
                if datetime.now() - timestamp < self.cache_expiry:
                    return cached_data
            
            # Try API call first
            api_result = await self._call_namaste_api(condition)
            if api_result:
                # Cache successful API result
                self.mapping_cache[cache_key] = (api_result, datetime.now())
                return api_result
            
            # Fallback to local mapping data
            local_result = self._search_local_mappings(condition)
            if local_result:
                return local_result
            
            # Return empty result if nothing found
            return {
                "ayush_code": "UNKNOWN",
                "ayush_term": condition,
                "mappings": [],
                "confidence": 0.0,
                "source": "none"
            }
            
        except Exception as e:
            logger.error("Failed to get AYUSH code mapping", error=str(e), condition=condition)
            return {"error": str(e), "source": "error"}
    
    async def _call_namaste_api(self, condition: str) -> Optional[Dict[str, Any]]:
        """Call real NAMASTE API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Search for condition in NAMASTE database
                search_url = f"{self.base_url}/search/conditions"
                search_payload = {
                    "query": condition,
                    "system": "all",  # Search in all AYUSH systems
                    "limit": 10,
                    "include_mappings": True
                }
                
                response = await client.post(
                    search_url,
                    json=search_payload,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._process_namaste_response(data, condition)
                
                elif response.status_code == 401:
                    logger.error("NAMASTE API authentication failed - check API key")
                    return None
                
                elif response.status_code == 404:
                    logger.info("Condition not found in NAMASTE database", condition=condition)
                    return None
                
                else:
                    logger.error("NAMASTE API call failed", 
                               status_code=response.status_code, 
                               response=response.text)
                    return None
                    
        except httpx.TimeoutException:
            logger.error("NAMASTE API timeout", condition=condition)
            return None
        except Exception as e:
            logger.error("NAMASTE API call error", error=str(e), condition=condition)
            return None
    
    def _process_namaste_response(self, data: Dict[str, Any], condition: str) -> Dict[str, Any]:
        """Process NAMASTE API response"""
        try:
            results = data.get("results", [])
            if not results:
                return None
            
            # Get best match (assuming API returns sorted by relevance)
            best_match = results[0]
            
            # Extract mappings
            mappings = []
            for mapping in best_match.get("mappings", []):
                mappings.append({
                    "target_system": mapping.get("target_system"),
                    "code": mapping.get("code"),
                    "term": mapping.get("term"),
                    "confidence": mapping.get("confidence", 0.0),
                    "relationship": mapping.get("relationship_type", "related-to")
                })
            
            return {
                "ayush_code": best_match.get("code"),
                "ayush_term": best_match.get("term"),
                "system": best_match.get("system"),  # ayurveda, yoga, unani, etc.
                "mappings": mappings,
                "confidence": best_match.get("confidence", 0.0),
                "source": "namaste_api",
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Failed to process NAMASTE response", error=str(e))
            return None
    
    def _search_local_mappings(self, condition: str) -> Optional[Dict[str, Any]]:
        """Search local mapping data as fallback"""
        try:
            if self.local_mappings.empty:
                return None
            
            # Search for condition in AYUSH terms (case-insensitive)
            condition_lower = condition.lower()
            
            # Try exact match first
            exact_matches = self.local_mappings[
                self.local_mappings['AYUSH_Term'].str.lower() == condition_lower
            ]
            
            if not exact_matches.empty:
                return self._format_local_mapping_result(exact_matches, condition, "exact")
            
            # Try partial match
            partial_matches = self.local_mappings[
                self.local_mappings['AYUSH_Term'].str.lower().str.contains(condition_lower, na=False)
            ]
            
            if not partial_matches.empty:
                return self._format_local_mapping_result(partial_matches, condition, "partial")
            
            # Try reverse search in WHO terms
            who_matches = self.local_mappings[
                self.local_mappings['WHO_Term_Candidate'].str.lower().str.contains(condition_lower, na=False)
            ]
            
            if not who_matches.empty:
                return self._format_local_mapping_result(who_matches, condition, "who_term")
            
            return None
            
        except Exception as e:
            logger.error("Failed to search local mappings", error=str(e))
            return None
    
    def _format_local_mapping_result(self, matches: pd.DataFrame, condition: str, match_type: str) -> Dict[str, Any]:
        """Format local mapping search results"""
        try:
            # Get the best match (highest similarity score)
            best_match = matches.loc[matches['Similarity_Score'].idxmax()]
            
            # Get all related mappings
            mappings = []
            for _, row in matches.iterrows():
                mappings.append({
                    "target_system": row['Target_System'],
                    "code": row['WHO_Code_Candidate'],
                    "term": row['WHO_Term_Candidate'],
                    "confidence": float(row['Similarity_Score']),
                    "relationship": row['Suggested_Relationship']
                })
            
            return {
                "ayush_code": best_match['AYUSH_Code'],
                "ayush_term": best_match['AYUSH_Term'],
                "system": best_match['AYUSH_Code'].split('-')[0].lower() if '-' in best_match['AYUSH_Code'] else "unknown",
                "mappings": mappings,
                "confidence": float(best_match['Similarity_Score']),
                "source": f"local_mapping_{match_type}",
                "match_type": match_type,
                "total_mappings": len(mappings)
            }
            
        except Exception as e:
            logger.error("Failed to format local mapping result", error=str(e))
            return None
    
    async def get_treatment_protocols(self, ayush_code: str, system: str = None) -> Dict[str, Any]:
        """Get treatment protocols for AYUSH code"""
        try:
            # Try API call first
            async with httpx.AsyncClient(timeout=30.0) as client:
                protocols_url = f"{self.base_url}/protocols/{ayush_code}"
                
                response = await client.get(protocols_url, headers=self.headers)
                
                if response.status_code == 200:
                    data = response.json()
                    return self._process_protocol_response(data, ayush_code, system)
                
                # Fallback to local protocols
                return self._get_local_treatment_protocols(ayush_code, system)
                
        except Exception as e:
            logger.error("Failed to get treatment protocols", error=str(e))
            return self._get_local_treatment_protocols(ayush_code, system)
    
    def _process_protocol_response(self, data: Dict[str, Any], ayush_code: str, system: str) -> Dict[str, Any]:
        """Process treatment protocol API response"""
        try:
            protocol = data.get("protocol", {})
            
            return {
                "ayush_code": ayush_code,
                "system": system,
                "treatments": protocol.get("treatments", []),
                "herbs": protocol.get("herbs", []),
                "formulations": protocol.get("formulations", []),
                "procedures": protocol.get("procedures", []),
                "diet_recommendations": protocol.get("diet", []),
                "lifestyle_modifications": protocol.get("lifestyle", []),
                "contraindications": protocol.get("contraindications", []),
                "monitoring": protocol.get("monitoring", []),
                "source": "namaste_api",
                "evidence_level": protocol.get("evidence_level", "traditional")
            }
            
        except Exception as e:
            logger.error("Failed to process protocol response", error=str(e))
            return {"error": str(e)}
    
    def _get_local_treatment_protocols(self, ayush_code: str, system: str) -> Dict[str, Any]:
        """Get treatment protocols from local data"""
        try:
            # Load treatment protocols from JSON file
            import json
            with open(self.settings.TREATMENT_PROTOCOLS_PATH, 'r') as f:
                protocols = json.load(f)
            
            # Map AYUSH code to condition
            condition_mapping = {
                "AYURVEDA-DIS-001": "hypertension",
                "AYURVEDA-DIS-002": "diabetes",
                "AYURVEDA-DIS-003": "arthritis"
            }
            
            condition = condition_mapping.get(ayush_code)
            if condition and condition in protocols.get("treatment_protocols", {}):
                protocol_data = protocols["treatment_protocols"][condition]
                
                # Extract system-specific protocols
                system_protocols = {}
                if system and system.lower() in protocol_data:
                    system_protocols = protocol_data[system.lower()]
                
                return {
                    "ayush_code": ayush_code,
                    "system": system,
                    "condition": condition,
                    "protocols": system_protocols,
                    "all_modalities": protocol_data,
                    "source": "local_protocols",
                    "evidence_level": "traditional"
                }
            
            return {
                "ayush_code": ayush_code,
                "system": system,
                "protocols": {},
                "source": "local_protocols",
                "message": "No specific protocols found"
            }
            
        except Exception as e:
            logger.error("Failed to get local treatment protocols", error=str(e))
            return {"error": str(e), "source": "local_protocols"}
    
    async def validate_treatment_compatibility(
        self, 
        treatments: List[Dict[str, Any]], 
        patient_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate treatment compatibility across modalities"""
        try:
            compatibility_report = {
                "overall_compatibility": "compatible",
                "interactions": [],
                "contraindications": [],
                "synergies": [],
                "recommendations": []
            }
            
            # Check for known interactions
            allopathic_treatments = [t for t in treatments if t.get("modality") == "allopathy"]
            ayurvedic_treatments = [t for t in treatments if t.get("modality") == "ayurveda"]
            
            # Basic interaction checking
            if allopathic_treatments and ayurvedic_treatments:
                compatibility_report["recommendations"].append(
                    "Monitor for herb-drug interactions"
                )
                compatibility_report["recommendations"].append(
                    "Space allopathic and ayurvedic medications by 2 hours"
                )
            
            # Check patient allergies
            allergies = patient_data.get("allergies", [])
            for treatment in treatments:
                treatment_name = treatment.get("treatment", "").lower()
                for allergy in allergies:
                    if allergy.lower() in treatment_name:
                        compatibility_report["contraindications"].append({
                            "treatment": treatment_name,
                            "reason": f"Patient allergic to {allergy}",
                            "severity": "high"
                        })
            
            # Age-based contraindications
            age = patient_data.get("age", 0)
            if age < 18:
                for treatment in treatments:
                    if "aspirin" in treatment.get("treatment", "").lower():
                        compatibility_report["contraindications"].append({
                            "treatment": treatment.get("treatment"),
                            "reason": "Aspirin contraindicated in children",
                            "severity": "high"
                        })
            
            return compatibility_report
            
        except Exception as e:
            logger.error("Failed to validate treatment compatibility", error=str(e))
            return {"error": str(e)}
    
    async def get_constitution_assessment(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get Ayurvedic constitution assessment"""
        try:
            # Call NAMASTE API for constitution assessment
            async with httpx.AsyncClient(timeout=30.0) as client:
                assessment_url = f"{self.base_url}/assessment/constitution"
                
                payload = {
                    "age": patient_data.get("age"),
                    "gender": patient_data.get("gender"),
                    "symptoms": patient_data.get("symptoms", []),
                    "lifestyle_factors": patient_data.get("lifestyle_factors", {}),
                    "physical_characteristics": patient_data.get("physical_characteristics", {}),
                    "mental_characteristics": patient_data.get("mental_characteristics", {})
                }
                
                response = await client.post(
                    assessment_url,
                    json=payload,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    return response.json()
                
                # Fallback to basic assessment
                return self._basic_constitution_assessment(patient_data)
                
        except Exception as e:
            logger.error("Failed to get constitution assessment", error=str(e))
            return self._basic_constitution_assessment(patient_data)
    
    def _basic_constitution_assessment(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Basic constitution assessment based on simple rules"""
        try:
            age = patient_data.get("age", 30)
            symptoms = patient_data.get("symptoms", [])
            
            # Simple rule-based assessment
            vata_score = 0
            pitta_score = 0
            kapha_score = 0
            
            # Age-based scoring
            if age > 60:
                vata_score += 2
            elif age > 40:
                pitta_score += 2
            else:
                kapha_score += 2
            
            # Symptom-based scoring
            vata_symptoms = ["anxiety", "insomnia", "constipation", "dry skin"]
            pitta_symptoms = ["anger", "inflammation", "acidity", "rashes"]
            kapha_symptoms = ["weight gain", "lethargy", "congestion"]
            
            for symptom in symptoms:
                symptom_lower = symptom.lower()
                if any(vs in symptom_lower for vs in vata_symptoms):
                    vata_score += 1
                if any(ps in symptom_lower for ps in pitta_symptoms):
                    pitta_score += 1
                if any(ks in symptom_lower for ks in kapha_symptoms):
                    kapha_score += 1
            
            # Determine primary constitution
            scores = {"vata": vata_score, "pitta": pitta_score, "kapha": kapha_score}
            primary = max(scores, key=scores.get)
            
            return {
                "primary_constitution": primary,
                "constitution_scores": scores,
                "confidence": 0.6,  # Lower confidence for basic assessment
                "recommendations": self._get_constitutional_recommendations(primary),
                "source": "basic_assessment"
            }
            
        except Exception as e:
            logger.error("Failed basic constitution assessment", error=str(e))
            return {"error": str(e)}
    
    def _get_constitutional_recommendations(self, constitution: str) -> Dict[str, List[str]]:
        """Get basic constitutional recommendations"""
        recommendations = {
            "vata": {
                "diet": ["Warm, cooked foods", "Sweet, sour, salty tastes", "Regular meal times"],
                "lifestyle": ["Regular routine", "Adequate rest", "Gentle exercise"],
                "herbs": ["Ashwagandha", "Brahmi", "Jatamansi"]
            },
            "pitta": {
                "diet": ["Cool, fresh foods", "Sweet, bitter, astringent tastes", "Avoid spicy foods"],
                "lifestyle": ["Stay cool", "Avoid excessive heat", "Moderate exercise"],
                "herbs": ["Brahmi", "Amalaki", "Neem"]
            },
            "kapha": {
                "diet": ["Light, warm foods", "Pungent, bitter, astringent tastes", "Reduce dairy"],
                "lifestyle": ["Regular exercise", "Stay active", "Avoid excessive sleep"],
                "herbs": ["Guggulu", "Trikatu", "Punarnava"]
            }
        }
        
        return recommendations.get(constitution, {})