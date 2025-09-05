from opensearchpy import OpenSearch
from .config import settings
from urllib.parse import urlparse

# 환경변수에서 OS_HOST 가져오기
OS_HOST = settings.OS_HOST

# 기본 OpenSearch 클라이언트
os_client = OpenSearch(
    hosts=OS_HOST,
    http_compress=True,
    retry_on_timeout=True,
    max_retries=3,
    request_timeout=60,
)

# 우리가 사용하는 외부 OpenSearch와 연결하는 클라이언트
uri = "http://localhost:9200"
#uri = "http://192.168.0.77:9200"
parsed = urlparse(uri)
host_info = {
    "host": parsed.hostname,
    "port": parsed.port
}

os_client_remote = OpenSearch(
    hosts=[host_info],
    #http_auth=("admin", "admin"),
    use_ssl=(parsed.scheme == "https"),
    verify_certs=False
)

# ✅ 서비스에서 import 할 수 있도록 함수 추가
def get_opensearch_client():
    return os_client
