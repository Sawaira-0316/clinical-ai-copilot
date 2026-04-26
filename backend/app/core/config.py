from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Clinical AI Copilot"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./clinical_ai.db"
    ANTHROPIC_API_KEY: str = ""
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "clinical_knowledge_chunks"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
