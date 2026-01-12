#C:\Users\user\Documents\FAST_API_LLM\Utility\app\AI\services\equity_annotation_service.py
import time
from typing import List, Dict, Any
import logging
import json
from app.AI.models.llm_client import OpenRouterClient
from app.AI.models.prompt_template import EquityPromptTemplate
from app.AI.services.opensearch_service import OpenSearchService
from app.AI.schemas.equity_request import EquityAnnotationRequest
from app.AI.schemas.equity_response import EquityAnnotationResponse, ErrorResponse, FastApiResponseDto

logger = logging.getLogger(__name__)

class EquityAnnotationService:
    """주식 공모 주석 생성 서비스 - Java 백엔드와 완전 호환"""
    
    def __init__(self):
        self.llm_client = OpenRouterClient()
        self.opensearch_service = OpenSearchService()
        self.prompt_template = EquityPromptTemplate()
    
    async def process_kafka_request(self, kafka_message: Dict[str, Any]) -> FastApiResponseDto:
        """Kafka 메시지 처리 (Java FastApiRequestDto 형식)"""
        start_time = time.time()
        
        try:
            # Java FastApiRequestDto에서 실제 요청 데이터 추출
            request_id = kafka_message.get("requestId", "")
            company_name = kafka_message.get("companyName", "")
            request_data = kafka_message.get("requestData", {})
            
            logger.info(f"Kafka 메시지 처리 시작 - requestId: {request_id}, company: {company_name}")
            
            # EquityAnnotationRequest 객체 생성
            request = EquityAnnotationRequest(**request_data)
            
            # 실제 주석 생성
            response = await self.generate_annotations(request)
            
            # 처리 시간 계산
            processing_time = int((time.time() - start_time) * 1000)
            response.processing_time_ms = processing_time
            response.requestId = request_id
            
            # Java FastApiResponseDto 형식으로 변환
            return FastApiResponseDto.from_equity_response(response)
                
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            logger.error(f"Kafka 메시지 처리 실패 - requestId: {request_id}, error: {str(e)}")
            
            error_response = EquityAnnotationResponse.create_error_response(
                error_message=str(e),
                company_name=company_name,
                request_id=request_id
            )
            error_response.processing_time_ms = processing_time
            
            return FastApiResponseDto.from_equity_response(error_response)
    
    async def generate_annotations(self, request: EquityAnnotationRequest) -> EquityAnnotationResponse:
        """주식 공모 주석 생성 (RAG 포함)"""
        start_time = time.time()
        
        try:
            logger.info(f"주식 공모 주석 생성 시작 - 회사: {request.get_corp_name()}")
            
            # 1. OpenSearch에서 유사 사례 검색 (RAG) - 오류가 있어도 계속 진행
            rag_content = ""
            try:
                rag_content = await self.opensearch_service.search_similar_cases(request)
                logger.info(f"RAG 검색 완료 - 컨텐츠 길이: {len(rag_content)}")
            except Exception as e:
                logger.warning(f"RAG 검색 실패, 기본 프롬프트 사용: {str(e)}")
            
            # 2. 프롬프트 생성 (RAG 내용 포함)
            if rag_content:
                prompt = self.prompt_template.generate_rag_prompt(request, rag_content)
            else:
                prompt = self.prompt_template.generate_prompt(request)
            
            # 3. LLM으로 주석 생성
            try:
                # LLM 응답을 JSON으로 파싱하여 직접 주석 데이터 추출
                llm_response = await self.llm_client.generate_annotations(prompt)
                
                # JSON 응답 파싱 시도
                annotations_data = self._parse_llm_response(llm_response)
                
                # 처리 시간 계산
                processing_time = int((time.time() - start_time) * 1000)
                
                # EquityAnnotationResponse 직접 생성 
                response = EquityAnnotationResponse(
                    S4_NOTE1_1=annotations_data.get("S4_NOTE1_1", self._get_default_note(1)),
                    S4_NOTE1_2=annotations_data.get("S4_NOTE1_2", self._get_default_note(2)),
                    S4_NOTE1_3=annotations_data.get("S4_NOTE1_3", self._get_default_note(3)),
                    S4_NOTE1_4=annotations_data.get("S4_NOTE1_4", self._get_default_note(4)),
                    S4_NOTE1_5=annotations_data.get("S4_NOTE1_5", self._get_default_note(5)),
                    company_name=request.get_corp_name(),
                    processing_time_ms=processing_time,
                    processing_status="COMPLETED",
                    status="success",
                    message="5개의 주석이 성공적으로 생성되었습니다."
                )
                
                logger.info(f"주식 공모 주석 생성 완료 - 회사: {request.get_corp_name()}")
                return response
                
            except Exception as e:
                logger.error(f"LLM 주석 생성 실패: {str(e)}")
                # LLM 실패시 기본 주석 사용
                return self._create_error_response(request, f"LLM 서비스 오류: {str(e)}")
            
        except Exception as e:
            logger.error(f"주석 생성 실패: {str(e)}")
            return self._create_error_response(request, str(e))
    
    def _parse_llm_response(self, llm_response: str | List[str]) -> Dict[str, str]:
        """LLM 응답을 파싱하여 주석 데이터 추출"""
        try:
            # 문자열 응답인 경우 JSON 파싱 시도
            if isinstance(llm_response, str):
                # JSON 파싱 시도
                try:
                    parsed = json.loads(llm_response)
                    if isinstance(parsed, dict) and "S4_NOTE1_1" in parsed:
                        return parsed
                except json.JSONDecodeError:
                    pass
                
                # JSON이 아니면 텍스트에서 주석 추출
                annotations = self._extract_annotations_from_text(llm_response)
                return self._convert_annotations_to_dict(annotations)
            
            # 리스트 응답인 경우
            elif isinstance(llm_response, list):
                return self._convert_annotations_to_dict(llm_response)
            
            else:
                logger.warning("알 수 없는 LLM 응답 형식")
                return {}
                
        except Exception as e:
            logger.error(f"LLM 응답 파싱 실패: {str(e)}")
            return {}
    
    def _extract_annotations_from_text(self, text: str) -> List[str]:
        """텍스트에서 주석 추출"""
        annotations = []
        lines = text.split('\n')
        current_annotation = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('(주') and ')' in line:
                if current_annotation:
                    annotations.append(current_annotation.strip())
                current_annotation = line
            elif current_annotation and line and not line.startswith('(주'):
                current_annotation += " " + line
        
        # 마지막 주석 추가
        if current_annotation:
            annotations.append(current_annotation.strip())
        
        return annotations
    
    def _convert_annotations_to_dict(self, annotations: List[str]) -> Dict[str, str]:
        """주석 리스트를 딕셔너리로 변환"""
        result = {}
        for i in range(5):
            if i < len(annotations) and annotations[i]:
                result[f"S4_NOTE1_{i+1}"] = annotations[i]
            else:
                result[f"S4_NOTE1_{i+1}"] = self._get_default_note(i+1)
        return result
    
    async def generate_simple_annotations(self, request: EquityAnnotationRequest) -> EquityAnnotationResponse:
        """간단한 주석 생성 (RAG 없이)"""
        try:
            logger.info(f"간단 주석 생성 시작 - 회사: {request.get_corp_name()}")
            
            # 프롬프트 생성
            prompt = self.prompt_template.generate_prompt(request)
            
            # LLM으로 주석 생성
            try:
                llm_response = await self.llm_client.generate_annotations(prompt)
                annotations_data = self._parse_llm_response(llm_response)
                
                response = EquityAnnotationResponse(
                    S4_NOTE1_1=annotations_data.get("S4_NOTE1_1", self._get_default_note(1)),
                    S4_NOTE1_2=annotations_data.get("S4_NOTE1_2", self._get_default_note(2)),
                    S4_NOTE1_3=annotations_data.get("S4_NOTE1_3", self._get_default_note(3)),
                    S4_NOTE1_4=annotations_data.get("S4_NOTE1_4", self._get_default_note(4)),
                    S4_NOTE1_5=annotations_data.get("S4_NOTE1_5", self._get_default_note(5)),
                    company_name=request.get_corp_name(),
                    processing_status="COMPLETED",
                    status="success",
                    message="5개의 주석이 생성되었습니다."
                )
                
                logger.info(f"간단 주석 생성 완료 - 회사: {request.get_corp_name()}")
                return response
                
            except Exception as e:
                logger.error(f"LLM 주석 생성 실패: {str(e)}")
                return self._create_error_response(request, f"LLM 서비스 오류: {str(e)}")
            
        except Exception as e:
            logger.error(f"간단 주석 생성 실패: {str(e)}")
            return self._create_error_response(request, str(e))
    
    def _get_default_note(self, index: int) -> str:
        """기본 주석 반환 - 백엔드와 정확히 동일"""
        return EquityAnnotationResponse._get_default_note(index)
    
    def _create_error_response(self, request: EquityAnnotationRequest, error_message: str) -> EquityAnnotationResponse:
        """에러 응답 생성"""
        return EquityAnnotationResponse.create_error_response(
            error_message=error_message,
            company_name=request.get_corp_name()
        )
    
    async def health_check(self) -> dict:
        """서비스 상태 확인"""
        try:
            # OpenSearch 연결 확인
            opensearch_status = "ok" if self.opensearch_service.is_healthy() else "error"
            
            # LLM 클라이언트 상태 확인
            llm_status = "ok" if self.llm_client.is_healthy() else "error"
            
            overall_status = "healthy" if opensearch_status == "ok" and llm_status == "ok" else "unhealthy"
            
            return {
                "service": "EquityAnnotationService",
                "status": overall_status,
                "opensearch": opensearch_status,
                "llm_client": llm_status,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Health check error: {str(e)}")
            return {
                "service": "EquityAnnotationService", 
                "status": "error",
                "message": str(e),
                "timestamp": time.time()
            }