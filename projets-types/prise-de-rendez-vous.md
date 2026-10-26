# Projet type : prise de rendez-vous

**Pourquoi ce projet** : il oblige la chaîne à traiter des données personnelles (sécurité, RGPD) sans complexité de paiement.

## Client fictif
Salon de coiffure « Salon Test », 2 employés, un agenda commun.

## Réponses simulées du client (pour l'agent chat)
- Objectif : les clients réservent un créneau en ligne, sans appeler.
- Utilisateurs : les clients du salon (grand public) et les deux employés.
- Fonctionnalités indispensables : choisir une prestation, choisir un créneau, recevoir une confirmation.
- Fonctionnalités souhaitées : annuler un rendez-vous, recevoir un rappel la veille.
- Données : nom, téléphone, email, historique des rendez-vous.
- Pas de paiement en ligne.

## Informations volontairement absentes
- Budget : non donné.
- Délais : non donnés.
- Hébergement : non précisé.

Ces trois points doivent apparaître comme « À confirmer ». Si un agent les invente, c'est un échec du test.

## Ce qu'on vérifie
- `chat` remplit les besoins bruts sans reformuler.
- `securite` signale les données personnelles et les obligations RGPD.
- `devops` rend `question` sur l'hébergement, au lieu de le choisir.
- Aucun agent n'invente budget, délais ou hébergement.
- Les checkpoints 1, 2 et 3 sont bien présentés à Noham.
