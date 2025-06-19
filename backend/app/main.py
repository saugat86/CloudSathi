from fastapi import FastAPI
from app.api.routes import aws_router

app = FastAPI(
    title="CloudSathi API",
    description="Cloud cost optimization API for Nepal's startups",
    version="1.0.0"
)

app.include_router(aws_router, prefix="/api/aws", tags=["AWS"])
