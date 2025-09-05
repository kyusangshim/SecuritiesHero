#C:\Users\user\Documents\FAST_API_LLM\Utility\app\AI\models\prompt_template.py
from typing import Dict, List
from app.AI.schemas.equity_request import EquityAnnotationRequest


class EquityPromptTemplate:
    """주식 공모 주석 생성용 프롬프트 템플릿"""
    
    # 학습용 예시 주석들
    SAMPLE_ANNOTATIONS = """
참고 예시:

(주1) 모집(매출) 예정가액(이하 "공모희망가액", "희망공모가액"이라 한다.)과 관련된 내용은「제1부 모집 또는 매출에 관한 사항」- 「Ⅳ. 인수인의 의견(분석기관의 의견)」의 「4. 공모가격에 대한 의견」부분을 참조하시기 바랍니다.

(주2) 모집(매출)가액, 모집(매출)총액, 인수금액 및 인수대가는 발행회사와 대표주관회사가 협의하여 제시하는 공모희망가액인 15,000원 ~ 18,000원 중 최저가액인 15,000원 기준입니다.

(주3) 모집(매출)가액의 확정(이하 "확정공모가액"이라 한다)은 청약일 전에 실시하는 수요예측 결과를 반영하여 대표주관회사인 삼성증권㈜과 발행회사인 오픈엣지테크놀로지㈜가 협의하여 1주당 확정공모가액을 최종 결정할 예정이며, 모집(매출)가액 확정 시 정정신고서를 제출할 예정입니다.

(주4) 「증권의 발행 및 공시 등에 관한 규정」 제2-3조제2항제1호에 따라 정정신고서 상의 공모주식수는 금번 제출하는 증권신고서의 공모할 주식수의 100분의 80 이상과 100분의 120 이하에 해당하는 주식수로 변경가능합니다.

(주5) 청약일 - 우리사주조합 청약일: 2022년 09월 15일 (1일간) - 기관투자자 청약일: 2022년 09월 15일 ~ 09월 16일 (2일간) - 일반청약자 청약일: 2022년 09월 15일 ~ 09월 16일 (2일간) ※ 우리사주조합의 청약은 청약 초일인 2022년 09월 15일에 실시되고, 기관투자자의 청약과 일반투자자 청약은 2022년 09월 15일부터 09월 16일까지 이틀간 실시됨에 유의하시기 바라며, 상기 청약일 및 납입일 등 일정은 효력발생일의 변경 및 회사상황, 주식시장 상황 등에 따라 변경될 수 있습니다.

(주8) 인수대가는 공모금액 및 상장주선인의 의무인수 금액을 합산한 금액의 4.5%에 해당하는 금액이며, 상기 인수대가는 발행회사와 대표주관회사가 협의하여 제시한 공모희망가액 범위(15,000원 ~ 18,000원)의 최저가액 기준입니다.

(주9) 금번 공모에서는 「증권 인수업무 등에 관한 규정」 제10조의3(환매청구권) 제1항 제5호에 해당하는 사항이 존재하며, 이에 따라 「증권 인수업무 등에 관한 규정」 제10조의3(환매청구권)에 따른 일반청약자에게 공모주식을 인수회사에 매도할 수 있는 권리(이하 "환매청구권"이라 한다)를 부여합니다.

(주10) 금번 공모시 「코스닥시장 상장규정」제13조 제5항 제1호에 의해 상장주선인인 삼성증권㈜은 공모물량의 3%(취득금액이 10억원을 초과하는 경우에는 10억원에 해당하는 수량)를 당해 모집(매출)하는 가액과 동일한 가격으로 취득하여야 합니다.
"""
    
    @classmethod
    def generate_prompt(cls, request: EquityAnnotationRequest, similar_cases: List[str] = None) -> str:
        """주석 생성용 프롬프트 생성"""
        
        # 기본 공모 정보 추출
        summary = request.get_offering_summary()
        
        prompt = f"""
다음 주식 공모 정보를 바탕으로 전문적인 주석 3개를 생성해주세요.

## 공모 정보
- 회사명: {request.get_corp_name()}
- 증권의 종류: {summary['security_type']}
- 증권 수량: {summary['security_count']:,}주
- 액면가액: {summary['face_value']:,}원
- 모집가액: {summary['offering_price']:,}원
- 모집총액: {summary['total_amount']:,}원
- 모집방법: {summary['offering_method']}
- 대표주관회사: {summary['underwriter']}
- 청약기일: {summary['subscription_date']}
- 납입기일: {summary['payment_date']}

{cls.SAMPLE_ANNOTATIONS}

## 생성 요구사항
위 예시를 참고하여 다음 주제로 주석 3개를 생성하세요:
1. (주1) 공모가격 관련 설명
2. (주2) 청약 일정 및 방법 안내  
3. (주3) 인수 조건 또는 상장 관련 사항

각 주석은 전문적이고 정확한 금융 용어를 사용하여 작성하고, 투자자에게 실질적인 도움이 되는 정보를 포함해주세요.
"""
        
        # 유사 사례가 있으면 추가
        if similar_cases:
            prompt += f"\n\n## 유사 사례 참고\n"
            for i, case in enumerate(similar_cases[:2], 1):
                prompt += f"참고{i}: {case}\n"
        
        return prompt
    
    @classmethod 
    def generate_rag_prompt(cls, request: EquityAnnotationRequest, rag_content: str) -> str:
        """RAG 검색 결과를 포함한 프롬프트 생성"""
        
        summary = request.get_offering_summary()
        
        prompt = f"""
다음 주식 공모 정보와 검색된 관련 자료를 바탕으로 전문적인 주석 3개를 생성해주세요.

## 현재 공모 정보
- 회사명: {request.get_corp_name()}
- 증권의 종류: {summary['security_type']}
- 증권 수량: {summary['security_count']:,}주
- 액면가액: {summary['face_value']:,}원
- 모집가액: {summary['offering_price']:,}원
- 모집총액: {summary['total_amount']:,}원
- 모집방법: {summary['offering_method']}
- 대표주관회사: {summary['underwriter']}
- 청약기일: {summary['subscription_date']}
- 납입기일: {summary['payment_date']}

## 검색된 관련 자료
{rag_content}

{cls.SAMPLE_ANNOTATIONS}

## 생성 요구사항
위 정보들을 종합하여 다음 주제로 주석 3개를 생성하세요:
1. (주1) 공모가격 및 가액 확정 관련
2. (주2) 청약 일정 및 절차 안내
3. (주3) 인수 조건 또는 특별 사항

반드시 (주1), (주2), (주3) 형태로 시작하고, 각 주석은 정확한 금융 용어와 관련 법규를 인용하여 작성해주세요.
"""
        return prompt