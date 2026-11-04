from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
from core.models import TimestampBase


# --------------------------------------------------
# 4. LLMResponse
# --------------------------------------------------
class LLMResponseBase(SQLModel):
    content: str = Field()
    context: str = Field()


class LLMResponse(LLMResponseBase, TimestampBase, table=True):
    __tablename__ = "llm_response"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_request_id: int = Field(default=None, foreign_key="user_request.id", unique=True)
    user_request: Optional["UserRequest"] = Relationship(back_populates="llm_response")


# --------------------------------------------------
# 3. UserRequest
# --------------------------------------------------
class UserRequestBase(SQLModel):
    request_text: str = Field()


class UserRequest(UserRequestBase, TimestampBase, table=True):
    __tablename__ = "user_request"

    id: Optional[int] = Field(default=None, primary_key=True)

    play_session_id: int = Field(default=None, foreign_key="play_session.id")
    play_session: Optional["PlaySession"] = Relationship(back_populates="user_requests")

    llm_response: Optional[LLMResponse] = Relationship(
        back_populates="user_request",
        sa_relationship_kwargs={"uselist": False},
    )


# --------------------------------------------------
# 2. PlaySession
# --------------------------------------------------
class PlaySessionBase(SQLModel):
    session_title: str = Field()


class PlaySession(PlaySessionBase, TimestampBase, table=True):
    __tablename__ = "play_session"

    id: Optional[int] = Field(default=None, primary_key=True)

    play_session_setup_id: int = Field(default=None, foreign_key="play_session_setup.id")
    play_session_setup: Optional["PlaySessionSetup"] = Relationship(back_populates="play_sessions")

    user_requests: List[UserRequest] = Relationship(back_populates="play_session")


# --------------------------------------------------
# 1. PlaySessionSetup
# --------------------------------------------------
class PlaySessionSetupBase(SQLModel):
    setup_title: str = Field()
    setup_description: str = Field()
    setup_script: str = Field()


class PlaySessionSetup(PlaySessionSetupBase, table=True):
    __tablename__ = "play_session_setup"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Note: list["PlaySession"] works here without future annotations
    play_sessions: List[PlaySession] = Relationship(back_populates="play_session_setup")


class PlaySessionSetupCreate(PlaySessionSetupBase):
    pass


class PlaySessionSetupPublic(PlaySessionSetupBase):
    id: int


class PlaySessionSetupListPublic(SQLModel):
    id: int
    setup_title: str
    setup_description: str