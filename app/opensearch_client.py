from opensearchpy import OpenSearch
from .config import settings
from urllib.parse import urlparse

# 단일 OPENSEARCH_URI 기반 클라이언트 구성 (ngrok HTTPS 443 기본)
uri = settings.OPENSEARCH_URI
parsed = urlparse(uri)
default_port = 443 if parsed.scheme == "https" else 80
host_info = {
    "host": parsed.hostname,
    "port": parsed.port or default_port,
}

common_kwargs = {
    "http_compress": True,
    "retry_on_timeout": True,
    "max_retries": 3,
    "request_timeout": settings.OPENSEARCH_TIMEOUT_SECONDS,
}

os_client = OpenSearch(
    hosts=[host_info],
    use_ssl=(parsed.scheme == "https"),
    verify_certs=False,
    **common_kwargs,
)

# ✅ 서비스에서 import 할 수 있도록 함수 추가
def get_opensearch_client():
    """기본 OpenSearch 클라이언트 반환 (OPENSEARCH_URI 사용)"""
    return os_client