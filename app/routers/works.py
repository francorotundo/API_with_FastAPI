from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.routers.token import Auth, TokenData
from db import SessionDep
from models import Person, Work, WorkCreate, WorkUpdate

from .error_404 import error_404

router = APIRouter()
  

@router.get('/persons/{person_id}/works', response_model=list[Work], tags=['Work'])
async def list_persons_work(person_id: int, session: SessionDep, auth: TokenData = Depends(Auth())):
    works = session.exec(select(Work).where(person_id == person_id)).all()
    if not works:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Without data yet.")
    return works

@router.post('/persons/{person_id}/works', tags=['Work'], status_code=status.HTTP_201_CREATED)
async def create_persons_work(person_id: int, work_data: WorkCreate, session: SessionDep, auth: TokenData = Depends(Auth())):
    person = session.get(Person, person_id)
    
    error_404("Person", person)
    
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
    

@router.get('/persons/works/{work_id}', response_model=Work, tags=['Work'])
async def detail_persons_work(work_id: int, session: SessionDep, auth: TokenData = Depends(Auth())):
    work = session.get(Work, work_id)
    error_404("Work", work)
    return work


@router.patch('/persons/works/{work_id}', tags=['Work'])
async def update_persons_work(work_id: int, work_data: WorkUpdate, session: SessionDep, auth: TokenData = Depends(Auth())):
    work = session.get(Work, work_id)
    error_404("Work", work)
    work.sqlmodel_update(work_data.model_dump(exclude_unset=True))
    session.add(work)
    session.commit()
    session.refresh(work)
    return {
        "message": "Work updated correctly.",
        "data": work
    }
    
    
@router.delete('/persons/works/{work_id}', tags=['Work'])
async def delete_persons_work(work_id: int, session: SessionDep, auth: TokenData = Depends(Auth())):
    work = session.get(Work, work_id)
    error_404('Work', work)
    session.delete(work)
    session.commit()
    return {"message": "Work deleted correctly."}