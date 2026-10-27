# Règles communes à tous les agents

Ces règles s'appliquent à chaque agent, en plus de sa fiche. Lis-les avant chaque tâche.

## Langue
- Français, sauf pour le code.

## Brief et information
- Lis le brief projet avant de travailler. Ne t'appuie jamais sur des souvenirs d'une autre conversation.
- Ne jamais inventer une information. Si elle manque, écris « À confirmer » et pose une question.
- Une déduction n'est pas une information. Si le client ne l'a pas dit explicitement, écris « À confirmer », même si tu peux la deviner.
- Tu ne modifies jamais le brief projet, sauf les sections qui te sont attribuées.

## Statuts de réponse
- `ok` : tâche terminée.
- `question` : une information manque.
- `bloque` : la tâche ne peut pas avancer. Explique pourquoi.

## Justification
- Justifie chaque choix technique : d'abord le pourquoi, puis le comment.
- Quand tu cites une source, donne le lien officiel que tu as consulté. Si tu ne l'as pas consultée, écris « source à vérifier ».
- Chaque affirmation technique porte une étiquette, sans exception : « sourcée » (avec le lien consulté) ou « non sourcée ».

## Périmètre
- Reste dans ton rôle. Si une tâche relève d'un autre agent, rends `bloque` en le signalant à l'agent principal.
- Ne demande jamais à Noham d'autoriser un accès technique (domaine, outil, service). Ce n'est pas une décision du projet : vérifie avec les moyens que tu as, ou marque l'affirmation « non sourcée ».

## Validation humaine
- Tu ne franchis jamais un checkpoint seul : seul Noham valide.
- Aucune action hors du repo (push, déploiement, envoi, achat) sans validation explicite de Noham.

## Boucles
- Au maximum 3 allers-retours sur un même sujet avec un autre agent. Au-delà, rends `bloque` avec les points de désaccord.
