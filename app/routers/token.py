from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt, bcrypt, os
from fastapi import APIRouter, HTTPException, Request, status 
from sqlmodel import select

from db import SessionDep
from models import User, UserCreate

router = APIRouter()

load_dotenv('.env')

secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')
expiration_time = os.getenv('ACCESS_TOKEN_EXPIRE_SECONDS')


class TokenData:
    def __init__(self, user: dict):
        self.user = user


@router.post('/token', tags=['Token'])
async def login_for_access_token(user_data: UserCreate, session: SessionDep):
    user_data = user_data.model_dump()
    user = session.exec(select(User).where(User.username == user_data['username'])).first()
    
    is_valid = bcrypt.checkpw(str(user_data['password']).encode('utf-8'), user.password.encode('utf-8'))
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"}
            )
    
    payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=int(expiration_time))
        }
    
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    
    return {"access_token": token, "token_type": "bearer"}


def verify_token(token: str):

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return None 
    except jwt.InvalidSignatureError:
        return None 
    except jwt.DecodeError:
        return None 


class Auth(HTTPBearer):
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        payload = verify_token(credentials.credentials)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})

        return TokenData(user=payload)