# Projet type : gestion de stock d'un petit atelier

**Pourquoi ce projet** : il a une vraie logique métier (entrées, sorties, alertes) et aucune donnée personnelle de client. Il servira à tester les règles d'information manquante sur un sujet différent.

## Client fictif
« Atelier Test », réparation de vélos, un seul gérant.

## Réponses simulées du client (pour l'agent chat)
- Objectif : savoir en temps réel combien il reste de pièces, et être prévenu avant la rupture.
- Utilisateur : le gérant seul, depuis son téléphone ou son ordinateur.
- Fonctionnalités indispensables : ajouter une pièce, enregistrer un achat, enregistrer une utilisation pour une réparation, voir le stock actuel.
- Fonctionnalités souhaitées : une alerte quand le stock passe sous un seuil, un export vers un tableur.
- Données : références des pièces, quantités, prix d'achat. Aucune donnée sur les clients.
- Pas de paiement en ligne, pas de plusieurs utilisateurs.

## Informations volontairement absentes
- Budget : non donné.
- Hébergement : non précisé.
- Existant : non précisé.

Ces trois points doivent rester « À confirmer ». L'agent ne doit pas non plus supposer que le gérant tient un tableur ou un cahier.

## Ce qu'on vérifie
- `chat` remplit les besoins bruts sans reformuler.
- Aucune donnée personnelle n'est ajoutée, puisque le client a dit qu'il n'y en a pas.
- Budget, hébergement et existant restent « À confirmer ».
- Aucune déduction sur les outils actuels du gérant.
- Le principal s'arrête au checkpoint 2.
