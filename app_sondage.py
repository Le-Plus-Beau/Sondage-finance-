import uuid
from datetime import datetime

import requests
import streamlit as st


# =====================================
# CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Dépenses personnelles",
    page_icon="💰",
    layout="centered"
)

URL_API = st.secrets["URL_API"]
CLE_API = st.secrets["CLE_API"]


# =====================================
# FONCTION D'ENVOI
# =====================================

def enregistrer_reponse(reponse):
    donnees = dict(reponse)
    donnees["cle"] = CLE_API

    try:
        resultat = requests.post(
            URL_API,
            json=donnees,
            timeout=30
        )

        resultat.raise_for_status()

        try:
            retour = resultat.json()
        except ValueError:
            raise Exception(
                "La réponse de Google Apps Script n'est pas valide."
            )

        if retour.get("success") is not True:
            raise Exception(
                retour.get("error", "Erreur lors de l'enregistrement.")
            )

        return retour

    except requests.exceptions.RequestException as erreur:
        raise Exception(f"Erreur de connexion : {erreur}")


# =====================================
# TITRE
# =====================================

st.title("💰 Dépenses personnelles")

st.write(
    "Répondez à ce court questionnaire afin de nous aider "
    "à concevoir une application simple, visuelle et motivante."
)

st.info(
    "Questionnaire anonyme : ne renseignez aucune donnée bancaire, "
    "nom complet ou information sensible."
)


# =====================================
# QUESTIONS
# =====================================

age = st.number_input(
    "Quel est votre âge ?",
    min_value=ที่18,
    max_value=100,
    value=25,
    step=1
)

situation = st.selectbox(
    "Quelle est votre situation ?",
    [
        "Étudiant(e)",
        "Salarié(e)",
        "Indépendant(e)",
        "Sans emploi",
        "Retraité(e)",
        "Autre"
    ]
)

revenu = st.selectbox(
    "Quel est votre revenu mensuel approximatif ?",
    [
        "Moins de 1 000 €",
        "1 000 à 1 500 €",
        "1 500 à 2 000 €",
        "2 000 à 3 000 €",
        "3 000 à 5 000 €",
        "Plus de 5 000 €",
        "Je préfère ne pas répondre"
    ]
)

outils_actuels = st.multiselect(
    "Quels outils utilisez-vous actuellement pour gérer votre budget ?",
    [
        "Application bancaire",
        "Excel ou Google Sheets",
        "Application de gestion budgétaire",
        "Carnet papier",
        "Je ne gère pas vraiment mon budget",
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
    "Quelles sont vos principales difficultés ?",
    [
        "Je dépense trop",
        "Je ne sais pas où va mon argent",
        "J'ai du mal à épargner",
        "Je dépense de manière impulsive",
        "J'oublie mes abonnements",
        "Je manque de motivation",
        "Je trouve les applications trop compliquées",
        "Aucune difficulté particulière"
    ]
)

categories_depenses = st.multiselect(
    "Dans quelles catégories dépensez-vous le plus ?",
    [
        "Logement",
        "Alimentation",
        "Restaurants et livraisons",
        "Transport",
        "Shopping",
        "Loisirs",
        "Abonnements",
        "Voyages",
        "Autre"
    ]
)

difficultes = st.text_area(
    "Qu'est-ce qui vous frustre le plus dans la gestion de votre budget ?",
    placeholder="Écrivez votre réponse..."
)

objectifs = st.multiselect(
    "Quels objectifs souhaitez-vous atteindre ?",
    [
        "Épargner régulièrement",
        "Préparer un voyage",
        "Créer une épargne de sécurité",
        "Réduire mes dépenses",
        "Éviter les achats impulsifs",
        "Rembourser une dette",
        "Mieux comprendre mes habitudes"
    ]
)

fonctionnalites = st.multiselect(
    "Quelles fonctionnalités vous intéressent ?",
    [
        "Connexion bancaire",
        "Catégorisation automatique",
        "Graphiques clairs",
        "Recommandations par IA",
        "Objectifs d'épargne",
        "Badges et points",
        "Défis personnels",
        "Défis entre amis",
        "Classements anonymes",
        "Notifications motivantes"
    ]
)

connexion_bancaire = st.radio(
    "Seriez-vous prêt(e) à connecter votre compte bancaire ?",
    ["Oui", "Non", "Je ne sais pas"],
    index=None
)

freins_bancaires = st.multiselect(
    "Qu'est-ce qui pourrait vous empêcher de connecter votre banque ?",
    [
        "Peur pour mes données personnelles",
        "Peur du piratage",
        "Manque de confiance",
        "Procédure trop compliquée",
        "Je ne veux pas partager mes données",
        "Aucun frein particulier"
    ]
)

intention_usage = st.selectbox(
    "À quelle fréquence utiliseriez-vous cette application ?",
    [
        "Tous les jours",
        "Plusieurs fois par semaine",
        "Une fois par semaine",
        "Quelques fois par mois",
        "Je ne sais pas"
    ]
)

prix_premium = st.selectbox(
    "Combien seriez-vous prêt(e) à payer pour une version Premium ?",
    [
        "0 €",
        "Moins de 3 €",
        "3 à 5 €",
        "5 à 8 €",
        "Plus de 8 €",
        "Je ne sais pas"
    ]
)

# =====================================
# QUESTION CONDITIONNELLE
# =====================================

a_deja_utilise_app = st.radio(
    "Avez-vous déjà utilisé une application de gestion budgétaire ?",
    ["Oui", "Non"],
    index=None
)

if a_deja_utilise_app == "Oui":

    a_abandonne_app = st.radio(
        "Avez-vous abandonné cette application ?",
        ["Oui", "Non"],
        index=None
    )

    if a_abandonne_app == "Oui":
        raison_abandon = st.text_area(
            "Pourquoi avez-vous abandonné cette application ?",
            placeholder=(
                "Exemple : application trop compliquée, "
                "manque de motivation, trop de notifications..."
            )
        )
    else:
        raison_abandon = ""

elif a_deja_utilise_app == "Non":
    a_abandonne_app = "Non concerné"
    raison_abandon = ""

else:
    a_abandonne_app = ""
    raison_abandon = ""

# =====================================
# FIN DU QUESTIONNAIRE
# =====================================

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


# =====================================
# BOUTON D'ENVOI
# =====================================

if st.button("Envoyer ma réponse 🚀", use_container_width=True):

    if a_deja_utilise_app is None:
        st.warning(
            "Veuillez répondre à la question sur l'utilisation "
            "d'une application budgétaire."
        )
        st.stop()

    if a_deja_utilise_app == "Oui" and a_abandonne_app == "":
        st.warning(
            "Veuillez indiquer si vous avez abandonné cette application."
        )
        st.stop()

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
        "connexion_bancaire": connexion_bancaire or "",
        "freins_bancaires": ", ".join(freins_bancaires),
        "intention_usage": intention_usage,
        "prix_premium": prix_premium,
        "a_deja_utilise_app": a_deja_utilise_app,
        "a_abandonne_app": a_abandonne_app,
        "raison_abandon": raison_abandon,
        "aisance_sociale": aisance_sociale,
        "commentaire": commentaire
    }

    with st.spinner("Envoi de votre réponse..."):
        try:
            enregistrer_reponse(reponse)
            st.success("✅ Votre réponse a bien été enregistrée !")
            st.balloons()

        except Exception as erreur:
            st.error(f"❌ {erreur}")
