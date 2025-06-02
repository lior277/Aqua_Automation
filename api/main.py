from fastapi import FastAPI
from api.routes import user_routes
from api.routes.public_router import public_router

app = FastAPI()
app.include_router(public_router)
app.include_router(user_routes.public_router)
app.include_router(user_routes.protected_router)
