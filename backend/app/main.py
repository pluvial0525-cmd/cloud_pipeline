from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

    allow_methods=[
        "*",
    ],

    allow_headers=[
        "*",
    ],
)


# =========================================================
# Router 등록
# =========================================================

app.include_router(
    image_rag_router
)


# =========================================================
# 기본 API
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Image RAG API Server"
    }