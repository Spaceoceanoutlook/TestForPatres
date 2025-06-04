from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .book import Book
from .user import User
from .reader import Reader
from .borrowed_book import BorrowedBook