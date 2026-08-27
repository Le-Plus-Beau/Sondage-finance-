import uuid
from datetime import datetime

import requests
import streamlit as st


st.set_page_config(
    page_title="Gestion des dépenses",
    page_icon="💰",
    layout="centered"
)


URL_API = (
    "https://script.google.com/macros/s/AKfycbwDbPWxlSnG5DIHzdD1w550Q9YEabB43xp9bN28VcAR6bKuv11yMaOWJ3_mVw90imoiNw/exec"
)

CLE_API = st.secrets["CLE_API"]


def enregistrer_reponse(reponse):
    """
    Envoie une réponse à Google Apps Script.
    """

    donnees = dict(reponse)
    donnees["cle"] = CLE_API

    try:
        resultat = requests.post(
            URL_API,
            json=donnees,
            timeout=30
        )

        resultat.raise_for_status()

        retour = resultat.json()

        if retour.get("success") is not True:
            raise Exception(
                retour.get("error", "Erreur inconnue")
            )

        return retour

    except requests.exceptions.RequestException as erreur:
        raise Exception(
            f"Erreur de connexion à l'API : {erreur}"
        )

    except ValueError:
        raise Exception(
            "La réponse de Google Apps Script n'est pas un JSON valide."
        )


st.title("💰 Gestion des dépenses personnelles")
st.write("Répondez à ce court questionnaire.")


with st.form("questionnaire"):

    age = st.number_input(
        "Quel est votre âge ?",
        min_value=15,
        max_value=100,
        step=1
    )

    situation = st.selectbox(
        "Quelle est votre situation ?",
        [
            "Étudiant(e)",
            "Jeune actif(ve)",
            "Couple",
            "Famille",
            "Freelance / indépendant(e)",
            "Autre"
        ]
    )

    revenu = st.selectbox(
        "Quel est votre revenu mensuel net approximatif ?",
        [
            "Moins de 1 000 €",
            "1 000 à 1 500 €",
            "1 500 à 2 500 €",
            "2 500 à 4 000 €",
            "Plus de 4 000 €",
            "Je préfère ne pas répondre"
        ]
    )

    outils_actuels = st.multiselect(
        "Quels outils utilisez-vous pour gérer vos dépenses ?",
        [
            "Application bancaire",
            "Excel ou Google Sheets",
            "Application de budget",
            "Notes du téléphone",
            "Aucun outil",
            "Autre"
        ]
    )

    frequence_consultation = st.selectbox(
        "À quelle fréquence consultez-vous vos dépenses ?",
        [
            "Tous les jours",
            "Plusieurs fois par semaine",
            "Une fois par semaine",
            "Quelques fois par mois",
            "Rarement",
            "Jamais"
        ]
    )

    difficulte_gestion = st.multiselect(
        "Quelles difficultés rencontrez-vous ?",
        [
            "Je dépense trop sans m'en rendre compte",
            "J'ai du mal à épargner",
            "Je ne connais pas la répartition de mes dépenses",
            "Je dépense trop en restaurants ou livraisons",
            "J'oublie mes abonnements",
            "Je manque de motivation",
            "Je ne rencontre pas de difficulté particulière",
            "Autre"
        ]
    )

    categories_depenses = st.multiselect(
        "Dans quelles catégories dépensez-vous le plus ?",
        [
            "Logement",
            "Alimentation",
            "Restaurants / livraisons",
            "Transport",
            "Shopping",
            "Loisirs",
            "Abonnements",
            "Voyages",
            "Autre"
        ]
    )

    difficultes = st.text_area(
        "Décrivez votre principale difficulté avec la gestion de votre budget."
    )

    objectifs = st.multiselect(
        "Quels seraient vos objectifs ?",
        [
            "Épargner davantage",
            "Réduire mes dépenses",
            "Préparer un voyage",
            "Créer une épargne de sécurité",
            "Suivre mes dépenses",
            "Rembourser mes dettes",
            "Autre"
        ]
    )

    fonctionnalites = st.multiselect(
        "Quelles fonctionnalités vous intéressent ?",
        [
            "Connexion bancaire",
            "Catégorisation automatique",
            "Graphiques",
            "Recommandations par IA",
            "Objectifs d'épargne",
            "Badges et points",
            "Défis personnels",
            "Défis entre amis",
            "Notifications motivantes"
        ]
    )

    a_deja_utilise_app = st.radio(
        "Avez-vous déjà utilisé une application de gestion budgétaire ?",
        ["Oui", "Non"]
    )

    a_abandonne_app = st.radio(
        "Avez-vous abandonné cette application ?",
        ["Oui", "Non", "Je n'en ai jamais utilisé"]
    )

    raison_abandon = st.text_area(
        "Pourquoi avez-vous abandonné ou pourriez-vous abandonner une telle application ?"
    )

    connexion_bancaire = st.radio(
        "Seriez-vous prêt(e) à connecter votre compte bancaire ?",
        ["Oui", "Non", "Peut-être"]
    )

    freins_bancaires = st.multiselect(
        "Quels seraient vos freins ?",
        [
            "Sécurité",
            "Confidentialité",
            "Peur d'une fraude",
            "Manque de confiance",
            "Complexité",
            "Aucun frein",
            "Autre"
        ]
    )

    intention_usage = st.selectbox(
        "Quelle serait votre intention d'utiliser cette application ?",
        [
            "Très probablement",
            "Probablement",
            "Peut-être",
            "Probablement pas",
            "Pas du tout"
        ]
    )

    prix_premium = st.selectbox(
        "Quel prix mensuel pourriez-vous payer pour une version Premium ?",
        [
            "0 €",
            "Moins de 3 €",
            "3 à 5 €",
            "5 à 8 €",
            "Plus de 8 €",
            "Je ne sais pas"
        ]
    )

    aisance_sociale = st.selectbox(
        "Seriez-vous à l'aise pour participer à des défis avec vos proches ?",
        [
            "Très à l'aise",
            "Plutôt à l'aise",
            "Neutre",
            "Plutôt mal à l'aise",
            "Pas du tout à l'aise"
        ]
    )

    commentaire = st.text_area(
        "Avez-vous une remarque ou une idée supplémentaire ?"
    )

    envoyer = st.form_submit_button(
        "Envoyer ma réponse 🚀"
    )


if envoyer:

    reponse = {
        "id_reponse": str(uuid.uuid4()),
        "date_reponse": datetime.now().isoformat(timespec="seconds"),
        "age": age,
        "situation": situation,
        "revenu": revenu,
        "outils_actuels": ", ".join(outils_actuels),
        "frequence_consultation": frequence_consultation,
        "difficulte_gestion": ", ".join(difficulte_gestion),
        "categories_depenses": ", ".join(categories_depenses),
        "difficultes": difficultes,
        "objectifs": ", ".join(objectifs),
        "fonctionnalites": ", ".join(fonctionnalites),
        "a_deja_utilise_app": a_deja_utilise_app,
        "a_abandonne_app": a_abandonne_app,
        "raison_abandon": raison_abandon,
        "connexion_bancaire": connexion_bancaire,
        "freins_bancaires": ", ".join(freins_bancaires),
        "intention_usage": intention_usage,
        "prix_premium": prix_premium,
        "aisance_sociale": aisance_sociale,
        "commentaire": commentaire
    }

    try:
        resultat = enregistrer_reponse(reponse)

        if resultat.get("success") is True:
            st.success("✅ Votre réponse a bien été enregistrée !")
        else:
            st.error(
                resultat.get(
                    "error",
                    "Une erreur est survenue."
                )
            )

    except Exception as erreur:
        st.error(f"❌ {erreur}")
