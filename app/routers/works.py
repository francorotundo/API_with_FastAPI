from fastapi import APIRouter
from sqlmodel import select

from db import SessionDep
from models import Work, WorkCreate

router = APIRouter()

@router.get('/persons/{person_id}/works/', response_model=list[Work], tags=['Work'])
async def list_persons_work(person_id: int, session: SessionDep):
    works = session.exec(select(Work).where(person_id == person_id)).all()
    return works

@router.post('/persons/{person_id}/works/', tags=['Work'])
async def create_persons_work(person_id: int, work_data: WorkCreate, session: SessionDep):
    work_dict = work_data.model_dump()
    work_dict['person_id'] = person_id
    work = Work.model_validate(work_dict)
    session.add(work)
    session.commit()
    session.refresh(work)
    return {
        "message": "Person's work inserted correctly.",
        "data": work
            }