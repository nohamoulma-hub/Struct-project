"""
Pose des questions de contrôle à un agent, pour mesurer sa fiabilité.

Usage, depuis la racine du repo :
    python3 scripts/controle_fiabilite.py

Chaque réponse est enregistrée dans resultats/ avec la réponse attendue
et la vérification des liens cités, pour être relue à la main.
"""

import asyncio
import json
from datetime import datetime

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from lancer_projet_type import RACINE, lire_champ, lire_fichier, verifier_liens

# Plafond de dépense pour chaque question, en dollars
BUDGET_PAR_QUESTION_USD = 0.5


def charger_questions():
    # Lit la liste des questions dans controle/questions-fiabilite.json
    return json.loads(lire_fichier("controle/questions-fiabilite.json"))


async def poser_question(question):
    # Pose une question à l'agent architecture, avec la recherche web,
    # et renvoie sa réponse avec le coût de la question
    options = ClaudeAgentOptions(
        system_prompt=lire_fichier("brief/regles-agents.md"),
        model=lire_champ("architecture", "modele"),
        allowed_tools=["WebSearch", "WebFetch"],
        max_budget_usd=BUDGET_PAR_QUESTION_USD,
    )
    reponse, cout = "", None
    prompt = f"Réponds à cette question en citant le lien officiel que tu as consulté : {question}"
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, ResultMessage):
            reponse = message.result
            cout = message.total_cost_usd
    return reponse, cout


async def lancer():
    # Pose toutes les questions, puis range les réponses dans un fichier à relire
    maintenant = datetime.now()
    lignes = [f"# Contrôle de fiabilité, {maintenant:%Y-%m-%d %H:%M}\n"]
    cout_total = 0.0
    for numero, item in enumerate(charger_questions(), start=1):
        reponse, cout = await poser_question(item["question"])
        cout_total += cout or 0
        liens = verifier_liens(reponse)
        piege = " (piège : la bonne réponse peut être une absence d'information)" if item.get("piege") else ""
        lignes.append(f"## Question {numero} : {item['question']}{piege}\n")
        lignes.append(f"**Attendu** : {item['attendu']}\n")
        lignes.append(f"**Réponse de l'agent** :\n\n{reponse}\n")
        lignes.append("**Liens vérifiés** :\n" + ("\n".join(liens) if liens else "Aucun lien cité.") + "\n")
    # Ajoute le coût total en fin de fichier
    lignes.append(f"---\nCoût total du contrôle : {cout_total} $\n")
    dossier = RACINE / "resultats"
    dossier.mkdir(exist_ok=True)
    chemin = dossier / f"{maintenant:%Y-%m-%d_%H-%M}_controle.md"
    chemin.write_text("\n".join(lignes), encoding="utf-8")
    print(f"Coût total : {cout_total} $")
    print(f"Contrôle enregistré : {chemin}")


if __name__ == "__main__":
    asyncio.run(lancer())
