import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    DATA_GOV_IN_API_KEY = os.getenv('DATA_GOV_IN_API_KEY', '')
    
    # Data.gov.in Configuration
    DATA_GOV_BASE_URL = 'https://api.data.gov.in/resource'
    
    # Cache Configuration
    CACHE_DIR = 'datasets'
    CACHE_EXPIRY_DAYS = 7
    
    # Flask Configuration
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    PORT = int(os.getenv('PORT', 5000))
    
    # Gemini Configuration
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')