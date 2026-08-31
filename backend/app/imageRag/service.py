import base64
import json
import math
import sqlite3
from pathlib import Path

from openai import OpenAI

from app.config import (
    AWS_S3_IMAGE_PREFIX,
    OPENAI_API_KEY,
)

from app.storage.s3 import (
    get_image,
    get_image_url,
    list_images,
    normalize_s3_key,
)


# =========================================================
# OpenAI Client
# =========================================================

client = OpenAI(
    api_key=OPENAI_API_KEY,
)


# =========================================================
# 경로
# =========================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]
)

DB_PATH = (
    BASE_DIR
    / "image_rag.db"
)


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


# =========================================================
# SQLite 연결
# =========================================================

def get_connection():

    return sqlite3.connect(
        DB_PATH
    )


# =========================================================
# 테이블 생성
# =========================================================

def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS image_embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            image_path TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
        """
    )

    conn.commit()

    conn.close()


# =========================================================
# 이미지 MIME 타입
# =========================================================

def get_mime_type(
    filename: str,
) -> str:

    suffix = (
        Path(filename)
        .suffix
        .lower()
    )

    if suffix == ".png":
        return "image/png"

    if suffix == ".webp":
        return "image/webp"

    return "image/jpeg"


# =========================================================
# 이미지 → Base64
# =========================================================

def encode_image_bytes(
    image_bytes: bytes,
) -> str:

    return (
        base64
        .b64encode(
            image_bytes
        )
        .decode(
            "utf-8"
        )
    )


# =========================================================
# OpenAI Vision
# 이미지 → 설명
# =========================================================

def describe_image(
    image_bytes: bytes,
    filename: str,
) -> str:

    base64_image = (
        encode_image_bytes(
            image_bytes
        )
    )

    mime_type = (
        get_mime_type(
            filename
        )
    )

    response = (
        client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role":
                        "user",

                    "content": [
                        {
                            "type":
                                "input_text",

                            "text":
                                """
이 이미지에 있는 한국 음식이 무엇인지 분석해주세요.

검색용 Image RAG 임베딩으로 사용할 것이므로
음식 이름, 주요 재료, 색상, 형태,
조리 방식과 시각적 특징을 간결하게 설명해주세요.

음식 이름을 알 수 있다면
가장 먼저 음식 이름을 작성해주세요.
""",
                        },
                        {
                            "type":
                                "input_image",

                            "image_url": (
                                f"data:"
                                f"{mime_type};"
                                f"base64,"
                                f"{base64_image}"
                            ),
                        },
                    ],
                }
            ],
        )
    )

    return (
        response.output_text
    )


# =========================================================
# S3 이미지 설명
# build_embeddings 용
# =========================================================

def describe_s3_image(
    s3_key: str,
) -> str:

    image_bytes = get_image(
        s3_key
    )

    filename = (
        Path(s3_key).name
    )

    return describe_image(
        image_bytes=image_bytes,
        filename=filename,
    )


# =========================================================
# 텍스트 임베딩 생성
# =========================================================

def create_embedding(
    text: str,
) -> list[float]:

    response = (
        client.embeddings.create(
            model=(
                "text-embedding-3-small"
            ),
            input=text,
        )
    )

    return (
        response
        .data[0]
        .embedding
    )


# =========================================================
# 코사인 유사도
# =========================================================

def cosine_similarity(
    vector1: list[float],
    vector2: list[float],
) -> float:

    dot_product = sum(
        a * b
        for a, b in zip(
            vector1,
            vector2,
        )
    )

    magnitude1 = math.sqrt(
        sum(
            a * a
            for a in vector1
        )
    )

    magnitude2 = math.sqrt(
        sum(
            b * b
            for b in vector2
        )
    )

    if (
        magnitude1 == 0
        or magnitude2 == 0
    ):
        return 0.0

    return (
        dot_product
        / (
            magnitude1
            * magnitude2
        )
    )


# =========================================================
# S3 이미지 목록
# =========================================================

def get_image_files():

    image_keys = (
        list_images()
    )

    return [
        key
        for key in image_keys
        if (
            Path(key)
            .suffix
            .lower()
            in IMAGE_EXTENSIONS
        )
    ]


# =========================================================
# DB image_path → S3 Key 변환
# =========================================================

def image_path_to_s3_key(
    image_path: str,
) -> str:

    normalized = (
        image_path
        .replace(
            "\\",
            "/",
        )
        .lstrip("/")
    )


    # 기존 DB:
    # images/음식명/파일.jpg

    if normalized.startswith(
        f"{AWS_S3_IMAGE_PREFIX}/"
    ):
        return (
            normalize_s3_key(
                normalized
            )
        )


    # 혹시 DB에 images가 없는 경우

    return normalize_s3_key(
        f"{AWS_S3_IMAGE_PREFIX}/"
        f"{normalized}"
    )


# =========================================================
# DB 이미지 존재 여부
# =========================================================

def embedding_exists(
    image_path: str,
) -> bool:

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM image_embeddings
        WHERE image_path = ?
        """,
        (
            image_path,
        ),
    )

    result = (
        cursor.fetchone()
    )

    conn.close()

    return (
        result is not None
    )


