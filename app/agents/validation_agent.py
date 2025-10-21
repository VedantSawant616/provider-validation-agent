# app/agents/validation_agent.py

from celery import shared_task
# Import the QA Agent task to ensure the pipeline chain works (even if it's just a placeholder for now)
# NOTE: This creates a circular dependency, but Celery handles it fine for task chaining.
from app.agents.qa_agent import qa_task 
from app.core.database import engine
from app.models.provider import Provider, ValidationResult
from sqlmodel import Session
import time

@shared_task(bind=True)
def validate_provider_task(self, provider_id: int):
    """
    Agent 1: Performs mock API validation and chains to the QA Agent.
    """
    
    # --- 1. Fetch data and simulate work ---
    with Session(engine) as session:
        provider = session.get(Provider, provider_id)
        if not provider:
            print(f"Agent 1: ERROR - Provider {provider_id} not found.")
            return {"error": "Provider not found"}

        print(f"AGENT 1: Starting validation for Provider {provider.id} ({provider.input_name}).")
        
        # MOCK LOGIC: Simulate network latency and NPI check
        time.sleep(1) 
        
        # MOCK: Save evidence to satisfy the QA Agent later
        mock_result = ValidationResult(
            provider_id=provider_id,
            agent_type="DataValidationAgent",
            field_name="npi",
            extracted_value="1234567890",
            source_url="http://mock-npi.gov",
            confidence_score=0.9
        )
        session.add(mock_result)
        session.commit()
        
        print(f"AGENT 1: Validation data saved. Chaining to QA Agent.")

    # --- 2. Chain to the next agent (QA Agent) ---
    qa_task.delay(provider_id) 

    return {"status": "Validation task finished and chained."}