from pydantic import BaseModel


class UserCreateModel(BaseModel):
    name: str
    surname: str
    password: str


class UserUpdateModel(BaseModel):
    name: str
    surname: str
