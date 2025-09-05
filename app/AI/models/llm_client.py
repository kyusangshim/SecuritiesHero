#C:\Users\user\Documents\FAST_API_LLM\Utility\app\AI\models\llm_client.py
import httpx
import json
from typing import List
import os
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class OpenRouterClient:
    """OpenRouter API 클라이언트"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = settings.AI_MODEL
        self.temperature = settings.AI_TEMPERATURE
        self.max_tokens = settings.AI_MAX_TOKENS
        
        # API 키 검증
        if not self.api_key or self.api_key.strip() == "":
            logger.error("OPENROUTER_API_KEY가 설정되지 않았습니다.")
        
    async def generate_annotations(self, prompt: str) -> List[str]:
        """주식 공모 주석 생성"""
        if not self.api_key or self.api_key.strip() == "":
            raise Exception("OpenRouter API 키가 설정되지 않았습니다.")
            
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8000",  # OpenRouter에서 요구하는 경우
                    "X-Title": "Equity Annotation Service"  # OpenRouter에서 요구하는 경우
                }
                
                payload = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": """당신은 주식 공모 전문가입니다. 주어진 공모 정보를 바탕으로 정확하고 전문적인 주석을 생성해주세요.

규칙:
1. 정확히 3개의 주석을 생성하세요
2. 각 주석은 (주1), (주2), (주3) 형태로 시작하세요  
3. 금융 전문 용어를 정확히 사용하세요
4. 투자자에게 도움이 되는 실질적인 정보를 포함하세요
5. 각 주석은 2-3문장으로 구성하세요
6. 반드시 JSON 형식이 아닌 일반 텍스트로 답변하세요"""
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                }
                
                logger.info(f"OpenRouter API 호출 시작 - 모델: {self.model}")
                
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                logger.info(f"OpenRouter API 응답 - 상태코드: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    logger.info(f"생성된 컨텐츠 길이: {len(content)}")
                    return self._parse_annotations(content)
                else:
                    error_text = response.text
                    logger.error(f"OpenRouter API 오류: {response.status_code} - {error_text}")
                    
                    # 401 Unauthorized 오류 처리
                    if response.status_code == 401:
                        raise Exception("OpenRouter API 키가 유효하지 않습니다. API 키를 확인해주세요.")
                    # 429 Rate limit 오류 처리
                    elif response.status_code == 429:
                        raise Exception("API 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
                    # 기타 오류
                    else:
                        raise Exception(f"OpenRouter API 오류: {response.status_code} - {error_text}")
                    
        except httpx.TimeoutException:
            raise Exception("OpenRouter API 요청 시간 초과")
        except httpx.RequestError as e:
            raise Exception(f"OpenRouter API 연결 오류: {str(e)}")
        except Exception as e:
            logger.error(f"LLM 요청 실패: {str(e)}")
            raise Exception(f"LLM 요청 실패: {str(e)}")
    
    def _parse_annotations(self, content: str) -> List[str]:
        """생성된 내용에서 주석 3개 추출"""
        try:
            lines = content.split('\n')
            annotations = []
            current_annotation = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('(주') and ')' in line:
                    if current_annotation:
                        annotations.append(current_annotation.strip())
                    current_annotation = line
                elif current_annotation and line and not line.startswith('(주'):
                    current_annotation += " " + line
                elif current_annotation and not line:
                    # 빈 줄을 만나면 현재 주석을 완료
                    continue
            
            # 마지막 주석 추가
            if current_annotation:
                annotations.append(current_annotation.strip())
            
            # 정확히 3개가 아니면 재처리
            if len(annotations) != 3:
                logger.warning(f"파싱된 주석 개수: {len(annotations)}, 재처리 시도")
                return self._fallback_parse(content)
                
            logger.info(f"주석 파싱 완료 - {len(annotations)}개")
            return annotations
            
        except Exception as e:
            logger.error(f"주석 파싱 오류: {str(e)}")
            # 파싱 실패시 기본값 반환
            return self._get_default_annotations()
    
    def _fallback_parse(self, content: str) -> List[str]:
        """파싱 실패시 대체 방법"""
        try:
            # 줄 단위로 분리하여 (주로 시작하는 라인 찾기
            lines = content.split('\n')
            annotations = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('(주') and ')' in line:
                    annotations.append(line)
                    if len(annotations) == 3:
                        break
            
            # 여전히 3개가 아니면 기본값 사용
            if len(annotations) != 3:
                logger.warning("대체 파싱도 실패, 기본값 사용")
                return self._get_default_annotations()
            
            return annotations
            
        except Exception as e:
            logger.error(f"대체 파싱 실패: {str(e)}")
            return self._get_default_annotations()
    
    def _get_default_annotations(self) -> List[str]:
        """기본 주석 반환"""
        return [
            "(주1) 모집(매출)가액 관련 세부사항은 관련 규정에 따라 확정될 예정입니다.",
            "(주2) 청약 및 납입 일정은 시장 상황에 따라 변경될 수 있습니다.", 
            "(주3) 상장 관련 요건 충족 여부에 따라 거래 가능성이 결정됩니다."
        ]
        
    def is_healthy(self) -> bool:
        """LLM 클라이언트 상태 확인"""
        return bool(self.api_key and len(self.api_key.strip()) > 10)