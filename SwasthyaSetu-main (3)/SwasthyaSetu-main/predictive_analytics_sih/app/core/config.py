import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Application settings (loaded from .env or environment variables)"""
    
    # Application
    APP_NAME: str = "Hybrid Treatment Planner"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    SECRET_KEY: str  # must be set in .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./emr_system.db"
    DATABASE_URL_ASYNC: str = "sqlite+aiosqlite:///./emr_system.db"

    # Google AI
    GOOGLE_AI_API_KEY: str
    GOOGLE_PROJECT_ID: str
    GOOGLE_SERVICE_ACCOUNT_PATH: str = "config/service_account.json"
    GOOGLE_AI_MODEL: str = "gemini-1.5-flash"  # Stable model
    GOOGLE_AI_REGION: str = "us-central1"

    # Google Healthcare API
    HEALTHCARE_DATASET_ID: Optional[str] = None
    HEALTHCARE_FHIR_STORE_ID: Optional[str] = None

    # NAMASTE API
    NAMASTE_API_BASE_URL: str = "https://api.namaste.gov.in/v1"
    NAMASTE_API_KEY: Optional[str] = None

    # ICD-11 API
    ICD11_API_BASE_URL: str = "https://id.who.int/icd"
    ICD11_CLIENT_ID: Optional[str] = None
    ICD11_CLIENT_SECRET: Optional[str] = None

    # Predictive Analytics
    ENABLE_PREDICTIVE_ANALYTICS: bool = True
    PREDICTION_CONFIDENCE_THRESHOLD: float = 0.7
    MAX_TREATMENT_OPTIONS: int = 5

    # File Paths
    DATA_PATH: str = "data"
    MAPPING_DATA_PATH: str = "data/ayush_icd11_tm2_mapping.csv"
    TREATMENT_PROTOCOLS_PATH: str = "data/treatment_protocols.json"

    # Optional extras
    REDIS_URL: str = "redis://localhost:6379/0"
    API_RATE_LIMIT_PER_MINUTE: int = 100
    AI_REQUEST_TIMEOUT: int = 60
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
