import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from streamlit_gsheets import GSheetsConnection


# =============================
# Configuration
# =============================

st.set_page_config(
    page_title="Sondage - Gestion des dépenses",
    page_icon="💰",
    layout="centered"
)


# =============================
# Connexion Google Sheets
# =============================

conn = st.connection(
    "gsheets",
    type=GSheetsConnection
)

NOM_FEUILLE = "Feuille 1"


# =============================
# Fonction d'enregistrement
# =============================

def enregistrer_reponse(reponse):
    nouvelle_reponse = pd.DataFrame([reponse])

    try:
        anciennes_reponses = conn.read(
            worksheet=NOM_FEUILLE,
            ttl=0
        )

        if anciennes_reponses.empty:
            resultats = nouvelle_reponse
        else:
            resultats = pd.concat(
                [anciennes_reponses, nouvelle_reponse],
                ignore_index=True
            )

    except Exception:
        resultats = nouvelle_reponse

    conn.update(
        worksheet=NOM_FEUILLE,
        data=resultats
    )


# =============================
# Interface
# =============================

st.title("💰 Gestion des dépenses personnelles")

st.write(
    "Ce questionnaire dure environ 3 minutes. "
    "Il vise à mieux comprendre les habitudes, besoins et difficultés "
    "liés à la gestion des dépenses personnelles."
)

st.info(
    "Questionnaire anonyme : ne renseignez aucune donnée bancaire, "
    "nom complet ou information sensible."
)


