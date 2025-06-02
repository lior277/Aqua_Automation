from typing import List
from fastapi import APIRouter, HTTPException, Depends
from core.auth import verify_credentials
from api.schemas.user_schema import UserCreate, UserResponse
from api.services.user_service import UserService

public_router = APIRouter()

protected_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(verify_credentials)]
)


@protected_router.post("", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    created = UserService.create_user(user)
    return UserResponse.model_validate(created, from_attributes=True)


@protected_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user, from_attributes=True)


@protected_router.get("", response_model=List[int])
def list_user_ids():
    users = UserService.list_users()
    return [u.user_id for u in users]
