from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import relationship
from .database import Base

class Code(Base):
    __tablename__ = "codes"
    id = Column(Integer, primary_key=True, index=True)
    code_system = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False, index=True)
    display = Column(String, nullable=False)
    definition = Column(Text)

class Mapping(Base):
    __tablename__ = "mappings"
    id = Column(Integer, primary_key=True, index=True)
    source_code = Column(String, nullable=False, index=True)
    target_code = Column(String, nullable=False, index=True)
    target_system = Column(String, nullable=False)
    relationship = Column(String)
    similarity = Column(Float)

class IcdEntity(Base):
    __tablename__ = "icd_entities"
    id = Column(Integer, primary_key=True, index=True)
    icd_uri = Column(String, unique=True)
    icd_code = Column(String)
    label = Column(String)
    definition = Column(Text)
    source_query = Column(String)
    raw_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    by_user = Column(String)
    details = Column(JSON)
    ts = Column(DateTime(timezone=True), server_default=func.now())
