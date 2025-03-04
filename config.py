from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    db_url: str
    secret_key: str

    def __init__(self, **data):
        super().__init__(**data)

settings = Settings()
