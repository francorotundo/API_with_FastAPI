from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import SessionDep
from models import User

router = APIRouter()

@router.get('/users', response_model=List[User], tags=['User'])
async def list_user(session: SessionDep):
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Without data yet.")
    return users