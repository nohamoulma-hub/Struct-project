"""
Lance le premier test de la chaîne d'agents sur un projet type.

Usage, depuis la racine du repo :
    python3 scripts/lancer_projet_type.py projets-types/prise-de-rendez-vous.md

Ce test lance les phases 1 à 3, jusqu'au checkpoint 2. Le checkpoint 1 est
simulé comme validé, avec les points « À confirmer » encore ouverts.
"""

import asyncio
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions, ResultMessage, query

# Dossier racine du repo, calculé depuis l'emplacement de ce script
RACINE = Path(__file__).resolve().parent.parent

# Plafond de dépense pour un test, en dollars, pour éviter une facture surprise.
# Les phases 1 à 3 coûtent plus cher que la phase 1 seule, d'où un plafond plus haut.
BUDGET_MAX_USD = 5.0

# Agents qui doivent citer des sources : ils ont aussi accès au web
AGENTS_AVEC_WEB = {"architecture", "stack", "securite"}


def lire_fichier(chemin):
    # Ouvre un fichier du repo et renvoie son texte, comme lire une fiche de recette
    return (RACINE / chemin).read_text(encoding="utf-8")


def lire_champ(nom_agent, champ):
    # Cherche dans agents/config.yaml la valeur d'un champ (modele, role...) pour un agent
    # Le fichier est lu ligne par ligne, comme on suit une liste de courses jusqu'à la bonne rubrique
    dans_bloc = False
    for ligne in lire_fichier("agents/config.yaml").splitlines():
        # Une ligne "  nom:" ouvre le bloc d'un agent
        if re.match(r"^  \w+:\s*$", ligne):
            dans_bloc = ligne.strip() == f"{nom_agent}:"
        elif dans_bloc and ligne.strip().startswith(f"{champ}:"):
            return ligne.split(":", 1)[1].strip()
    raise ValueError(f"Champ {champ} introuvable pour l'agent {nom_agent}")


def lister_sous_agents():
    # Liste les noms des agents du config, sauf le principal (qui orchestre les autres)
    noms = re.findall(r"^  (\w+):\s*$", lire_fichier("agents/config.yaml"), re.MULTILINE)
    return [nom for nom in noms if nom != "principal"]


def construire_sous_agents():
    # Crée une définition par agent : son rôle, sa fiche et les règles communes
    regles = lire_fichier("brief/regles-agents.md")
    agents = {}
    for nom in lister_sous_agents():
        fiche = lire_fichier(f"agents/{nom}.md")
        # Lecture seule, plus la recherche web pour les agents qui citent des sources
        outils = ["Read", "Grep", "Glob"]
        if nom in AGENTS_AVEC_WEB:
            outils += ["WebSearch", "WebFetch"]
        agents[nom] = AgentDefinition(
            description=lire_champ(nom, "role"),
            # La fiche et les règles forment la consigne de l'agent
            prompt=f"{regles}\n\n{fiche}",
            tools=outils,
            model=lire_champ(nom, "modele"),
        )
    return agents


def verifier_liens(texte):
    # Ouvre chaque lien trouvé dans le texte et note s'il répond,
    # comme on essaie chaque numéro d'une liste pour voir lequel est encore valide
    liens = sorted({lien.rstrip(".,;:") for lien in re.findall(r"https?://[^\s)\]>\"']+", texte)})
    lignes = []
    for lien in liens:
        requete = urllib.request.Request(lien, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(requete, timeout=10) as reponse_web:
                etat = f"OK ({reponse_web.status})"
        except urllib.error.HTTPError as erreur:
            etat = f"erreur HTTP {erreur.code}"
        except (urllib.error.URLError, TimeoutError):
            etat = "injoignable"
        lignes.append(f"- {lien} : {etat}")
    return lignes


def enregistrer_trace(chemin_projet, reponse, cout, verification):
    # Range la réponse du principal dans resultats/, avec la date dans le nom,
    # comme on classe une copie de chaque test dans un classeur daté
    dossier = RACINE / "resultats"
    dossier.mkdir(exist_ok=True)
    horodatage = datetime.now().strftime("%Y-%m-%d_%H-%M")
    chemin = dossier / f"{horodatage}_{Path(chemin_projet).stem}.md"
    # Ajoute la liste des liens vérifiés, ou une ligne si la réponse n'en cite aucun
    liens = "\n".join(verification) if verification else "Aucun lien cité."
    chemin.write_text(
        f"{reponse}\n\n---\n## Vérification des liens\n{liens}\n\nCoût du test : {cout} $\n",
        encoding="utf-8",
    )
    return chemin


async def lancer(chemin_projet):
    # Prépare la mission du principal : le projet type et ce qu'on attend de lui
    mission = (
        "Pour ce test, le checkpoint 1 est considéré comme validé, avec les points "
        "« À confirmer » encore ouverts (décision de test, pas une validation réelle). "
        "Enchaîne donc les phases suivantes, pour le projet type ci-dessous :\n"
        "- Phase 1 (découverte) : délègue la conversation au sous-agent `chat`, en lui "
        "donnant les réponses simulées du client. Rédige le résumé du besoin.\n"
        "- Phase 2 (cadrage) : délègue à `planification` et à `ux`.\n"
        "- Phase 3 (conception) : délègue à `architecture`, puis à `stack`, qui dépend "
        "de l'architecture.\n"
        "Arrête-toi au checkpoint 2 : présente l'architecture et la stack à Noham pour "
        "validation. Ne lance pas les phases 4 à 7.\n"
        "Conserve dans ta réponse finale les liens cités par les sous-agents : "
        "les liens sont vérifiés à partir de ta réponse.\n"
        "Ne tente pas d'écrire de fichier : ta réponse finale est enregistrée automatiquement.\n\n"
        f"--- PROJET TYPE ---\n{lire_fichier(chemin_projet)}\n--- FIN ---\n\n"
        f"--- MODÈLE DE BRIEF ---\n{lire_fichier('brief/modele-brief-projet.md')}"
    )
    # Le brief du principal sert de consigne système, avec les règles communes
    consigne = f"{lire_fichier('brief/agent-principal.md')}\n\n{lire_fichier('brief/regles-agents.md')}"
    options = ClaudeAgentOptions(
        system_prompt=consigne,
        model=lire_champ("principal", "modele"),
        agents=construire_sous_agents(),
        allowed_tools=["Read", "Grep", "Glob", "Agent"],
        max_budget_usd=BUDGET_MAX_USD,
    )
    reponse = ""
    cout = None
    # Garde la réponse finale du principal et le coût du test
    async for message in query(prompt=mission, options=options):
        if isinstance(message, ResultMessage):
            reponse = message.result
            cout = message.total_cost_usd
    chemin = enregistrer_trace(chemin_projet, reponse, cout, verifier_liens(reponse))
    print(reponse)
    print(f"Coût du test : {cout} $")
    print(f"Trace enregistrée : {chemin}")


def main():
    # Vérifie qu'un fichier de projet type a bien été donné en argument
    if len(sys.argv) != 2:
        print("Usage : python3 scripts/lancer_projet_type.py projets-types/<fichier>.md")
        sys.exit(1)
    asyncio.run(lancer(sys.argv[1]))


if __name__ == "__main__":
    main()
