from pydantic import BaseModel, Field

class AuthorBase(BaseModel):
    name: str = Field(..., max_length=255)

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)

class AuthorOut(AuthorBase):
    id: int
    class Config:
        from_attributes = True
