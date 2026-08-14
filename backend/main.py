import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from src.rate_limit import limiter
from src.routes import api_router
from src.db.supabase import get_supabase_admin
from src.config import ADMIN_EMAIL, ADMIN_PASSWORD
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    sb = get_supabase_admin()
    try:
        listed = sb.auth.admin.list_users()
        users = getattr(listed, "users", listed) or []
        if not any(getattr(u, "email", None) == ADMIN_EMAIL for u in users):
            print("Creating default admin user...")
            sb.auth.admin.create_user({
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD,
                "email_confirm": True,
                "user_metadata": {"username": "admin"},
                "app_metadata": {"role": "admin", "is_active": True},
            })
            print("Default admin user created successfully.")
        else:
            print("Admin user already exists.")
    except Exception as e:
        print(f"Admin bootstrap error: {e}")
    yield


app = FastAPI(
    title="EcoTrans API",
    description="Sistema de Monitoreo y Análisis de la Red de Transporte Urbano",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

o = [x.strip() for x in os.getenv("ORIGINS", "").split(",") if x.strip()]
origins = o or [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:4321",
    "http://127.0.0.1:4321",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SlowAPIMiddleware)


@app.get("/")
async def root():
    return {"status": "ok", "app": "RentCars api", "docs": "/docs"}


app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
