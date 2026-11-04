from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from sqlalchemy import func

class TimestampBase(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )