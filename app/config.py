from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Colmeia Urbana API"
    secret_key: str = "altere-esta-chave-em-producao"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./data/colmeia.db"
    cors_origins: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"


settings = Settings()
