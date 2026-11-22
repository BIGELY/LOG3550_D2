from datetime import date
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Categorie(str, Enum):
    roman = "roman"
    science = "science"
    histoire = "histoire"
    informatique = "informatique"
    autre = "autre"


class LivreCreate(BaseModel):
    titre: str = Field(min_length=2, max_length=200)
    auteur: str = Field(min_length=2, max_length=200)
    annee: int = Field(ge=1450, le=date.today().year)
    categorie: Categorie
    isbn: Optional[str] = None
    disponible: bool = True

    @field_validator("isbn")
    @classmethod
    def valider_isbn(cls, valeur):
        if valeur is not None:
            isbn = valeur.replace("-", "").replace(" ", "")
            if len(isbn) not in (10, 13) or not isbn.isdigit():
                raise ValueError("ISBN doit contenir 10 ou 13 chiffres.")
            return isbn
        return valeur


class LivreUpdate(BaseModel):
    titre: Optional[str] = Field(default=None, min_length=2, max_length=200)
    auteur: Optional[str] = Field(default=None, min_length=2, max_length=200)
    annee: Optional[int] = Field(default=None, ge=1450, le=date.today().year)
    categorie: Optional[Categorie] = None
    isbn: Optional[str] = None
    disponible: Optional[bool] = None

    @field_validator("isbn")
    @classmethod
    def valider_isbn(cls, valeur):
        if valeur is not None:
            isbn = valeur.replace("-", "").replace(" ", "")
            if len(isbn) not in (10, 13) or not isbn.isdigit():
                raise ValueError("ISBN doit contenir 10 ou 13 chiffres.")
            return isbn
        return valeur


class LivreRead(BaseModel):
    id: int
    titre: str
    auteur: str
    annee: int
    categorie: Categorie
    isbn: Optional[str]
    disponible: bool