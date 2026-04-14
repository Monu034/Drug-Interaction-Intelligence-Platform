from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class InteractionHistory(Base):
    __tablename__ = "interaction_history"

    id = Column(Integer, primary_key=True, index=True)
    drug_a = Column(String(100), index=True)
    drug_b = Column(String(100), index=True)
    severity = Column(String(50))
    explanation = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DrugKnowledge(Base):
    """Optional: For storing drug information if we migrate from CSV"""
    __tablename__ = "drug_knowledge"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text, nullable=True)
    side_effects = Column(Text, nullable=True)

class ClinicalInteraction(Base):
    """Stores the known interaction database from final_dataset.csv"""
    __tablename__ = "clinical_interactions"

    id = Column(Integer, primary_key=True, index=True)
    drug_a = Column(String(100), index=True)
    drug_b = Column(String(100), index=True)
    severity = Column(String(50))
    description = Column(Text)
