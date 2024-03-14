import asyncio
from pathlib import Path
from typing import Annotated

from pydantic import HttpUrl, PostgresDsn, SecretStr, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

BASEDIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = BASEDIR / "task_board"


class Settings(BaseSettings):
    # App
    APP_TITLE: str = "Async architecture authentication service"
    APP_DESCRIPTION: str = "Default description"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Auth
    PUBLIC_KEY: SecretStr
    # PRIVATE_KEY: SecretStr
    ALGORITHM: str = "RS256"
    # ACCESS_TOKEN_EXPIRE_TIME_SECONDS: int = 60 * 300

    # Postgres
    TASK_BOARD_DB_HOST: str
    TASK_BOARD_DB_USER: str
    TASK_BOARD_DB_PASSWORD: SecretStr
    TASK_BOARD_DB_NAME: str
    TASK_BOARD_DB_PORT: int
    TASK_BOARD_DB_DSN: PostgresDsn | str = ""

    # Postgres logs
    SQL_LOGS: bool = False
    SQL_POOL_LOGS: bool = False

    AUTH_API: HttpUrl = "http://127.0.0.1:8000/api/"
    KAFKA_BOOTSTRAP_SERVERS: str = "127.0.0.1:29092"

    model_config = SettingsConfigDict(env_file=APP_DIR / ".env")

    @field_validator("TASK_BOARD_DB_DSN")
    def build_postgres_dsn(
        cls, value: PostgresDsn | None, info: ValidationInfo
    ) -> Annotated[str, PostgresDsn]:
        if not value:
            value = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=info.data["TASK_BOARD_DB_USER"],
                password=info.data["TASK_BOARD_DB_PASSWORD"].get_secret_value(),
                host=info.data["TASK_BOARD_DB_HOST"],
                port=info.data["TASK_BOARD_DB_PORT"],
                path=f"{info.data['TASK_BOARD_DB_NAME'] or ''}",
            )
        return str(value)


app_settings = Settings()
