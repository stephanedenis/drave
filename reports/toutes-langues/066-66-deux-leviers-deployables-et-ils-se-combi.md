> Campagne : **toutes-langues** · expérience **66**
> Titre : 66. Deux leviers DÉPLOYABLES, et ils se combinent
> Date réelle : **2026-10-06 22:45 HAE** (source : commit `09291d7`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 66. Deux leviers DÉPLOYABLES, et ils se combinent

### 66.1 Retirer le sous-espace de langue DANS LES ÉTATS

Tous les moyens des §58-§64 agissaient soit sur l'**objectif** du fit, soit sur la
**sortie**. Or le §64 a montré que les deux axes sont mêlés **dans les états** du
réservoir. L'idée ici est donc d'agir **avant la lecture** :

1. sur l'apprentissage, calculer la covariance **inter-langue** des états
   `C_lang = Σ_L n_L (ν_L − ν̄)(ν_L − ν̄)ᵀ`, où `ν_L` est l'état moyen de la langue `L` ;
2. en prendre les `r` directions dominantes et **projeter les états sur leur
   complément** : `X' = X·(I − Π_lang)` ;
3. ajuster la lecture sur `X'`.

`Π_lang` est une **matrice fixe** : à l'inférence on applique la même projection à un
texte neuf, **sans étiquette de langue ni regroupement**.

**Résultat** (3 langues d'apprentissage cette fois — voir §65) :

| rang | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 0 | 0,4767 | 242,1 | 317,4 | 1,311 |
| 5 | 0,4747 | 183,5 | 285,7 | 1,556 |
| 20 | 0,4737 | 174,6 | 270,7 | 1,551 |
| **40** | **0,4713** | **141,9** | 224,7 | **1,584** |

**`P_lang` tombe de 242 à 142 (÷ 1,7) quand `P_cont` ne tombe que de 317 à 225
(÷ 1,4)** — le rapport gagne 21 % pour 0,005 de fidélité. Contrairement au §63, l'effet
**se transfère** aux langues inconnues, parce que la projection s'applique aux états,
qui sont calculés de la même façon quelle que soit la langue.

### 66.2 Les deux leviers ensemble

Le centrage agit sur l'entrée **avant** le réservoir ; le retrait du sous-espace agit
sur les états **après**. Les deux attaquent le même axe par des chemins différents — on
les combine.

| rang | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 0 (centrage seul) | 0,4703 | 42,4 | 81,8 | 1,927 |
| **5** | **0,4706** | **22,9** | 70,2 | **3,064** |
| 10 | 0,4709 | 22,9 | 69,7 | 3,035 |
| 40 | 0,4692 | 21,9 | 61,9 | 2,832 |

**Et la fidélité ne bouge pas** (0,4703 → 0,4706). Le rapport passe de 1,927 à
**3,064**, soit **+59 %** par rapport au centrage seul.

### 66.3 Le bilan des leviers

| moyen | déployable | rapport | fidélité |
|---|---|---|---|
| rien | — | 1,460 | 0,4747 |
| centrage de l'entrée (§64) | oui | 1,871 | 0,4668 |
| retrait du sous-espace dans les états (§66.1) | oui | 1,584 | 0,4713 |
| **les deux (§66.2)** | **oui** | **3,064** | **0,4706** |
| *professeur* | — | *10,912* | — |

**Deux leviers déployables, gratuits à 0,004 près, qui portent le rapport de 1,46 à
3,06 — soit 28 % de la cible au lieu de 13 %.**

### 66.4 La réserve, et elle est importante

**Le rapport monte surtout par le DÉNOMINATEUR.** À rang 5, `P_lang` tombe à 22,9 —
**17 fois sous celui du professeur** (399,2) — tandis que `P_cont` reste à 70,2,
**62 fois sous le sien** (4 356,4).

C'est exactement le piège signalé au §62.3, et il faut le redire ici : **un rapport
élevé obtenu en écrasant l'axe de langue ne prouve pas qu'on a rapproché les langues
*à contenu égal*.** Les deux énergies restent très en dessous de celles du professeur.

**Ce qui manque reste le même qu'au §61** : remonter `P_cont` à la magnitude du
professeur. Et le seul moyen qui y parvienne (l'amplification ciblée, β=3 → `P_cont`
5 100) exige le regroupement par contenu, donc n'est pas déployable.

**La formulation honnête du progrès** : on sait maintenant **réduire l'axe de langue
sans écraser l'axe de contenu** — c'est nouveau, et c'est déployable. On ne sait
toujours pas **remonter l'axe de contenu** sans information sur le contenu.


---
