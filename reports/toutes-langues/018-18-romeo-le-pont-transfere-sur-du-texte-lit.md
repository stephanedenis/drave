> Campagne : **toutes-langues** · expérience **18**
> Titre : 18. Romeo : le pont transfère sur du texte LITTÉRAIRE
> Date réelle : **2026-10-06 04:27 HAE** (source : commit `9070ecf`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 18. Romeo : le pont transfère sur du texte LITTÉRAIRE

Premier test hors de l'UDHR. Corpus **parallèle** — 24 scènes appariées en/fr —
donc l'invariance se mesure **segment par segment**, et le transfert se mesure
**en entraînant sur l'anglais et en testant sur le français**, sans réapprentissage.

| | |
|---|---:|
| invariance du professeur (segment par segment) | 0,6532 · pire segment 0,2966 |
| fidélité sur l'anglais (apprise) | **0,6660** |
| **fidélité sur le français (transférée)** | **0,5802** |
| **invariance de notre sortie** | **0,9540** · pire segment 0,8738 |
| oracle sur le français | 0,6207 |
| **écart oracle** | **+0,0405** |
| taille | 120 neurones · 1 couche |

### Trois observations

**1. Le pont transfère sur du littéraire long.** De l'anglais au français, sans
réapprentissage : 0,6660 → 0,5802. Une perte de 0,086, du même ordre que les
écarts de transfert mesurés sur l'UDHR.

**2. Notre sortie est BEAUCOUP plus interlingue que le professeur** : 0,9540 contre
0,6532. Le pont dépasse largement la couche qu'il émule sur l'invariance — cohérent
avec tout ce qui précède, et c'est le prix de la fidélité.

**3. La restriction de canaux est confirmée par une voie indépendante.** L'invariance
du professeur mesurée **sur les canaux à forte énergie** vaut **0,6532**, contre
**0,5703** sur les 896 canaux. Les canaux énergétiques sont donc bien **plus
interlingues** — ce que la sélection par énergie supposait, et qui n'avait pas
encore été vérifié directement.

### La comparaison couche 8 / couche 10

Mesurée en parallèle (les traces de Romeo contiennent déjà la couche 8) : elle dira
si viser le plateau plutôt que la couche 10 améliore le pont.


---
