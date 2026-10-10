> Campagne : **toutes-langues** · expérience **09**
> Titre : 9. Dimensionnement de l'analyse finale, mesuré
> Date réelle : **2026-10-06 00:24 HAE** (source : commit `a96b553`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 9. Dimensionnement de l'analyse finale, mesuré

Avant de laisser tourner, j'ai chiffré ce que coûtera l'analyse sur les **351
langues** d'apprentissage (301 + 50), au lieu de le découvrir à 3 h du matin.

| | |
|---|---:|
| cache attendu | **~437 000 positions** · ~919 Mo |
| mémoire du readout quadratique (120 neurones → 240 colonnes) | 419 Mo |
| disque libre / RAM disponible | 2,1 To / 108 Go |

**Le coût dominant est la régression**, mesuré sur des matrices à l'échelle :

| taille de X | `XᵀX + XᵀY` |
|---|---:|
| 154 307 × 120 | 4,5 s |
| 436 788 × 120 | 11,4 s |
| **436 788 × 240** (readout quadratique) | **22,0 s** |

Soit **~22 s par neurone** — et 35 min à 1,7 h par run selon que la naissance
s'arrête à 40 ou à 120 neurones. L'analyse en fait deux.

**Décision : on n'optimise pas.** Il serait facile de rendre cette étape 20× plus
rapide en maintenant la Gram `XᵀX` de façon incrémentale — ajouter UN neurone ne
change qu'une ligne et une colonne. Mais la chaîne est **validée de bout en bout**,
et le temps n'est pas le facteur limitant : la phase 1 ne finit pas avant 02h30 de
toute façon. Toucher à un pipeline vérifié pour gagner une heure qu'on n'attend pas
serait un mauvais échange. Le chiffre est consigné pour que la décision soit
réexaminable si le volume change.


---
