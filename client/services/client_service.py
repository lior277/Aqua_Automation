import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, List, Optional
from core.config import settings
from core.logger import get_logger
from core.exceptions import AuthenticationError, ApiClientError

logger = get_logger(__name__)


class ClientService:

    def __init__(self, base_url: str, auth: Optional[HTTPBasicAuth] = None, timeout: float = 5.0):
        self.base_url = base_url.rstrip('/')
        self.auth = auth
        self.timeout = timeout
        self.session = requests.Session()
        if auth:
            self.session.auth = auth

    @staticmethod
    def _handle_response(response: requests.Response) -> Dict:
        if response.status_code == 401:
            logger.error("Authentication failed")
            raise AuthenticationError("Authentication required")

        if response.status_code == 404:
            logger.warning("Resource not found (404)")
            return {"error": "Resource not found", "status_code": 404}

        response.raise_for_status()
        return response.json()

    def _request(self, method: str, url: str, **kwargs) -> Dict:
        full_url = f"{self.base_url}{url}"
        logger.info("%s %s", method, full_url)

        if method == "POST" and "data" in kwargs:
            logger.info("Payload: %s", kwargs["data"])
            kwargs["json"] = kwargs.pop("data")

        try:
            response = self.session.request(
                method,
                full_url,
                timeout=self.timeout,
                **kwargs
            )
        except requests.RequestException as e:
            logger.error("%s request failed: %s", method, e)
            raise ApiClientError(f"Request failed: {e}") from e

        result = self._handle_response(response)
        logger.info("Response status: %d / Body: %s", response.status_code, result)
        return result

    def get(self, url: str, **kwargs) -> Dict:
        return self._request("GET", url, **kwargs)

    def post(self, url: str, data: Dict, **kwargs) -> Dict:
        return self._request("POST", url, data=data, **kwargs)


class UserApiClient:

    def __init__(self, http_client: ClientService):
        self.http_client = http_client

    def create_user(self, israel_id: str, name: str, phone_number: str, address: str) -> Dict:
        user_data = {
            "israel_id": israel_id,
            "name": name,
            "phone_number": phone_number,
            "address": address
        }
        return self.http_client.post("/users", user_data)

    def get_user(self, user_id: int) -> Dict:
        return self.http_client.get(f"/users/{user_id}")

    def list_users(self) -> List[int]:
        return self.http_client.get("/users")

    def health_check(self) -> Dict:
        return self.http_client.get("/health")


def create_api_client() -> UserApiClient:
    auth = HTTPBasicAuth(settings.basic_username, settings.basic_password)
    http_client = ClientService(
        base_url=settings.server_url,
        auth=auth,
        timeout=5.0
    )
    return UserApiClient(http_client)


def create_user(israel_id: str, name: str, phone_number: str, address: str) -> Dict:
    client = create_api_client()
    return client.create_user(israel_id, name, phone_number, address)


def get_user(user_id: int) -> Dict:
    client = create_api_client()
    return client.get_user(user_id)


def list_users() -> List[int]:
    client = create_api_client()
    return client.list_users()


def health_check() -> Dict:
    client = create_api_client()
    return client.health_check()
