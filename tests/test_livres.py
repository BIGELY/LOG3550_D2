import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_session


engine_test = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


def session_test():
    with Session(engine_test) as session:
        yield session


app.dependency_overrides[get_session] = session_test


@pytest.fixture
def client():
    SQLModel.metadata.create_all(engine_test)

    with TestClient(app) as test_client:
        yield test_client

    SQLModel.metadata.drop_all(engine_test)


def nouveau_livre():
    return {
        "titre": "Python pour débutants",
        "auteur": "Guido van Rossum",
        "annee": 2020,
        "categorie": "informatique",
        "isbn": "9781234567890",
        "disponible": True
    }


def test_creer_livre(client):
    reponse = client.post("/livres/", json=nouveau_livre())
    assert reponse.status_code == 201
    assert reponse.json()["titre"] == "Python pour débutants"
    assert reponse.headers["location"] == f"/livres/{reponse.json()['id']}"

def test_lire_livres(client):
    reponse = client.get("/livres/")
    assert reponse.status_code == 200
    assert isinstance(reponse.json(), list)


def test_filtrer_livres(client):
    client.post("/livres/", json=nouveau_livre())
    reponse = client.get("/livres/?categorie=informatique")
    assert reponse.status_code == 200
    assert len(reponse.json()) == 1


def test_modifier_livre(client):
    livre = client.post("/livres/", json=nouveau_livre()).json()
    reponse = client.patch(
        f"/livres/{livre['id']}",
        json={"disponible": False}
    )
    assert reponse.status_code == 200
    assert reponse.json()["disponible"] is False


def test_supprimer_livre(client):
    livre = client.post("/livres/", json=nouveau_livre()).json()
    reponse = client.delete(f"/livres/{livre['id']}")
    assert reponse.status_code == 204


def test_livre_introuvable(client):
    reponse = client.get("/livres/999")
    assert reponse.status_code == 404


def test_validation_422(client):
    donnees = nouveau_livre()
    donnees["titre"] = "A"

    reponse = client.post("/livres/", json=donnees)
    assert reponse.status_code == 422


def test_isbn_duplique_409(client):
    client.post("/livres/", json=nouveau_livre())

    reponse = client.post("/livres/", json=nouveau_livre())
    assert reponse.status_code == 409