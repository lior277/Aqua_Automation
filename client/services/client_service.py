import requests
from requests.auth import HTTPBasicAuth
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)
BASE_URL = settings.server_url
AUTH = HTTPBasicAuth(settings.basic_username, settings.basic_password)

AUTH_ERROR_MSG = "Authentication required"
AUTH_FAILED_MSG = "Authentication failed"


class AuthenticationError(Exception):
    pass


REQUEST_TIMEOUT = 5.0


def create_user(israel_id: str, name: str, phone_number: str, address: str) -> dict:
    user_data = {
        "israel_id": israel_id,
        "name": name,
        "phone_number": phone_number,
        "address": address
    }
    logger.info("POST %s/users → Payload: %s", BASE_URL, user_data)
    try:
        res = requests.post(
            f"{BASE_URL}/users",
            json=user_data,
            auth=AUTH,
            timeout=REQUEST_TIMEOUT
        )
    except requests.RequestException as e:
        logger.error("Request to create_user failed: %s", e)
        raise

    if res.status_code == 401:
        logger.error(AUTH_FAILED_MSG)
        raise AuthenticationError(AUTH_ERROR_MSG)

    res.raise_for_status()
    response_json = res.json()
    logger.info("Response status: %d / Body: %s", res.status_code, response_json)
    return response_json


def get_user(user_id: int) -> dict:
    logger.info("GET %s/users/%d", BASE_URL, user_id)
    try:
        res = requests.get(
            f"{BASE_URL}/users/{user_id}",
            auth=AUTH,
            timeout=REQUEST_TIMEOUT
        )
    except requests.RequestException as e:
        logger.error("Request to get_user failed: %s", e)
        raise

    if res.status_code == 401:
        logger.error(AUTH_FAILED_MSG)
        raise AuthenticationError(AUTH_ERROR_MSG)

    if res.status_code == 404:
        logger.warning("User %d not found (404)", user_id)
        return {"error": "User not found", "status_code": 404}

    res.raise_for_status()
    response_json = res.json()
    logger.info("Response status: %d / Body: %s", res.status_code, response_json)
    return response_json


def list_users() -> list[int]:
    logger.info("GET %s/users", BASE_URL)
    try:
        res = requests.get(
            f"{BASE_URL}/users",
            auth=AUTH,
            timeout=REQUEST_TIMEOUT
        )
    except requests.RequestException as e:
        logger.error("Request to list_users failed: %s", e)
        raise

    if res.status_code == 401:
        logger.error(AUTH_FAILED_MSG)
        raise AuthenticationError(AUTH_ERROR_MSG)

    res.raise_for_status()
    return res.json()


def health_check() -> dict:
    logger.info("GET %s/health", BASE_URL)
    try:
        res = requests.get(
            f"{BASE_URL}/health",
            timeout=REQUEST_TIMEOUT
        )
    except requests.RequestException as e:
        logger.error("Request to health_check failed: %s", e)
        raise

    res.raise_for_status()
    return res.json()
