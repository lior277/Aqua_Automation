import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from core.config import settings

security = HTTPBasic()


def verify_credentials(
        credentials: HTTPBasicCredentials = Depends(security)
) -> str:
    correct_username = secrets.compare_digest(
        credentials.username,
        settings.basic_username
    )
    correct_password = secrets.compare_digest(
        credentials.password,
        settings.basic_password
    )

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username