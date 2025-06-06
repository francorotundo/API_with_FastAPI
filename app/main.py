from fastapi import FastAPI
from db import create_all_tables
from app.routers import persons, token, users, works

app = FastAPI(lifespan=create_all_tables)

app.include_router(persons.router)
app.include_router(works.router)
app.include_router(users.router)
app.include_router(token.router)