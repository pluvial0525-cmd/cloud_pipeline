from pathlib import Path
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError

from app.config import (
    AWS_REGION,
    AWS_S3_BUCKET,
    AWS_S3_IMAGE_PREFIX,
)


# =========================================================
# S3 Client
# =========================================================

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
)


# =========================================================
# S3 Key 정규화
# =========================================================

def normalize_s3_key(
    key: str,
) -> str:

    key = key.replace(
        "\\",
        "/",
    )

    key = key.lstrip("/")

    return key


# =========================================================
# 이미지 Key 생성
# =========================================================

def create_image_key(
    filename: str,
    food_name: str | None = None,
) -> str:

    suffix = (
        Path(filename)
        .suffix
        .lower()
    )

    if not suffix:
        suffix = ".jpg"

    unique_filename = (
        f"{uuid4().hex}{suffix}"
    )

    if food_name:
        return (
            f"{AWS_S3_IMAGE_PREFIX}/"
            f"{food_name}/"
            f"{unique_filename}"
        )

    return (
        f"{AWS_S3_IMAGE_PREFIX}/"
        f"{unique_filename}"
    )


# =========================================================
# CREATE
# 이미지 업로드
# =========================================================

def upload_image(
    image_bytes: bytes,
    filename: str,
    content_type: str,
    food_name: str | None = None,
) -> str:

    key = create_image_key(
        filename=filename,
        food_name=food_name,
    )

    s3_client.put_object(
        Bucket=AWS_S3_BUCKET,
        Key=key,
        Body=image_bytes,
        ContentType=content_type,
    )

    return key


# =========================================================
# READ
# 이미지 다운로드
# =========================================================

def get_image(
    key: str,
) -> bytes:

    key = normalize_s3_key(
        key
    )

    response = s3_client.get_object(
        Bucket=AWS_S3_BUCKET,
        Key=key,
    )

    return (
        response["Body"]
        .read()
    )


# =========================================================
# READ
# 이미지 목록
# =========================================================

def list_images() -> list[str]:

    prefix = (
        f"{AWS_S3_IMAGE_PREFIX}/"
    )

    keys = []

    paginator = (
        s3_client
        .get_paginator(
            "list_objects_v2"
        )
    )

    for page in paginator.paginate(
        Bucket=AWS_S3_BUCKET,
        Prefix=prefix,
    ):

        contents = page.get(
            "Contents",
            [],
        )

        for item in contents:

            key = item["Key"]

            if not key.endswith("/"):
                keys.append(
                    key
                )

    return keys


# =========================================================
# READ
# Presigned URL 생성
# =========================================================

def get_image_url(
    key: str,
    expires_in: int = 3600,
) -> str:

    key = normalize_s3_key(
        key
    )

    return (
        s3_client
        .generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket":
                    AWS_S3_BUCKET,

                "Key":
                    key,
            },
            ExpiresIn=expires_in,
        )
    )


# =========================================================
# UPDATE
# 기존 Key에 이미지 덮어쓰기
# =========================================================

def update_image(
    key: str,
    image_bytes: bytes,
    content_type: str,
) -> str:

    key = normalize_s3_key(
        key
    )

    s3_client.put_object(
        Bucket=AWS_S3_BUCKET,
        Key=key,
        Body=image_bytes,
        ContentType=content_type,
    )

    return key


# =========================================================
# DELETE
# 이미지 삭제
# =========================================================

def delete_image(
    key: str,
) -> None:

    key = normalize_s3_key(
        key
    )

    s3_client.delete_object(
        Bucket=AWS_S3_BUCKET,
        Key=key,
    )


# =========================================================
# 이미지 존재 확인
# =========================================================

def image_exists(
    key: str,
) -> bool:

    key = normalize_s3_key(
        key
    )

    try:

        s3_client.head_object(
            Bucket=AWS_S3_BUCKET,
            Key=key,
        )

        return True

    except ClientError as e:

        error_code = (
            e.response
            .get(
                "Error",
                {},
            )
            .get(
                "Code"
            )
        )

        if error_code in {
            "404",
            "NoSuchKey",
            "NotFound",
        }:
            return False

        raise