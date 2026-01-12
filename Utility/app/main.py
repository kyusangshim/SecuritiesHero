import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 기존 라우터
from .routers import search, financials
# AI 라우터
from app.AI.routers.equity_router import router as equity_router
# Kafka 서비스
from app.AI.kafka.kafka_service import kafka_service
from app.config import settings

# --- 💡 로깅 설정 수정 💡 ---
logging.basicConfig(
    level=settings.LOG_LEVEL,  # config.py에서 로그 레벨 가져오기
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # 파일 핸들러에 UTF-8 인코딩을 명시하여 이모지/한글 깨짐 방지
        logging.FileHandler(settings.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 시작/종료시 실행되는 컨텍스트 매니저"""
    # 시작
    logger.info("🚀 FastAPI 서버 시작 중...")

    try:
        await kafka_service.start()
        logger.info("✅ Kafka 서비스 시작 완료")
    except Exception as e:
        logger.error(f"Kafka 시작 중 오류 발생: {str(e)}")
        # Kafka가 실패하더라도 HTTP API 서버는 계속 실행
        pass

    yield  # 서버 실행 구간

    # 종료
    logger.info("🛑 FastAPI 서버 종료 중...")
    try:
        await kafka_service.stop()
        logger.info("✅ Kafka 서비스 중지 완료")
    except Exception as e:
        logger.error(f"Kafka 종료 중 오류 발생: {str(e)}")

# FastAPI 앱 생성
app = FastAPI(
    title="FastAPI + OpenSearch + AI",
    description="검색 + 재무제표 + AI 주석 서비스",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포 시에는 실제 서비스 도메인으로 제한하는 것이 안전합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(financials.router, prefix="/financials", tags=["Financials"])
app.include_router(equity_router)

@app.get("/")
def root():
    return {
        "message": "FastAPI + OpenSearch + AI 서비스가 실행 중입니다!",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "search": "/search",
            "financials": "/financials",
            "equity_annotations": "/api/v1/equity/annotations",
            "kafka_health": "/kafka/health",
        },
    }

@app.get("/kafka/health")
async def kafka_health_check():
    """Kafka 서비스의 상태를 확인합니다."""
    try:
        health_status = await kafka_service.health_check()
        status_code = 200 if health_status["status"] == "healthy" else 503
        return JSONResponse(status_code=status_code, content=health_status)
    except Exception as e:
        logger.error(f"Kafka 헬스체크 중 오류 발생: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "service": "KafkaService",
                "status": "error",
                "message": str(e),
            },
        )

