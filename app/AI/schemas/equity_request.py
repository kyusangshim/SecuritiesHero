#C:\Users\user\Documents\FastAPI2\Utility\app\AI\schemas\equity_request.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EquityAnnotationRequest(BaseModel):
    """주식 공모 주석 생성 요청 - 백엔드 DTO와 정확히 매칭"""
    
    # 회사 기본 정보
    company_name: str = Field(..., description="회사명")
    ceo_name: Optional[str] = Field(None, description="대표이사명")
    address: Optional[str] = Field(None, description="주소")
    establishment_date: Optional[str] = Field(None, description="설립일")
    company_phone: Optional[str] = Field(None, description="회사 전화번호")
    company_website: Optional[str] = Field(None, description="회사 웹사이트")
    
    # 증권의 종류 (S4_11A)
    S4_11A_1: Optional[str] = Field(None, description="증권의 종류")
    S4_11A_2: Optional[str] = Field(None, description="주식수")
    S4_11A_3: Optional[str] = Field(None, description="액면가")
    S4_11A_4: Optional[str] = Field(None, description="공모가격대")
    S4_11A_5: Optional[str] = Field(None, description="공모총액")
    S4_11A_6: Optional[str] = Field(None, description="공모방법")
    
    # 인수인 관련 (S4_11B)
    S4_11B_1: Optional[str] = Field(None, description="인수 방식")
    S4_11B_2: Optional[str] = Field(None, description="인수회사명")
    S4_11B_3: Optional[str] = Field(None, description="인수증권")
    S4_11B_4: Optional[str] = Field(None, description="인수주식수")
    S4_11B_5: Optional[str] = Field(None, description="인수금액")
    S4_11B_6: Optional[str] = Field(None, description="인수가격")
    S4_11B_7: Optional[str] = Field(None, description="인수방법")
    
    # 청약 일정 (S4_11C)
    S4_11C_1: Optional[str] = Field(None, description="청약근거")
    S4_11C_2: Optional[str] = Field(None, description="납입일")
    S4_11C_3: Optional[str] = Field(None, description="청약기간")
    S4_11C_4: Optional[str] = Field(None, description="배정일")
    S4_11C_5: Optional[str] = Field(None, description="상장예정일")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def get_corp_name(self) -> str:
        """회사명 반환"""
        return self.company_name
    
    def get_offering_summary(self) -> dict:
        """공모 요약 정보 반환"""
        return {
            "security_type": self.S4_11A_1 or "",
            "security_count": self.S4_11A_2 or "",
            "face_value": self.S4_11A_3 or "",
            "offering_price": self.S4_11A_4 or "",
            "total_amount": self.S4_11A_5 or "",
            "offering_method": self.S4_11A_6 or "",
            "underwriter": self.S4_11B_2 or "",
            "subscription_date": self.S4_11C_3 or "",
            "payment_date": self.S4_11C_2 or "",
            "underwriter_type": self.S4_11B_1 or "",
            "underwriter_securities": self.S4_11B_3 or "",
            "underwriter_count": self.S4_11B_4 or "",
            "underwriter_amount": self.S4_11B_5 or "",
            "underwriter_price": self.S4_11B_6 or "",
            "underwriter_method": self.S4_11B_7 or "",
            "subscription_basis": self.S4_11C_1 or "",
            "allocation_date": self.S4_11C_4 or "",
            "listing_date": self.S4_11C_5 or ""
        }
    
    def get_company_info(self) -> dict:
        """회사 기본 정보 반환"""
        return {
            "name": self.company_name,
            "ceo": self.ceo_name,
            "address": self.address,
            "establishment_date": self.establishment_date,
            "phone": self.company_phone,
            "website": self.company_website
        }
    
    def get_securities_info(self) -> dict:
        """증권 정보 반환"""
        return {
            "type": self.S4_11A_1,
            "count": self.S4_11A_2,
            "face_value": self.S4_11A_3,
            "price_range": self.S4_11A_4,
            "total_amount": self.S4_11A_5,
            "method": self.S4_11A_6
        }
    
    def get_underwriter_info(self) -> dict:
        """인수인 정보 반환"""
        return {
            "type": self.S4_11B_1,
            "name": self.S4_11B_2,
            "securities": self.S4_11B_3,
            "count": self.S4_11B_4,
            "amount": self.S4_11B_5,
            "price": self.S4_11B_6,
            "method": self.S4_11B_7
        }
    
    def get_schedule_info(self) -> dict:
        """청약 일정 정보 반환"""
        return {
            "basis": self.S4_11C_1,
            "payment_date": self.S4_11C_2,
            "subscription_period": self.S4_11C_3,
            "allocation_date": self.S4_11C_4,
            "listing_date": self.S4_11C_5
        }