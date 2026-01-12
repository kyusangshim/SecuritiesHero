# ingest_to_os.py  (기존 ingest_to_es.py 대체)

import os
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
from .parse_xml import parse_darter_xml, preprocess_xml_content
import codecs

from app.opensearch_client import os_client

from typing import Dict, Any, Generator

# 파싱 데이터 OpenSearch 인덱스 매핑 정의
from app.models.parsing_schemas import RPT_MAPPINGS

def create_indices(corp_code: str = None):
    """사전 정의 인덱스 생성(있으면 skip)"""
    index_name = f"rpt_{corp_code}"
    mapping=RPT_MAPPINGS
    
    if not os_client.indices.exists(index=index_name):
        print(f"Creating index '{index_name}' with mapping...")
        body = RPT_MAPPINGS
        os_client.indices.create(index=index_name, body=body)
    else:
        print(f"Index '{index_name}' already exists.")

# 하나만 파싱해서 오픈서치에 넣기
def one_parse_xml(file_dict: Dict[str, Any], corp_code: str) -> Generator[Dict[str, Any], None, None]:
    create_indices(corp_code)
    try:
        # 딕셔너리 키에 안전하게 접근합니다.
        xml_content = file_dict.get("content")
        rcept_no = file_dict.get("rcept_no")
        
        # 필수 키가 없는 경우 바로 에러 로그를 출력하고 종료
        if not xml_content or not rcept_no:
            print("Error: Missing 'content' or 'rcept_no' in input dictionary.")
            return

        # XML 파싱
        parsed_data = parse_darter_xml(xml_content, rcept_no)
        
        # 파싱된 데이터가 유효한지 확인
        if parsed_data and parsed_data.get("doc_id"):
            target_index= f"rpt_{corp_code}" # 인덱스를 기업코드로 설정

            # OpenSearch에 보낼 데이터를 yield
            yield {
                "_index": target_index,
                "_id": parsed_data["doc_id"],
                "_source": parsed_data,
            }
        else:
            print(f"Warning: No valid data or doc_id parsed from rcept_no '{rcept_no}'.")
    
    except Exception as e:
        print(f"Critical Error during XML parsing for rcept_no '{rcept_no}': {e}")

# 사업보고서 하나만 파싱 통으로 파싱
def one_parse_xml_biz(file_dict: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    try:
        # 딕셔너리 키에 안전하게 접근합니다.
        xml_content = file_dict.get("content")
        rcept_no = file_dict.get("rcept_no")
        
        # 필수 키가 없는 경우 바로 에러 로그를 출력하고 종료
        if not xml_content or not rcept_no:
            print("Error: Missing 'content' or 'rcept_no' in input dictionary.")
            return

        # XML 파싱
        parsed_data = preprocess_xml_content(xml_content)
        
        return parsed_data
    
    except Exception as e:
        print(f"Critical Error during XML parsing for rcept_no '{rcept_no}': {e}")