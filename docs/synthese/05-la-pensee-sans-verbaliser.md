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
| **apprendre un pont** | l'état mappé bat le mot (68,6 % contre 122,9 %) | la sortie prélinguistique **dit mieux** que le **jeton de sortie** |
| **mesurer l'écart** | facteur **648** d'échelle, cosinus **+0,14** | les deux espaces ne sont pas le même |
| **aligner** | cosinus **0,70**, échelle **1,015** — et la langue **s'améliore** | l'alignement est un régularisant, pas un coût |
| **boucler quand même** | λ = **7 311**, contenu détruit | aligner les espaces ne suffit pas : il faut la **dynamique** |
| **opérateur post-hoc** | λ = **0,997** (le premier pas contractant) et +15 points… sur **un** pas | l'itération n'accumule pas |
| **récurrence à l'entraînement** | itération **plate** (88,4 · 88,2 · 88,5) | l'état devient **habitable** — au prix de 5 points |
| **la falaise** | au **troisième** pas (le pas tient deux pas) | le pas partagé dégénère en **point fixe** ; il faut une perte qui l'empêche |
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

**Mesure 77 (20 octobre)** : sur **Qwen2.5-3B** et **139 paragraphes en 12 langues** (corpus JW 2026), un **pont
linéaire** par langue atteint un **cosinus de 0,78-0,92** et retrouve la bonne traduction dans **28-67 %** des cas
(hasard 0,7 %), le contrôle négatif restant à ~0 — *la représentation neutre existe mais doit être alignée*, comme
le pont de la nuit du 16, retrouvé ici à plus grande échelle. **Mesure 78** : le passage du 3 B au 7 B ne change
presque rien (+3,7 en lecture, +1,4 en écriture), **lire ≈ écrire**, et la meilleure couche est **la couche 4** pour
cinq langues — *le sens partagé est tôt et stable ; c'est une base d'architecture, pas un effet de taille*.
**Mesure 79** : la **composition** n'est pas démontrée — seuls les paragraphes **complets** s'alignent (0,2-0,78),
les préfixes de caractères restent près du hasard et la trajectoire est plate ; le test est **confondu** (les
préfixes ne sont pas des unités de sens). **Mesure 80** : sur des phrases **alignées** (Verne FR/EN, 200 phrases),
la composition **est là** — retrieval **0,61** (hasard 0,5 %), **ordre 0,84** (hasard 25 %) à la **couche 18** ; le
pont est inutile (0,42) et la dernière couche s'effondre (0,09) : *le sens est au milieu, la langue à la fin*.
**Mesure 81** : la composition **profite de la taille** — 0,76 / 0,865 au 7 B (couche 14 sur 28, soit 50 % de la
profondeur) contre 0,61 / 0,84 au 3 B (couche 18 sur 36) ; la fin s'effondre encore plus (0,125). *Le sens neutre
vit à mi-profondeur, et la composition est un levier de taille, pas un plafond.* **Mesure 87** : la courbe **plafonne** entre 7 et 14 B
(0,68 / 0,855 au 14 B contre 0,76 / 0,865 au 7 B, avec un OOM de répartition) — *le levier de la composition est la
profondeur et la taille **jusqu'à 7 B**, pas les paramètres au-delà*.
**Le pas de pensée tient deux pas** (le linéaire, la mesure 82 : 0,73 puis 0,53, hasard 25 %) et **s'effondre au
troisième** (0,13). La taille ne l'étend pas (la mesure 83), et **aucun** des opérateurs testés ne l'étend : la
contraction (la mesure 87), le MLP (la mesure 88), la récurrence partagée (la mesure 108), l'**état latent entraîné
avec la tâche** (la mesure 109) — ce dernier **collapse** : le pas 3 monte à 0,60-0,67, mais le pas 1 tombe à 0,00,
parce que le pas partagé **saute au dernier état** (point fixe). *Le problème n'est ni le modèle ni la forme de
l'opérateur : c'est le **pas** qui dégénère en raccourci.*

## Ce qui reste à construire

Une **dynamique qui avance d'un pas à la fois sans se figer** : une perte qui **pénalise le point fixe** (les pas
1/2/3 à égalité), une **reconstruction** de l'état, ou une **variété contrôlée**. Le prix (la falaise) et le gain
(la récurrence améliore la langue) sont connus ; la mesure est outillée (`tools/banc_lecteur.py`,
`tools/operateur_pensee.py`, `tools/composition_latente.py`).
