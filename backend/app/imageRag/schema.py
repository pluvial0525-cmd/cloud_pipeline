from pydantic import BaseModel


class ImageRagResult(BaseModel):
    rank: int
    food_name: str
    image_path: str
    similarity: float


class ImageRagResponse(BaseModel):
    query_description: str
    results: list[ImageRagResult]