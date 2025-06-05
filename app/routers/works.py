from fastapi import APIRouter
from sqlmodel import select

from db import SessionDep
from models import Work

router = APIRouter()

@router.get('/persons/{person_id}/works/', response_model=list[Work], tags=['Work'])
async def list_persons_work(person_id: int, session: SessionDep):
    works = session.exec(select(Work).where(person_id == person_id)).all()
    return works