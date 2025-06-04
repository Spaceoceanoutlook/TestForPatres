from pydantic import BaseModel, EmailStr, Field, ConfigDict
from .base import BaseResponse

class ReaderBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., max_length=200)

class ReaderCreate(ReaderBase):
    pass

class Reader(ReaderBase, BaseResponse):
    model_config = ConfigDict(from_attributes=True)
