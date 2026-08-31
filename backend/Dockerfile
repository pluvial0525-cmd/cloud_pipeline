FROM python:3.12-slim


WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app


# =========================================================
# Python 패키지 설치
# =========================================================

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# =========================================================
# FastAPI 코드
# =========================================================

COPY app ./app


# =========================================================
# Image RAG 임베딩 DB
# 원본 images 폴더는 배포하지 않음
# =========================================================

COPY image_rag.db ./image_rag.db


# =========================================================
# FastAPI
# =========================================================

EXPOSE 8000


CMD [
    "python",
    "-m",
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]