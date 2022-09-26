# Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
from http import HTTPStatus

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# Fast API
from fastapi import FastAPI

app = FastAPI()


# Modelos
class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=64)


class User(UserBase):
    nombre: str = Field(..., min_length=1, max_length=50)
    apellido_paterno: str = Field(..., min_length=1, max_length=50)
    fecha_nacimiento: Optional[date] = Field(default=None)


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(..., min_length=1, max_length=256)
    created_at: datetime = Field(default=datetime.now())
    update_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)


# Path Operation




## Users
@app.post(
    path="/signip",
    response_model=User,
    status_code=HTTPStatus.CREATED,
    summary="RTegister a user",
    tags=["Users"],
)
def signup():
    pass


@app.post(
    path="/login",
    response_model=User,
    status_code=HTTPStatus.OK,
    summary="Loguear un usuario",
    tags=["Users"],
)
def login():
    pass


@app.get(
    path="/users",
    response_model=List[User],
    status_code=HTTPStatus.OK,
    summary="Muestra todos los usuarios",
    tags=["Users"],
)
def show_all_users():
    pass


@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=HTTPStatus.OK,
    summary="Show a user",
    tags=["Users"],
)
def show_a_user():
    pass


@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=HTTPStatus.OK,
    summary="Delete a user",
    tags=["Users"],
)
def delete_a_user():
    pass


@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=HTTPStatus.OK,
    summary="Update a user",
    tags=["Users"],
)
def update_a_user():
    pass


## Tweets

@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=HTTPStatus.OK,
    summary="Muestra todos los tweets",
    tags=["Tweets"]
)
def home():
    """ Muestra todos los tweets """
    return {"Twitter API": "Working"}


@app.get(
    path="/post",
    response_model=Tweet,
    status_code=HTTPStatus.CREATED,
    summary="Postea un tweet",
    tags=["Tweets"]
)
def post():
    """ Postea un tweet"""
    return {"Twitter API": "Working"}


@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=HTTPStatus.OK,
    summary="Postea un tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    """ Muestra un tweet """
    return {"Twitter API": "Working"}


@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=HTTPStatus.OK,
    summary="Elimina un tweet",
    tags=["Tweets"]
)
def elimina_un_tweet():
    """ Elimina un tweet """
    return {"Twitter API": "Working"}


@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=HTTPStatus.OK,
    summary="Actualiza un tweet",
    tags=["Tweets"]
)
def elimina_un_tweet():
    """ Actualiza un tweet """
    return {"Twitter API": "Working"}