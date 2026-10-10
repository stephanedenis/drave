> Campagne : **toutes-langues** · expérience **21**
> Titre : 21. PIÈGE : l'invariance sur Wikipedia ne veut RIEN dire
> Date réelle : **2026-10-06 05:11 HAE** (source : commit `0ccef36`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 21. PIÈGE : l'invariance sur Wikipedia ne veut RIEN dire

`analyse_final.sh` fait tourner `pont_parallele.py` sur Wikipedia. Or **ce tool
apparie les segments PAR INDEX** : il compare le morceau 1 de l'anglais au morceau 1
du français, etc.

**Sur Wikipedia, ces morceaux n'ont rien à voir.** Vérifié :

| | premiers morceaux |
|---|---|
| anglais | *Actrius*, *Animalia (book)*, *Alain Connes* |
| français | *Algèbre générale*, *Armée républicaine irlandaise*, *Aka* |

Ce sont des **articles différents**, pris dans l'ordre alphabétique de deux wikis
distincts. Le chiffre d'« invariance » que le tool produira est donc **dépourvu de
sens** — il mesurera la similarité entre un film et un article de mathématiques.

**Ce qui reste mesurable sur Wikipedia** : la **fidélité** (notre sortie contre la
couche du professeur, dans chaque langue) et le **transfert** en→fr. Pas
l'invariance : elle exige du contenu **apparié**, et Wikipedia n'en a pas.

**Corrigé dans l'outil** : il imprime maintenant un avertissement explicite quand
on ne lui a pas passé `--apparie`, et signale une valeur basse comme « cohérente
avec un corpus NON apparié — NE PAS l'interpréter ».

**Ce que j'aurais dû faire** : ne pas mettre cette étape dans la chaîne, ou la
garder mais avec un outil qui ne calcule que la fidélité. Je ne peux pas corriger
`analyse_final.sh` — **il tourne**, et l'éditer en cours d'exécution est ce qui a
tué le guetteur de Wikipedia plus tôt. Le chiffre sera donc produit ; il est
désigné ici comme **non interprétable**.


---
