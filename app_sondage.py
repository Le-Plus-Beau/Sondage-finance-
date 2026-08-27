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

URL_API = (
    "https://script.google.com/macros/s/"
    "AKfycbwDbPWxlSnG5DIHzdD1w550Q9YEabB43xp9bN28VcAR6bKuv11yMaOWJ3_mVw90imoiNw"
    "/exec"
)

EMAIL_AUTORISE = "izylok@outlook.fr"


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
# FONCTION D'ENREGISTREMENT
# =====================================

def enregistrer_reponse(donnees):
    try:
        response = requests.post(
            URL_API,
            json=donnees,
            timeout=30
        )

        response.raise_for_status()

        # Google Apps Script peut retourner du texte ou du JSON
        try:
            resultat = response.json()

            if isinstance(resultat, dict):
                if resultat.get("success") is False:
                    raise Exception(
                        resultat.get(
                            "error",
                            "Erreur lors de l'enregistrement."
                        )
                    )

        except ValueError:
            # Réponse texte acceptée
            pass

        return True

    except requests.exceptions.RequestException as erreur:
        st.error(f"Erreur de connexion : {erreur}")
        return False

    except Exception as erreur:
        st.error(str(erreur))
        return False


# =====================================
# TITRE
# =====================================

st.title("💰 Gestion des dépenses personnelles")

st.write(
    "Ce questionnaire nous aide à concevoir une application simple, "
    "visuelle et motivante pour mieux gérer ses dépenses."
)

st.info(
    "🔒 Vos réponses sont utilisées uniquement dans le cadre de cette étude."
)


# =====================================
# FORMULAIRE
# =====================================

