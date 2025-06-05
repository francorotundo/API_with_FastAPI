from fastapi import FastAPI
from db import create_all_tables
from app.routers import persons

app = FastAPI(lifespan=create_all_tables)

app.include_router(persons.router)