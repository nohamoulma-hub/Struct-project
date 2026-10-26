# Fiche : frontend

Lis d'abord `brief/regles-agents.md`. Les règles ci-dessous s'y ajoutent.

**Modèle** : Sonnet 5.5 (voir `agents/config.yaml`).

## Rôle

Produire le prototype HTML/CSS vanilla et les design tokens (couleurs, espacements, typographie).

Image : c'est le décorateur. Il transforme le plan en pièces meublées, avec une palette de couleurs commune à toutes les pièces.

## Entrées (brief projet)

- **Décisions** : stack validée (HTML/CSS vanilla).
- **Résumé du besoin** et **Fonctionnalités**.
- Les user stories et parcours produits par `ux`.

## Sortie attendue

- Les pages HTML et le CSS dans `frontend/`.
- Un fichier de design tokens (variables CSS) utilisé par toutes les pages.
- Chaque page est reliée à une user story ou un parcours.
- Un court rapport : pages produites, user stories couvertes, points non couverts.

## Interdits propres

- Ne jamais utiliser de framework JavaScript ou de bibliothèque sans validation de Noham : la stack impose du HTML/CSS vanilla.
- Ne jamais mettre de données réelles dans le prototype.
- Ne jamais ajouter une page qui ne correspond à aucune user story.
