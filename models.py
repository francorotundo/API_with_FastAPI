from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import date

class PersonCreate(SQLModel):
    name : Optional[str] = None 
    lastname : Optional[str] = None 
    nationality: Optional[str] = None 
    year: Optional[int] = None 
    
    
class Person(PersonCreate, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    works: List['Work'] = Relationship(back_populates="person")
    
    
class WorkCreate(SQLModel):
    company: Optional[str] = None
    initContract: Optional[date] = None
    finishContract: Optional[date] = None
         
         
class Work(WorkCreate, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(foreign_key="person.id")
    person: Person = Relationship(back_populates='works')