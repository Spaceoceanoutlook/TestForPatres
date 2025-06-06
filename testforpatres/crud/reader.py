from sqlalchemy.orm import Session
from testforpatres.models.reader import Reader as ReaderModel
from testforpatres.schemas.readers import ReaderCreate

def create_reader(db: Session, reader: ReaderCreate) -> ReaderModel:
    db_reader = ReaderModel(**reader.dict())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

def get_readers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ReaderModel).offset(skip).limit(limit).all()

def get_reader(db: Session, reader_id: int):
    return db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()

def update_reader(db: Session, reader_id: int, reader: ReaderCreate):
    db_reader = get_reader(db, reader_id)
    if not db_reader:
        return None
    for key, value in reader.dict().items():
        setattr(db_reader, key, value)
    db.commit()
    db.refresh(db_reader)
    return db_reader

def delete_reader(db: Session, reader_id: int):
    db_reader = get_reader(db, reader_id)
    if not db_reader:
        return False
    db.delete(db_reader)
    db.commit()
    return True
