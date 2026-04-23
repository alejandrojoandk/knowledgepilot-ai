from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "KnowledgePilot AI"
    env: str = "dev"
    debug: bool = True

    groq_api_key: str = ""
    model_name: str = "llama-3.1-8b-instant"

    chroma_path: str = "chroma_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()