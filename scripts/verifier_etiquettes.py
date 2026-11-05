"""
Vérifie les étiquettes « sourcée » ou « non sourcée » dans une trace de test.
Ce contrôle n'appelle aucune API : il est gratuit.

Usage, depuis la racine du repo :
    python3 scripts/verifier_etiquettes.py resultats/<fichier>.md

Le script est un aide, pas un juge : il liste les puces sans étiquette,
à relire à la main.
"""

import sys
from pathlib import Path

# Marqueurs qui indiquent une étiquette de confiance
ETIQUETTES = ("non sourcée", "sourcée")

# Longueur minimale d'une puce pour la considérer comme une affirmation
LONGUEUR_MINI = 40

# Sections qui ne contiennent pas d'affirmation technique (réponses du client, questions)
SECTIONS_IGNOREES = ("découverte", "besoin", "question", "décision", "checkpoint", "reste à faire")


def corps_de_la_trace(texte):
    # Garde la partie avant la liste des liens : les liens n'ont pas besoin d'étiquette
    return texte.split("## Vérification des liens")[0]


def affirmations_techniques(lignes):
    # Parcourt la trace et garde les puces longues, hors sections ignorées
    dans_section_ignoree = False
    resultat = []
    for ligne in lignes:
        propre = ligne.strip()
        # Un titre (ligne commençant par #) ouvre une nouvelle section
        if propre.startswith("#"):
            dans_section_ignoree = any(mot in propre.lower() for mot in SECTIONS_IGNOREES)
        elif not dans_section_ignoree and propre.startswith(("- ", "* ")) and len(propre) >= LONGUEUR_MINI:
            resultat.append(propre)
    return resultat


def a_une_etiquette(ligne):
    # Vérifie si la ligne contient une des étiquettes (sans tenir compte des majuscules)
    return any(etiquette in ligne.lower() for etiquette in ETIQUETTES)


def verifier(chemin):
    # Compte les affirmations étiquetées et affiche celles qui ne le sont pas
    texte = Path(chemin).read_text(encoding="utf-8")
    lignes = corps_de_la_trace(texte).splitlines()
    affirmations = affirmations_techniques(lignes)
    sans_etiquette = [ligne for ligne in affirmations if not a_une_etiquette(ligne)]

    print(f"Affirmations techniques (puces) : {len(affirmations)}")
    print(f"Avec étiquette : {len(affirmations) - len(sans_etiquette)}")
    print(f"Sans étiquette : {len(sans_etiquette)}")
    for ligne in sans_etiquette:
        # Retire le tiret de la puce avant d'afficher la ligne
        print(f"  - {ligne.lstrip('-* ')[:120]}")


def main():
    # Vérifie qu'un fichier de trace a bien été donné en argument
    if len(sys.argv) != 2:
        print("Usage : python3 scripts/verifier_etiquettes.py resultats/<fichier>.md")
        sys.exit(1)
    verifier(sys.argv[1])


if __name__ == "__main__":
    main()
