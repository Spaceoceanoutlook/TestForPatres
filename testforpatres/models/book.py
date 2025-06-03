from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Book(Base):
    __tablename__ = 'books'
    __table_args__ = (
        CheckConstraint('copies_available >= 0', name='check_copies_non_negative'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    publication_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    isbn: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    copies_available: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    borrowings = relationship("BorrowedBook", back_populates="book")
