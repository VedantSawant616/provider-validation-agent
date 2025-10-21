from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime

# --- 1. Audit and Evidence Models ---
class ValidationResultBase(SQLModel):
    agent_type: str = Field(index=True)
    field_name: str
    extracted_value: Optional[str]
    source_url: Optional[str]
    confidence_score: float = Field(default=0.0)

class ValidationResult(ValidationResultBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    provider_id: int = Field(foreign_key="provider.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Provider relationship (needs to be defined here)
    provider: "Provider" = Relationship(back_populates="validations")


class QAFlagBase(SQLModel):
    flag_type: str
    severity: str
    notes: Optional[str]

class QAFlag(QAFlagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    provider_id: int = Field(foreign_key="provider.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Provider relationship (needs to be defined here)
    provider: "Provider" = Relationship(back_populates="qa_flags") # Added relationship here

# --- 2. Core Provider Record Model ---

class ProviderBase(SQLModel):
    input_name: str
    input_phone: Optional[str]
    input_address: Optional[str]
    pdf_path: Optional[str]
    
    # FIX: Added '= None' for Pydantic validation
    npi: Optional[str] = None       
    specialty: Optional[str] = None 
    
    status: str = Field(default="RAW")
    final_confidence: float = Field(default=0.0)


class Provider(ProviderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships (needs back_populates that matches the property on the other model)
    validations: List[ValidationResult] = Relationship(back_populates="provider")
    qa_flags: List[QAFlag] = Relationship(back_populates="provider") # Matches QAFlag.provider
    
# NOTE: Removed the separate TYPE_CHECKING block as the classes are defined in order.