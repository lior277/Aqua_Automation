from typing import List, Optional
from fastapi import HTTPException

from core.logger import get_logger
from api.models.user_model import User
from api.schemas.user_schema import UserCreate

logger = get_logger(__name__)

class UserService:
    fake_db: dict[int, User] = {}
    israeli_id_index: dict[str, int] = {}
    id_counter: int = 1

    @classmethod
    def create_user(cls, data: UserCreate) -> User:
        if data.israel_id in cls.israeli_id_index:
            existing_user_id = cls.israeli_id_index[data.israel_id]
            logger.warning(
                "Attempted to create duplicate Israeli ID: %s (existing user_id: %d)",
                data.israel_id, existing_user_id
            )
            raise HTTPException(
                status_code=409,
                detail=f"User with Israeli ID {data.israel_id} already exists"
            )

        new_user = User(
            user_id=cls.id_counter,
            israel_id=data.israel_id,
            name=data.name,
            phone_number=data.phone_number,
            address=data.address
        )

        cls.fake_db[cls.id_counter] = new_user
        cls.israeli_id_index[data.israel_id] = cls.id_counter

        logger.info("Created User: %s", new_user.__dict__)
        cls.id_counter += 1
        return new_user

    @classmethod
    def get_user(cls, user_id: int) -> Optional[User]:
        user = cls.fake_db.get(user_id)
        if user:
            logger.info("Retrieved User %d: %s", user_id, user.__dict__)
        else:
            logger.warning("User %d not found", user_id)
        return user

    @classmethod
    def get_user_by_israeli_id(cls, israeli_id: str) -> Optional[User]:
        user_id = cls.israeli_id_index.get(israeli_id)
        if user_id:
            return cls.get_user(user_id)
        return None

    @classmethod
    def list_users(cls) -> List[User]:
        users = list(cls.fake_db.values())
        logger.info("Listing all users: %s", [u.user_id for u in users])
        return users

    @classmethod
    def clear_all(cls):
        cls.fake_db.clear()
        cls.israeli_id_index.clear()
        cls.id_counter = 1
        logger.info("Cleared all user data")
