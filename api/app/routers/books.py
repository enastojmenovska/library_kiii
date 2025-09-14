from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..deps import get_db
from ..models import Book, Author, Genre
from ..schemas import BookCreate, BookUpdate, BookOut

router = APIRouter(prefix="/api/books", tags=["books"])

@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    # Optional FK existence checks (minimal)
    if payload.author_id and not db.get(Author, payload.author_id):
        raise HTTPException(status_code=400, detail="author_id does not exist")
    if payload.genre_id and not db.get(Genre, payload.genre_id):
        raise HTTPException(status_code=400, detail="genre_id does not exist")

    b = Book(
        title=payload.title,
        author_id=payload.author_id,
        genre_id=payload.genre_id,
        year=payload.year,
        isbn=payload.isbn,
    )
    db.add(b)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create book") from e
    db.refresh(b)
    return b

@router.get("", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).order_by(Book.id.asc()).all()

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    b = db.get(Book, book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    return b

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    b = db.get(Book, book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")

    # Minimal field-by-field update
    if payload.title is not None:
        b.title = payload.title
    if payload.author_id is not None:
        if payload.author_id and not db.get(Author, payload.author_id):
            raise HTTPException(status_code=400, detail="author_id does not exist")
        b.author_id = payload.author_id
    if payload.genre_id is not None:
        if payload.genre_id and not db.get(Genre, payload.genre_id):
            raise HTTPException(status_code=400, detail="genre_id does not exist")
        b.genre_id = payload.genre_id
    if payload.year is not None:
        b.year = payload.year
    if payload.isbn is not None:
        b.isbn = payload.isbn

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update book") from e
    db.refresh(b)
    return b

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    b = db.get(Book, book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(b)
    db.commit()
