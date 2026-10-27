# Journal

## 2026-10-23

- Définition des agents et de leur rôle.
- Choix du modèle par agent. Les lignes marquées `a_tester` seront tranchées avec les projets types.
- Rédaction du brief de l'agent principal (en attente de validation).
- Création de la structure du repo, sans commit.
- Déplacement du travail dans le dossier `Struct-project`, qui contient déjà le dépôt Git lié à GitHub.
- Vérification de Claude Agent SDK (sous-agents) et de GitHub Actions dans la documentation officielle.
- Agent devops : rôle précisé (vérification technique en phase 6, CI/CD en phase 7), modèle Sonnet, statut valide. Phases 6 et 7 et liste des agents mises à jour dans le brief.
- Règles communes à tous les agents rédigées dans `brief/regles-agents.md`. Règles de l'agent principal allégées pour éviter les doublons. Fiches par agent à venir dans `agents/`.
- Fiches écrites dans `agents/` pour les 10 agents (devops, chat, planification, ux, architecture, stack, securite, frontend, documentation, validation, compte_rendu). L'agent principal reste décrit dans `brief/agent-principal.md`.

## 2026-10-26

- Relecture des fiches d'agents, validée.
- Premier projet type choisi : prise de rendez-vous pour un petit commerce fictif. Écrit dans `projets-types/prise-de-rendez-vous.md`, avec une ligne ajoutée au README.
- Script `scripts/lancer_projet_type.py` écrit (phase 1 seulement, agents en lecture seule, plafond de dépense de 2 $). Non installé ni lancé.
- Constat : Python 3.9 installé, le SDK demande une version plus récente. Installation et lancement à valider.
- Conteneur mis en place : `Dockerfile` (Python 3.12 et SDK) et `.dockerignore` (exclut `.git` et les fichiers `.env`). Image construite sous le nom `struct-project`, le conteneur se lance sous le nom `Struct-project`. Import du SDK vérifié dans le conteneur. Le test n'a pas été lancé, il consomme des crédits API.
- Ajout de `.gitignore` (exclut `.env` et `.DS_Store`) et d'un `.env` vide, à remplir avec la clé API par Noham. Le `.env` ne doit jamais être commité.
- Premier lancement du test `prise-de-rendez-vous` : la chaîne tourne jusqu'au checkpoint 1, le statut `question` est rendu, budget, délais et hébergement restent « À confirmer ». Le brief n'a pas été enregistré (écrit dans le conteneur, supprimé avec `--rm`).
- Écart relevé : « problème résolu » déduit de « sans appeler », alors que le client ne l'a pas dit. À corriger dans les règles avant le prochain projet type.
- Dossier `resultats/` créé et ignoré par Git, pour garder une trace des tests (montage avec `-v "$(pwd)/resultats:/app/projets"`).
- Règles ajoutées : une déduction n'est pas une information (`brief/regles-agents.md`, `agents/chat.md`). Image reconstruite avant le relancement.
- Second test : « problème résolu » passe bien en « À confirmer ». Le brief n'est toujours pas enregistré : le principal n'a pas d'outil d'écriture (`Write` absent de `allowed_tools`). Proposition : le script enregistre lui-même la réponse dans `resultats/` et affiche le coût.
- Coût estimé du test phase 1 : environ 1 $ (Opus 5.5 : 4 $ / 20 $ par million de tokens). Non mesuré, à confirmer quand le script affichera le coût réel.
- Script modifié : il enregistre la réponse finale dans `resultats/` (nom daté) et affiche le coût réel. Le principal est prévenu qu'il ne doit pas écrire de fichier. Fonction d'enregistrement testée dans le conteneur, sans appel à l'API.
- Montage à utiliser désormais : `-v "$(pwd)/resultats:/app/resultats"`.
- Checkpoint 1 du projet type `prise-de-rendez-vous` validé par Noham avec les points « À confirmer » ouverts (option b, comme prévu par le scénario).
- Premier test complet enregistré : `resultats/2026-10-26_12-13_prise-de-rendez-vous.md`. Coût réel : 0,18 $, soit bien moins que l'estimation de 1 $. « Problème résolu » reste « À confirmer ».
- Décision de Noham sur le checkpoint 1 : option b (résumé accepté, budget, délais, hébergement et existant restent « À confirmer »). Moyen d'envoi de la confirmation et du rappel : également « À confirmer ».
- Deuxième projet type écrit : `projets-types/gestion-stock-atelier.md` (stock d'un atelier de vélos, sans données clients).
- Script étendu aux phases 1 à 3 (jusqu'au checkpoint 2). Le checkpoint 1 est simulé comme validé, avec les points « À confirmer ». Plafond de dépense relevé à 5 $. Vérifié dans le conteneur, sans appel à l'API.
- Test `gestion-stock-atelier` lancé jusqu'au checkpoint 2. Coût : 0,73 $. Trace : `resultats/2026-10-26_12-30_gestion-stock-atelier.md`.
- Constats du test : `architecture` et `stack` ont figé deux règles que le client n'a pas données (références uniques, stock jamais négatif), et `stack` a justifié Node.js par une supposition sur la personne qui maintiendra le code. Le principal l'a relevé lui-même. Aucune source officielle n'est citée, alors que la règle l'exige. Correctif à valider : règles de conception et exigence de sources.
- Validé et appliqué : `architecture`, `stack` et `securite` reçoivent la recherche web (`WebSearch`, `WebFetch`). Règle sur les sources : lien consulté, sinon « source à vérifier ». Image reconstruite et vérifiée.
- Ouvert : la fiabilité des réponses. Pistes : vérifier mécaniquement les liens de la trace, marquer chaque affirmation (sourcée, estimée, à vérifier), faire relire les sources par `validation`, et tester les agents sur des questions dont la réponse est connue. Ce chantier n'est pas encore décidé.
- README mis à jour (statut, lancement d'un test, nouveaux fichiers). Push préparé sur une branche séparée de `main`.
- Branche renommée `dev` (au lieu de `add/agents-et-tests`).
- Validé et appliqué, pistes 1 à 3 : vérification automatique des liens de la trace (`verifier_liens`, testée hors API) ; étiquettes « sourcée », « estimée », « à vérifier » dans les règles communes ; rappel « ne fige jamais une règle métier que le client n'a pas donnée » dans les fiches `architecture` et `stack`.
- Le principal doit conserver les liens des sous-agents dans sa réponse finale, sinon la vérification ne voit rien.
- Pistes 4 (relecture des sources par `validation`) et 5 (questions de contrôle) : pas encore décidées.
- Piste 4 ajoutée : `validation` reçoit la recherche web et vérifie les liens cités par `architecture` et `stack` (mission du script et fiche `validation.md`). Non testée avec l'API.
- Piste 5 ajoutée : dix questions dans `controle/questions-fiabilite.json`, chacune vérifiée à la source le 26/10/2026 (dont une question piège sur la version de Python, que la doc ne précise pas). Script `scripts/controle_fiabilite.py`, qui écrit les réponses dans `resultats/` pour relecture. Non lancé : il consomme des crédits API.
- Commits sur `dev` (1792f24), puis `main` mis à jour par fast-forward avec le même commit.
- Premier contrôle lancé : `resultats/2026-10-26_13-42_controle.md`, coût 0,85 $. 9 réponses justes sur 10, chacune avec une source qui répond (200).
- Erreur de ma part : la question 10 était fausse. Je n'avais lu que la page de référence du SDK, pas le quickstart, qui indique « Python 3.10+ ». L'agent a eu raison. La question est corrigée dans le JSON (réponse attendue : Python 3.10).
- Limite relevée : vérifier qu'un lien répond ne prouve pas que la page confirme l'affirmation. C'est le rôle de la relecture par `validation` (piste 4), qui n'est pas encore testée.
- Test complet `gestion-stock-atelier` jusqu'au checkpoint 2 : `resultats/2026-10-26_13-46_gestion-stock-atelier.md`, coût 0,86 $.
  - Amélioration : plus de règle métier figée (architecture en deux options A et B, avec des questions au client). Plus de supposition sur Node.js.
  - Piste 4 fonctionnelle : `validation` a relu les pages et a corrigé deux affirmations (HTTPS « dans certains navigateurs », `persist()` sans garantie).
  - Problème 1 : `validation` a rendu « bloque » pour de simples corrections de formulation. Le statut est trop sévère. À revoir.
  - Problème 2 : la RFC 4180 répond 200 au contrôle mécanique, mais `validation` la déclare inaccessible. Les deux vérifications ne sont pas équivalentes.
  - Problème 3 : `architecture` demande une autorisation d'accès à des domaines. Ce n'est pas une décision que Noham peut prendre ici. La question doit être supprimée des décisions attendues.
  - Étiquettes « sourcée », « estimée », « à vérifier » : présentes, mais pas systématiques.
- 2026-10-27 : corrections appliquées.
  - Chaque affirmation technique est « sourcée » ou « non sourcée », sans exception (`brief/regles-agents.md`).
  - Un agent ne demande plus à Noham d'autoriser un accès technique.
  - `validation` rend `ok` pour une simple correction de formulation, et `bloque` seulement pour une incohérence grave (`agents/validation.md`).
  - Correction de la question 10 du contrôle dans le JSON.
  - Relance du test complet `gestion-stock-atelier` en cours.
- Résultat de la relance : `resultats/2026-10-27_09-29_gestion-stock-atelier.md`, coût 1,38 $ (contre 0,86 $ avant, à cause de la relecture).
  - Étiquettes : 12 « sourcée » et 10 « non sourcée ». La règle est bien appliquée.
  - Question d'autorisation d'accès : absente. Réglé.
  - RFC 4180 : expliquée à Noham (format CSV, document IETF d'information, non norme).
  - Point non réglé : `validation` a encore rendu `bloque`, pour cinq formulations, alors que la fiche demande `ok` avec corrections. Il faut renforcer la consigne dans la mission du script.
  - Bug relevé : l'expression qui extrait les liens capture un accent grave à la fin (`http://localhost`), d'où un lien « injoignable » parasite. Il faut exclure le caractère dans la regex.
