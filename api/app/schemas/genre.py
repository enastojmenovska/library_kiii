from pydantic import BaseModel, Field

class GenreBase(BaseModel):
    name: str = Field(..., max_length=255)

class GenreCreate(GenreBase):
    pass

class GenreUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)

class GenreOut(GenreBase):
    id: int
    class Config:
        from_attributes = True
