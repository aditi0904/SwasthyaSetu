"""Real ICD-11 TM2 Integration Service"""

import httpx
import base64
from typing import Dict, List, Any, Optional
import structlog
from datetime import datetime, timedelta
import asyncio
import json

from app.core.config import get_settings

logger = structlog.get_logger(__name__)

class RealICD11Service:
    """Real ICD-11 TM2 integration service"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.ICD11_API_BASE_URL
        self.client_id = self.settings.ICD11_CLIENT_ID
        self.client_secret = self.settings.ICD11_CLIENT_SECRET
        self.access_token = None
        self.token_expires_at = None
        self.api_version = "v2"
        
    async def initialize(self):
        """Initialize ICD-11 API connection"""
        try:
            await self._get_access_token()
            logger.info("ICD-11 TM2 service initialized successfully")
            return True
        except Exception as e:
            logger.error("Failed to initialize ICD-11 service", error=str(e))
            return False
    
    async def _get_access_token(self):
        """Get OAuth2 access token from WHO"""
        try:
            # Encode credentials
            credentials = base64.b64encode(
                f"{self.client_id}:{self.client_secret}".encode()
            ).decode()
            
            headers = {
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {
                "grant_type": "client_credentials",
                "scope": "icdapi_access"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://icdaccessmanagement.who.int/connect/token",
                    headers=headers,
                    data=data
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.access_token = token_data["access_token"]
                    
                    # Calculate expiry time
                    expires_in = token_data.get("expires_in", 3600)
                    self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
                    
                    logger.info("Successfully obtained ICD-11 access token")
                else:
                    raise Exception(f"Token request failed: {response.status_code} - {response.text}")
                    
        except Exception as e:
            logger.error("Failed to get ICD-11 access token", error=str(e))
            raise
    
    async def _ensure_valid_token(self):
        """Ensure we have a valid access token"""
        if not self.access_token or datetime.now() >= self.token_expires_at:
            await self._get_access_token()
    
    async def search_tm2_codes(self, query: str, language: str = "en") -> List[Dict[str, Any]]:
        """Search TM2 codes using ICD-11 API"""
        try:
            await self._ensure_valid_token()
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/json",
                "Accept-Language": language,
                "API-Version": self.api_version
            }
            
            # Search in TM2 module
            search_url = f"{self.base_url}/entity/search"
            params = {
                "q": query,
                "subtreeFilterUsesFoundationDescendants": "false",
                "includeKeywordResult": "true",
                "useFlexisearch": "true",
                "flatResults": "false",
                "highlightingEnabled": "false",
                "medicalCodingMode": "false",
                "chapterFilter": "31"  # TM2 chapter
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    search_url,
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._process_search_results(data, query)
                else:
                    logger.error("TM2 search failed", 
                               status_code=response.status_code, 
                               response=response.text)
                    return []
                    
        except Exception as e:
            logger.error("Failed to search TM2 codes", error=str(e), query=query)
            return []
    
    def _process_search_results(self, data: Dict[str, Any], query: str) -> List[Dict[str, Any]]:
        """Process ICD-11 search results"""
        try:
            results = []
            destination_entities = data.get("destinationEntities", [])
            
            for entity in destination_entities:
                # Extract TM2 specific information
                tm2_info = {
                    "icd11_code": entity.get("theCode", ""),
                    "title": entity.get("title", {}).get("@value", ""),
                    "definition": entity.get("definition", {}).get("@value", ""),
                    "uri": entity.get("@id", ""),
                    "chapter": "TM2",
                    "match_score": self._calculate_match_score(entity, query),
                    "synonyms": [],
                    "parent_info": {},
                    "child_count": 0
                }
                
                # Extract synonyms
                synonyms = entity.get("synonym", [])
                for synonym in synonyms:
                    if isinstance(synonym, dict) and "label" in synonym:
                        tm2_info["synonyms"].append(synonym["label"].get("@value", ""))
                
                # Get parent information
                parent = entity.get("parent", [])
                if parent and isinstance(parent, list) and len(parent) > 0:
                    parent_info = parent[0]
                    tm2_info["parent_info"] = {
                        "code": parent_info.get("theCode", ""),
                        "title": parent_info.get("title", {}).get("@value", ""),
                        "uri": parent_info.get("@id", "")
                    }
                
                # Count children
                children = entity.get("child", [])
                tm2_info["child_count"] = len(children) if children else 0
                
                results.append(tm2_info)
            
            # Sort by match score
            results.sort(key=lambda x: x["match_score"], reverse=True)
            return results
            
        except Exception as e:
            logger.error("Failed to process search results", error=str(e))
            return []
    
    def _calculate_match_score(self, entity: Dict[str, Any], query: str) -> float:
        """Calculate match score for search result"""
        try:
            score = 0.0
            query_lower = query.lower()
            
            # Title match
            title = entity.get("title", {}).get("@value", "").lower()
            if query_lower == title:
                score += 1.0
            elif query_lower in title:
                score += 0.8
            elif any(word in title for word in query_lower.split()):
                score += 0.6
            
            # Code match
            code = entity.get("theCode", "").lower()
            if query_lower in code:
                score += 0.5
            
            # Synonym match
            synonyms = entity.get("synonym", [])
            for synonym in synonyms:
                if isinstance(synonym, dict) and "label" in synonym:
                    synonym_text = synonym["label"].get("@value", "").lower()
                    if query_lower in synonym_text:
                        score += 0.7
                        break
            
            # Definition match
            definition = entity.get("definition", {}).get("@value", "").lower()
            if query_lower in definition:
                score += 0.3
            
            return min(score, 1.0)  # Cap at 1.0
            
        except Exception as e:
            logger.error("Failed to calculate match score", error=str(e))
            return 0.0
    
    async def get_tm2_entity_details(self, entity_uri: str) -> Dict[str, Any]:
        """Get detailed information about a TM2 entity"""
        try:
            await self._ensure_valid_token()
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/json",
                "API-Version": self.api_version
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(entity_uri, headers=headers)
                
                if response.status_code == 200:
                    entity_data = response.json()
                    return self._process_entity_details(entity_data)
                else:
                    logger.error("Failed to get entity details", 
                               status_code=response.status_code,
                               uri=entity_uri)
                    return {}
                    
        except Exception as e:
            logger.error("Failed to get TM2 entity details", error=str(e), uri=entity_uri)
            return {}
    
    def _process_entity_details(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process detailed entity information"""
        try:
            details = {
                "icd11_code": entity_data.get("theCode", ""),
                "title": entity_data.get("title", {}).get("@value", ""),
                "definition": entity_data.get("definition", {}).get("@value", ""),
                "longDefinition": entity_data.get("longDefinition", {}).get("@value", ""),
                "fullySpecifiedName": entity_data.get("fullySpecifiedName", {}).get("@value", ""),
                "uri": entity_data.get("@id", ""),
                "synonyms": [],
                "inclusions": [],
                "exclusions": [],
                "postcoordinationScale": [],
                "indexTerms": [],
                "browserUrl": entity_data.get("browserUrl", ""),
                "chapter": "TM2"
            }
            
            # Extract synonyms
            synonyms = entity_data.get("synonym", [])
            for synonym in synonyms:
                if isinstance(synonym, dict):
                    synonym_info = {
                        "label": synonym.get("label", {}).get("@value", ""),
                        "language": synonym.get("label", {}).get("@language", "en")
                    }
                    details["synonyms"].append(synonym_info)
            
            # Extract inclusions
            inclusions = entity_data.get("inclusion", [])
            for inclusion in inclusions:
                if isinstance(inclusion, dict):
                    details["inclusions"].append(
                        inclusion.get("label", {}).get("@value", "")
                    )
            
            # Extract exclusions
            exclusions = entity_data.get("exclusion", [])
            for exclusion in exclusions:
                if isinstance(exclusion, dict):
                    details["exclusions"].append(
                        exclusion.get("label", {}).get("@value", "")
                    )
            
            # Extract index terms
            index_terms = entity_data.get("indexTerm", [])
            for term in index_terms:
                if isinstance(term, dict):
                    details["indexTerms"].append(
                        term.get("label", {}).get("@value", "")
                    )
            
            return details
            
        except Exception as e:
            logger.error("Failed to process entity details", error=str(e))
            return {}
    
    async def map_condition_to_tm2(self, condition: str) -> Dict[str, Any]:
        """Map medical condition to ICD-11 TM2 codes"""
        try:
            # Search for the condition in TM2
            search_results = await self.search_tm2_codes(condition)
            
            if not search_results:
                # Try alternative search terms
                alternative_terms = self._get_alternative_terms(condition)
                for alt_term in alternative_terms:
                    search_results = await self.search_tm2_codes(alt_term)
                    if search_results:
                        break
            
            if search_results:
                # Get detailed information for top results
                detailed_mappings = []
                for result in search_results[:3]:  # Top 3 results
                    if result.get("uri"):
                        details = await self.get_tm2_entity_details(result["uri"])
                        if details:
                            mapping = {
                                "tm2_code": details["icd11_code"],
                                "tm2_title": details["title"],
                                "tm2_definition": details["definition"],
                                "match_score": result["match_score"],
                                "uri": details["uri"],
                                "synonyms": details["synonyms"],
                                "browser_url": details["browserUrl"]
                            }
                            detailed_mappings.append(mapping)
                
                return {
                    "condition": condition,
                    "tm2_mappings": detailed_mappings,
                    "total_matches": len(search_results),
                    "search_successful": True,
                    "source": "icd11_api"
                }
            else:
                return {
                    "condition": condition,
                    "tm2_mappings": [],
                    "total_matches": 0,
                    "search_successful": False,
                    "source": "icd11_api",
                    "message": "No TM2 mappings found"
                }
                
        except Exception as e:
            logger.error("Failed to map condition to TM2", error=str(e), condition=condition)
            return {"error": str(e), "condition": condition}
    
    def _get_alternative_terms(self, condition: str) -> List[str]:
        """Get alternative search terms for a condition"""
        # Basic alternative term generation
        alternatives = []
        
        # Add plurals/singulars
        if condition.endswith('s'):
            alternatives.append(condition[:-1])
        else:
            alternatives.append(condition + 's')
        
        # Add common medical synonyms
        synonyms_map = {
            "hypertension": ["high blood pressure", "elevated blood pressure"],
            "diabetes": ["diabetes mellitus", "high blood sugar"],
            "arthritis": ["joint inflammation", "arthritic condition"],
            "headache": ["cephalgia", "head pain"],
            "fever": ["pyrexia", "hyperthermia"],
            "nausea": ["feeling sick", "stomach upset"]
        }
        
        condition_lower = condition.lower()
        if condition_lower in synonyms_map:
            alternatives.extend(synonyms_map[condition_lower])
        
        return alternatives
    
    async def get_tm2_hierarchy(self, tm2_code: str) -> Dict[str, Any]:
        """Get hierarchical structure for TM2 code"""
        try:
            # Search for the code first
            search_results = await self.search_tm2_codes(tm2_code)
            
            if not search_results:
                return {"error": "TM2 code not found", "code": tm2_code}
            
            # Get the entity URI
            entity_uri = search_results[0].get("uri")
            if not entity_uri:
                return {"error": "Entity URI not found", "code": tm2_code}
            
            # Get detailed information
            entity_details = await self.get_tm2_entity_details(entity_uri)
            
            if not entity_details:
                return {"error": "Failed to get entity details", "code": tm2_code}
            
            # Build hierarchy information
            hierarchy = {
                "code": tm2_code,
                "title": entity_details.get("title", ""),
                "level": "specific",
                "parent": entity_details.get("parent_info", {}),
                "children": [],
                "ancestors": [],
                "descendants": []
            }
            
            # Get parent hierarchy (simplified)
            parent_info = entity_details.get("parent_info", {})
            if parent_info:
                hierarchy["ancestors"].append({
                    "code": parent_info.get("code", ""),
                    "title": parent_info.get("title", ""),
                    "uri": parent_info.get("uri", "")
                })
            
            return hierarchy
            
        except Exception as e:
            logger.error("Failed to get TM2 hierarchy", error=str(e), code=tm2_code)
            return {"error": str(e), "code": tm2_code}
    
    async def validate_tm2_code(self, tm2_code: str) -> bool:
        """Validate if a TM2 code exists and is valid"""
        try:
            search_results = await self.search_tm2_codes(tm2_code)
            return len(search_results) > 0 and any(
                result.get("icd11_code") == tm2_code for result in search_results
            )
            
        except Exception as e:
            logger.error("Failed to validate TM2 code", error=str(e), code=tm2_code)
            return False