from typing import Optional
from sqlmodel import SQLModel, Field


class Livre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titre: str
    auteur: str
    annee: int
    categorie: str
    isbn: Optional[str] = Field(default=None, unique=True, index=True)
    disponible: bool = True