# Rapport — le pont linguistique-sémantique, mesuré

**Mission** (clarifiée par Stéphane) : émuler **en boîte noire** le premier niveau
abstrait des gros modèles — celui où la représentation cesse d'être dominée par la
langue — pour avoir **notre propre pont linguistique-sémantique brut**. Il ne
s'agit pas de reproduire le gros modèle couche par couche, mais d'avoir un modèle
capable de **répondre à ce premier niveau abstrait**, pour n'importe quelle langue.

**Le professeur est une boîte noire** : on ne prend que son entrée et sa sortie.
`--trace-flux` les donne toutes les deux — la **couche 0 est la plongée du jeton**,
la **couche L est la cible**.

## Protocole

- **Corpus** : article 1 de l'UDHR, `tools/extrait_udhr.py`.
- **Entraînement** : 8 langues — deu, eng, fra, ita, nld, por, rus, spa
  (7 écritures latines + le cyrillique).
- **Test** : 6 langues **jamais vues** — ell (grec), heb (hébreu), hin
  (devanagari), jpn (japonais), kor (coréen), tha (thaï). **Six écritures non
  latines absentes de l'entraînement.**
- Mesure : similarité cosinus inter-langue à la dernière position, cosinus moyen
  et **pire paire**.

## Résultat 1 — la récurrence linéaire échoue, et le témoin dit pourquoi

Un étudiant `s_t = A·s_{t-1} + B·e_t` ajusté par moindres carrés (crête, forme
fermée) :

| | fidélité en UN PAS | boucle libre |
|---|---:|---:|
| rang 32 | 0,5822 | 0,0447 |
| rang 64 | 0,5380 | 0,0016 |
| rang 128 | 0,4912 | 0,0579 |
| rang 256 | 0,5654 | 0,1266 |

**La capacité d'état n'est pas le mur** : la fidélité en un pas est plate de 32 à
256. Et la boucle libre reste inutilisable **même en ramenant le rayon spectral de
1,424 à 0,70** — ce n'est donc pas une divergence, c'est que *l'ajustement local
n'optimise pas la trajectoire*.

## Résultat 2 — LE TÉMOIN QUI RENVERSE TOUT : la plongée seule suffit

Une **simple application linéaire de la plongée du jeton courant**, sans aucune
récurrence :

| couche cible | récurrence (1 pas) | **linéaire de e_t seul** |
|---|---:|---:|
| 4 | 0,4664 | **0,9216** |
| 10 | 0,4912 | **0,9021** |
| 17 | 0,4946 | **0,9198** |

**La récurrence n'est pas seulement inutile : elle est deux fois moins bonne.** Le
niveau abstrait du professeur est **déjà à ~90 % déterminé par la plongée du jeton
courant** — les 10 à 17 couches d'attention et de FFN n'ajoutent qu'environ 10 %
de variance.

## Résultat 3 — LE PONT : une matrice 896×896 qui rend la langue invisible

Le même ajustement linéaire, jugé non plus sur sa fidélité mais sur
**l'invariance inter-langue qu'il produit**, sur les 6 écritures **jamais vues** :

| couche cible | professeur (cos moyen / pire paire) | **pont linéaire** |
|---|---|---|
| 4 | 0,6027 / 0,4269 | **0,6965 / 0,5487** |
| 10 | 0,5464 / 0,2790 | **0,6357 / 0,3828** |
| 17 | 0,4609 / 0,2807 | **0,5657 / 0,3867** |

**Le pont rend une représentation PLUS invariante que le professeur lui-même** —
et sur la pire paire, 0,279 → **0,383 (+37 %)** à la couche 10.

**Pourquoi, et c'est le mécanisme** : une **seule** application linéaire doit
servir **toutes** les langues d'entraînement à la fois. Elle ne peut donc retenir
que ce qu'elles ont **en commun**, et laisse tomber ce qui est propre à chacune.
C'est un **projecteur sur le partagé**, obtenu par moindres carrés — sans
récurrence, sans rétropropagation, sans oracle.

Et il fait **mieux que l'annulation oracle** mesurée la nuit dernière
(`tools/cancellation_langue.py` : 0,279 → 0,378, avec un δ calculé **sur les
langues de test**), tout en étant **entièrement hors échantillon**.

## Résultat 4 — validé à l'échelle : 20 langues d'entraînement, 20 langues jamais vues

Les 40 langues de l'UDHR tracées, réparties au hasard 20/20 (graine fixée) :

| couche 10 | cos moyen | pire paire |
|---|---:|---:|
| professeur | 0,6284 | 0,3281 |
| **pont linéaire** | **0,7343** (+17 %) | **0,4421** (+35 %) |

Et le témoin sans récurrence confirme encore : **0,7304** en un pas contre
**0,6600** pour la récurrence linéaire.

