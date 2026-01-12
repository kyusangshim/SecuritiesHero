from typing import Dict, List
from app.AI.schemas.equity_request import EquityAnnotationRequest


class EquityPromptTemplate:
    """주식 공모 주석 생성용 프롬프트 템플릿"""
    
    @classmethod
    def _format_amount(cls, amount_str: str) -> str:
        """숫자 문자열을 천단위 구분자로 포맷"""
        try:
            if not amount_str:
                return ""
            # 쉼표 제거 후 숫자만 추출
            import re
            numbers = re.findall(r'\d+', amount_str.replace(',', ''))
            if numbers:
                return f"{int(numbers[0]):,}"
            return amount_str
        except:
            return amount_str
    
    @classmethod
    def _extract_price_info(cls, price_str: str) -> dict:
        """가격 정보에서 최저가, 최고가 추출"""
        try:
            if not price_str:
                return {"min_price": "", "max_price": "", "range": ""}
            
            import re
            # 단일 가격인 경우 (예: "15,000")
            if '~' not in price_str and '-' not in price_str:
                price = re.findall(r'[\d,]+', price_str)
                if price:
                    formatted = f"{int(price[0].replace(',', '')):,}원"
                    return {"min_price": formatted, "max_price": formatted, "range": formatted}
            
            # 범위 가격인 경우 (예: "15,000 ~ 18,000")
            prices = re.findall(r'[\d,]+', price_str)
            if len(prices) >= 2:
                min_val = int(prices[0].replace(',', ''))
                max_val = int(prices[1].replace(',', ''))
                return {
                    "min_price": f"{min_val:,}원",
                    "max_price": f"{max_val:,}원", 
                    "range": f"{min_val:,}원 ~ {max_val:,}원"
                }
            
            return {"min_price": "", "max_price": "", "range": price_str}
        except:
            return {"min_price": "", "max_price": "", "range": price_str}
    
    @classmethod
    def generate_prompt(cls, request: EquityAnnotationRequest, similar_cases: List[str] = None) -> str:
        """표준 형식에 맞는 주석 생성용 프롬프트"""
        
        offering_summary = request.get_offering_summary()
        
        # 실제 데이터 값들 추출 및 포맷팅
        company_name = request.company_name or "발행회사"
        security_type = offering_summary['security_type'] or "기명식보통주"
        security_count = cls._format_amount(offering_summary['security_count'])
        face_value = cls._format_amount(offering_summary['face_value'])
        total_amount = cls._format_amount(offering_summary['total_amount'])
        underwriter = offering_summary['underwriter'] or "대표주관회사"
        subscription_period = offering_summary['subscription_date']
        
        # 가격 정보 처리
        price_info = cls._extract_price_info(offering_summary['offering_price'])
        
        prompt = f"""다음 실제 주식 공모 정보를 바탕으로 정확한 주석 5개를 생성해주세요.

## 실제 공모 데이터
- 회사명: {company_name}
- 증권의 종류: {security_type}
- 증권 수량: {security_count}주
- 액면가액: {face_value}원
- 공모가격: {price_info['range']}
- 공모총액: {total_amount}원
- 대표주관회사: {underwriter}
- 청약기간: {subscription_period}

## 표준 주석 예시 (정확히 이런 형식으로 작성)
참고 템플릿:
1. "모집(매출) 예정가액(이하 \"공모희망가액\", \"희망공모가액\"이라 한다.)과 관련된 내용은「제1부 모집 또는 매출에 관한 사항」- 「Ⅳ. 인수인의 의견(분석기관의 의견)」의 「4. 공모가격에 대한 의견」부분을 참조하시기 바랍니다."

2. "모집(매출)가액, 모집(매출)총액, 인수금액 및 인수대가는 발행회사와 대표주관회사가 협의하여 제시하는 공모희망가액인 [가격범위] 중 최저가액인 [최저가] 기준입니다."

3. "모집(매출)가액의 확정(이하 \"확정공모가액\"이라 한다)은 청약일 전에 실시하는 수요예측 결과를 반영하여 대표주관회사인 [주관회사명]과 발행회사인 [회사명]가 협의하여 1주당 확정공모가액을 최종 결정할 예정이며, 모집(매출)가액 확정 시 정정신고서를 제출할 예정입니다."

4. "「증권의 발행 및 공시 등에 관한 규정」 제2-3조제2항제1호에 따라 정정신고서 상의 공모주식수는 금번 제출하는 증권신고서의 공모할 주식수의 100분의 80 이상과 100분의 120 이하에 해당하는 주식수로 변경가능합니다."

5. "청약일 관련 일정 또는 투자 위험에 관한 안내사항"

## 생성 지침
1. 위 실제 데이터의 정확한 수치를 반드시 사용하세요
2. 표준 증권신고서 문구를 따라 전문적으로 작성하세요  
3. 금액은 천단위 구분자(쉼표)를 포함하여 정확히 표기하세요
4. 회사명과 주관회사명을 정확히 사용하세요

## 응답 형식 (JSON만 반환, 다른 텍스트 없이)
{{
    "S4_NOTE1_1": "공모가격 관련 표준 문구",
    "S4_NOTE1_2": "공모가액 산정 기준 (실제 데이터 사용)",
    "S4_NOTE1_3": "가액 확정 절차 (실제 회사명/주관사명 사용)",
    "S4_NOTE1_4": "관련 규정 표준 문구",
    "S4_NOTE1_5": "청약 일정 또는 투자자 유의사항"
}}

중요: 
- 실제 제공된 수치만 사용하고 임의의 값을 만들지 마세요
- 표준 증권신고서 문구 형식을 정확히 따라주세요
- JSON 형식을 정확히 지켜주세요"""
        
        return prompt
    
    @classmethod 
    def generate_rag_prompt(cls, request: EquityAnnotationRequest, rag_content: str) -> str:
        """RAG 검색 결과를 포함한 개선된 프롬프트"""
        
        offering_summary = request.get_offering_summary()
        
        # 실제 데이터 값들 추출 및 포맷팅
        company_name = request.company_name or "발행회사"
        security_count = cls._format_amount(offering_summary['security_count'])
        face_value = cls._format_amount(offering_summary['face_value'])
        total_amount = cls._format_amount(offering_summary['total_amount'])
        underwriter = offering_summary['underwriter'] or "대표주관회사"
        subscription_period = offering_summary['subscription_date']
        
        # 가격 정보 처리
        price_info = cls._extract_price_info(offering_summary['offering_price'])
        
        prompt = f"""다음 실제 공모 정보와 검색된 관련 자료를 바탕으로 정확한 주석 5개를 생성해주세요.

## 현재 실제 공모 정보
- 회사명: {company_name}
- 증권의 종류: {offering_summary['security_type']}
- 증권 수량: {security_count}주
- 액면가액: {face_value}원
- 공모가격: {price_info['range']}
- 공모총액: {total_amount}원
- 대표주관회사: {underwriter}
- 청약기간: {subscription_period}

## 검색된 참고 자료
{rag_content}

## 표준 주석 생성 가이드라인
다음 5개 주제로 표준 증권신고서 형식에 맞는 주석을 생성하세요:

1. **공모가격 관련 참조 안내** (표준 문구)
   - "모집(매출) 예정가액과 관련된 내용은「제1부 모집 또는 매출에 관한 사항」참조" 형식

2. **공모가액 산정 기준** (실제 데이터 사용)
   - 실제 가격 범위와 최저가 기준 명시
   - "발행회사와 대표주관회사가 협의하여 제시하는..." 형식

3. **가액 확정 절차** (실제 회사명 사용)
   - 수요예측 후 확정 절차 설명
   - 실제 주관회사명과 발행회사명 사용

4. **관련 규정** (표준 문구)
   - 증권의 발행 및 공시 등에 관한 규정 인용
   - 공모주식수 변경 가능 범위 (80%-120%) 명시

5. **청약 일정 및 투자자 유의사항**
   - 실제 청약 기간 정보 활용
   - 투자 위험 또는 상장 관련 안내

## 응답 형식 (JSON만 반환)
{{
    "S4_NOTE1_1": "표준 참조 안내 문구",
    "S4_NOTE1_2": "실제 데이터를 반영한 가액 산정 기준",
    "S4_NOTE1_3": "실제 회사명이 포함된 확정 절차",
    "S4_NOTE1_4": "표준 규정 문구",
    "S4_NOTE1_5": "청약 일정 및 투자자 안내"
}}

주의사항:
- 반드시 실제 제공된 수치와 회사명만 사용
- 표준 증권신고서 문체와 용어 준수
- 정확한 JSON 형식 유지
- 검색 자료의 유용한 정보 적극 활용"""
        
        return prompt
    
    @classmethod
    def generate_simple_prompt(cls, request: EquityAnnotationRequest) -> str:
        """간단한 프롬프트 생성 (실제 데이터 기반)"""
        
        offering_summary = request.get_offering_summary()
        
        return f"""주식공모 주석 5개를 표준 증권신고서 형식으로 생성해주세요.

## 실제 공모 정보
- 회사: {request.company_name}
- 증권종류: {offering_summary['security_type']}
- 공모주식수: {cls._format_amount(offering_summary['security_count'])}주
- 공모가격: {offering_summary['offering_price']}
- 공모총액: {cls._format_amount(offering_summary['total_amount'])}원
- 주관회사: {offering_summary['underwriter']}
- 청약기간: {offering_summary['subscription_date']}

위 실제 데이터를 정확히 반영한 전문적인 주석을 JSON 형식으로 생성해주세요.

{{
    "S4_NOTE1_1": "공모가격 관련",
    "S4_NOTE1_2": "가액 산정 기준", 
    "S4_NOTE1_3": "확정 절차",
    "S4_NOTE1_4": "관련 규정",
    "S4_NOTE1_5": "청약 일정 및 안내"
}}"""