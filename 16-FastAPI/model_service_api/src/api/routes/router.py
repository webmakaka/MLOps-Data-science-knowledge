from fastapi import APIRouter
from src.api.routes import (
    predict,
    healthcheck,
)

router = APIRouter()

router.include_router(predict.router, tags=["predict"])
router.include_router(healthcheck.router, tags=["healthcheck"])
