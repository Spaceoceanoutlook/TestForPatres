import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testforpatres.models import Base, Book, Reader
from testforpatres.crud import borrowed as borrow_crud

# SQLite в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def create_sample_data(db):
    book = Book(title="Sample Book", author="Author", copies_available=3)
    reader = Reader(name="Test Reader", email="reader@example.com")
    db.add(book)
    db.add(reader)
    db.commit()
    return book, reader

def test_borrow_book_success(db):
    book, reader = create_sample_data(db)
    borrowed = borrow_crud.borrow_book(db, book.id, reader.id)
    assert borrowed is not None
    assert borrowed.book_id == book.id
    assert borrowed.reader_id == reader.id

def test_borrow_book_no_copies(db):
    book, reader = create_sample_data(db)
    book.copies_available = 0
    db.commit()
    borrowed = borrow_crud.borrow_book(db, book.id, reader.id)
    assert borrowed is None

def test_borrow_book_limit_exceeded(db):
    book, reader = create_sample_data(db)
    for _ in range(3):
        borrow_crud.borrow_book(db, book.id, reader.id)
    # Пытаемся взять 4-ю книгу
    result = borrow_crud.borrow_book(db, book.id, reader.id)
    assert result is None
