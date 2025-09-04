from opensearchpy import OpenSearch
from .config import settings
from urllib.parse import urlparse

# 환경변수 설정
from app.config import settings
OS_HOST = settings.OS_HOST

# OpenSearch 접속 정보
os_client = OpenSearch(
    hosts=OS_HOST,# OpenSearch 노드 URL
    http_compress=True,
    retry_on_timeout=True,
    max_retries=3,
    request_timeout=60,
)




# 우리가 사용하는 외부 OpenSearch와 연결하는 클라이언트
uri="http://192.168.0.77:9200"

# URI 파싱
parsed = urlparse(uri)
host_info = {
    "host": parsed.hostname,
    "port": parsed.port
}

# OpenSearch client 생성
os_client_reomte = OpenSearch(
    hosts=[host_info],
    http_auth=("admin", "admin"),  # 필요한 경우
    use_ssl=(parsed.scheme == "https"),
    verify_certs=False
)