with st.form("formulaire_sondage"):

    st.subheader("👤 À propos de vous")

    age = st.selectbox(
        "Quel est votre âge ?",
        [
            "Moins de 18 ans",
            "18-24 ans",
            "25-34 ans",
            "35-44 ans",
            "45-54 ans",
            "55 ans et plus"
        ]
    )

    situation = st.selectbox(
        "Quelle est votre situation ?",
        [
            "Étudiant(e)",
            "Salarié(e)",
            "Indépendant(e) / Freelance",
            "Demandeur(se) d'emploi",
            "Retraité(e)",
            "Autre"
        ]
    )

    revenu = st.selectbox(
        "Quel est votre revenu mensuel net approximatif ?",
        [
            "Aucun revenu",
            "Moins de 1 000 €",
            "1 000 € à 1 499 €",
            "1 500 € à 1 999 €",
            "2 000 € à 2 999 €",
            "3 000 € à 3 999 €",
            "4 000 € ou plus",
            "Je préfère ne pas répondre"
        ]
    )

    st.subheader("📊 Vos habitudes")

    outils_actuels = st.multiselect(
        "Quels outils utilisez-vous pour gérer vos dépenses ?",
        [
            "Application bancaire",
            "Excel ou Google Sheets",
            "Application de budget",
            "Carnet papier",
            "Je ne fais aucun suivi",
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
            "Je dépense trop",
            "Je ne sais pas où part mon argent",
            "J'oublie certaines dépenses",
            "J'ai du mal à épargner",
            "Je manque de motivation",
            "Je trouve cela compliqué",
            "Aucune difficulté particulière",
            "Autre"
        ]
    )

    categories_depenses = st.multiselect(
        "Dans quelles catégories dépensez-vous le plus ?",
        [
            "Logement",
            "Alimentation",
            "Restaurants et livraisons",
            "Transports",
            "Shopping",
            "Loisirs",
            "Abonnements",
            "Voyages",
            "Autre"
        ]
    )

    difficultes = st.text_area(
        "Quelle est votre principale difficulté avec votre budget ?"
    )

    st.subheader("🎯 Objectifs")

    objectifs = st.multiselect(
        "Quels objectifs aimeriez-vous atteindre ?",
        [
            "Épargner régulièrement",
            "Réduire mes dépenses",
            "Préparer un voyage",
            "Créer une épargne de sécurité",
            "Rembourser des dettes",
            "Mieux comprendre mes habitudes",
            "Suivre un budget familial",
            "Autre"
        ]
    )

    st.subheader("📱 Application idéale")

    fonctionnalites = st.multiselect(
        "Quelles fonctionnalités vous intéresseraient ?",
        [
            "Connexion à mes comptes bancaires",
            "Catégorisation automatique",
            "Graphiques simples",
            "Objectifs d'épargne",
            "Conseils personnalisés",
            "Détection des dépenses inhabituelles",
            "Notifications motivantes",
            "Points et badges",
            "Défis personnels",
            "Défis entre amis",
            "Classements anonymes"
        ]
    )

    connexion_bancaire = st.radio(
        "Seriez-vous prêt(e) à connecter votre compte bancaire ?",
        [
            "Oui",
            "Non",
            "Je ne sais pas"
        ]
    )

    freins_bancaires = st.multiselect(
        "Qu'est-ce qui pourrait vous empêcher de connecter votre banque ?",
        [
            "La sécurité",
            "La confidentialité",
            "La peur d'une fraude",
            "Je ne comprends pas le fonctionnement",
            "Je ne veux pas partager mes données",
            "Cela ne me dérange pas",
            "Autre"
        ]
    )

    st.subheader("🎮 Motivation et gamification")

    intention_usage = st.radio(
        "Une application ludique vous aiderait-elle à mieux gérer votre argent ?",
        [
            "Certainement",
            "Probablement",
            "Je ne sais pas",
            "Probablement pas",
            "Certainement pas"
        ]
    )

    a_deja_utilise_app = st.radio(
        "Avez-vous déjà utilisé une application de gestion budgétaire ?",
        [
            "Oui",
            "Non"
        ]
    )

    a_abandonne_app = ""

    if a_deja_utilise_app == "Oui":
        a_abandonne_app = st.radio(
            "Avez-vous abandonné cette application ?",
            [
                "Oui",
                "Non"
            ]
        )

    raison_abandon = st.text_area(
        "Si vous avez abandonné une application, pourquoi ?"
    )

    aisance_sociale = st.radio(
        "Seriez-vous à l'aise pour participer à un défi financier avec vos proches ?",
        [
            "Oui, tout à fait",
            "Oui, si les montants restent anonymes",
            "Je ne sais pas",
            "Non"
        ]
    )

    st.subheader("💳 Offre payante")

    prix_premium = st.radio(
        "Quel prix mensuel accepteriez-vous pour une version premium ?",
        [
            "Je ne paierais pas",
            "Moins de 3 €",
            "3 € à 5 €",
            "5 € à 8 €",
            "Plus de 8 €",
            "Je ne sais pas"
        ]
    )

    commentaire = st.text_area(
        "Avez-vous une remarque ou une idée à nous partager ?"
    )

    email = st.text_input(
        "Votre adresse e-mail pour participer à la bêta "
        "(facultatif)"
    )

    envoyer = st.form_submit_button(
        "🚀 Envoyer mes réponses"
    )


# =====================================
# TRAITEMENT
# =====================================

if envoyer:

    if email and email.lower().strip() != EMAIL_AUTORISE.lower():
        st.error(
            "Cette adresse e-mail n'est pas autorisée pour le moment."
        )
        st.stop()

    donnees = {
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
        "intention_usage": intention_usage,
        "a_deja_utilise_app": a_deja_utilise_app,
        "a_abandonne_app": a_abandonne_app,
        "raison_abandon": raison_abandon,
        "aisance_sociale": aisance_sociale,
        "prix_premium": prix_premium,
        "commentaire": commentaire,
        "email": email
    }

    with st.spinner("Enregistrement de vos réponses..."):

        succes = enregistrer_reponse(donnees)

        if succes:
            st.success("✅ Vos réponses ont bien été enregistrées.")
            st.balloons()
