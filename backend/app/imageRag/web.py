from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.imageRag.schema import (
    ImageRagResponse,
)

from app.imageRag.service import (
    search_similar_images,
)


router = APIRouter(
    prefix="/api/image-rag",
    tags=["Image RAG"],
)


@router.post(
    "/search",
    response_model=ImageRagResponse,
)
async def search_image(
    file: UploadFile = File(...),
    top_k: int = 5,
):

    # -----------------------------------------
    # 이미지 파일 확인
    # -----------------------------------------

    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="파일 형식을 확인할 수 없습니다.",
        )

    if not file.content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail="이미지 파일만 업로드 가능합니다.",
        )


    # -----------------------------------------
    # 이미지 읽기
    # -----------------------------------------

    image_bytes = await file.read()


    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="빈 이미지 파일입니다.",
        )


    # -----------------------------------------
    # Image RAG
    # -----------------------------------------

    try:

        result = search_similar_images(
            image_bytes=image_bytes,
            filename=file.filename
            or "upload.jpg",
            top_k=top_k,
        )

        return result


    except Exception as e:

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )