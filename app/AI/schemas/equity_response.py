#C:\Users\user\Documents\FAST_API_LLM\Utility\app\AI\schemas\equity_response.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EquityAnnotationResponse(BaseModel):
    """주식 공모 주석 생성 응답"""
    corp_code: str = Field(..., description="회사 고유번호")
    corp_name: str = Field(..., description="회사명")
    annotations: List[str] = Field(..., min_items=3, max_items=3, description="생성된 주석 3개")
    status: str = Field(..., description="처리 상태 (success/error)")
    message: Optional[str] = Field(None, description="처리 메시지")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ErrorResponse(BaseModel):
    """에러 응답"""
    status: str = Field(default="error", description="에러 상태")
    message: str = Field(..., description="에러 메시지")
    error_code: Optional[str] = Field(None, description="에러 코드")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }