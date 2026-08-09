from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone_number: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone_number: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class UpdateProfile(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str