# =========================================================
# 임베딩 DB 저장
# =========================================================

def save_embedding(
    food_name: str,
    image_path: str,
    description: str,
    embedding: list[float],
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE
        INTO image_embeddings (
            food_name,
            image_path,
            description,
            embedding
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            food_name,
            image_path,
            description,
            json.dumps(
                embedding
            ),
        ),
    )

    conn.commit()

    conn.close()


# =========================================================
# 전체 임베딩 로드
# =========================================================

def load_embeddings():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            food_name,
            image_path,
            description,
            embedding
        FROM image_embeddings
        """
    )

    rows = (
        cursor.fetchall()
    )

    conn.close()

    results = []


    for row in rows:

        results.append(
            {
                "food_name":
                    row[0],

                "image_path":
                    row[1],

                "description":
                    row[2],

                "embedding":
                    json.loads(
                        row[3]
                    ),
            }
        )


    return results


# =========================================================
# Image RAG 검색
# =========================================================

def search_similar_images(
    image_bytes: bytes,
    filename: str,
    top_k: int = 5,
):

    # -----------------------------------------------------
    # 1. 사용자 이미지 분석
    # -----------------------------------------------------

    query_description = (
        describe_image(
            image_bytes=image_bytes,
            filename=filename,
        )
    )

    print(
        "사용자 이미지 설명:",
        query_description,
    )


    # -----------------------------------------------------
    # 2. 사용자 이미지 임베딩
    # -----------------------------------------------------

    query_embedding = (
        create_embedding(
            query_description
        )
    )


    # -----------------------------------------------------
    # 3. 기존 임베딩 DB
    # -----------------------------------------------------

    stored_images = (
        load_embeddings()
    )

    print(
        "저장된 이미지 임베딩 수:",
        len(stored_images),
    )


    if not stored_images:

        raise ValueError(
            "저장된 이미지 임베딩이 없습니다."
        )


    # -----------------------------------------------------
    # 4. 유사도 계산
    # -----------------------------------------------------

    results = []


    for item in stored_images:

        similarity = (
            cosine_similarity(
                query_embedding,
                item["embedding"],
            )
        )


        s3_key = (
            image_path_to_s3_key(
                item[
                    "image_path"
                ]
            )
        )


        results.append(
            {
                "food_name":
                    item[
                        "food_name"
                    ],

                "image_path":
                    item[
                        "image_path"
                    ],

                "s3_key":
                    s3_key,

                "similarity":
                    similarity,
            }
        )


    # -----------------------------------------------------
    # 5. 유사도 높은 순 정렬
    # -----------------------------------------------------

    results.sort(
        key=lambda x:
            x["similarity"],
        reverse=True,
    )


    # -----------------------------------------------------
    # 6. TOP K
    # -----------------------------------------------------

    top_results = (
        results[:top_k]
    )


    # -----------------------------------------------------
    # 7. S3 URL 생성
    # -----------------------------------------------------

    for index, result in enumerate(
        top_results,
        start=1,
    ):

        result["rank"] = (
            index
        )

        result["similarity"] = (
            round(
                result[
                    "similarity"
                ],
                4,
            )
        )

        result["image_url"] = (
            get_image_url(
                result[
                    "s3_key"
                ]
            )
        )


    # -----------------------------------------------------
    # 8. 결과 반환
    # -----------------------------------------------------

    return {
        "query_description":
            query_description,

        "results":
            top_results,
    }