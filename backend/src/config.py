import os
from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER",'ecotrans')
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD","ecotrans123")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./backend.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_CLIENT_ID = os.getenv("STRIPE_CLIENT_ID", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:4321")

API_V1_PREFIX = "/api/v1"
