#Utility\app\AI\schemas\equity_request.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EquityGeneralInfo(BaseModel):
    """일반사항 정보"""
    rcept_no: str = Field(..., description="접수번호")
    corp_cls: str = Field(..., description="법인구분 (Y:유가, K:코스닥, N:코넥스, E:기타)")
    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    sbd: Optional[str] = Field(None, description="청약기일")
    pymd: Optional[str] = Field(None, description="납입기일") 
    sband: Optional[str] = Field(None, description="청약공고일")
    asand: Optional[str] = Field(None, description="배정공고일")
    asstd: Optional[str] = Field(None, description="배정기준일")

class EquitySecurityType(BaseModel):
    """증권의 종류 정보"""
    rcept_no: str = Field(..., description="접수번호")
    corp_code: str = Field(..., description="고유번호")
    corp_name: str = Field(..., description="회사명")
    stksen: str = Field(..., description="증권의종류")
    stkcnt: int = Field(..., description="증권수량")
    fv: int = Field(..., description="액면가액")
    slprc: int = Field(..., description="모집(매출)가액")
    slta: int = Field(..., description="모집(매출)총액")
    slmthn: str = Field(..., description="모집(매출)방법")

class EquityUnderwriterInfo(BaseModel):
    """인수인 정보"""
    rcept_no: str = Field(..., description="접수번호")
    corp_code: str = Field(..., description="고유번호") 
    corp_name: str = Field(..., description="회사명")
    actsen: str = Field(..., description="인수인구분")
    actnmn: str = Field(..., description="인수인명")
    stksen: str = Field(..., description="증권의종류")
    udtcnt: int = Field(..., description="인수수량")
    udtamt: int = Field(..., description="인수금액")
    udtprc: int = Field(..., description="인수대가")
    udtmth: str = Field(..., description="인수방법")

class EquityAnnotationRequest(BaseModel):
    """주식 공모 주석 생성 요청"""
    general_info: EquityGeneralInfo = Field(..., description="일반사항 정보")
    security_type: EquitySecurityType = Field(..., description="증권의 종류 정보")
    underwriter_info: EquityUnderwriterInfo = Field(..., description="인수인 정보")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def get_corp_code(self) -> str:
        """공통 회사 코드 반환"""
        return self.general_info.corp_code
    
    def get_corp_name(self) -> str:
        """회사명 반환"""
        return self.general_info.corp_name
    
    def get_offering_summary(self) -> dict:
        """공모 요약 정보 반환"""
        return {
            "security_type": self.security_type.stksen,
            "security_count": self.security_type.stkcnt,
            "face_value": self.security_type.fv,
            "offering_price": self.security_type.slprc,
            "total_amount": self.security_type.slta,
            "offering_method": self.security_type.slmthn,
            "underwriter": self.underwriter_info.actnmn,
            "subscription_date": self.general_info.sbd,
            "payment_date": self.general_info.pymd
        }