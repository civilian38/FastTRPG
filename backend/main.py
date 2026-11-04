from contextlib import asynccontextmanager
from fastapi import FastAPI
from memos.router import router as memo_router
from trpg.controllers import controller as trgp_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
app = FastAPI(title="FastTRPG", lifespan=lifespan)

app.include_router(memo_router)
app.include_router(trgp_controller)
