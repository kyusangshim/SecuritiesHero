# test_api_key.py - API 키 검증용 스크립트
import httpx
import asyncio
import sys
import os

# 상위 디렉토리를 path에 추가
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.config import settings

async def test_openrouter_api():
    """OpenRouter API 키 테스트"""
    api_key = settings.OPENROUTER_API_KEY
    
    print(f"API 키 확인: {'설정됨' if api_key else '설정되지 않음'}")
    print(f"API 키 길이: {len(api_key) if api_key else 0}")
    print(f"API 키 앞 10자: {api_key[:10] if api_key else 'None'}...")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY가 .env 파일에 설정되지 않았습니다!")
        return False
    
    # 간단한 API 테스트
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "API Key Test"
                },
                json={
                    "model": "anthropic/claude-3.5-sonnet",
                    "messages": [
                        {"role": "user", "content": "Hello, this is a test."}
                    ],
                    "max_tokens": 10
                }
            )
            
            print(f"API 응답 상태: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ API 키가 정상 작동합니다!")
                result = response.json()
                print(f"모델 응답: {result['choices'][0]['message']['content']}")
                return True
            elif response.status_code == 401:
                print("❌ API 키가 유효하지 않습니다!")
                print("OpenRouter 계정을 확인하고 올바른 API 키를 사용하세요.")
                return False
            elif response.status_code == 429:
                print("⚠️ API 요청 한도 초과")
                return False
            else:
                print(f"❌ API 오류: {response.status_code}")
                print(f"응답: {response.text}")
                return False
                
    except httpx.TimeoutException:
        print("❌ API 요청 시간 초과")
        return False
    except Exception as e:
        print(f"❌ API 테스트 실패: {str(e)}")
        return False

async def test_opensearch_connection():
    """OpenSearch 연결 테스트"""
    try:
        from app.opensearch_client import get_opensearch_client
        client = get_opensearch_client()
        
        # 클러스터 정보 확인
        info = client.info()
        print(f"✅ OpenSearch 연결 성공!")
        print(f"클러스터명: {info.get('cluster_name', 'Unknown')}")
        print(f"버전: {info.get('version', {}).get('number', 'Unknown')}")
        
        # 인덱스 목록 확인
        indices = client.cat.indices(format="json")
        print(f"사용 가능한 인덱스 수: {len(indices)}")
        
        for idx in indices:
            if idx.get('index', '').startswith(('.', 'security')):
                continue  # 시스템 인덱스 제외
            print(f"  - {idx.get('index', 'Unknown')}: {idx.get('docs.count', 0)} documents")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenSearch 연결 실패: {str(e)}")
        print("OpenSearch 서버가 실행 중인지 확인하세요 (http://192.168.0.77:9200")
        return False

if __name__ == "__main__":
    print("=== API 키 및 서비스 연결 테스트 ===\n")
    
    # OpenRouter API 테스트
    print("1. OpenRouter API 테스트:")
    api_result = asyncio.run(test_openrouter_api())
    print()
    
    # OpenSearch 연결 테스트  
    print("2. OpenSearch 연결 테스트:")
    os_result = asyncio.run(test_opensearch_connection())
    print()
    
    # 전체 결과
    print("=== 테스트 결과 요약 ===")
    print(f"OpenRouter API: {'✅ 정상' if api_result else '❌ 실패'}")
    print(f"OpenSearch: {'✅ 정상' if os_result else '❌ 실패'}")
    
    if api_result and os_result:
        print("\n🎉 모든 서비스가 정상 작동합니다!")
    else:
        print(f"\n⚠️ 일부 서비스에 문제가 있습니다. 위의 오류를 확인하세요.")