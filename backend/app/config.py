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
    "pluvial-s3-resource",
)

AWS_S3_IMAGE_PREFIX = os.getenv(
    "AWS_S3_IMAGE_PREFIX",
    "images",
)