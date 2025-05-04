import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = "gpt-4"
    TEMPERATURE: float = 0.2
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173"]  

settings = Settings()