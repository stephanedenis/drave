# 5. La pensée sans verbaliser — le travail de la nuit du 16 octobre

## La question, et pourquoi elle n'est pas abstraite

Un modèle de langue « réfléchit » en **écrivant** : chaque pas de pensée est un jeton, qu'il relit ensuite.
Un cerveau d'expert fait l'inverse — il pense **sans dialogue intérieur**. Peut-on obtenir la même chose
d'un modèle ?

C'est une question **exécutable** avec Drave, parce que le moteur sait déjà **écrire et relire un état** :
on peut faire évoluer la pensée **sans qu'aucun jeton ne soit émis**.

![Penser sans verbaliser](schemas/pensee.svg)

## Ce que la nuit a mesuré, dans l'ordre

| étape | le résultat | ce qui a été appris |
|---|---|---|
| **réinjecter l'état brut** | la prédiction détruit de 5 ordres de grandeur (×30 000) | et **normer n'y change rien** : ce n'est pas l'échelle |
| **apprendre un pont** | l'état mappé bat le mot (68,6 % contre 122,9 %) | la sortie prélinguistique **dit mieux** que le jeton |
| **mesurer l'écart** | facteur **648** d'échelle, cosinus **+0,14** | les deux espaces ne sont pas le même |
| **aligner** | cosinus **0,70**, échelle **1,015** — et la langue **s'améliore** | l'alignement est un régularisant, pas un coût |
| **boucler quand même** | λ = **7 311**, contenu détruit | aligner les espaces ne suffit pas : il faut la **dynamique** |
| **opérateur post-hoc** | λ = **0,997** (le premier pas contractant) et +15 points… sur **un** pas | l'itération n'accumule pas |
| **récurrence à l'entraînement** | itération **plate** (88,4 · 88,2 · 88,5) | l'état devient **habitable** — au prix de 5 points |
| **la falaise** | dès le premier pas de récurrence | ce n'est pas un réglage, c'est un **interrupteur** |
| **la cause** | déplacement 44,8 % contre 77,5 % | les modèles plats ont appris un **point fixe** |

## Les trois piliers, et ce qu'ils valent

Après avoir **réparé l'instrument** (un λ de ridge choisi par validation croisée, et une batterie de
longueurs), trois conclusions **survivent** :

1. **l'état porte le sens** : 16 jetons d'avance à **80,3 %**, quand le mot est à **118,4 %** — 38 points
   d'écart ; et l'empreinte de copie à **49,3 % contre 76,9 %** en lecture (trois exécutions) ;
2. **l'itération s'obtient et se paie** : plate, contre **+3,2** points de lisibilité à 2,43 M et **+2,4** à
   9,57 M — le prix **baisse** avec la capacité, lentement ;
3. **la récurrence n'est pas qu'un coût** : elle **améliore** le modèle de langue (2,73 contre 2,76
   bits/octet). *Le modèle qui pense est aussi un meilleur lecteur.*

## Ce qui reste à construire

Une **dynamique apprise, contractante et informative** — c'est-à-dire un pas de pensée qui ne dérive pas et
qui ne perde pas le contenu. Le prix est connu (la falaise), le gain aussi (la récurrence améliore la
langue), et la mesure est outillée (`tools/banc_lecteur.py`, `tools/operateur_pensee.py`).
