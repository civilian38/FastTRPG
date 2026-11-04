from fastapi import APIRouter, status, HTTPException
from sqlmodel import select, col
from typing import cast

from .models import (PlaySessionSetupPublic, PlaySessionSetupCreate, PlaySessionSetup, PlaySessionSetupListPublic,
                     PlaySession, PlaySessionCreate, PlaySessionPublic)
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

@controller.post("/sessions/{setup_id}", response_model=PlaySessionPublic, status_code=status.HTTP_201_CREATED)
def create_play_session(setup_id: int, play_session_in: PlaySessionCreate, session: SessionDep):
    db_play_session_setup = session.get(PlaySessionSetup, setup_id)
    if not db_play_session_setup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db_play_session = PlaySession(
        session_title=play_session_in.session_title,
        play_session_setup_id=cast(int, setup_id),
    )
    session.add(db_play_session)
    session.commit()
    session.refresh(db_play_session)
    return db_play_session

@controller.get("/sessions/all", response_model=list[PlaySessionPublic], status_code=status.HTTP_200_OK)
def get_all_sessions(session: SessionDep):

    # TODO: CursorPaginationImplementation

    statement = select(PlaySession)
    return list(session.exec(statement).all())
