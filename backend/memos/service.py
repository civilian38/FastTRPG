from sqlmodel import Session, select
from .models import Memo, MemoCreate

def create_memo(session: Session, memo_in: MemoCreate) -> Memo:
    db_memo = Memo.model_validate(memo_in)
    session.add(db_memo)
    session.commit()
    session.refresh(db_memo)
    return db_memo

def get_memos(session: Session) -> list[Memo]:
    statement = select(Memo)
    return list(session.exec(statement).all())

def get_memo_by_id(session: Session, memo_id: int) -> Memo | None:
    return session.get(Memo, memo_id)