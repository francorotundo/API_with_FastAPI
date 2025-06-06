from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from app.routers.token import Auth, TokenData
from db import SessionDep
from models import Person, PersonCreate

from .error_404 import error_404

router = APIRouter()

@router.get('/persons', tags=['Person'], response_model=List[Person], status_code=status.HTTP_200_OK)
async def list_person(session: SessionDep, auth: TokenData = Depends(Auth())):
    persons = session.exec(select(Person)).all()
    if not persons:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Without data yet.")
    return persons


@router.post('/persons', tags=['Person'], status_code=status.HTTP_201_CREATED)
async def create_person(person_data: PersonCreate, session: SessionDep, auth: TokenData = Depends(Auth())):
    person = Person.model_validate(person_data.model_dump())
    session.add(person)
    session.commit()
    session.refresh(person)
    return {"message": "Person created correctly.", "data": person }
    

@router.get('/persons/{person_id}', tags=['Person'], response_model=Person, status_code=status.HTTP_200_OK)
async def detail_person(person_id: int, session: SessionDep, auth: TokenData = Depends(Auth())):
    person = session.get(Person, person_id)
    error_404("Person", person)
    return person


@router.patch('/persons/{person_id}', tags=['Person'])
async def update_person(person_id: int, person_data: PersonCreate, session: SessionDep, auth: TokenData = Depends(Auth())):
    person = session.get(Person, person_id)
    error_404("Person", person)
    person_update = person_data.model_dump(exclude_unset=True)
    person.sqlmodel_update(person_update)
    session.add(person)
    session.commit()
    return {"message": "Person updated correctly."}


@router.delete('/persons/{person_id}', tags=['Person'])
async def delete_person(person_id: int, session: SessionDep, auth: TokenData = Depends(Auth())):
    person = session.get(Person, person_id)
    error_404("Person", person)
    session.delete(person)
    session.commit()
    return {"message": "Person deleted correctly."}


