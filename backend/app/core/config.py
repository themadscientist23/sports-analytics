from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_user: str = "root"
    db_password: str = ""
    db_host: str = "localhost"
    db_port: str = "3306"
    db_name: str = "sportsdb"

    balldontlie_api_key: str | None = None

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"


settings = Settings()

DB_USER = settings.db_user
DB_PASSWORD = settings.db_password
DB_HOST = settings.db_host
DB_PORT = settings.db_port
DB_NAME = settings.db_name

BALLDONTLIE_API_KEY = settings.balldontlie_api_key

CORS_ORIGINS = settings.cors_origins.split(",")
