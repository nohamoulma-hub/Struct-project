# Struct-project

Outil qui structure un nouveau projet grâce à plusieurs agents Claude coordonnés. Il reçoit le besoin d'un client, le fait valider, puis produit un repo Git prêt à coder et un prototype frontend.

Projet personnel d'apprentissage, pensé pour être réutilisé à chaque nouveau projet.

## Structure

- `brief/` : brief de l'agent principal et modèle du brief projet (mémoire partagée)
- `agents/` : configuration des agents (`config.yaml`) et une fiche par agent
- `frontend/` : prototype HTML/CSS vanilla (vide pour l'instant)
- `skills/` : procédures réutilisables (vide pour l'instant)
- `projets-types/` : cas de test fictifs pour vérifier la chaîne d'agents
- `scripts/` : script qui lance un projet type sur la chaîne d'agents, et script de contrôle de fiabilité
- `controle/` : questions dont la réponse est connue, pour mesurer la fiabilité des agents
- `resultats/` : briefs produits par les tests (ignoré par Git)
- `Dockerfile` et `.dockerignore` : conteneur qui fait tourner les tests, avec Python et le SDK
- `JOURNAL.md` : suivi des sessions
- `contexte.md` : sujet, tâches, stack, attendus

## Statut

Phase de conception. Les fiches des dix agents sont écrites, et le script de test fait tourner les phases 1 à 3 sur deux projets types. La fiabilité des réponses des agents reste à améliorer, voir `JOURNAL.md`.

## Lancer un test

Il faut Docker, et une clé API Anthropic dans un fichier `.env` à la racine. Ce fichier n'est jamais commité.

```bash
docker build -t struct-project .
docker run --rm --name Struct-project --env-file .env -v "$(pwd)/resultats:/app/resultats" struct-project python3 scripts/lancer_projet_type.py projets-types/gestion-stock-atelier.md
```

La réponse de l'agent principal est enregistrée dans `resultats/`, avec le coût du test.
