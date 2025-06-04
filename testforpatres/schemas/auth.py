from pydantic import BaseModel, EmailStr, Field
from .base import BaseResponse

class UserCreate(BaseModel):
    email: EmailStr = Field(..., max_length=200)
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseResponse):
    email: EmailStr
