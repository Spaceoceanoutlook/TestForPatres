from sqlalchemy.orm import Session
from testforpatres.models.borrowed_book import BorrowedBook
from testforpatres.models.book import Book
from datetime import datetime, timezone

MAX_BORROWED_BOOKS = 3

def borrow_book(db: Session, book_id: int, reader_id: int) -> BorrowedBook | None:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.copies_available < 1:
        return None

    active_borrows_count = db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    ).count()

    if active_borrows_count >= MAX_BORROWED_BOOKS:
        return None

    borrowed = BorrowedBook(
        book_id=book_id,
        reader_id=reader_id,
        borrow_date=datetime.now(timezone.utc)
    )
    book.copies_available -= 1
    db.add(borrowed)
    db.commit()
    db.refresh(borrowed)
    return borrowed

def return_book(db: Session, book_id: int, reader_id: int) -> bool:
    borrowed = db.query(BorrowedBook).filter(
        BorrowedBook.book_id == book_id,
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    ).first()

    if not borrowed:
        return False

    borrowed.return_date = datetime.now(timezone.utc)

    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.copies_available += 1

    db.commit()
    return True

def get_borrowed_books_by_reader(db: Session, reader_id: int):
    return db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    ).all()
