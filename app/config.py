# settings.py
from typing import Optional, List, Tuple
from pydantic import Field, AliasChoices, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    로컬 .env(네가 주신 키들) 우선, 일부 AWS/배포 키도 겸용 지원
    - .env 상대경로 사용: model_config.env_file = ".env"
    - 대소문자 혼용/키 변형 일부 허용(case_sensitive=False)
    """

    # --- 🔹 필수 키 ---
    OPENROUTER_API_KEY: str
    DART_API_KEY: str

    # --- 🔹 AI / LLM ---
    AI_MODEL: str = "deepseek/deepseek-chat-v3.1:free"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 1600
    LLM_TIMEOUT_SECONDS: int = 120

    # --- 🔹 OpenSearch (로컬 키 + 배포 호환) ---
    OPENSEARCH_HOST: Optional[str] = None
    OPENSEARCH_PORT: Optional[int] = None
    OPENSEARCH_USER: Optional[str] = None
    OPENSEARCH_PASSWORD: Optional[str] = None
    OPENSEARCH_SCHEME: Optional[str] = Field(default=None, validation_alias=AliasChoices("OPENSEARCH_SCHEME", "OS_SCHEME"))
    OPENSEARCH_USE_SSL: bool = False
    OPENSEARCH_TIMEOUT_SECONDS: int = 30

    # 로컬/배포 모두에서 쓰일 수 있는 단일 URL (우선순위: OPENSEARCH_URIS > OPENSEARCH_URI > OS_HOST > HOST:PORT 조립)
    OPENSEARCH_URI: Optional[str] = None         # 로컬 .env에 있음
    OPENSEARCH_URIS: Optional[str] = None        # 배포에서 종종 복수형으로 들어옴
    OS_HOST: Optional[str] = None                # 네 .env에 같이 들어있음

    @computed_field(return_type=str)
    def OPENSEARCH_BASE_URL(self) -> str:
        if self.OPENSEARCH_URIS:
            return self.OPENSEARCH_URIS.rstrip("/")
        if self.OPENSEARCH_URI:
            return self.OPENSEARCH_URI.rstrip("/")
        if self.OS_HOST:
            return self.OS_HOST.rstrip("/")
        if self.OPENSEARCH_HOST and self.OPENSEARCH_PORT:
            scheme = (self.OPENSEARCH_SCHEME or ("https" if self.OPENSEARCH_USE_SSL else "http")).lower()
            return f"{scheme}://{self.OPENSEARCH_HOST}:{self.OPENSEARCH_PORT}"
        return ""

    @computed_field(return_type=Optional[Tuple[str, str]])
    def OPENSEARCH_HTTP_AUTH(self) -> Optional[Tuple[str, str]]:
        if self.OPENSEARCH_USER is not None and self.OPENSEARCH_PASSWORD is not None:
            return (self.OPENSEARCH_USER, self.OPENSEARCH_PASSWORD)
        return None

    # --- 🔹 외부 API ---
    MY_API_BASE_URL: str = "http://localhost:8080"
    MY_API_CORE_REPORTS: Optional[str] = None

    @computed_field(return_type=str)
    def CORE_REPORTS_URL(self) -> str:
        return (self.MY_API_CORE_REPORTS or f"{self.MY_API_BASE_URL.rstrip('/')}/api/reports")

    # --- 🔹 Kafka ---
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_CONSUMER_GROUP: str = "fastapi-equity-group"
    KAFKA_REQUEST_TOPIC: str = "fastapi-equity-request"
    KAFKA_RESPONSE_TOPIC: str = "fastapi-equity-response"
    KAFKA_TIMEOUT_SECONDS: int = 60

    @computed_field(return_type=List[str])
    def KAFKA_BOOTSTRAP_SERVERS_LIST(self) -> List[str]:
        return [s.strip() for s in self.KAFKA_BOOTSTRAP_SERVERS.split(",") if s.strip()]

    # --- 🔹 서버 / 로깅 ---
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "fastapi_ai.log"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,   # FastAPI_URL 같은 대소문자 혼용 대비
        extra="ignore"          # 예기치 않은 추가 키 무시
    )


# 전역 설정 객체
settings = Settings()
