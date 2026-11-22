from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app.database import engine, create_db_and_tables
from app.models import Livre
from app.routers.livres import router as livres_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    livres_depart = [
        Livre(titre="Les Misérables", auteur="Victor Hugo", annee=1862,
              categorie="roman", disponible=True),
        Livre(titre="Le Petit Prince", auteur="Antoine de Saint-Exupéry",
              annee=1943, categorie="roman", disponible=False),
        Livre(titre="Une brève histoire du temps", auteur="Stephen Hawking",
              annee=1988, categorie="science", disponible=True),
        Livre(titre="L'origine des espèces", auteur="Charles Darwin",
              annee=1859, categorie="science", disponible=True),
        Livre(titre="Sapiens", auteur="Yuval Noah Harari",
              annee=2011, categorie="histoire", disponible=True),
        Livre(titre="Histoire de France", auteur="Jules Michelet",
              annee=1910, categorie="histoire", disponible=False),
        Livre(titre="Clean Code", auteur="Robert C. Martin",
              annee=2008, categorie="informatique", disponible=True),
        Livre(titre="JavaScript: The Good Parts", auteur="Douglas Crockford",
              annee=2008, categorie="informatique", disponible=True),
    ]

    with Session(engine) as session:
        if not session.exec(select(Livre)).first():
            session.add_all(livres_depart)
            session.commit()

    yield


app = FastAPI(
    title="API Catalogue de Bibliothèque",
    description="API de gestion du catalogue de livres.",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(livres_router)


@app.get("/sante")
def verifier_sante():
    return {"statut": "ok"}