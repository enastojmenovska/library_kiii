from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..deps import get_db
from ..models import Genre
from ..schemas import GenreCreate, GenreUpdate, GenreOut

router = APIRouter(prefix="/genres", tags=["genres"])

@router.post("", response_model=GenreOut, status_code=status.HTTP_201_CREATED)
def create_genre(payload: GenreCreate, db: Session = Depends(get_db)):
    g = Genre(name=payload.name)
    db.add(g)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create genre") from e
    db.refresh(g)
    return g

@router.get("", response_model=list[GenreOut])
def list_genres(db: Session = Depends(get_db)):
    return db.query(Genre).order_by(Genre.id.asc()).all()

@router.get("/{genre_id}", response_model=GenreOut)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    g = db.get(Genre, genre_id)
    if not g:
        raise HTTPException(status_code=404, detail="Genre not found")
    return g

@router.put("/{genre_id}", response_model=GenreOut)
def update_genre(genre_id: int, payload: GenreUpdate, db: Session = Depends(get_db)):
    g = db.get(Genre, genre_id)
    if not g:
        raise HTTPException(status_code=404, detail="Genre not found")
    if payload.name is not None:
        g.name = payload.name
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update genre") from e
    db.refresh(g)
    return g

@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    g = db.get(Genre, genre_id)
    if not g:
        raise HTTPException(status_code=404, detail="Genre not found")
    db.delete(g)
    db.commit()
