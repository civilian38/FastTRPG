from fastapi import APIRouter, status

from .models import MemoCreate, MemoPublic
from memos import service
from core.database import SessionDep

router = APIRouter(prefix="/memos", tags=["memos"])

@router.post("/", response_model=MemoPublic, status_code=status.HTTP_201_CREATED)
def create_memo(memo_in: MemoCreate, session: SessionDep):
    return service.create_memo(session, memo_in)

@router.get("/", response_model=list[MemoPublic], status_code=status.HTTP_200_OK)
def read_memos(session: SessionDep):
    return service.get_memos(session)

@router.get("/{memo_id}", response_model=MemoPublic, status_code=status.HTTP_200_OK)
def read_memo_by_id(memo_id: int, session: SessionDep):
    return service.get_memo_by_id(session, memo_id)