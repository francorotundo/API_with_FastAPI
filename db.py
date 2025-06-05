from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine

## URL de conexión a SQLite
sqlite_name = "db.sqlite3"
db_url = f"sqlite:///{sqlite_name}"

# creación de motor de base de datos
engine = create_engine(db_url)

# Crear las tablas si no existen
def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    
# Crear una sesión
def get_session():
    with Session(engine) as session:
        yield session
    
# Registro de dependencia para todos nuestro endpoints    
SessionDep = Annotated[Session, Depends(get_session)]