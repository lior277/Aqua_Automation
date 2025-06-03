import sys
from typing import NoReturn
from requests import RequestException
from client.services.client_service import (
    create_user,
    get_user,
    list_users,
    health_check,
)
from core.exceptions import AuthenticationError, ApiClientError
from core.logger import get_logger

logger = get_logger(__name__)


def handle_error(operation: str, error: Exception) -> NoReturn:
    logger.error("Error during %s: %s", operation, error)
    print(f"Error during {operation}: {error}")
    sys.exit(1)


def run_demo() -> None:
    try:
        hc = health_check()
        print("→ Health:", hc)
    except (AuthenticationError, RequestException, ApiClientError) as e:
        handle_error("health check", e)

    try:
        payload = {
            "israel_id": "123456789",
            "name": "Charlie",
            "phone_number": "+972501234567",
            "address": "123 Main St, Tel Aviv"
        }
        print("Creating user via client...")
        new_user = create_user(**payload)
        print("→ Created user:", new_user)
    except (AuthenticationError, RequestException, ApiClientError) as e:
        handle_error("user creation", e)

    try:
        uid = new_user.get("user_id")
        if not uid:
            raise ApiClientError("No 'user_id' returned")

        fetched = get_user(uid)
        print("→ Fetched user:", fetched)
    except (AuthenticationError, RequestException, ApiClientError) as e:
        handle_error("fetching user", e)

    try:
        ids = list_users()
        print("→ All user IDs:", ids)
    except (AuthenticationError, RequestException, ApiClientError) as e:
        handle_error("listing user IDs", e)


if __name__ == "__main__":
    run_demo()
