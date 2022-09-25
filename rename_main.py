# Python

from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, EmailStr

# FastAPI
from fastapi import FastAPI, Header, Cookie, UploadFile, File
from fastapi import Body, Query, Path, Form, status
from fastapi import HTTPException

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


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="miguel20")
    message: str = Field(default="Login succesfully")


@app.get(path="/", status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "World"}


# Request and Response Body
@app.post(
    path="/person/new",
    response_model=Person,
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
)
def create_person(person: Person = Body(...)):
    """
    Crear Persona

    Esta path operation cra una persona en la app y guarda la informacion en la base de datos

    Parameters:
    - Request body parameter:
        - **person: Person** -> Modelo de una persona con el primer nombre, segundo nombre,
        apellido, edad, color de pelo y estatus civil.
    Returns
    retorna un modelo de persona con su primer nombre, apellidos, edad, color de pelo y estado civil
    """
    return person


# Validaciones: Query Parameters
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Crear persona en la app",
    deprecated=True,  #Permite deprecar un endpoint
)
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


persons = [1, 2, 3, 4, 5]


# Validaciones: Path Parameters
@app.get(path="/person/detail/{person_id}", tags=["Persons"])
def show_person(person_id: int = Path(..., gt=0)):
    """Path(...) 3 puntos para inticar que el parametro es obligatorio"""
    if person_id not in persons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esta persona no existe!")
    return {person_id: "Si existe!"}


# Validaciones: Request Body
@app.put(path="/person/{person_id}", tags=["Persons"])
def update_person(
    person_id: int = Path(..., title="Person ID", description="This is the person ID", gt=0),
    person: Person = Body(...),
    # location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())

    return person


@app.post(path="/login", response_model=LoginOut, status_code=status.HTTP_200_OK, tags=["Auth"])
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


@app.post(path="/contact", status_code=status.HTTP_200_OK)
def contact(
    first_name: str = Form(..., max_length=20, min_length=1),
    last_name: str = Form(..., max_length=20, min_length=1),
    email: EmailStr = Form(...),
    message: str = Form(..., min_length=20),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
):
    return user_agent


# Files
@app.post(path="/post-image")
def post_image(image: UploadFile = File(...)):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, ndigits=2),
    }
