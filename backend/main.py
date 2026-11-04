from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.database import init_db
from memos.router import router as memo_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 DB 테이블 초기화
    init_db()
    yield
app = FastAPI(title="FastTRPG", lifespan=lifespan)

app.include_router(memo_router)