from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models import Livre
from app.schemas import LivreCreate, LivreUpdate, LivreRead

router = APIRouter(prefix="/livres", tags=["Livres"])


@router.post("/", response_model=LivreRead, status_code=201)
def creer_livre(
    livre: LivreCreate,
    response: Response,
    session: Session = Depends(get_session)
):
    if livre.isbn and session.exec(
        select(Livre).where(Livre.isbn == livre.isbn)
    ).first():
        raise HTTPException(status_code=409, detail="Cet ISBN existe déjà.")

    nouveau_livre = Livre(**livre.model_dump())
    session.add(nouveau_livre)
    session.commit()
    session.refresh(nouveau_livre)

    response.headers["Location"] = f"/livres/{nouveau_livre.id}"

    return nouveau_livre


@router.get("/", response_model=list[LivreRead])
def lister_livres(
    q: Optional[str] = None,
    categorie: Optional[str] = None,
    disponible: Optional[bool] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: Session = Depends(get_session)
):

    requete = select(Livre)

    if q:
        requete = requete.where(
            (Livre.titre.contains(q)) | (Livre.auteur.contains(q))
        )
    if categorie:
        requete = requete.where(Livre.categorie == categorie)
    if disponible is not None:
        requete = requete.where(Livre.disponible == disponible)

    return session.exec(requete.offset(skip).limit(limit)).all()


@router.get("/{livre_id}", response_model=LivreRead)
def obtenir_livre(livre_id: int, session: Session = Depends(get_session)):
    livre = session.get(Livre, livre_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable.")
    return livre


@router.put("/{livre_id}", response_model=LivreRead)
def remplacer_livre(
    livre_id: int,
    donnees: LivreCreate,
    session: Session = Depends(get_session)
):
    livre = session.get(Livre, livre_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable.")

    if donnees.isbn and session.exec(
        select(Livre).where(Livre.isbn == donnees.isbn, Livre.id != livre_id)
    ).first():
        raise HTTPException(status_code=409, detail="Cet ISBN existe déjà.")

    for cle, valeur in donnees.model_dump().items():
        setattr(livre, cle, valeur)

    session.add(livre)
    session.commit()
    session.refresh(livre)
    return livre


@router.patch("/{livre_id}", response_model=LivreRead)
def modifier_livre(
    livre_id: int,
    donnees: LivreUpdate,
    session: Session = Depends(get_session)
):
    livre = session.get(Livre, livre_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable.")

    modifications = donnees.model_dump(exclude_unset=True)

    if "isbn" in modifications and modifications["isbn"]:
        doublon = session.exec(
            select(Livre).where(
                Livre.isbn == modifications["isbn"],
                Livre.id != livre_id
            )
        ).first()
        if doublon:
            raise HTTPException(status_code=409, detail="Cet ISBN existe déjà.")

    for cle, valeur in modifications.items():
        setattr(livre, cle, valeur)

    session.add(livre)
    session.commit()
    session.refresh(livre)
    return livre


@router.delete("/{livre_id}", status_code=204)
def supprimer_livre(livre_id: int, session: Session = Depends(get_session)):
    livre = session.get(Livre, livre_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable.")

    session.delete(livre)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)