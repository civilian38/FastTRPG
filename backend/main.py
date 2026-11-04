from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.database import init_db
from memos.router import router as memo_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
app = FastAPI(title="FastTRPG", lifespan=lifespan)

app.include_router(memo_router)