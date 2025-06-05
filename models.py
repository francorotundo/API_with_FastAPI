from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import date

class Person(SQLModel, table=True):
    id : Optional[int] = Field(primary_key=True)
    name : str 
    lastname : str
    works: List['Work'] = Relationship(back_populates="person")
    nationality: str
    year: int
    
        
    
class Work(SQLModel, table=True):
    id : Optional[int] = Field(primary_key=True)
    company: str
    initContract: date
    finishContract: date
    person_id: int = Field(foreign_key="person.id")
    person: Person = Relationship(back_populates='works')