import os
from dotenv import load_dotenv

load_dotenv()

OPENSEARCH_URI = os.getenv("OPENSEARCH_URI")
MY_API_BASE_URL = os.getenv("MY_API_BASE_URL")
DART_API_KEY = os.getenv("DART_API_KEY")