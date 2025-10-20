from fastapi import FastAPI
from app.api.endpoints import validation

# Create the main application instance
app = FastAPI(
    title="Agentic Provider Validation System",
    description="Multi-agent platform for validating healthcare provider data.",
    version="0.1.0"
)

# Include API routers
app.include_router(validation.router, prefix="/api/v1", tags=["validation"])

@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "Agent System API is running. See /docs for endpoints."}