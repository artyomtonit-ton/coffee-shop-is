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
        default="postgresql://postgres:postgres@localhost:5432/coffee_shop_db",
        validation_alias="DATABASE_URL",
    )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
