from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from testforpatres.dependencies import get_current_user
from testforpatres.database import get_db
from testforpatres.schemas.borrowed_books import BorrowBook, ReturnBook, BorrowedBookWithRelations
from testforpatres.crud import borrowed as borrowed_crud

router = APIRouter(
    prefix="/borrow",
    tags=["borrow"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/issue", response_model=BorrowedBookWithRelations)
def issue_book(data: BorrowBook, db: Session = Depends(get_db)):
    borrowed = borrowed_crud.borrow_book(db, data.book_id, data.reader_id)
    if not borrowed:
        raise HTTPException(status_code=400, detail="Cannot issue book: no copies available or limit exceeded")
    return borrowed

@router.post("/return", status_code=status.HTTP_204_NO_CONTENT)
def return_book(data: ReturnBook, db: Session = Depends(get_db)):
    success = borrowed_crud.return_book(db, data.book_id, data.reader_id)
    if not success:
        raise HTTPException(status_code=400, detail="Book not borrowed or already returned")
    return None

@router.get("/reader/{reader_id}", response_model=List[BorrowedBookWithRelations])
def get_borrowed_books(reader_id: int, db: Session = Depends(get_db)):
    borrowed_books = borrowed_crud.get_borrowed_books_by_reader(db, reader_id)
    return borrowed_books
