from fastapi import FastAPI
from app.api.routes import aws_router
from app.api.azure_routes import azure_router

app = FastAPI(
    title="CloudSathi API",
    description="Cloud cost optimization API for Nepal's startups",
    version="1.0.0"
)

app.include_router(aws_router, prefix="/api/aws", tags=["AWS"])
app.include_router(azure_router, prefix="/api/azure", tags=["Azure"])
