from sqlalchemy.orm import Session
from testforpatres.models.book import Book
from testforpatres.schemas.books import BookCreate

def create_book(db: Session, book_data: BookCreate) -> Book:
    db_book = Book(**book_data.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()

def update_book(db: Session, book_id: int, book_data: BookCreate) -> Book | None:
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    for key, value in book_data.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True
