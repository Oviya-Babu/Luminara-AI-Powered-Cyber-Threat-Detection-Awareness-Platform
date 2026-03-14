"""
Application configuration settings.
Loads environment variables from .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Luminara API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0")

    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")


# Create settings instance
settings = Settings()