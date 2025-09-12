from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..deps import get_db
from ..models import Author
from ..schemas import AuthorCreate, AuthorUpdate, AuthorOut

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post("", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author(payload: AuthorCreate, db: Session = Depends(get_db)):
    a = Author(name=payload.name)
    db.add(a)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create author") from e
    db.refresh(a)
    return a

@router.get("", response_model=list[AuthorOut])
def list_authors(db: Session = Depends(get_db)):
    return db.query(Author).order_by(Author.id.asc()).all()

@router.get("/{author_id}", response_model=AuthorOut)
def get_author(author_id: int, db: Session = Depends(get_db)):
    a = db.get(Author, author_id)
    if not a:
        raise HTTPException(status_code=404, detail="Author not found")
    return a

@router.put("/{author_id}", response_model=AuthorOut)
def update_author(author_id: int, payload: AuthorUpdate, db: Session = Depends(get_db)):
    a = db.get(Author, author_id)
    if not a:
        raise HTTPException(status_code=404, detail="Author not found")
    if payload.name is not None:
        a.name = payload.name
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update author") from e
    db.refresh(a)
    return a

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    a = db.get(Author, author_id)
    if not a:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(a)
    db.commit()
