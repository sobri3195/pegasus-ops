"""Pegasus Ops configuration.
Author: Muhammad Sobri Maulana
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Pegasus Ops"
    app_env: str = "development"
    secret_key: str
    access_token_expire_minutes: int = 120
    database_url: str
    redis_url: str
    allowed_hosts: str = "localhost,127.0.0.1"
    owned_asset_whitelist: str = "localhost"
    rate_limit: str = "100/minute"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
