from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.auth.schema import (
    LoginRequest,
    LoginResponse,
    SignupRequest,
    UserResponse,
)
from app.auth.service import (
    create_user,
    login_user,
    logout_user,
)
from app.database.postgres import (
    get_db,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
)


# =========================================================
# 회원가입
# =========================================================

@router.post(
    "/signup",
    response_model=UserResponse,
)
def signup(
    request: SignupRequest,
    db: Session = Depends(
        get_db
    ),
):

    try:

        user = create_user(
            db=db,
            username=request.username,
            email=request.email,
            password=request.password,
        )

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# =========================================================
# 로그인
# =========================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(
        get_db
    ),
):

    try:

        user, token = login_user(
            db=db,
            username=request.username,
            password=request.password,
        )

        return LoginResponse(
            access_token=token,
            user=UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
            ),
        )

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e),
        )

# =========================================================
# 로그아웃
# =========================================================

@router.post(
    "/logout"
)
def logout(
    user_id: int,
):

    logout_user(
        user_id=user_id,
    )

    return {
        "message":
            "로그아웃 되었습니다."
    }