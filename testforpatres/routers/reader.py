from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from testforpatres.dependencies import get_current_user
from testforpatres.database import get_db
from testforpatres.schemas.readers import ReaderCreate, Reader
from testforpatres.crud import reader as reader_crud

router = APIRouter(
    prefix="/readers",
    tags=["readers"],
    dependencies=[Depends(get_current_user)]  # Защита JWT
)

@router.post("/", response_model=Reader, status_code=status.HTTP_201_CREATED)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    return reader_crud.create_reader(db, reader)

@router.get("/", response_model=List[Reader])
def read_readers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return reader_crud.get_readers(db, skip=skip, limit=limit)

@router.get("/{reader_id}", response_model=Reader)
def read_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = reader_crud.get_reader(db, reader_id)
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return db_reader

@router.put("/{reader_id}", response_model=Reader)
def update_reader(reader_id: int, reader: ReaderCreate, db: Session = Depends(get_db)):
    db_reader = reader_crud.update_reader(db, reader_id, reader)
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return db_reader

@router.delete("/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    success = reader_crud.delete_reader(db, reader_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reader not found")
    return None
