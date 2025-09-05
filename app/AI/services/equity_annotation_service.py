#C:\Users\user\Documents\FAST_API_LLM\Utility\app\AI\services\equity_annotation_service.py
from typing import List
import logging
from app.AI.models.llm_client import OpenRouterClient
from app.AI.models.prompt_template import EquityPromptTemplate
from app.AI.services.opensearch_service import OpenSearchService
from app.AI.schemas.equity_request import EquityAnnotationRequest
from app.AI.schemas.equity_response import EquityAnnotationResponse, ErrorResponse

logger = logging.getLogger(__name__)

class EquityAnnotationService:
    """주식 공모 주석 생성 서비스"""
    
    def __init__(self):
        self.llm_client = OpenRouterClient()
        self.opensearch_service = OpenSearchService()
        self.prompt_template = EquityPromptTemplate()
    
    async def generate_annotations(self, request: EquityAnnotationRequest) -> EquityAnnotationResponse:
        """주식 공모 주석 생성 (RAG 포함)"""
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
                annotations = await self.llm_client.generate_annotations(prompt)
                logger.info(f"LLM 주석 생성 완료 - {len(annotations)}개")
            except Exception as e:
                logger.error(f"LLM 주석 생성 실패: {str(e)}")
                # LLM 실패시 기본 주석 사용
                annotations = self._get_fallback_annotations(request)
                return self._create_error_response(request, f"LLM 서비스 오류: {str(e)}")
            
            # 4. 응답 구성
            response = EquityAnnotationResponse(
                corp_code=request.get_corp_code(),
                corp_name=request.get_corp_name(),
                annotations=annotations,
                status="success",
                message=f"{len(annotations)}개의 주석이 성공적으로 생성되었습니다."
            )
            
            logger.info(f"주식 공모 주석 생성 완료 - 회사: {request.get_corp_name()}")
            return response
            
        except Exception as e:
            logger.error(f"주석 생성 실패: {str(e)}")
            return self._create_error_response(request, str(e))
    
    async def generate_simple_annotations(self, request: EquityAnnotationRequest) -> EquityAnnotationResponse:
        """간단한 주석 생성 (RAG 없이)"""
        try:
            logger.info(f"간단 주석 생성 시작 - 회사: {request.get_corp_name()}")
            
            # 프롬프트 생성
            prompt = self.prompt_template.generate_prompt(request)
            
            # LLM으로 주석 생성
            try:
                annotations = await self.llm_client.generate_annotations(prompt)
            except Exception as e:
                logger.error(f"LLM 주석 생성 실패: {str(e)}")
                # LLM 실패시 기본 주석 사용
                annotations = self._get_fallback_annotations(request)
                return self._create_error_response(request, f"LLM 서비스 오류: {str(e)}")
            
            # 응답 구성
            response = EquityAnnotationResponse(
                corp_code=request.get_corp_code(),
                corp_name=request.get_corp_name(),
                annotations=annotations,
                status="success",
                message=f"{len(annotations)}개의 주석이 생성되었습니다."
            )
            
            logger.info(f"간단 주석 생성 완료 - 회사: {request.get_corp_name()}")
            return response
            
        except Exception as e:
            logger.error(f"간단 주석 생성 실패: {str(e)}")
            return self._create_error_response(request, str(e))
    
    async def generate_with_examples(self, request: EquityAnnotationRequest) -> EquityAnnotationResponse:
        """예시 기반 주석 생성"""
        try:
            logger.info(f"예시 기반 주석 생성 시작 - 회사: {request.get_corp_name()}")
            
            # 관련 주석 예시 검색
            examples = []
            try:
                summary = request.get_offering_summary()
                keywords = [summary['security_type'], summary['underwriter'], "공모"]
                examples = await self.opensearch_service.search_annotations_examples(keywords)
            except Exception as e:
                logger.warning(f"예시 검색 실패: {str(e)}")
            
            # 프롬프트 생성
            prompt = self.prompt_template.generate_prompt(request, examples)
            
            # LLM으로 주석 생성
            try:
                annotations = await self.llm_client.generate_annotations(prompt)
            except Exception as e:
                logger.error(f"LLM 주석 생성 실패: {str(e)}")
                annotations = self._get_fallback_annotations(request)
                return self._create_error_response(request, f"LLM 서비스 오류: {str(e)}")
            
            # 응답 구성
            response = EquityAnnotationResponse(
                corp_code=request.get_corp_code(),
                corp_name=request.get_corp_name(),
                annotations=annotations,
                status="success",
                message=f"예시를 참고하여 {len(annotations)}개의 주석이 생성되었습니다."
            )
            
            logger.info(f"예시 기반 주석 생성 완료 - 회사: {request.get_corp_name()}")
            return response
            
        except Exception as e:
            logger.error(f"예시 기반 주석 생성 실패: {str(e)}")
            return self._create_error_response(request, str(e))
    
    def _get_fallback_annotations(self, request: EquityAnnotationRequest) -> List[str]:
        """기본 대체 주석"""
        return [
            f"(주1) {request.get_corp_name()}의 공모가격 관련 세부사항은 관련 규정에 따라 확정될 예정입니다.",
            f"(주2) 청약 및 납입 일정은 시장 상황에 따라 변경될 수 있으니 투자 전 확인하시기 바랍니다.",
            f"(주3) {request.underwriter_info.actnmn}이 대표주관회사로서 관련 업무를 수행할 예정입니다."
        ]
    
    def _create_error_response(self, request: EquityAnnotationRequest, error_message: str) -> EquityAnnotationResponse:
        """에러 응답 생성"""
        fallback_annotations = self._get_fallback_annotations(request)
        
        return EquityAnnotationResponse(
            corp_code=request.get_corp_code(),
            corp_name=request.get_corp_name(),
            annotations=fallback_annotations,
            status="error",
            message=f"주석 생성 중 오류 발생: {error_message}. 기본 주석으로 대체되었습니다."
        )
    
    async def health_check(self) -> dict:
        """서비스 상태 확인"""
        try:
            # OpenSearch 연결 확인 - 단순화
            opensearch_status = "ok"
            try:
                # 실제 인덱스 존재 확인으로 변경
                from app.opensearch_client import get_opensearch_client
                client = get_opensearch_client()
                # 간단한 클러스터 정보 확인
                info = client.info()
                if info.get('cluster_name'):
                    opensearch_status = "ok"
                else:
                    opensearch_status = "error"
            except Exception as e:
                opensearch_status = "error"
                logger.error(f"OpenSearch health check failed: {str(e)}")
            
            # LLM 클라이언트 상태 확인 (API 키 유무와 간단한 테스트)
            llm_status = "error"
            try:
                if self.llm_client.api_key and len(self.llm_client.api_key) > 10:
                    # API 키가 있으면 일단 ok
                    llm_status = "ok"
            except Exception as e:
                logger.error(f"LLM client health check failed: {str(e)}")
            
            overall_status = "healthy" if opensearch_status == "ok" and llm_status == "ok" else "unhealthy"
            
            return {
                "service": "EquityAnnotationService",
                "status": overall_status,
                "opensearch": opensearch_status,
                "llm_client": llm_status
            }
            
        except Exception as e:
            logger.error(f"Health check error: {str(e)}")
            return {
                "service": "EquityAnnotationService", 
                "status": "error",
                "message": str(e)
            }