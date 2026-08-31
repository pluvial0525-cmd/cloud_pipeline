import os
from pathlib import Path

from dotenv import load_dotenv


# =========================================================
# 프로젝트 경로
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ENV_PATH = BASE_DIR / ".env"


# =========================================================
# .env 로드
# =========================================================

load_dotenv(
    dotenv_path=ENV_PATH,
)


# =========================================================
# OpenAI
# =========================================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)


if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY가 설정되어 있지 않습니다."
    )


# =========================================================
# AWS S3
# =========================================================

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-northeast-2",
)

AWS_S3_BUCKET = os.getenv(
    "AWS_S3_BUCKET",
    "pluvial-s3-pipeline",
)

AWS_S3_IMAGE_PREFIX = os.getenv(
    "AWS_S3_IMAGE_PREFIX",
    "images",
)


# =========================================================
# PostgreSQL
# =========================================================

POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "postgres",
)

POSTGRES_PORT = int(
    os.getenv(
        "POSTGRES_PORT",
        "5432",
    )
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "ksm_db",
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "ksm",
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "ksm1234",
)


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)


# =========================================================
# Redis
# =========================================================

REDIS_HOST = os.getenv(
    "REDIS_HOST",
    "redis",
)

REDIS_PORT = int(
    os.getenv(
        "REDIS_PORT",
        "6379",
    )
)

REDIS_DB = int(
    os.getenv(
        "REDIS_DB",
        "0",
    )
)


REDIS_URL = (
    f"redis://"
    f"{REDIS_HOST}:"
    f"{REDIS_PORT}/"
    f"{REDIS_DB}"
)


# =========================================================
# JWT
# =========================================================

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "ksm-super-secret-key-change-this",
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30",
    )
)