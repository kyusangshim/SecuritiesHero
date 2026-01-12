#C:\Users\user\Documents\FAST_API_LLM\Utility\app\AI\services\opensearch_service.py
from typing import List, Dict, Optional
import json
import logging
from app.opensearch_client import get_opensearch_client
from app.AI.schemas.equity_request import EquityAnnotationRequest

logger = logging.getLogger(__name__)

class OpenSearchService:
    """OpenSearch 검색 서비스 (RAG용)"""
    
    def __init__(self):
        try:
            self.client = get_opensearch_client()
        except Exception as e:
            logger.error(f"OpenSearch 클라이언트 초기화 실패: {str(e)}")
            self.client = None
        
    async def search_similar_cases(self, request: EquityAnnotationRequest) -> str:
        """유사한 공모 사례 검색"""
        if not self.client:
            logger.warning("OpenSearch 클라이언트가 없어 검색을 수행할 수 없습니다.")
            return ""
            
        try:
            # 검색 쿼리 구성
            search_query = self._build_search_query(request)
            
            # OpenSearch에서 검색
            results = []
            
            # rpt_sec_eq 인덱스에서 검색 (주식 공모 관련)
            try:
                eq_results = await self._search_index("rpt_sec_eq", search_query)
                results.extend(eq_results)
            except Exception as e:
                logger.warning(f"rpt_sec_eq 인덱스 검색 실패: {str(e)}")
            
            # standard 인덱스에서 검색 (일반 문서)
            try:
                std_results = await self._search_index("standard", search_query)
                results.extend(std_results)
            except Exception as e:
                logger.warning(f"standard 인덱스 검색 실패: {str(e)}")
            
            # 검색 결과 정리
            return self._process_search_results(results)
            
        except Exception as e:
            logger.error(f"OpenSearch 검색 오류: {str(e)}")
            return ""
    
    def _build_search_query(self, request: EquityAnnotationRequest) -> Dict:
        """검색 쿼리 구성"""
        corp_name = request.get_corp_name()
        summary = request.get_offering_summary()
        
        # 검색 키워드 구성
        keywords = [
            "공모", "모집", "청약", "인수", "주석",
            summary['security_type'], 
            summary['underwriter'],
            "주식발행", "증권신고서"
        ]
        
        query = {
            "size": 5,
            "query": {
                "bool": {
                    "should": [
                        # 회사명으로 검색
                        {
                            "match": {
                                "corp_name": {
                                    "query": corp_name,
                                    "boost": 2.0
                                }
                            }
                        },
                        # 키워드로 검색
                        {
                            "multi_match": {
                                "query": " ".join(keywords),
                                "fields": ["content^1.5", "sections.sec_content", "sections.sec_title^2"],
                                "type": "best_fields"
                            }
                        }
                    ],
                    "minimum_should_match": 1
                }
            },
            "_source": ["corp_name", "content", "sections.sec_title", "sections.sec_content"]
        }
        
        return query
    
    async def _search_index(self, index_name: str, query: Dict) -> List[Dict]:
        """특정 인덱스에서 검색"""
        if not self.client:
            return []
            
        try:
            # 인덱스 존재 확인
            if not self.client.indices.exists(index=index_name):
                logger.warning(f"인덱스 {index_name}가 존재하지 않습니다.")
                return []
                
            response = self.client.search(
                index=index_name,
                body=query
            )
            
            hits = response.get('hits', {}).get('hits', [])
            return [hit['_source'] for hit in hits]
            
        except Exception as e:
            logger.error(f"{index_name} 인덱스 검색 오류: {str(e)}")
            return []
    
    def _process_search_results(self, results: List[Dict]) -> str:
        """검색 결과 처리 및 텍스트 구성"""
        if not results:
            return ""
        
        processed_content = []
        
        for result in results[:3]:  # 상위 3개만 사용
            content_parts = []
            
            # 기본 컨텐츠
            if 'content' in result and result['content']:
                content_parts.append(str(result['content'])[:500])  # 500자 제한
            
            # 섹션 컨텐츠 (nested 구조)
            if 'sections' in result and isinstance(result['sections'], list):
                for section in result['sections'][:2]:  # 상위 2개 섹션만
                    if isinstance(section, dict) and 'sec_content' in section:
                        content_parts.append(str(section['sec_content'])[:300])  # 300자 제한
            
            if content_parts:
                processed_content.append("\n".join(content_parts))
        
        if processed_content:
            return "\n\n--- 관련 자료 ---\n".join(processed_content)
        else:
            return ""
    
    async def search_annotations_examples(self, keywords: List[str]) -> List[str]:
        """주석 예시 검색"""
        if not self.client:
            logger.warning("OpenSearch 클라이언트가 없어 예시 검색을 수행할 수 없습니다.")
            return []
            
        try:
            query = {
                "size": 3,
                "query": {
                    "multi_match": {
                        "query": " ".join(keywords + ["주석", "(주", "공모", "모집"]),
                        "fields": ["content", "sections.sec_content"],
                        "type": "phrase"
                    }
                },
                "_source": ["content", "sections.sec_content"]
            }
            
            # 여러 인덱스에서 검색
            examples = []
            for index in ["rpt_sec_eq", "standard"]:
                try:
                    results = await self._search_index(index, query)
                    for result in results:
                        content = result.get('content', '')
                        if isinstance(content, str) and '(주' in content:
                            # 주석 부분 추출
                            annotations = self._extract_annotations(content)
                            examples.extend(annotations)
                except Exception as e:
                    logger.warning(f"{index} 인덱스에서 예시 검색 실패: {str(e)}")
                    continue
            
            return examples[:5]  # 상위 5개만 반환
            
        except Exception as e:
            logger.error(f"주석 예시 검색 오류: {str(e)}")
            return []
    
    def _extract_annotations(self, content: str) -> List[str]:
        """텍스트에서 주석 추출"""
        annotations = []
        if not isinstance(content, str):
            return annotations
            
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
        
        if current_annotation:
            annotations.append(current_annotation.strip())
            
        return annotations
    
    def is_healthy(self) -> bool:
        """OpenSearch 연결 상태 확인"""
        try:
            if not self.client:
                return False
            info = self.client.info()
            return bool(info.get('cluster_name'))
        except Exception as e:
            logger.error(f"OpenSearch health check failed: {str(e)}")
            return False