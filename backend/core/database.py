from typing import Annotated, Generator
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'database.db'}"
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def init_db() -> None:
    """테이블 자동 생성 (앱 시작 시 호출)"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """요청 단위 세션 제어"""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]