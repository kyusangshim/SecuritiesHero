#C:\Users\user\Documents\FAST_API_LLM\Utility\app\AI\schemas\equity_response.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class EquityAnnotationResponse(BaseModel):
    """주식 공모 주석 생성 응답 - Java 백엔드 DTO와 정확히 매칭"""
    
    # Java EquityAnnotationResponseDto와 동일한 구조
    S4_NOTE1_1: str = Field(..., description="첫 번째 주석 내용")
    S4_NOTE1_2: str = Field(..., description="두 번째 주석 내용") 
    S4_NOTE1_3: str = Field(..., description="세 번째 주석 내용")
    S4_NOTE1_4: str = Field(..., description="네 번째 주석 내용")
    S4_NOTE1_5: str = Field(..., description="다섯 번째 주석 내용")
    
    # 추가 정보 필드들
    processing_status: str = Field(default="COMPLETED", description="처리 상태")
    company_name: Optional[str] = Field(None, description="회사명")
    processing_time_ms: Optional[int] = Field(None, description="처리 시간 (밀리초)")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="처리 시각")
    
    # FastApiResponseDto 호환성을 위한 추가 필드들
    requestId: Optional[str] = Field(None, description="요청 ID")
    status: str = Field(default="success", description="상태")
    message: str = Field(default="주석 생성이 완료되었습니다.", description="메시지")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    @classmethod
    def create_from_annotations(
        cls, 
        annotations: List[str], 
        company_name: str = None,
        request_id: str = None,
        processing_time_ms: int = None
    ):
        """주석 리스트로부터 응답 생성"""
        # 5개로 맞추기 (부족하면 기본값으로 채움)
        padded_annotations = annotations + [""] * (5 - len(annotations))
        
        # 빈 주석은 기본값으로 대체
        final_annotations = [
            annotation or cls._get_default_note(i + 1) 
            for i, annotation in enumerate(padded_annotations[:5])
        ]
        
        return cls(
            S4_NOTE1_1=final_annotations[0],
            S4_NOTE1_2=final_annotations[1],
            S4_NOTE1_3=final_annotations[2],
            S4_NOTE1_4=final_annotations[3],
            S4_NOTE1_5=final_annotations[4],
            company_name=company_name,
            requestId=request_id,
            processing_time_ms=processing_time_ms,
            processing_status="COMPLETED",
            status="success",
            message=f"{len([a for a in annotations if a])}개의 주석이 성공적으로 생성되었습니다."
        )
    
    @classmethod
    def create_error_response(
        cls,
        error_message: str,
        company_name: str = None,
        request_id: str = None
    ):
        """에러 응답 생성 - 백엔드와 동일한 기본값 사용"""
        return cls(
            S4_NOTE1_1=cls._get_default_note(1),
            S4_NOTE1_2=cls._get_default_note(2),
            S4_NOTE1_3=cls._get_default_note(3),
            S4_NOTE1_4=cls._get_default_note(4),
            S4_NOTE1_5=cls._get_default_note(5),
            company_name=company_name,
            requestId=request_id,
            processing_status="FAILED",
            status="error",
            message=f"주석 생성 중 오류 발생: {error_message}. 기본 주석으로 대체되었습니다."
        )
    
    @staticmethod
    def _get_default_note(index: int) -> str:
        """기본 주석 반환 - 백엔드 DTO의 createDefault와 동일"""
        default_notes = {
            1: "모집(매출) 예정가액과 관련된 내용은 「제1부 모집 또는 매출에 관한 사항」- 「Ⅳ. 인수인의 의견(분석기관의 의견)」의 「4. 공모가격에 대한 의견」부분을 참조하시기 바랍니다.",
            2: "모집(매출)가액, 모집(매출)이액, 인수금액 및 인수대가는 발행회사와 대표주관회사가 협의하여 제시하는 공모희망가액 기준입니다.",
            3: "모집(매출)가액의 확정은 청약일 전에 실시하는 수요예측 결과를 반영하여 대표주관회사와 발행회사가 협의하여 최종 결정할 예정입니다.",
            4: "증권의 발행 및 공시 등에 관한 규정에 따라 정정신고서 상의 공모주식수는 증권신고서의 공모할 주식수의 80% 이상 120% 이하로 변경가능합니다.",
            5: "투자 위험 등 자세한 내용은 투자설명서를 참조하시기 바라며, 투자결정시 신중하게 검토하시기 바랍니다."
        }
        return default_notes.get(index, f"주석 {index}에 대한 내용입니다.")


class ErrorResponse(BaseModel):
    """에러 전용 응답 (호환성 유지용)"""
    processing_status: str = Field(default="FAILED", description="처리 상태")
    company_name: Optional[str] = Field(None, description="회사명")
    error_message: str = Field(..., description="에러 메시지")
    error_code: Optional[str] = Field(None, description="에러 코드")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="생성 시간")
    
    # Java 호환성을 위한 필드들
    requestId: Optional[str] = Field(None, description="요청 ID")
    status: str = Field(default="error", description="상태")
    message: Optional[str] = Field(None, description="메시지")
    
    # 기본 주석들로 채우기 (에러 시에도 응답 구조 유지)
    S4_NOTE1_1: str = Field(default=EquityAnnotationResponse._get_default_note(1))
    S4_NOTE1_2: str = Field(default=EquityAnnotationResponse._get_default_note(2))
    S4_NOTE1_3: str = Field(default=EquityAnnotationResponse._get_default_note(3))
    S4_NOTE1_4: str = Field(default=EquityAnnotationResponse._get_default_note(4))
    S4_NOTE1_5: str = Field(default=EquityAnnotationResponse._get_default_note(5))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# FastAPI 응답을 Java FastApiResponseDto로 매핑하는 헬퍼 클래스
class FastApiResponseDto(BaseModel):
    """Java FastApiResponseDto와 정확히 매칭되는 응답 모델"""
    
    requestId: str = Field(..., description="요청 ID")
    status: str = Field(..., description="처리 상태 (success/error)")
    message: str = Field(..., description="처리 메시지")
    companyName: Optional[str] = Field(None, description="회사명")
    processingTimeMs: Optional[int] = Field(None, description="처리 시간")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # 실제 주석 데이터
    S4_NOTE1_1: str
    S4_NOTE1_2: str
    S4_NOTE1_3: str
    S4_NOTE1_4: str
    S4_NOTE1_5: str
    
    # 에러 관련 필드들
    errorMessage: Optional[str] = Field(None, description="에러 메시지")
    errorCode: Optional[str] = Field(None, description="에러 코드")
    
    @classmethod
    def from_equity_response(cls, equity_response: EquityAnnotationResponse):
        """EquityAnnotationResponse를 FastApiResponseDto로 변환"""
        return cls(
            requestId=equity_response.requestId or "",
            status=equity_response.status,
            message=equity_response.message,
            companyName=equity_response.company_name,
            processingTimeMs=equity_response.processing_time_ms,
            timestamp=equity_response.timestamp,
            S4_NOTE1_1=equity_response.S4_NOTE1_1,
            S4_NOTE1_2=equity_response.S4_NOTE1_2,
            S4_NOTE1_3=equity_response.S4_NOTE1_3,
            S4_NOTE1_4=equity_response.S4_NOTE1_4,
            S4_NOTE1_5=equity_response.S4_NOTE1_5,
            errorMessage=None if equity_response.status == "success" else equity_response.message
        )
    
    def is_success(self) -> bool:
        """성공 여부 확인"""
        return self.status == "success"