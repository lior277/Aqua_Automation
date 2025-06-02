import sys
from requests import RequestException

from client.services.client_service import (
    create_user,
    get_user,
    list_users,
    health_check,
    AuthenticationError,
)


def run_demo() -> None:
    try:
        hc = health_check()
        print("→ Health:", hc)
    except (AuthenticationError, RequestException) as e:
        print("Error during health check:", e)
        sys.exit(1)

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
    except (AuthenticationError, RequestException) as e:
        print("Error during user creation:", e)
        sys.exit(1)

    try:
        uid = new_user.get("user_id")
        if not uid:
            print("No 'user_id' returned; aborting fetch.")
            sys.exit(1)

        fetched = get_user(uid)
        print("→ Fetched user:", fetched)
    except (AuthenticationError, RequestException) as e:
        print("Error during fetching user:", e)
        sys.exit(1)

    try:
        ids = list_users()
        print("→ All user IDs:", ids)
    except (AuthenticationError, RequestException) as e:
        print("Error during listing user IDs:", e)
        sys.exit(1)


if __name__ == "__main__":
    run_demo()
