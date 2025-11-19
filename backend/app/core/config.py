import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "CloudSathi"
    
    # AWS Credentials
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    
    # Azure Credentials
    AZURE_SUBSCRIPTION_ID: str = os.getenv("AZURE_SUBSCRIPTION_ID", "")
    AZURE_TENANT_ID: str = os.getenv("AZURE_TENANT_ID", "")
    AZURE_CLIENT_ID: str = os.getenv("AZURE_CLIENT_ID", "")
    AZURE_CLIENT_SECRET: str = os.getenv("AZURE_CLIENT_SECRET", "")
    
    # NLP Model
    RECOMMENDER_MODEL_PATH: str = os.getenv("RECOMMENDER_MODEL_PATH", "models/recommender")
    
    # AWS Athena (CUR)
    AWS_ATHENA_DATABASE: str = os.getenv("AWS_ATHENA_DATABASE", "athenacurcfn_my_cur_report")
    AWS_ATHENA_TABLE: str = os.getenv("AWS_ATHENA_TABLE", "my_cur_report")
    AWS_ATHENA_OUTPUT_LOCATION: str = os.getenv("AWS_ATHENA_OUTPUT_LOCATION", "s3://my-athena-results-bucket/")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
