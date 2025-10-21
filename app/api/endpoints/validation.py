# app/api/endpoints/validation.py

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.models.provider import Provider, ProviderBase
from app.core.database import get_session
# CRITICAL IMPORT: Import the task from Agent 1
from app.agents.validation_agent import validate_provider_task 

# --- CRITICAL FIX: Define the router object ---
router = APIRouter() 
# ---------------------------------------------

@router.post("/providers/ingest", response_model=List[ProviderBase])
def ingest_providers(
    providers_data: List[ProviderBase],
    session: Session = Depends(get_session)
):
    """
    Saves new providers to the database and triggers the asynchronous 
    validation pipeline (Agent 1).
    """
    new_providers = []
    
    for data in providers_data:
        # 1. FIX: Use ProviderBase for initial Pydantic validation (safe with raw JSON)
        # We need to explicitly use model_validate here because SQLModel's from_orm/model_validate 
        # on the table model (Provider) was crashing due to SQLAlchemy mapping issues during threadpool execution.
        provider_base = ProviderBase.model_validate(data)
        
        # 2. Convert the validated base model data into the Provider table object
        provider = Provider.model_validate(provider_base.model_dump())
        
        session.add(provider)
        new_providers.append(provider)

    session.commit()
    
    # Refresh to get the generated primary keys (IDs) from the database
    for provider in new_providers:
        session.refresh(provider) 
        
        # Trigger validation task for each new provider
        validate_provider_task.delay(provider.id) 

    return new_providers