**Le chiffre à retenir** : le pont atteint une pire paire de **0,4421**, à
comparer au **0,471** du plateau d'un modèle de **30 B** — soit 60 fois plus gros.
Un pont appris sur un modèle de 0,5 B atteint donc l'invariance inter-langue d'un
modèle bien plus grand.

## Résultat 5 — **UN SEUL NEURONE SUFFIT**, et c'est « l'apprentissage hyper-rapide » annoncé

Intuition de Stéphane : commencer avec **un neurone par sortie**, puis itérer en
ajoutant des neurones pour les exclusivités — l'apprentissage est **hyper-rapide au
début**. C'est exactement le **rang** du pont. Courbe mesurée, 20 langues
d'entraînement → 20 langues jamais vues :

| neurones | fidélité au professeur | **invariance inter-langue** | **pire paire** |
|---|---:|---:|---:|
| **1** | 0,6677 | **0,9492** | **0,7762** |
| 2 | 0,7170 | 0,9347 | 0,8252 |
| 4 | 0,7479 | 0,9139 | 0,7769 |
| 8 | 0,7467 | 0,8847 | 0,6739 |
| 16 | 0,7262 | 0,8431 | 0,5189 |
| 64 | 0,6816 | 0,7658 | 0,4842 |

**Un seul neurone donne 0,9492 d'invariance** — contre **0,6284** pour le
professeur, et **0,471** pour le plateau d'un modèle de **30 B**. Sa pire paire,
**0,7762**, écrase le 0,3281 du professeur.

**Et la courbe dit pourquoi** : le premier neurone capte la **direction partagée,
indépendante de la langue** — c'est le pont brut au sens exact. Les neurones
suivants ajoutent du **détail propre à chaque langue** : la fidélité au professeur
monte (0,668 → 0,748) mais **l'invariance baisse, monotonement** (0,949 → 0,766).

**Il y a donc un compromis, et il est net** : si l'on veut copier le professeur,
il faut des neurones ; si l'on veut le **pont sémantique brut**, **un seul suffit**
et les autres nuisent.

## Résultat 6 — la sonde n'a RIEN prouvé, et je le dis

Pour lever la réserve « plus invariant ≠ meilleur », j'ai voulu mesurer si le pont
garde l'information **prédictive** : une sonde linéaire qui prédit la plongée du
jeton suivant depuis l'état (`tools/sonde_pont.py`).

| état en entrée de la sonde | R² entraînement | R² test |
|---|---:|---:|
| professeur (couche 10) | 0,7088 | **−1,7411** |
| pont | 0,2599 | 0,0066 |
| témoin : plongée du jeton courant | 0,6600 | **−3,3080** |

**Le R² de test est négatif pour LES TROIS, professeur compris.** Une sonde qui ne
transfère pas d'un groupe de langues à l'autre ne dit donc **rien** sur le pont —
elle dit que le dispositif est mauvais (la cible — la plongée du jeton suivant
d'une autre langue — n'est pas dans le même repère).

**Ce n'est pas une preuve, c'est un échec de protocole.** Je le laisse écrit plutôt
que de le passer sous silence, et la réserve du § précédent **reste entière** : le
pont peut jeter de l'information utile, et personne ne l'a mesuré.

## Ce que ça donne à la mission

**Le pont est un artefact concret et mesuré**, et il tient en **UN neurone** :

```
  abstrait = (e_t · W0) · Pᵀ + moy
  W0 : 896 × 1        P : 896 × 1        moy : 896
```

soit ~1 800 nombres, ajustés par moindres carrés sur 20 langues, qui transforment
la plongée d'un jeton de **n'importe quelle langue** en une représentation
inter-langue à **0,9492** (pire paire **0,7762**) sur 20 langues **jamais vues**.

**Artefact** : `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz`
**Applicateur** : `python3 tools/applique_pont.py <pont.npz> <trace.drvf>`
Vérifié sur grec, hébreu, japonais, thaï, coréen — écritures absentes de
l'entraînement.

## Ce que ce rapport ne dit PAS — et il faut le lire avant de s'en servir

1. **Plus invariant ne veut pas dire meilleur.** Le pont peut obtenir son
   invariance en **jetant** de l'information propre à la langue que le professeur,
   lui, porte — et cette information peut servir en aval. Le test qui le dirait :
   brancher le pont devant les couches suivantes du professeur et mesurer ce que
   la **perplexité** devient. **Ce test n'a pas été fait.**
2. **La fidélité au professeur est mesurée sur l'ensemble entraînement + test
   mêlés** (0,90-0,92 en un pas). La fidélité **par langue tenue à l'écart** n'a
   pas été isolée.
3. **Un seul article**, une seule position (la dernière), 14 langues sur 400.
4. **Le pont n'est pas récurrent**, alors que la mission demandait n couches
   récurrentes. La mesure dit que la récurrence linéaire n'apporte rien ici — elle
   ne dit pas qu'une récurrence **non linéaire** (de type DeltaNet, que le moteur
   implémente déjà et qui est vérifiée sur K3) n'apporterait rien.
