from fastapi import APIRouter, Depends, status
from typing import List

from core.auth import verify_credentials
from core.exceptions import UserNotFoundError
from api.schemas.user_schema import UserCreate, UserResponse
from api.services.user_service import UserService, get_user_service

protected_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(verify_credentials)]
)


@protected_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
        user: UserCreate,
        service: UserService = Depends(get_user_service)
) -> UserResponse:
    created = service.create_user(user)
    return UserResponse.model_validate(created, from_attributes=True)


@protected_router.get("/{user_id}", response_model=UserResponse)
def get_user(
        user_id: int,
        service: UserService = Depends(get_user_service)
) -> UserResponse:
    user = service.get_user(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return UserResponse.model_validate(user, from_attributes=True)


@protected_router.get("", response_model=List[int])
def list_user_ids(
        service: UserService = Depends(get_user_service)
) -> List[int]:
    return service.list_user_ids()

