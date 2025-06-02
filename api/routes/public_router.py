from fastapi import APIRouter

public_router = APIRouter()

@public_router.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "aqua-api"
    }
