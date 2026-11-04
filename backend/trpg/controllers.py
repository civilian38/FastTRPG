from fastapi import APIRouter, status
from sqlmodel import select, col
from typing import cast

from .models import PlaySessionSetupPublic, PlaySessionSetupCreate, PlaySessionSetup, PlaySessionSetupListPublic
from core.database import SessionDep

controller = APIRouter(prefix="/trpg", tags=["trpg"])

@controller.post("/session_setups", response_model=PlaySessionSetupPublic, status_code=status.HTTP_201_CREATED)
def create_play_session_setup(setup_in: PlaySessionSetupCreate, session: SessionDep):
    db_play_session_setup = PlaySessionSetup.model_validate(setup_in)
    session.add(db_play_session_setup)
    session.commit()
    session.refresh(db_play_session_setup)
    return db_play_session_setup

@controller.get("/session_setups", response_model=list[PlaySessionSetupListPublic], status_code=status.HTTP_200_OK)
def get_play_session_setups(session: SessionDep):
    statement = select(
        col(PlaySessionSetup.id),
        col(PlaySessionSetup.setup_title),
        col(PlaySessionSetup.setup_description),
    )

    results = session.exec(statement).all()

    return [
        PlaySessionSetupListPublic(
            id=cast(int, setup_id),
            setup_title=title,
            setup_description=description,
        )
        for setup_id, title, description in results
    ]