from opensearchpy import OpenSearch
from .config import settings
from urllib.parse import urlparse

# 환경변수에서 OS_HOST 가져오기
OS_HOST = settings.OS_HOST

# 기본 OpenSearch 클라이언트 (settings에서 동적으로 구성)
os_client = OpenSearch(
    hosts=OS_HOST,
    http_compress=True,
    retry_on_timeout=True,
    max_retries=3,
    request_timeout=settings.OPENSEARCH_TIMEOUT_SECONDS,  # 설정에서 가져옴
)

# 우리가 사용하는 외부 OpenSearch와 연결하는 클라이언트
uri = settings.OPENSEARCH_URI  # 설정에서 가져옴
parsed = urlparse(uri)
host_info = {
    "host": parsed.hostname,
    "port": parsed.port
}

os_client_remote = OpenSearch(
    hosts=[host_info],
    # http_auth=(settings.OPENSEARCH_USER, settings.OPENSEARCH_PASSWORD),  # 필요시 주석 해제
    use_ssl=(parsed.scheme == "https"),
    verify_certs=False,
    timeout=settings.OPENSEARCH_TIMEOUT_SECONDS
)

# ✅ 서비스에서 import 할 수 있도록 함수 추가
def get_opensearch_client():
    """기본 OpenSearch 클라이언트 반환"""
    return os_client

def get_opensearch_remote_client():
    """원격 OpenSearch 클라이언트 반환"""
    return os_client_remote