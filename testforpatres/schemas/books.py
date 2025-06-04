from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .base import BaseResponse

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    publication_year: Optional[int] = Field(None, ge=0)
    isbn: Optional[str] = Field(None, max_length=20)
    copies_available: int = Field(default=1, ge=0)
    description: Optional[str] = Field(None, max_length=500)

class BookCreate(BookBase):
    pass

class Book(BookBase, BaseResponse):
    model_config = ConfigDict(from_attributes=True)
