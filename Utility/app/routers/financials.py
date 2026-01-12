from fastapi import APIRouter, HTTPException
from opensearchpy.helpers import bulk

from app.opensearch_client import os_client_remote as remote_client
from app.services.financials.financials_service import get_final_list
from app.constants.financials.financials_mappings import financial_mapping

router = APIRouter()


@router.post("/")
def index_document(corp_code: str):
    index_name = f"fin_{corp_code}"

    # 인덱스가 이미 존재하면 바로 리턴
    if remote_client.indices.exists(index=index_name):
        return {"message": "이미 인덱스가 존재합니다", "success": 0}

    # 재무정보 가져오기
    final_docs = get_final_list(corp_code)
    if not final_docs:
        raise HTTPException(status_code=400, detail="재무정보를 가져오지 못했습니다.")

    # 인덱스 생성
    res = remote_client.indices.create(index=index_name, body=financial_mapping)
    if not res.get("acknowledged", False):
        raise HTTPException(status_code=500, detail="인덱스 생성 실패")

    # Bulk 색인
    actions = [{"_index": index_name, "_source": doc} for doc in final_docs]
    success, errors = bulk(remote_client, actions)
    if errors:
        return {"message": "색인 완료 (일부 실패)", "success": success, "errors": errors}

    return {"message": "색인 성공", "success": success}