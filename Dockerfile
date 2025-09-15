FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 시스템 의존성 (필요시 최소화)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# 의존성 설치
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# 소스 복사
COPY . .

EXPOSE 8000

# 기본 실행: uvicorn으로 FastAPI 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
