from fastapi import FastAPI
from api.routes.public_router import public_router
from api.routes.user_routes import protected_router

app = FastAPI(title="Aqua API")

app.include_router(public_router)
app.include_router(protected_router)
