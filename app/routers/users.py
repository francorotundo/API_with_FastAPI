from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
import bcrypt

from app.routers.token import Auth, TokenData
from db import SessionDep
from models import User, UserCreate

router = APIRouter()

@router.get('/users', response_model=List[User], tags=['User'])
async def list_user(session: SessionDep, auth: TokenData = Depends(Auth())):
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Without data yet.")
    return users

@router.post('/user', tags=['User'])
async def create_user(user_data: UserCreate, session: SessionDep, auth: TokenData = Depends(Auth())):
    user_data = user_data.model_dump()
    
    password = user_data['password'].encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    user_data['password'] = hashed
    
    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    return {"message": "User created correctly."} 
    