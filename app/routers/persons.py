from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Person

router = APIRouter()

@router.get('/', tags=['Person'], response_model=Person, status_code=status.HTTP_200_OK)
async def list_person(session: SessionDep):
    persons = session.exec(select(Person)).all()
    if not persons:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person doens't found.")
    return persons