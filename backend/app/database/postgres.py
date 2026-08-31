from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
)

from app.config import (
    DATABASE_URL,
)


# =========================================================
# PostgreSQL Engine
# =========================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# =========================================================
# Session
# =========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# =========================================================
# Base Model
# =========================================================

class Base(
    DeclarativeBase
):
    pass


# =========================================================
# DB Dependency
# =========================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()