from pydantic import BaseModel, Field

class BookBase(BaseModel):
    title: str = Field(..., max_length=255)
    author_id: int | None = None
    genre_id: int | None = None
    year: int | None = None
    isbn: str | None = Field(default=None, max_length=32)

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    author_id: int | None = None
    genre_id: int | None = None
    year: int | None = None
    isbn: str | None = Field(None, max_length=32)

class BookOut(BookBase):
    id: int
    class Config:
        from_attributes = True
