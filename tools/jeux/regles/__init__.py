"""Les règles internes des jeux — l'étage 2 ne lit que la RSN.

Chaque module expose un `Jeu` (ou des fonctions) qui convertit la RSN en un état
interne rapide, énumère les coups légaux, applique, teste la terminalité et rend
une utilité du point de vue du joueur au trait. Les codecs de l'étage 1 peuvent
s'en servir pour valider une lecture (niveau 4), jamais l'inverse.
"""
