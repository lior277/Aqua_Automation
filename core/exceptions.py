from fastapi import HTTPException


class UserError(HTTPException):
    pass


class UserAlreadyExistsError(UserError):
    def __init__(self, israel_id: str):
        super().__init__(
            status_code=409,
            detail=f"User with Israeli ID {israel_id} already exists"
        )


class UserNotFoundError(UserError):
    def __init__(self, user_id: int = None, detail: str = None):
        message = detail or (f"User {user_id} not found" if user_id else "User not found")
        super().__init__(status_code=404, detail=message)


class ApiClientError(Exception):
    pass


class AuthenticationError(Exception):
    pass
