from fastapi import APIRouter, HTTPException
from opensearchpy.helpers import bulk

from app.opensearch_client import os_client_remote as remote_client
from app.services.financials.financials_service import get_final_list
from app.constants.financials.financials_mappings import financial_mapping

router = APIRouter()


@router.post("/")
def index_document(corp_code: str):
    final_docs = get_final_list(corp_code)

    if not final_docs:
        raise HTTPException(status_code=400, detail="재무정보를 가져오지 못했습니다.")

    index_name = f"fin_{corp_code}"

    if not remote_client.indices.exists(index=index_name):
        res = remote_client.indices.create(index=index_name, body=financial_mapping)
        if not res.get("acknowledged", False):
            raise HTTPException(status_code=500, detail="인덱스 생성 실패")

    actions = [{"_index": index_name, "_source": doc} for doc in final_docs]

    success, errors = bulk(remote_client, actions)
    if errors:
        return {"message": "색인 완료 (일부 실패)", "success": success, "errors": errors}
    return {"message": "색인 성공", "success": success}