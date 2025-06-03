from typing import List, Optional
from api.models.user_model import User
from api.schemas.user_schema import UserCreate
from core.exceptions import UserAlreadyExistsError
from core.logger import get_logger

logger = get_logger(__name__)


class UserService:

    def __init__(self):
        self._db: dict[int, User] = {}
        self._israeli_id_index: dict[str, int] = {}
        self._id_counter: int = 1

    def create_user(self, data: UserCreate) -> User:

        if data.israel_id in self._israeli_id_index:
            existing_user_id = self._israeli_id_index[data.israel_id]
            logger.warning(
                "Duplicate Israeli ID: %s (user_id: %d)",
                data.israel_id, existing_user_id
            )
            raise UserAlreadyExistsError(data.israel_id)

        user = User(
            user_id=self._id_counter,
            **data.model_dump()
        )
        self._id_counter += 1

        self._db[user.user_id] = user
        self._israeli_id_index[user.israel_id] = user.user_id
        logger.info("Created User: %s", user.__dict__)

        return user

    def get_user(self, user_id: int) -> Optional[User]:
        user = self._db.get(user_id)
        if user:
            logger.info("Retrieved User %d: %s", user_id, user.__dict__)
        else:
            logger.warning("User %d not found", user_id)
        return user

    def get_user_by_israeli_id(self, israeli_id: str) -> Optional[User]:
        user_id = self._israeli_id_index.get(israeli_id)
        if user_id:
            return self.get_user(user_id)
        return None

    def list_users(self) -> List[User]:
        users = list(self._db.values())
        logger.info("Listing all users: %s", [u.user_id for u in users])
        return users

    def list_user_ids(self) -> List[int]:
        return [user.user_id for user in self._db.values()]

    def clear_all(self) -> None:
        self._db.clear()
        self._israeli_id_index.clear()
        self._id_counter = 1
        logger.info("Cleared all user data")


# Dependency injection setup
# For in-memory storage, we need a shared instance
# In production, this should be replaced with a proper database
_user_service_instance = UserService()


def get_user_service() -> UserService:
    return _user_service_instance
