from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    israel_id: str = Field(
        ...,
        pattern=r"^\d{9}$",
        description="9-digit Israeli ID"
    )
    name: str = Field(
        ...,
        min_length=1,
        description="Full name of the user"
    )
    phone_number: str = Field(
        ...,
        pattern=r"^\+\d{7,15}$",
        description="Phone number in international format, e.g. +972501234567"
    )
    address: str = Field(
        ...,
        min_length=1,
        description="User address"
    )


class UserResponse(UserCreate):
    user_id: int = Field(..., description="Unique user ID assigned by the system")
