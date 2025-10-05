"""Fixed Backend - Diet + Hybrid Treatment Planner with Gemini API Fix"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import json
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
import time

load_dotenv()

# Logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Google AI import
try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    logger.warning("Google AI library not available")

from app.core.config import get_settings
from app.core.database import init_db

# CRITICAL FIX: Initialize knowledge base at module level (not just in lifespan)
# This ensures it's available even when mounted as sub-app
KNOWLEDGE_BASE = {
    "food_medicine_interactions": {
        "turmeric": {
            "medical_name": "Curcuma longa",
            "benefits": ["anti-inflammatory", "antioxidant", "digestive"],
            "pairs_with": ["ginger", "black_pepper", "honey"],
            "avoid_with": ["blood_thinners"],
            "dosage": "1-2 tsp daily",
            "preparation": ["golden milk", "curry", "supplement"]
        },
        "ginger": {
            "medical_name": "Zingiber officinale", 
            "benefits": ["nausea relief", "digestive", "anti-inflammatory"],
            "pairs_with": ["turmeric", "lemon", "honey"],
            "avoid_with": ["blood_thinners"],
            "dosage": "1-3g daily",
            "preparation": ["tea", "fresh", "powder"]
        },
        "garlic": {
            "medical_name": "Allium sativum",
            "benefits": ["cardiovascular", "immune", "antimicrobial"],
            "pairs_with": ["onion", "herbs"],
            "avoid_with": ["warfarin"],
            "dosage": "1-2 cloves daily",
            "preparation": ["raw", "cooked", "supplement"]
        }
    },
    "diet_protocols": {
        "anti_inflammatory": {
            "foods": ["leafy greens", "berries", "fatty fish", "nuts", "olive oil"],
            "avoid": ["processed foods", "sugar", "trans fats"],
            "meal_plan": "Mediterranean-style with turmeric",
            "benefits": ["reduces inflammation", "supports healing"]
        },
        "digestive_health": {
            "foods": ["fiber-rich vegetables", "probiotic yogurt", "ginger", "fennel"],
            "avoid": ["spicy foods", "caffeine", "alcohol"],
            "meal_plan": "Light, frequent meals with digestive spices",
            "benefits": ["improves digestion", "reduces bloating"]
        },
        "immune_support": {
            "foods": ["citrus fruits", "garlic", "spinach", "almonds", "green tea"],
            "avoid": ["excessive sugar", "alcohol"],
            "meal_plan": "Nutrient-dense with immune-boosting foods",
            "benefits": ["strengthens immunity", "faster recovery"]
        }
    },
    "yoga_protocols": {
        "digestive": ["cat-cow", "spinal twist", "child's pose", "wind-relieving pose"],
        "stress_relief": ["deep breathing", "shavasana", "gentle forward bends"],
        "circulation": ["sun salutations", "inversions", "twists"],
        "pain_relief": ["gentle stretches", "restorative poses", "meditation"]
    },
    "hybrid_combinations": {
        "fever_treatment": {
            "modern": "Paracetamol 500mg",
            "ayurvedic": "Tulsi tea with honey",
            "diet": "Warm fluids, light foods",
            "yoga": "Gentle breathing exercises",
            "synergy": "Combined approach reduces fever faster"
        },
        "digestive_issues": {
            "modern": "Antacid if severe",
            "ayurvedic": "Ginger-fennel tea",
            "diet": "BRAT diet + probiotics",
            "yoga": "Digestive poses",
            "synergy": "Holistic approach addresses root cause"
        }
    }
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting Diet + Hybrid Treatment Planner")
    
    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    
    # Initialize Google AI
    app.state.ai_available = False
    app.state.ai_model = None
    app.state.ai_error = None
    
    if GOOGLE_AI_AVAILABLE:
        try:
            api_key = os.getenv("GOOGLE_AI_API_KEY")
            if api_key and api_key.strip():
                logger.info("Configuring Google AI...")
                genai.configure(api_key=api_key)
                
                model = genai.GenerativeModel("models/gemini-2.5-flash-lite")

                logger.info("Testing AI model...")
                test_response = model.generate_content(
                    "Hello, AI!",
                    generation_config=genai.GenerationConfig(
                        temperature=0.5,
                        max_output_tokens=50
                    )
                )

                if test_response and getattr(test_response, "text", None):
                    app.state.ai_model = model
                    app.state.ai_available = True
                    logger.info("Google AI model gemini-2.5-flash-lite loaded successfully")
                else:
                    app.state.ai_error = "AI test failed"
                    logger.error("AI test response invalid")
            else:
                app.state.ai_error = "API key missing"
                logger.error("Google AI API key missing")
        except Exception as e:
            app.state.ai_error = str(e)
            logger.error(f"Google AI initialization failed: {e}")
    
    # Set knowledge base (also available at module level)
    app.state.knowledge_base = KNOWLEDGE_BASE
    logger.info("Hybrid treatment knowledge base loaded")
    
    if app.state.ai_available:
        logger.info("System ready with AI capabilities")
    else:
        logger.warning(f"System ready WITHOUT AI - using knowledge base fallback")
    
    yield
    logger.info("Shutting down system")

# Initialize FastAPI app
settings = get_settings()

app = FastAPI(
    title="Diet + Hybrid Treatment Planner",
    description="AI-Powered Holistic Health with Diet, Yoga, and Modern Medicine",
    version="2.0.0",
    lifespan=lifespan
)

# IMPORTANT: Initialize state before any requests
app.state.knowledge_base = KNOWLEDGE_BASE
app.state.ai_available = False
app.state.ai_model = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Diet + Hybrid Treatment Planner",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Hybrid treatment recommendations",
            "Diet + nutrition planning", 
            "Yoga therapy integration",
            "Modern medicine + Ayurveda harmony",
            "Evidence-based holistic care"
        ],
        "ai_status": "Available" if getattr(app.state, 'ai_available', False) else "Knowledge-base mode"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "operational",
            "database": "operational",
            "ai": "operational" if getattr(app.state, 'ai_available', False) else "fallback mode",
            "knowledge_base": "loaded"
        }
    }

@app.post("/hybrid-assessment")
async def hybrid_assessment(data: Dict[str, Any]):
    try:
        patient_data = data.get("patient_data", {})
        symptoms = data.get("symptoms", [])
        dietary_preferences = data.get("dietary_preferences", {})
        lifestyle_factors = data.get("lifestyle_factors", {})
        
        logger.info(f"Starting hybrid assessment for: {patient_data.get('name', 'unknown')}")
        
        if getattr(app.state, 'ai_available', False) and app.state.ai_model:
            recommendations = await get_ai_hybrid_recommendations(
                patient_data, symptoms, dietary_preferences, lifestyle_factors
            )
        else:
            recommendations = get_knowledge_base_recommendations(
                patient_data, symptoms, dietary_preferences, lifestyle_factors
            )
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "patient": patient_data.get("name", "Patient"),
            "hybrid_recommendations": recommendations,
            "approach": "holistic_integration"
        }
        
    except Exception as e:
        logger.error(f"Hybrid assessment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_ai_hybrid_recommendations(patient_data, symptoms, dietary_prefs, lifestyle):
    """AI-powered hybrid recommendations"""
    if not app.state.ai_model:
        return get_knowledge_base_recommendations(patient_data, symptoms, dietary_prefs, lifestyle)
    
    prompt = f"""
