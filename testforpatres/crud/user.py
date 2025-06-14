from sqlalchemy.orm import Session
from testforpatres.models.user import User
from testforpatres.schemas.user import UserCreate
from testforpatres.security import get_password_hash
from pydantic import EmailStr


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
