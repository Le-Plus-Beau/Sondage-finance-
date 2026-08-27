import uuid
from datetime import datetime

import requests
import streamlit as st


# =====================================
# CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Sondage - Gestion des dépenses",
    page_icon="💰",
    layout="centered"
)

CLE_API = st.secrets["CLE_API"]

URL_API = (
    "https://script.google.com/macros/s/AKfycbwDbPWxlSnG5DIHzdD1w550Q9YEabB43xp9bN28VcAR6bKuv11yMaOWJ3_mVw90imoiNw/exec"
)


# =====================================
# STYLE
# =====================================

st.markdown(
    """
    <style>
    .main {
        max-width: 850px;
        margin: auto;
    }

    h1 {
        color: #2563eb;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        padding: 0.7rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =====================================
# ENREGISTREMENT
# =====================================

def enregistrer_reponse(donnees):
    try:
        response = requests.post(
            URL_API,
            json=donnees,
            timeout=30
        )

        response.raise_for_status()

        try:
            resultat = response.json()

            if isinstance(resultat, dict):
                if resultat.get("success") is False:
                    st.error(
                        resultat.get(
                            "error",
                            "Erreur lors de l'enregistrement."
                        )
                    )
                    return False

        except ValueError:
            pass

        return True

    except requests.exceptions.RequestException as erreur:
        st.error(f"Erreur de connexion : {erreur}")
        return False


# =====================================
# INTRODUCTION
# =====================================

st.title("💰 Gestion des dépenses personnelles")

st.write(
    "Ce questionnaire nous aide à concevoir une application simple, "
    "visuelle et agréable pour mieux gérer ses dépenses."
)

st.info(
    "🔒 Vos réponses sont utilisées uniquement dans le cadre de cette étude."
)


# =====================================
# PROFIL
# =====================================

st.header("👤 À propos de vous")

age = st.number_input(
    "Quel âge avez-vous ?",
    min_value=13,
    max_value=100,
    value=25,
    step=1
)

situation = st.selectbox(
    "Quelle est votre situation ?",
    [
        "Étudiant(e)",
        "Salarié(e)",
        "Indépendant(e) / Freelance",
        "Sans emploi",
        "Retraité(e)",
        "Couple",
        "Autre"
    ]
)

revenu = st.selectbox(
    "Quel est votre revenu mensuel approximatif ?",
    [
        "Moins de 1 000 €",
        "1 000 € à 1 500 €",
        "1 500 € à 2 000 €",
        "2 000 € à 3 000 €",
        "3 000 € à 4 000 €",
        "Plus de 4 000 €",
        "Je préfère ne pas répondre"
    ]
)


# =====================================
# GESTION ACTUELLE
# =====================================

st.header("📊 Votre gestion actuelle")

outils_actuels = st.multiselect(
    "Quels outils utilisez-vous actuellement pour gérer vos dépenses ?",
    [
        "Application bancaire",
        "Tableau Excel ou Google Sheets",
        "Notes du téléphone",
        "Application de gestion budgétaire",
        "Papier / carnet",
        "Je n'utilise aucun outil",
        "Autre"
    ]
)

frequence_consultation = st.radio(
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
        "Je dépense trop en restaurants ou livraisons",
        "J'ai du mal à épargner",
        "Je ne connais pas précisément mes dépenses",
        "Je dépasse souvent mon budget",
        "Je manque de temps",
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
        "Santé",
        "Autre"
    ]
)

difficultes = st.text_area(
    "Pouvez-vous préciser votre principale difficulté ?",
    placeholder="Exemple : je dépense beaucoup le week-end..."
)


# =====================================
# OBJECTIFS
# =====================================

st.header("🎯 Vos objectifs")

objectifs = st.multiselect(
    "Que souhaiteriez-vous améliorer ?",
    [
        "Épargner davantage",
        "Réduire mes dépenses",
        "Préparer un voyage",
        "Créer une épargne de sécurité",
        "Suivre mes dépenses",
        "Rembourser mes dettes",
        "Mieux gérer mon budget",
        "Autre"
    ]
)


# =====================================
# APPLICATION IDÉALE
# =====================================

st.header("📱 L'application idéale")

fonctionnalites = st.multiselect(
    "Quelles fonctionnalités vous intéresseraient le plus ?",
    [
        "Connexion à mes comptes bancaires",
        "Catégorisation automatique des dépenses",
        "Graphiques simples",
        "Objectifs d'épargne",
        "Conseils personnalisés",
        "Détection des dépenses inhabituelles",
        "Notifications intelligentes",
        "Suivi des abonnements",
        "Autre"
    ]
)

connexion_bancaire = st.radio(
    "Seriez-vous prêt(e) à connecter vos comptes bancaires ?",
    [
        "Oui",
        "Non",
        "Je ne sais pas encore"
    ]
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


# =====================================
# EXPÉRIENCE AVEC LES APPLICATIONS
# =====================================

st.header("📱 Expérience avec les applications")

a_deja_utilise_app = st.radio(
    "Avez-vous déjà utilisé une application de gestion budgétaire ?",
    [
        "Oui",
        "Non",
        "Je ne sais plus"
    ],
    key="a_deja_utilise_app"
)

a_abandonne_app = ""
raison_abandon = ""

if a_deja_utilise_app == "Oui":

    a_abandonne_app = st.radio(
        "Avez-vous abandonné cette application ?",
        [
            "Oui",
            "Non"
        ],
        key="a_abandonne_app"
    )

    if a_abandonne_app == "Oui":
        raison_abandon = st.text_area(
            "Si vous avez abandonné une application, pourquoi ?",
            placeholder="Exemple : trop compliquée, manque de motivation...",
            key="raison_abandon"
        )


# =====================================
# DIMENSION SOCIALE
# =====================================

st.header("👥 Dimension sociale")

aisance_sociale = st.radio(
    "Seriez-vous à l'aise pour participer à un défi financier avec vos proches ?",
    [
        "Très à l'aise",
        "À l'aise si les montants restent anonymes",
        "Je ne sais pas",
        "Peu à l'aise",
        "Pas du tout à l'aise"
    ]
)


# =====================================
# OFFRE PREMIUM
# =====================================

st.header("💳 Offre premium")

prix_premium = st.radio(
    "Quel prix mensuel accepteriez-vous pour une version premium ?",
    [
        "0 €",
        "Moins de 3 €",
        "Entre 3 € et 5 €",
        "Entre 5 € et 8 €",
        "Plus de 8 €",
        "Je ne sais pas"
    ]
)


# =====================================
# COMMENTAIRE ET EMAIL
# =====================================

st.header("💬 Pour terminer")

commentaire = st.text_area(
    "Avez-vous une remarque ou une idée à partager ?"
)

# =====================================
# ENVOI
# =====================================

if st.button("🚀 Envoyer mes réponses"):

    donnees = {
        "cle": CLE_API,
        "id_reponse": str(uuid.uuid4()),
        "date_reponse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
        "connexion_bancaire": connexion_bancaire,
        "freins_bancaires": ", ".join(freins_bancaires),
        "a_deja_utilise_app": a_deja_utilise_app,
        "a_abandonne_app": a_abandonne_app,
        "raison_abandon": raison_abandon,
        "aisance_sociale": aisance_sociale,
        "prix_premium": prix_premium,
        "commentaire": commentaire,
    }

    with st.spinner("Enregistrement de vos réponses..."):
        succes = enregistrer_reponse(donnees)

    if succes:
        st.success("✅ Vos réponses ont bien été enregistrées.")
        st.balloons()
