from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str
    app_name: str = "CargoPeer"
    secret_key: str = secrets.token_urlsafe(32)  # 32+ байт для безопасности


settings = Settings()