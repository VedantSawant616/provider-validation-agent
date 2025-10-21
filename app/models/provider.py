from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

# --- Forward References for Relationships (Crucial for SQLModel) ---
# If ValidationResult is defined later in this same file, 
# we need to reference it as a string.

# --- 1. Audit and Evidence Models ---

class ValidationResultBase(SQLModel):
    agent_type: str = Field(index=True)
    field_name: str
    extracted_value: Optional[str]
    source_url: Optional[str]
    confidence_score: float = Field(default=0.0) # c_f score

class ValidationResult(ValidationResultBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    provider_id: int = Field(foreign_key="provider.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship back to the Provider
    provider: "Provider" = Relationship(back_populates="validations")


class QAFlagBase(SQLModel):
    flag_type: str
    severity: str
    notes: Optional[str]

class QAFlag(QAFlagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    provider_id: int = Field(foreign_key="provider.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# --- 2. Core Provider Record Model ---

class ProviderBase(SQLModel):
    input_name: str
    input_phone: Optional[str]
    input_address: Optional[str]
    pdf_path: Optional[str]
    
    # Enriched Fields (Filled by Agent 2 & 4) 
    # FIX: Adding '= None' makes these fields OPTIONAL in the API POST request.
    npi: Optional[str] = None       
    specialty: Optional[str] = None 
    
    # QA/Status Fields (Set by Agent 3)
    status: str = Field(default="RAW")
    final_confidence: float = Field(default=0.0)


class Provider(ProviderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships (Using string literals for forward reference)
    validations: List["ValidationResult"] = Relationship(back_populates="provider")
    qa_flags: List["QAFlag"] = Relationship(back_populates="provider")
    
# Add the reverse relationship link to QAFlag
QAFlag.provider = Relationship(back_populates="qa_flags")