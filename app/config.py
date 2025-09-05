from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    OPENSEARCH_HOST: str = "localhost"
    OPENSEARCH_PORT: int = 9200
    OPENSEARCH_USER: str = "admin"
    OPENSEARCH_PASSWORD: str = "admin"
    OPENSEARCH_SCHEME: str = "http"

    OS_HOST: str = "http://localhost:9200"
    MY_API_BASE_URL: str = "http://localhost:8080"
    MY_API_CORE_REPORTS: str = "http://localhost:8080/api/reports"
    DART_API_KEY: str = "default_key"

    # AI 관련 설정
    OPENROUTER_API_KEY: Optional[str] = None
    AI_MODEL: str = "anthropic/claude-3.5-sonnet"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 1500

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
