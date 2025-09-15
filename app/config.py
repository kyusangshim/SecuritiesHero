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
    AI_MODEL: str
    AI_TEMPERATURE: float
    AI_MAX_TOKENS: int
    LLM_TIMEOUT_SECONDS: int
    
    # --- 🔹 OpenSearch 설정 🔹 ---
    # ngrok HTTPS URL만 사용 (예: https://xxxxx.ngrok.io)
    OPENSEARCH_URI: str  # 전체 URL만 필요
    OPENSEARCH_TIMEOUT_SECONDS: int = 30
 
    # --- 🔹 Kafka 설정 (오류 해결) 🔹 ---
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_CONSUMER_GROUP: str
    KAFKA_REQUEST_TOPIC: str
    KAFKA_RESPONSE_TOPIC: str
    KAFKA_TIMEOUT_SECONDS: int

    # --- 🔹 외부 API 설정 🔹 ---

    MY_API_BASE_URL: str

    # --- 🔹 서버 및 디버그 설정 🔹 ---
    SERVER_HOST: str
    SERVER_PORT: int
    DEBUG: bool
    
    # --- 🔹 로깅 설정 🔹 ---
    LOG_LEVEL: str
    LOG_FILE: str
    
    # --- 🔹 spring 백엔드와 연동 🔹 ---
    MY_API_BASE_URL: str
    
    class Config:
        # .env 파일을 읽어서 환경변수처럼 사용하도록 설정
        env_file = ".env"
        env_file_encoding = "utf-8"

# 설정 객체 생성 (애플리케이션 전체에서 이 객체를 import하여 사용)
settings = Settings()