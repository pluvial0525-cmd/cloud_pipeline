from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.auth.web import (
    router as auth_router,
)
from app.database.postgres import (
    Base,
    engine,
)
from app.database.redis import (
    redis_client,
)
from app.imageRag.web import (
    router as image_rag_router,
)


# =========================================================
# FastAPI 앱 생성
# =========================================================

app = FastAPI(
    title="Image RAG API",
)


# =========================================================
# PostgreSQL 테이블 생성
# =========================================================

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# CORS 설정
# React(Vite) 프론트엔드 접근 허용
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Router 등록
# =========================================================

app.include_router(
    image_rag_router
)

app.include_router(
    auth_router
)


# =========================================================
# 기본 API
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Image RAG API Server"
    }


# =========================================================
# PostgreSQL 연결 테스트
# =========================================================

@app.get(
    "/test/postgres"
)
def test_postgres():

    with engine.connect() as connection:

        result = connection.execute(
            text(
                "SELECT 1"
            )
        )

        value = result.scalar()

    return {
        "postgres": "connected",
        "result": value,
    }


# =========================================================
# Redis 연결 테스트
# =========================================================

@app.get(
    "/test/redis"
)
def test_redis():

    result = redis_client.ping()

    return {
        "redis": "connected",
        "result": result,
    }