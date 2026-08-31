from datetime import (
    datetime,
    timedelta,
    timezone,
)

from jose import jwt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.model import User
from app.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
)
from app.database.redis import redis_client
import bcrypt


# =========================================================
# Password
# =========================================================


# =========================================================
# 비밀번호 해시
# =========================================================

# =========================================================
# 비밀번호 해시
# =========================================================

def hash_password(
    password: str,
) -> str:

    password_bytes = password.encode(
        "utf-8"
    )

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    )

    return hashed_password.decode(
        "utf-8"
    )


# =========================================================
# 비밀번호 검증
# =========================================================

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:

    return bcrypt.checkpw(
        plain_password.encode(
            "utf-8"
        ),
        hashed_password.encode(
            "utf-8"
        ),
    )
def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:

    statement = (
        select(User)
        .where(
            User.username
            == username
        )
    )

    return (
        db.execute(
            statement
        )
        .scalar_one_or_none()
    )


# =========================================================
# Email 중복 확인
# =========================================================

def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:

    statement = (
        select(User)
        .where(
            User.email
            == email
        )
    )

    return (
        db.execute(
            statement
        )
        .scalar_one_or_none()
    )


# =========================================================
# 회원가입
# =========================================================

def create_user(
    db: Session,
    username: str,
    email: str,
    password: str,
) -> User:

    if get_user_by_username(
        db,
        username,
    ):
        raise ValueError(
            "이미 사용 중인 사용자 이름입니다."
        )

    if get_user_by_email(
        db,
        email,
    ):
        raise ValueError(
            "이미 사용 중인 이메일입니다."
        )

    user = User(
        username=username,
        email=email,
        password_hash=(
            hash_password(
                password
            )
        ),
    )

    db.add(
        user
    )

    db.commit()

    db.refresh(
        user
    )

    return user


# =========================================================
# JWT Access Token 생성
# =========================================================

def create_access_token(
    user: User,
) -> str:

    expire = (
        datetime.now(
            timezone.utc
        )
        + timedelta(
            minutes=(
                ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )
    )

    payload = {
        "sub":
            str(
                user.id
            ),

        "username":
            user.username,

        "exp":
            expire,
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return token


# =========================================================
# Redis에 로그인 토큰 저장
# =========================================================

def save_login_token(
    user_id: int,
    token: str,
):

    redis_key = (
        f"login:"
        f"{user_id}"
    )

    redis_client.setex(
        redis_key,
        (
            ACCESS_TOKEN_EXPIRE_MINUTES
            * 60
        ),
        token,
    )


# =========================================================
# 로그인
# =========================================================

def login_user(
    db: Session,
    username: str,
    password: str,
):

    user = get_user_by_username(
        db,
        username,
    )

    if not user:
        raise ValueError(
            "사용자를 찾을 수 없습니다."
        )

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise ValueError(
            "비밀번호가 올바르지 않습니다."
        )

    access_token = (
        create_access_token(
            user
        )
    )

    save_login_token(
        user_id=user.id,
        token=access_token,
    )

    return (
        user,
        access_token,
    )

# =========================================================
# 로그아웃
# Redis 로그인 토큰 삭제
# =========================================================

def logout_user(
    user_id: int,
):

    redis_key = (
        f"login:"
        f"{user_id}"
    )

    redis_client.delete(
        redis_key
    )