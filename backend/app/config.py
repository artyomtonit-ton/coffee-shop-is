from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = Field(
        default="Coffee Shop Information System",
        validation_alias="APP_NAME",
    )
    app_version: str = Field(default="0.1.0", validation_alias="APP_VERSION")
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    database_url: str = Field(
        default="postgresql://postgres:postgres@127.0.0.1:5433/coffee_shop_db",
        validation_alias="DATABASE_URL",
    )
    database_echo: bool = Field(default=False, validation_alias="DATABASE_ECHO")
    secret_key: str = Field(
        default="change_this_secret_key",
        validation_alias="SECRET_KEY",
    )
    algorithm: str = Field(default="HS256", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
