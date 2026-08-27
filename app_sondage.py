const ID_TABLEUR = "1jUhGKTxuyQm0I2swoIiaMXJjLTiTj8vVkoVJsZJ90O8";
const NOM_ONGLET = "Réponses";

const COLONNES = [
  "id_reponse",
  "date_reponse",
  "age",
  "situation",
  "revenu",
  "outils_actuels",
  "frequence_consultation",
  "difficulte_gestion",
  "categories_depenses",
  "difficultes",
  "objectifs",
  "fonctionnalites",
  "a_deja_utilise_app",
  "a_abandonne_app",
  "raison_abandon",
  "connexion_bancaire",
  "freins_bancaires",
  "intention_usage",
  "prix_premium",
  "aisance_sociale",
  "commentaire"
];


function doPost(e) {
  try {
    const feuille = SpreadsheetApp
      .openById(ID_TABLEUR)
      .getSheetByName(NOM_ONGLET);

    if (!feuille) {
      throw new Error("L'onglet « Réponses » est introuvable.");
    }

    const donnees = JSON.parse(e.postData.contents);

    // Création automatique de la ligne d'en-têtes
    if (feuille.getLastRow() === 0) {
      feuille.appendRow(COLONNES);
    }

    const ligne = COLONNES.map(function(colonne) {
      return donnees[colonne] ?? "";
    });

    feuille.appendRow(ligne);

    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        message: "Réponse enregistrée"
      }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (erreur) {
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: erreur.message
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}


function doGet() {
  return ContentService
    .createTextOutput("API du sondage active")
    .setMimeType(ContentService.MimeType.TEXT);
}
