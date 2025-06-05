from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import SessionDep
from models import Person, Work, WorkCreate

router = APIRouter()

@router.get('/persons/{person_id}/works/', response_model=list[Work], tags=['Work'])
async def list_persons_work(person_id: int, session: SessionDep):
    works = session.exec(select(Work).where(person_id == person_id)).all()
    return works

@router.post('/persons/{person_id}/works/', tags=['Work'], status_code=status.HTTP_201_CREATED)
async def create_persons_work(person_id: int, work_data: WorkCreate, session: SessionDep):
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found.")
    
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
    

@router.get('/persons/works/{work_id}', tags=['Work'])
async def detail_persons_work(work_id: int, session: SessionDep):
    work = session.get(Work, work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found.")
    return work