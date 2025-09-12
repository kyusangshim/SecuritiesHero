from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    애플리케이션의 모든 설정을 .env 파일에서 불러옵니다.
    pydantic-settings를 사용하여 타입 검사와 기본값 설정을 자동으로 처리합니다.
    """

    # --- 🔹 .env 파일 필수 값 🔹 ---
    # 이 값들은 .env 파일에 반드시 존재해야 합니다.
    OPENROUTER_API_KEY: str
    DART_API_KEY: str

    # --- 🔹 AI 및 LLM 설정 🔹 ---
    AI_MODEL: str = "deepseek/deepseek-chat-v3.1:free"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 1500
    LLM_TIMEOUT_SECONDS: int = 120
    
    # --- 🔹 OpenSearch 설정 🔹 ---
    OPENSEARCH_HOST: str = "localhost"
    OPENSEARCH_PORT: int = 9200
    OPENSEARCH_USER: str = "admin"
    OPENSEARCH_PASSWORD: str = "admin"
    OPENSEARCH_SCHEME: str = "http"
    OPENSEARCH_USE_SSL: bool = False
    OPENSEARCH_TIMEOUT_SECONDS: int = 30
    OS_HOST: str = "http://localhost:9200"
    
    # --- 🔹 Kafka 설정 (오류 해결) 🔹 ---
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_CONSUMER_GROUP: str = "fastapi-equity-group"
    KAFKA_REQUEST_TOPIC: str = "fastapi-equity-request"
    KAFKA_RESPONSE_TOPIC: str = "fastapi-equity-response"
    KAFKA_TIMEOUT_SECONDS: int = 60

    # --- 🔹 외부 API 설정 🔹 ---
    MY_API_BASE_URL: str = "http://localhost:8080"
    
    # --- 🔹 서버 및 디버그 설정 🔹 ---
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = True
    
    # --- 🔹 로깅 설정 🔹 ---
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "fastapi_ai.log"
    
    # --- 🔹 spring 백엔드와 연동 🔹 ---
    MY_API_BASE_URL: str
    
    class Config:
        # .env 파일을 읽어서 환경변수처럼 사용하도록 설정
        env_file = ".env"
        env_file_encoding = "utf-8"

# 설정 객체 생성 (애플리케이션 전체에서 이 객체를 import하여 사용)
settings = Settings()
