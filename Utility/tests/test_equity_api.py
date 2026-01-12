import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import asyncio
import httpx
import json

# 테스트 데이터
test_data = {
    "general_info": {
        "rcept_no": "20220915000001",
        "corp_cls": "K",  # 코스닥
        "corp_code": "00123456",
        "corp_name": "오픈엣지테크놀로지",
        "sbd": "2022년 09월 15일 ~ 2022년 09월 16일",
        "pymd": "2022년 09월 20일",
        "sband": "2022년 09월 15일",
        "asand": "2022년 09월 20일",
        "asstd": None
    },
    "security_type": {
        "rcept_no": "20220915000001", 
        "corp_code": "00123456",
        "corp_name": "오픈엣지테크놀로지",
        "stksen": "기명식보통주",
        "stkcnt": 3636641,
        "fv": 100,
        "slprc": 15000,
        "slta": 54549615000,
        "slmthn": "일반공모"
    },
    "underwriter_info": {
        "rcept_no": "20220915000001",
        "corp_code": "00123456", 
        "corp_name": "오픈엣지테크놀로지",
        "actsen": "대표주관회사",
        "actnmn": "삼성증권",
        "stksen": "기명식보통주",
        "udtcnt": 3636641,
        "udtamt": 54549615000,
        "udtprc": 2499732200,
        "udtmth": "총액인수"
    }
}

async def test_api():
    """API 테스트 함수"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            # 1. 헬스체크
            print("=== 헬스체크 ===")
            health_response = await client.get(f"{base_url}/api/v1/equity/health")
            print(f"Status: {health_response.status_code}")
            print(f"Response: {health_response.json()}")
            print()
            
            # 2. 테스트 엔드포인트
            print("=== 테스트 엔드포인트 ===")
            test_response = await client.get(f"{base_url}/api/v1/equity/test")
            print(f"Status: {test_response.status_code}")
            print(f"Response: {test_response.json()}")
            print()
            
            # 3. 간단한 주석 생성 테스트
            print("=== 간단한 주식 공모 주석 생성 ===")
            simple_response = await client.post(
                f"{base_url}/api/v1/equity/annotations/simple",
                json=test_data
            )
            print(f"Status: {simple_response.status_code}")
            result = simple_response.json()
            print(f"회사명: {result.get('corp_name')}")
            print(f"상태: {result.get('status')}")
            print("생성된 주석:")
            for i, annotation in enumerate(result.get('annotations', []), 1):
                print(f"{i}. {annotation}")
            print()
            
            # 4. RAG 포함 주석 생성 테스트  
            print("=== RAG 포함 주식 공모 주석 생성 ===")
            rag_response = await client.post(
                f"{base_url}/api/v1/equity/annotations",
                json=test_data
            )
            print(f"Status: {rag_response.status_code}")
            result = rag_response.json()
            print(f"회사명: {result.get('corp_name')}")
            print(f"상태: {result.get('status')}")
            print("생성된 주석:")
            for i, annotation in enumerate(result.get('annotations', []), 1):
                print(f"{i}. {annotation}")
            print()
            
        except Exception as e:
            print(f"테스트 중 오류 발생: {str(e)}")

def test_schema():
    """스키마 테스트 함수"""
    print("=== 스키마 테스트 ===")
    
    try:
        from app.AI.schemas.equity_request import EquityAnnotationRequest
        from app.AI.schemas.equity_response import EquityAnnotationResponse
        
        # 요청 스키마 테스트
        request = EquityAnnotationRequest(**test_data)
        print(f"회사코드: {request.get_corp_code()}")
        print(f"회사명: {request.get_corp_name()}")
        
        summary = request.get_offering_summary()
        print("공모 요약:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        print("스키마 테스트 성공!")
        
    except Exception as e:
        print(f"스키마 테스트 실패: {str(e)}")

if __name__ == "__main__":
    print("주식 공모 주석 생성 API 테스트 시작\n")
    
    # 스키마 테스트
    test_schema()
    print()
    
    # API 테스트 (서버가 실행 중일 때만)
    try:
        asyncio.run(test_api())
    except KeyboardInterrupt:
        print("테스트 중단")
    except Exception as e:
        print(f"API 테스트 실패: {str(e)}")
        print("서버가 실행 중인지 확인하세요: uvicorn app.main:app --reload")