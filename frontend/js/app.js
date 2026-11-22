// =========================
// CONFIGURATION DE L'API
// =========================

const API_URL = "http://127.0.0.1:8000/livres/";

let livres = [];


// =========================
// ELEMENTS HTML
// =========================

const listeLivres = document.getElementById("liste-livres");
const recherche = document.getElementById("recherche");
const filtreCategorie = document.getElementById("filtre-categorie");
const disponiblesSeulement = document.getElementById("disponibles-seulement");
const tri = document.getElementById("tri");
const nombreResultats = document.getElementById("nombre-resultats");

const formulaireLivre = document.getElementById("formulaire-livre");
const boutonReinitialiser = document.getElementById("bouton-reinitialiser");

const champTitre = document.getElementById("titre");
const champAuteur = document.getElementById("auteur");
const champAnnee = document.getElementById("annee");
const champCategorie = document.getElementById("categorie");

const erreurTitre = document.getElementById("erreur-titre");
const erreurAuteur = document.getElementById("erreur-auteur");
const erreurAnnee = document.getElementById("erreur-annee");
const erreurCategorie = document.getElementById("erreur-categorie");


// =========================
// CHARGEMENT DES LIVRES
// =========================

async function chargerLivres() {

    listeLivres.textContent = "Chargement des livres...";
    nombreResultats.textContent = "";

    try {
        const reponse = await fetch(API_URL);

        if (!reponse.ok) {
            throw new Error("Impossible de charger les livres.");
        }

        livres = await reponse.json();

        afficherLivres();

    } catch (erreur) {
        listeLivres.textContent =
            "Erreur : impossible de contacter le serveur API.";

        nombreResultats.textContent = "";
        console.error(erreur);
    }
}


// =========================
// NORMALISATION DU TEXTE
// =========================

function normaliser(texte) {
    return texte
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}


// =========================
// RECHERCHE ET FILTRAGE
// =========================

function obtenirLivresFiltres() {

    const terme = normaliser(recherche.value);

    return livres.filter(function(livre) {

        const correspondRecherche =
            normaliser(livre.titre).includes(terme) ||
            normaliser(livre.auteur).includes(terme);

        const correspondCategorie =
            filtreCategorie.value === "" ||
            livre.categorie === filtreCategorie.value;

        const correspondDisponibilite =
            !disponiblesSeulement.checked || livre.disponible;

        return correspondRecherche &&
               correspondCategorie &&
               correspondDisponibilite;
    });
}


// =========================
// TRI DES LIVRES
// =========================

function trierLivres(resultats) {

    switch (tri.value) {

        case "titre-asc":
            resultats.sort((a, b) =>
                a.titre.localeCompare(b.titre, "fr")
            );
            break;

        case "titre-desc":
            resultats.sort((a, b) =>
                b.titre.localeCompare(a.titre, "fr")
            );
            break;

        case "annee-asc":
            resultats.sort((a, b) => a.annee - b.annee);
            break;

        case "annee-desc":
            resultats.sort((a, b) => b.annee - a.annee);
            break;
    }

    return resultats;
}


// =========================
// CREATION D'UNE CARTE
// =========================

function creerCarteLivre(livre) {

    const carte = document.createElement("article");
    carte.classList.add("carte-livre");

    const titre = document.createElement("h3");
    titre.textContent = livre.titre;

    const auteur = document.createElement("p");
    auteur.textContent = "Auteur : " + livre.auteur;

    const annee = document.createElement("p");
    annee.textContent = "Année : " + livre.annee;

    const categorie = document.createElement("p");
    categorie.textContent = "Catégorie : " + livre.categorie;

    const disponibilite = document.createElement("p");

    if (livre.disponible) {
        disponibilite.textContent = "Disponible";
        disponibilite.classList.add("disponible");
    } else {
        disponibilite.textContent = "Emprunté";
        disponibilite.classList.add("emprunte");
    }

    const boutonSupprimer = document.createElement("button");
    boutonSupprimer.type = "button";
    boutonSupprimer.textContent = "Supprimer";

    boutonSupprimer.addEventListener("click", function() {
        supprimerLivre(livre.id);
    });

    carte.append(
        titre,
        auteur,
        annee,
        categorie,
        disponibilite,
        boutonSupprimer
    );

    return carte;
}


