from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from .base import BaseResponse

class BorrowBook(BaseModel):
    book_id: int
    reader_id: int

class ReturnBook(BaseModel):
    book_id: int
    reader_id: int

class BorrowedBookOut(BaseResponse):
    book_id: int
    reader_id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class BorrowedBookWithRelations(BorrowedBookOut):
    book: 'Book'
    reader: 'Reader'

    model_config = ConfigDict(from_attributes=True)

# Для разрешения циклических импортов
from .books import Book
from .readers import Reader
BorrowedBookWithRelations.model_rebuild()
