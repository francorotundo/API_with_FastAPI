from fastapi import FastAPI
from db import create_all_tables
from app.routers import persons, works

app = FastAPI(lifespan=create_all_tables)

app.include_router(persons.router)
app.include_router(works.router)