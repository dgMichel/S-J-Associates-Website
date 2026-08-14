from fastapi import APIRouter
from src.config import API_V1_PREFIX
from src.routes.auth.Auth import router as auth_router
from src.routes.cars.availability import router as avail_router


api_router = APIRouter(prefix=API_V1_PREFIX)
api_router.include_router(auth_router)
api_router.include_router(avail_router)
