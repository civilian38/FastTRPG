from sqlmodel import Field, SQLModel

class MemoBase(SQLModel):
    content: str = Field()

class Memo(MemoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class MemoCreate(MemoBase):
    content: str

class MemoPublic(MemoBase):
    id: int