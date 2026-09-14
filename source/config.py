"""
Configuration settings for Personal Assistant API.
"""
import os

# Load environment variables from .env file


class Config:
    """Configuration class for the Personal Assistant API."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "1"))

    # TAVILY
    TAVILY_SEARCH_KEY: str = os.getenv("TAVILY_SEARCH_KEY", "")
    MAX_RESULTS: int = int(os.getenv("MAX_RESULTS", "5"))
    
    # Google API Configuration
    GOOGLE_CREDENTIALS_FILE: str = "credentials.json"
    GOOGLE_TOKEN_FILE: str = "token.json"
    GOOGLE_SCOPES: list = [
    'https://www.googleapis.com/auth/calendar',
    'https://mail.google.com/']


    # Timezone Configuration
    DEFAULT_TIMEZONE: str = os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")
    
    # Weather API Configuration
    OPEN_METEO_URL: str = "https://api.open-meteo.com/v1/forecast"
    NOMINATIM_URL: str = "https://nominatim.openstreetmap.org/search"
    
    


# Initialize and validate configuration
config = Config()
