import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

class Settings:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    GDB_PATH: str = os.getenv('PROD_GDB' if ENVIRONMENT == 'production' else 'DEV_GDB', '')
    DATABASE_URL = os.getenv("PRODUCTION_URL") if os.getenv("ENVIRONMENT") == "production" else os.getenv("DATABASE_URL")
    print(DATABASE_URL)


settings = Settings()