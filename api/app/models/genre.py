from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from ..db import Base

class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
