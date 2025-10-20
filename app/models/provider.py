from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime

# --- Audit and Evidence Models ---

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
    
    provider: "Provider" = Relationship(back_populates="validations")


class QAFlagBase(SQLModel):
    flag_type: str
    severity: str
    notes: Optional[str]

class QAFlag(QAFlagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    provider_id: int = Field(foreign_key="provider.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# --- Core Provider Record Model ---

class ProviderBase(SQLModel):
    input_name: str
    input_phone: Optional[str]
    input_address: Optional[str]
    pdf_path: Optional[str]
    
    # Enriched Fields (Agent 2 & 4)
    npi: Optional[str]
    specialty: Optional[str]
    
    # QA/Status Fields (Agent 3)
    status: str = Field(default="RAW")
    final_confidence: float = Field(default=0.0)


class Provider(ProviderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    validations: List[ValidationResult] = Relationship(back_populates="provider")
    qa_flags: List[QAFlag] = Relationship()

# Fix circular import issue for SQLModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .audit import ValidationResult