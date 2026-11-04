from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# --- [1] SQLModel 및 프로젝트 모듈 import 추가 ---
import os
import sys
from pathlib import Path

# backend 경로를 sys.path에 추가 (파이썬 import 경로 문제 방지)
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlmodel import SQLModel
from core.database import DATABASE_URL

# 주의: Alembic이 테이블을 감지하려면 모델 모듈을 반드시 import해야 합니다!
from memos.models import Memo  # noqa: F401
from trpg.models import PlaySessionSetup
# --------------------------------------------------

config = context.config

# --- [2] alembic.ini의 DB 주소 대신 core/database.py의 DATABASE_URL 사용 ---
config.set_main_option("sqlalchemy.url", DATABASE_URL)
# --------------------------------------------------------------------------

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- [3] target_metadata를 SQLModel.metadata로 변경 ---
target_metadata = SQLModel.metadata
# -----------------------------------------------------


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # SQLite 컬럼 변경(ALTER)을 위해 필수 권장
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # SQLite의 check_same_thread 옵션을 위해 커넥션 인자 전달 처리
    connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # SQLite 컬럼 변경/삭제 시 필수 옵션!
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()