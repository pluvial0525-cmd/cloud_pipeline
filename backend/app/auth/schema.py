from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)


# =========================================================
# 회원가입 요청
# =========================================================

class SignupRequest(
    BaseModel
):

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        min_length=4,
        max_length=100,
    )


# =========================================================
# 로그인 요청
# =========================================================

class LoginRequest(
    BaseModel
):

    username: str

    password: str


# =========================================================
# 사용자 응답
# =========================================================

class UserResponse(
    BaseModel
):

    id: int

    username: str

    email: str


# =========================================================
# 로그인 응답
# =========================================================

class LoginResponse(
    BaseModel
):

    access_token: str

    token_type: str = "bearer"

    user: UserResponse