with st.form("formulaire_sondage"):

    # -------------------------
    # Profil
    # -------------------------

    st.header("👤 À propos de vous")

    age = st.selectbox(
        "Dans quelle tranche d'âge êtes-vous ?",
        [
            "Moins de 18 ans",
            "18-24 ans",
            "25-34 ans",
            "35-44 ans",
            "45-54 ans",
            "55 ans ou plus",
            "Je préfère ne pas répondre"
        ]
    )

    situation = st.selectbox(
        "Quelle est votre situation principale ?",
        [
            "Étudiant(e)",
            "Salarié(e)",
            "Indépendant(e) / freelance",
            "Demandeur(se) d'emploi",
            "Retraité(e)",
            "Autre",
            "Je préfère ne pas répondre"
        ]
    )

    revenu = st.selectbox(
        "Quel est approximativement votre revenu mensuel net ?",
        [
            "Aucun revenu",
            "Moins de 1 000 €",
            "1 000 à 1 500 €",
            "1 500 à 2 000 €",
            "2 000 à 3 000 €",
            "3 000 à 4 000 €",
            "Plus de 4 000 €",
            "Je préfère ne pas répondre"
        ]
    )

    # -------------------------
    # Habitudes actuelles
    # -------------------------

    st.header("📊 Vos habitudes")

    outils_actuels = st.multiselect(
        "Quels outils utilisez-vous pour suivre vos dépenses ?",
        [
            "Application bancaire",
            "Tableur Excel ou Google Sheets",
            "Application spécialisée",
            "Carnet ou notes papier",
            "Notes sur téléphone",
            "Je ne suis pas particulièrement mes dépenses",
            "Autre"
        ]
    )

    frequence = st.selectbox(
        "À quelle fréquence consultez-vous vos dépenses ?",
        [
            "Plusieurs fois par jour",
            "Tous les jours",
            "Quelques fois par semaine",
            "Quelques fois par mois",
            "Rarement",
            "Jamais"
        ]
    )

    difficulte = st.select_slider(
        "À quel point est-il difficile de gérer vos dépenses ?",
        options=[
            "Très facile",
            "Plutôt facile",
            "Moyennement difficile",
            "Plutôt difficile",
            "Très difficile"
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
            "Santé",
            "Voyages",
            "Autre",
            "Je ne sais pas"
        ]
    )

    # -------------------------
    # Difficultés et objectifs
    # -------------------------

    st.header("🎯 Vos besoins")

    declencheur = st.multiselect(
        "Quelles difficultés rencontrez-vous le plus souvent ?",
        [
            "Je ne sais pas où va mon argent",
            "Je dépense trop dans certaines catégories",
            "J'ai du mal à respecter un budget",
            "J'oublie certaines dépenses ou abonnements",
            "Je manque de visibilité sur mes dépenses",
            "J'ai du mal à mettre de l'argent de côté",
            "Je ne rencontre pas de difficulté particulière",
            "Autre"
        ]
    )

    objectif = st.multiselect(
        "Quels sont vos objectifs financiers actuels ?",
        [
            "Réduire mes dépenses",
            "Épargner régulièrement",
            "Constituer une épargne de précaution",
            "Préparer un projet",
            "Rembourser des dettes",
            "Mieux comprendre mes habitudes",
            "Aucun objectif particulier",
            "Autre"
        ]
    )

    fonctionnalites = st.multiselect(
        "Quelles fonctionnalités pourraient vous être utiles ?",
        [
            "Suivre automatiquement mes dépenses",
            "Classer les dépenses par catégorie",
            "Visualiser mes dépenses avec des graphiques",
            "Définir un budget mensuel",
            "Suivre un objectif financier",
            "Recevoir des alertes",
            "Identifier les dépenses inhabituelles",
            "Obtenir des conseils personnalisés",
            "Exporter mes données",
            "Aucune de ces fonctionnalités",
            "Autre"
        ]
    )

    # -------------------------
    # Applications existantes
    # -------------------------

    st.header("📱 Vos expériences avec les applications")

    deja_utilise = st.radio(
        "Avez-vous déjà utilisé une application de gestion des dépenses ?",
        [
            "Oui",
            "Non",
            "Je ne sais plus"
        ]
    )

    abandon = st.radio(
        "Avez-vous déjà abandonné l'utilisation d'une telle application ?",
        [
            "Oui",
            "Non",
            "Je n'en ai jamais utilisé"
        ]
    )

    raison_abandon = st.multiselect(
        "Pour quelles raisons avez-vous arrêté ou pourriez-vous arrêter ?",
        [
            "Application trop compliquée",
            "Trop de saisie manuelle",
            "Manque d'intérêt",
            "Informations peu utiles",
            "Manque de temps",
            "Problème de confiance ou de sécurité",
            "Notifications trop nombreuses",
            "Je n'ai jamais arrêté",
            "Autre"
        ]
    )

    # -------------------------
    # Connexion bancaire
    # -------------------------

    st.header("🏦 Connexion bancaire")

    connexion_bancaire = st.radio(
        "Seriez-vous prêt(e) à connecter votre compte bancaire à une application ?",
        [
            "Oui, sans problème",
            "Oui, mais seulement si les garanties sont claires",
            "Je ne sais pas",
            "Non"
        ]
    )

    freins_bancaires = st.multiselect(
        "Qu'est-ce qui pourrait vous freiner ?",
        [
            "La sécurité des données",
            "La peur d'une fraude",
            "Le manque d'informations",
            "L'accès aux données bancaires",
            "La complexité de la connexion",
            "Je préfère saisir mes dépenses manuellement",
            "Aucun frein particulier",
            "Autre"
        ]
    )

    # -------------------------
    # Intérêt et prix
    # -------------------------

    st.header("💡 Votre intérêt")

    intention_usage = st.select_slider(
        "Quelle serait votre probabilité d'utiliser une application répondant à vos besoins ?",
        options=[
            "Très faible",
            "Faible",
            "Moyenne",
            "Élevée",
            "Très élevée"
        ]
    )

    prix = st.selectbox(
        "Quel montant mensuel pourriez-vous envisager pour une version complète ?",
        [
            "Je ne paierais pas",
            "Moins de 3 €",
            "3 à 5 €",
            "5 à 8 €",
            "Plus de 8 €",
            "Je ne sais pas"
        ]
    )

    # -------------------------
    # Dimension sociale
    # -------------------------

    st.header("👥 Dimension sociale")

    aisance_sociale = st.slider(
        "Seriez-vous à l'aise pour participer à un défi financier avec des proches ?",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = pas du tout à l'aise, 5 = très à l'aise"
    )

    commentaire = st.text_area(
        "Avez-vous une remarque ou une suggestion ?"
    )

    envoyer = st.form_submit_button(
        "Envoyer mes réponses",
        use_container_width=True
    )


# =============================
# Enregistrement
# =============================

if envoyer:

    reponse = {
        "id_reponse": str(uuid.uuid4()),
        "date_reponse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "age": age,
        "situation": situation,
        "revenu": revenu,
        "outils_actuels": ", ".join(outils_actuels),
        "frequence_consultation": frequence,
        "difficulte_gestion": difficulte,
        "categories_depenses": ", ".join(categories_depenses),
        "difficultes": ", ".join(declencheur),
        "objectifs": ", ".join(objectif),
        "fonctionnalites": ", ".join(fonctionnalites),
        "a_deja_utilise_app": deja_utilise,
        "a_abandonne_app": abandon,
        "raison_abandon": ", ".join(raison_abandon),
        "connexion_bancaire": connexion_bancaire,
        "freins_bancaires": ", ".join(freins_bancaires),
        "intention_usage": intention_usage,
        "prix_premium": prix,
        "aisance_sociale": aisance_sociale,
        "commentaire": commentaire
    }

    try:
        enregistrer_reponse(reponse)

        st.success(
            "Merci pour votre participation ! "
            "Votre réponse a bien été enregistrée."
        )

    except Exception as erreur:
        st.error(
            "Une erreur est survenue lors de l'enregistrement. "
            "Vérifiez la connexion Google Sheets."
        )
        st.exception(erreur)
