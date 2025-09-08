#C:\Users\user\Documents\FAST_API_LLM\Utility\app\AI\models\llm_client.py
import httpx
import json
from typing import List, Dict, Any, Union
import os
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class OpenRouterClient:
    """OpenRouter API 클라이언트 - Java 백엔드와 완전 호환"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = settings.AI_MODEL
        self.temperature = settings.AI_TEMPERATURE
        self.max_tokens = settings.AI_MAX_TOKENS
        
        # API 키 검증
        if not self.api_key or self.api_key.strip() == "":
            logger.error("OPENROUTER_API_KEY가 설정되지 않았습니다.")
        
    async def generate_annotations(self, prompt: str) -> Union[str, Dict[str, str]]:
        """주식 공모 주석 5개 생성 - JSON 응답 또는 텍스트 응답 반환"""
        if not self.api_key or self.api_key.strip() == "":
            raise Exception("OpenRouter API 키가 설정되지 않았습니다.")
            
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "Equity Annotation Service"
                }
                
                payload = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": """당신은 주식 공모 전문가입니다. 주어진 공모 정보를 바탕으로 정확하고 전문적인 주석을 생성해주세요.

규칙:
1. 정확히 5개의 주석을 생성하세요
2. JSON 형식으로 S4_NOTE1_1부터 S4_NOTE1_5까지 반환하세요
3. 금융 전문 용어를 정확히 사용하세요
4. 투자자에게 도움이 되는 실질적인 정보를 포함하세요
5. 각 주석은 2-3문장으로 구성하세요
6. 반드시 유효한 JSON 형식으로만 답변하세요
7. 금액을 정확하게 표시하세요 54549615000원 이런식으로 전부 포함하세요

응답 예시:
{
    "S4_NOTE1_1": "첫 번째 주석 내용",
    "S4_NOTE1_2": "두 번째 주석 내용",
    "S4_NOTE1_3": "세 번째 주석 내용",
    "S4_NOTE1_4": "네 번째 주석 내용",
    "S4_NOTE1_5": "다섯 번째 주석 내용"
}"""
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
                    
                    # 백엔드 호환성을 위해 원시 응답 반환 (파싱은 service에서 처리)
                    return content
                    
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
            logger.error("OpenRouter API 요청 시간 초과")
            raise Exception("OpenRouter API 요청 시간 초과")
        except httpx.RequestError as e:
            logger.error(f"OpenRouter API 연결 오류: {str(e)}")
            raise Exception(f"OpenRouter API 연결 오류: {str(e)}")
        except Exception as e:
            logger.error(f"LLM 요청 실패: {str(e)}")
            raise Exception(f"LLM 요청 실패: {str(e)}")
    
    def parse_json_response(self, content: str) -> Dict[str, str]:
        """LLM JSON 응답을 파싱하여 주석 딕셔너리 반환"""
        try:
            # JSON 파싱 시도
            parsed = json.loads(content)
            if isinstance(parsed, dict) and "S4_NOTE1_1" in parsed:
                # 5개 주석이 모두 있는지 확인하고 보완
                result = {}
                for i in range(1, 6):
                    key = f"S4_NOTE1_{i}"
                    if key in parsed and parsed[key]:
                        result[key] = parsed[key]
                    else:
                        result[key] = self._get_default_note(i)
                        logger.warning(f"주석 {i} 누락, 기본값 사용")
                
                logger.info("JSON 파싱 성공 - 5개 주석 추출")
                return result
            else:
                logger.warning("JSON 형식이지만 필수 키가 없음")
                return self._get_default_dict()
                
        except json.JSONDecodeError:
            logger.warning("JSON 파싱 실패, 텍스트 파싱 시도")
            return self._parse_text_to_dict(content)
        except Exception as e:
            logger.error(f"JSON 파싱 중 오류: {str(e)}")
            return self._get_default_dict()
    
    def _parse_text_to_dict(self, content: str) -> Dict[str, str]:
        """텍스트에서 주석을 추출하여 딕셔너리로 변환"""
        try:
            annotations = self._extract_annotations_from_text(content)
            result = {}
            
            for i in range(5):
                key = f"S4_NOTE1_{i+1}"
                if i < len(annotations) and annotations[i]:
                    result[key] = annotations[i]
                else:
                    result[key] = self._get_default_note(i+1)
            
            logger.info(f"텍스트 파싱 완료 - {len(annotations)}개 주석 추출")
            return result
            
        except Exception as e:
            logger.error(f"텍스트 파싱 실패: {str(e)}")
            return self._get_default_dict()
    
    def _extract_annotations_from_text(self, content: str) -> List[str]:
        """텍스트에서 주석 추출 - 기존 로직 유지"""
        annotations = []
        lines = content.split('\n')
        current_annotation = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('(주') and ')' in line:
                if current_annotation:
                    annotations.append(current_annotation.strip())
                current_annotation = line
            elif current_annotation and line and not line.startswith('(주'):
                current_annotation += " " + line
        
        # 마지막 주석 추가
        if current_annotation:
            annotations.append(current_annotation.strip())
        
        return annotations
    
    def _get_default_dict(self) -> Dict[str, str]:
        """기본 주석 딕셔너리 반환 - 백엔드와 동일"""
        return {
            "S4_NOTE1_1": self._get_default_note(1),
            "S4_NOTE1_2": self._get_default_note(2),
            "S4_NOTE1_3": self._get_default_note(3),
            "S4_NOTE1_4": self._get_default_note(4),
            "S4_NOTE1_5": self._get_default_note(5)
        }
    
    def _get_default_note(self, index: int) -> str:
        """개별 기본 주석 반환 - EquityAnnotationResponseDto.createDefault()와 동일"""
        default_notes = {
            1: "모집(매출) 예정가액과 관련된 내용은 「제1부 모집 또는 매출에 관한 사항」- 「Ⅳ. 인수인의 의견(분석기관의 의견)」의 「4. 공모가격에 대한 의견」부분을 참조하시기 바랍니다.",
            2: "모집(매출)가액, 모집(매출)이액, 인수금액 및 인수대가는 발행회사와 대표주관회사가 협의하여 제시하는 공모희망가액 기준입니다.",
            3: "모집(매출)가액의 확정은 청약일 전에 실시하는 수요예측 결과를 반영하여 대표주관회사와 발행회사가 협의하여 최종 결정할 예정입니다.",
            4: "증권의 발행 및 공시 등에 관한 규정에 따라 정정신고서 상의 공모주식수는 증권신고서의 공모할 주식수의 80% 이상 120% 이하로 변경가능합니다.",
            5: "투자 위험 등 자세한 내용은 투자설명서를 참조하시기 바라며, 투자결정시 신중하게 검토하시기 바랍니다."
        }
        return default_notes.get(index, f"주석 {index}에 대한 내용입니다.")
    
    def is_healthy(self) -> bool:
        """LLM 클라이언트 상태 확인"""
        return bool(self.api_key and len(self.api_key.strip()) > 10)
    
    # 백엔드 호환성을 위한 추가 메서드들
    
    def get_model_info(self) -> Dict[str, Any]:
        """모델 정보 반환"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_available": self.is_healthy()
        }
    
    def validate_api_key(self) -> bool:
        """API 키 유효성 검증"""
        try:
            if not self.api_key or len(self.api_key.strip()) < 10:
                return False
            # 실제 API 호출 없이 형식만 확인
            return self.api_key.startswith("sk-or-") or len(self.api_key) > 20
        except Exception:
            return False