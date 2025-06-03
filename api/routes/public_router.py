from fastapi import APIRouter
from typing import Dict

public_router = APIRouter()


@public_router.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    return {
        "status": "healthy",
        "service": "aqua-api"
    }
