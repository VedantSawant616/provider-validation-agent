# app/api/endpoints/validation.py

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.models.provider import Provider, ProviderBase
from app.core.database import get_session
# Import the task from the agent file
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
        # 1. Create and save the raw provider record
        provider = Provider.from_orm(data)
        session.add(provider)
        new_providers.append(provider)

    session.commit()
    
    # Refresh to get the generated primary keys (IDs) from the database
    for provider in new_providers:
        session.refresh(provider) 
        
        # 2. Trigger validation task for each new provider
        # .delay() sends the task to the Celery worker via Redis
        validate_provider_task.delay(provider.id) 

    return new_providers