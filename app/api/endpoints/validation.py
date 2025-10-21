# app/api/endpoints/validation.py

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.models.provider import Provider, ProviderBase
from app.core.database import get_session
# CRITICAL IMPORT: Import the task from Agent 1
from app.agents.validation_agent import validate_provider_task 

# --- Define the router object ---
router = APIRouter() 
# ---------------------------------------------

# FIX: Changed response_model from List[ProviderBase] to a simple dict
@router.post("/providers/ingest", response_model=dict) 
def ingest_providers(
    providers_data: List[ProviderBase],
    session: Session = Depends(get_session)
):
    """
    Saves new providers to the database and triggers the asynchronous 
    validation pipeline (Agent 1).
    """
    
    # Use a list to store the database objects temporarily
    new_providers = []
    
    for data in providers_data:
        # 1. Validate incoming data using the Pydantic base model
        provider_base = ProviderBase.model_validate(data)
        
        # 2. Convert the validated base model data into the Provider table object
        #    This two-step validation is safer for complex SQLModel mappings
        provider = Provider.model_validate(provider_base.model_dump())
        
        session.add(provider)
        new_providers.append(provider)

    # 3. Commit the transaction to the database
    # This is where the database assigns the ID and the transaction completes.
    session.commit()
    
    # 4. Refresh and Queue
    # Now that the records exist, we retrieve the IDs and queue the tasks.
    for provider in new_providers:
        session.refresh(provider) 
        
        # Trigger validation task using the newly generated ID
        validate_provider_task.delay(provider.id) 

    # 5. Return a simple, non-relational response to prevent serialization crash (500 error)
    return {
        "status": "success", 
        "message": f"Successfully queued {len(providers_data)} validation tasks.", 
        "first_id": new_providers[0].id if new_providers else None
    }