from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class RoleUpdate(BaseModel):
    role: str
