from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class Reader(Base):
    __tablename__ = 'readers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)

    borrowings = relationship("BorrowedBook", back_populates="reader")
