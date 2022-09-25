# Python

from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, status

app = FastAPI()


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str
    state: str
    country: str


# Models
class Person(BaseModel):
    """Field(...)  es para declarar el campo como obligatorio"""

    first_name: str = Field(..., min_length=1, max_length=50, example="Marco")
    last_name: str = Field(..., min_length=1, max_length=40)
    age: int = Field(..., gt=0, le=115)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    password: str = Field(..., min_length=8)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo",
    #             "last_name": "Garcia Martoni",
    #             "age": 21,
    #             "hair_color": "blonde",
    #             "is_married": False
    #         }
    #     }


@app.get(path="/", status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "World"}


# Request and Response Body


@app.post(
    path="/person/new",
    response_model=Person,
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED,
)
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters
@app.get(path="/person/detail", status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 charters",
    ),
    age: str = Query(..., title="Person Age", description="This is the person age. It's required"),
):
    return {name: age}


# Validaciones: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(..., gt=0)):
    """Path(...) 3 puntos para inticar que el parametro es obligatorio"""
    return {person_id: "It exists!"}


# Validaciones: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(..., title="Person ID", description="This is the person ID", gt=0),
    person: Person = Body(...),
    # location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())

    return person
