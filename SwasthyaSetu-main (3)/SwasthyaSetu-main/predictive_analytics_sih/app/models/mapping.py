
from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base
from pydantic import BaseModel

class CodeMapping(Base):
    __tablename__ = "code_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    ayush_code = Column(String, index=True)
    ayush_term = Column(String)
    target_system = Column(String)  # TM2, Biomedicine
    who_code = Column(String)
    who_term = Column(String)
    similarity_score = Column(Float)
    relationship = Column(String)

class MappingData(BaseModel):
    """Pydantic model for code mapping"""
    ayush_code: str
    ayush_term: str
    target_system: str
    who_code: str
    who_term: str
    similarity_score: float
    relationship: str
