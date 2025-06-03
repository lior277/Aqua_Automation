from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    basic_username: str
    basic_password: str
    server_url: str = "http://127.0.0.1:8000"

    class Config:
        env_file = ".env"


settings = Settings()