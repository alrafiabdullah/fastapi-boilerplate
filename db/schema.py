from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class UserSchema(BaseModel):
    id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True


class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(None, title="Parameter")


class RequestUser(BaseModel):
    parameter: UserSchema = Field(..., example={
        "full_name": "Abdullah Al Rafi",
        "email": "abdullah@al.com",
        "password": "123456"
    })


class RequestLogin(BaseModel):
    parameter: UserSchema = Field(..., example={
        "email": "abdullah@al.com",
        "password": "123456",
    })


class Response(GenericModel, Generic[T]):
    data: Optional[T] = Field(None, title="Data")
    message: Optional[str] = Field(None, title="Message")
    code: Optional[int] = Field(None, title="Code")
