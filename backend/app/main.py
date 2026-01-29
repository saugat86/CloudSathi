from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.routes import aws_router
from app.api.azure_routes import azure_router
from app.api.recommendation_routes import router as recommendation_router

from app.api.aws_cur_routes import router as aws_cur_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="CloudSathi API",
    description="Cloud cost optimization API for Nepal's startups",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aws_router, prefix="/api/aws", tags=["AWS"])
app.include_router(aws_cur_router, prefix="/api/aws/cur", tags=["AWS CUR"])
app.include_router(azure_router, prefix="/api/azure", tags=["Azure"])
app.include_router(recommendation_router, prefix="/api", tags=["Recommendations"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "CloudSathi API is running"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "CloudSathi API",
        "version": "1.0.0",
        "description": "Cloud cost optimization API for Nepal's startups",
        "docs_url": "/docs",
        "health_url": "/health"
    }