You are a holistic health AI specializing in hybrid treatment approaches.

PATIENT: {patient_data.get('age')}y {patient_data.get('gender')}
SYMPTOMS: {', '.join(symptoms)}
DIETARY PREFERENCES: {dietary_prefs}
LIFESTYLE: {lifestyle}

Create a comprehensive hybrid treatment plan in JSON format.
"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = app.state.ai_model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=3000,
                )
            )
            if response and getattr(response, "text", None):
                try:
                    text = response.text.strip()
                    start = text.find('{')
                    end = text.rfind('}') + 1
                    if start != -1 and end != -1:
                        return json.loads(text[start:end])
                except json.JSONDecodeError:
                    if attempt == max_retries - 1:
                        return {"ai_text_response": response.text}
                    continue
            if attempt < max_retries - 1:
                time.sleep(1)
        except Exception as e:
            logger.error(f"AI API call failed on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    return get_knowledge_base_recommendations(patient_data, symptoms, dietary_prefs, lifestyle)

def get_knowledge_base_recommendations(patient_data, symptoms, dietary_prefs, lifestyle):
    """Fallback recommendations - uses module-level KNOWLEDGE_BASE"""
    # Use module-level knowledge base as fallback
    kb = getattr(app.state, 'knowledge_base', KNOWLEDGE_BASE)
    
    recommendations = {
        "source": "evidence_based_knowledge_base",
        "diet_plan": {"therapeutic_foods": [], "meal_schedule": {}, "foods_to_avoid": []},
        "modern_treatment": {"medications": [], "monitoring": ["Consult healthcare provider for prescriptions"]},
        "ayurvedic_treatment": {"herbs": [], "lifestyle": ["Regular routine", "Adequate rest"]},
        "yoga_therapy": {"poses": [], "breathing": ["Deep breathing exercises"], "meditation": "10 minutes daily mindfulness"},
        "integration_plan": {"morning_routine": "Yoga + healthy breakfast + medications",
                             "throughout_day": "Therapeutic foods + herbal teas",
                             "evening_routine": "Light dinner + meditation + rest"}
    }
    
    symptom_text = ' '.join(symptoms).lower()
    
    for food, details in kb["food_medicine_interactions"].items():
        for benefit in details["benefits"]:
            if any(word in symptom_text for word in benefit.split()):
                recommendations["diet_plan"]["therapeutic_foods"].append({
                    "food": food, "benefit": benefit, "preparation": details["preparation"][0], "dosage": details["dosage"]
                })
    
    if "stress" in symptom_text or "anxiety" in symptom_text:
        recommendations["yoga_therapy"]["poses"].extend(kb["yoga_protocols"]["stress_relief"])
    if "digestive" in symptom_text or "stomach" in symptom_text:
        recommendations["yoga_therapy"]["poses"].extend(kb["yoga_protocols"]["digestive"])
    if "inflammation" in symptom_text:
        protocol = kb["diet_protocols"]["anti_inflammatory"]
        recommendations["diet_plan"]["therapeutic_foods"].extend(
            [{"food": food, "benefit": "anti-inflammatory"} for food in protocol["foods"][:3]]
        )
        recommendations["diet_plan"]["foods_to_avoid"].extend(protocol["avoid"])
    
    return recommendations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)