// =========================
// SUPPRESSION D'UN LIVRE
// =========================

async function supprimerLivre(id) {

    const confirmation = confirm(
        "Voulez-vous vraiment supprimer ce livre ?"
    );

    if (!confirmation) {
        return;
    }

    try {
        const reponse = await fetch(API_URL + id, {
            method: "DELETE"
        });

        if (!reponse.ok) {
            throw new Error("La suppression a échoué.");
        }

        await chargerLivres();

    } catch (erreur) {
        alert("Erreur lors de la suppression du livre.");
        console.error(erreur);
    }
}


// =========================
// AFFICHAGE DU CATALOGUE
// =========================

function afficherLivres() {

    let resultats = obtenirLivresFiltres();

    resultats = trierLivres(resultats);

    nombreResultats.textContent =
        resultats.length + " résultat(s)";

    listeLivres.innerHTML = "";

    if (resultats.length === 0) {
        listeLivres.textContent = "Aucun livre trouvé.";
        return;
    }

    resultats.forEach(function(livre) {
        const carte = creerCarteLivre(livre);
        listeLivres.appendChild(carte);
    });
}


// =========================
// VALIDATION DU FORMULAIRE
// =========================

function validerFormulaire() {

    erreurTitre.textContent = "";
    erreurAuteur.textContent = "";
    erreurAnnee.textContent = "";
    erreurCategorie.textContent = "";

    let valide = true;

    if (champTitre.value.trim().length < 2) {
        erreurTitre.textContent =
            "Le titre doit contenir au moins 2 caractères.";
        valide = false;
    }

    if (champAuteur.value.trim().length < 2) {
        erreurAuteur.textContent =
            "L'auteur doit contenir au moins 2 caractères.";
        valide = false;
    }

    const annee = Number(champAnnee.value);
    const anneeActuelle = new Date().getFullYear();

    if (
        champAnnee.value === "" ||
        annee < 1450 ||
        annee > anneeActuelle
    ) {
        erreurAnnee.textContent =
            "L'année doit être comprise entre 1450 et " +
            anneeActuelle + ".";
        valide = false;
    }

    if (champCategorie.value === "") {
        erreurCategorie.textContent =
            "Veuillez choisir une catégorie.";
        valide = false;
    }

    return valide;
}


// =========================
// AJOUT D'UN LIVRE
// =========================

async function ajouterLivre() {

    const nouveauLivre = {
        titre: champTitre.value.trim(),
        auteur: champAuteur.value.trim(),
        annee: Number(champAnnee.value),
        categorie: champCategorie.value,
        disponible: document.getElementById("disponible").checked
    };

    try {
        const reponse = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(nouveauLivre)
        });

        if (!reponse.ok) {
            const erreur = await reponse.json();
            throw new Error(erreur.detail || "Erreur lors de l'ajout.");
        }

        formulaireLivre.reset();

        await chargerLivres();

        alert("Livre ajouté avec succès !");

    } catch (erreur) {
        alert("Erreur : " + erreur.message);
        console.error(erreur);
    }
}


// =========================
// EVENEMENTS
// =========================

recherche.addEventListener("input", afficherLivres);
filtreCategorie.addEventListener("change", afficherLivres);
disponiblesSeulement.addEventListener("change", afficherLivres);
tri.addEventListener("change", afficherLivres);

formulaireLivre.addEventListener("submit", async function(event) {

    event.preventDefault();

    if (!validerFormulaire()) {
        return;
    }

    await ajouterLivre();
});


// Le catalogue est maintenant géré par l'API.
chargerLivres();