#C:\Users\user\Documents\FAST_API_LLM\Utility\app\AI\routers\equity_router.py
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
import logging
from typing import Optional

from app.AI.schemas.equity_request import EquityAnnotationRequest
from app.AI.schemas.equity_response import EquityAnnotationResponse, ErrorResponse
from app.AI.services.equity_annotation_service import EquityAnnotationService

logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter(prefix="/api/v1/equity", tags=["equity-annotations"])

# 서비스 의존성
def get_equity_service() -> EquityAnnotationService:
    return EquityAnnotationService()

@router.post("/annotations", response_model=EquityAnnotationResponse)
async def generate_equity_annotations(
    request: EquityAnnotationRequest,
    service: EquityAnnotationService = Depends(get_equity_service)
):
    """
    주식 공모 주석 생성 (RAG 포함)
    
    - OpenSearch에서 유사 사례를 검색하여 RAG 방식으로 주석 생성
    - OpenRouter를 사용하여 전문적인 주식 공모 주석 5개 생성
    """
    try:
        logger.info(f"주식 공모 주석 생성 요청 - 회사: {request.get_corp_name()}")
        
        response = await service.generate_annotations(request)
        
        if response.status == "error":
            logger.warning(f"주석 생성 중 오류 발생: {response.message}")
        
        return response
        
    except Exception as e:
        logger.error(f"주식 공모 주석 생성 API 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"주석 생성 실패: {str(e)}")

@router.post("/annotations/simple", response_model=EquityAnnotationResponse)
async def generate_simple_annotations(
    request: EquityAnnotationRequest,
    service: EquityAnnotationService = Depends(get_equity_service)
):
    """
    간단한 주식 공모 주석 생성 (RAG 없이)
    
    - OpenSearch 검색 없이 기본 템플릿으로만 주석 생성
    - 빠른 응답이 필요한 경우 사용
    """
    try:
        logger.info(f"간단 주석 생성 요청 - 회사: {request.get_corp_name()}")
        
        response = await service.generate_simple_annotations(request)
        
        return response
        
    except Exception as e:
        logger.error(f"간단 주석 생성 API 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"간단 주석 생성 실패: {str(e)}")

@router.get("/health")
async def health_check(service: EquityAnnotationService = Depends(get_equity_service)):
    """
    AI 서비스 상태 확인
    
    - OpenSearch 연결 상태 확인
    - LLM 클라이언트 상태 확인
    """
    try:
        health_status = await service.health_check()
        
        status_code = 200 if health_status["status"] == "healthy" else 503
        
        return JSONResponse(
            status_code=status_code,
            content=health_status
        )
        
    except Exception as e:
        logger.error(f"헬스체크 오류: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "service": "EquityAnnotationService",
                "status": "error", 
                "message": str(e)
            }
        )

@router.get("/test")
async def test_endpoint():
    """
    테스트용 엔드포인트
    """
    return {
        "message": "Equity Annotation Service is running!",
        "service": "EquityAnnotationService",
        "version": "1.0.0"
    }

# Kafka 메시지 처리용 (백그라운드 태스크)
@router.post("/kafka/process")
async def process_kafka_message(
    message: dict,
    background_tasks: BackgroundTasks,
    service: EquityAnnotationService = Depends(get_equity_service)
):
    """
    Kafka 메시지 처리
    
    - 백엔드에서 Kafka를 통해 전송된 요청 처리
    - 비동기로 주석 생성 후 다시 Kafka로 응답 전송
    """
    try:
        logger.info(f"Kafka 메시지 처리 시작: {message}")
        
        # 백엔드 FastApiRequestDto 구조에 맞춰서 처리
        response = await service.process_kafka_request(message)
        
        # 실제 환경에서는 여기서 Kafka로 응답을 다시 전송해야 함
        logger.info(f"Kafka 메시지 처리 완료: requestId={response.requestId}, status={response.status}")
        
        return {"status": "processed", "requestId": response.requestId}
        
    except Exception as e:
        logger.error(f"Kafka 메시지 처리 오류: {str(e)}")
        raise HTTPException(status_code=400, detail=f"메시지 처리 실패: {str(e)}")

async def process_annotation_request(
    service: EquityAnnotationService,
    request: EquityAnnotationRequest, 
    correlation_id: str
):
    """백그라운드에서 주석 생성 처리"""
    try:
        # 주식 생성
        response = await service.generate_annotations(request)
        
        # TODO: Kafka로 응답 전송
        # kafka_producer.send("ai_response_topic", {
        #     "correlation_id": correlation_id,
        #     "data": response.dict()
        # })
        
        logger.info(f"주석 생성 완료 및 응답 전송: {correlation_id}")
        
    except Exception as e:
        logger.error(f"백그라운드 주석 생성 실패: {str(e)}")
        
        # 에러 응답 전송
        error_response = ErrorResponse(
            message=f"주석 생성 실패: {str(e)}",
            error_code="ANNOTATION_GENERATION_FAILED"
        )
        
        # TODO: Kafka로 에러 응답 전송
        # kafka_producer.send("ai_response_topic", {
        #     "correlation_id": correlation_id,
        #     "data": error_response.dict()
        # })