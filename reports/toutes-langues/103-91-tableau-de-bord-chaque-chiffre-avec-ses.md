> Campagne : **toutes-langues** · expérience **91**
> Titre : 91. TABLEAU DE BORD — chaque chiffre avec ses conditions
> Date réelle : **2026-10-07 12:43 HAE** (source : commit `3f7df44`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 91. TABLEAU DE BORD — chaque chiffre avec ses conditions

Les §81 à §90 ont montré qu'un chiffre du projet sans ses conditions est un chiffre faux à
l'usage. Voici donc **tous les chiffres de la session, regroupés, chacun avec sa graine, son
panel, son pooling et son ajustement**. C'est le tableau à citer ; les paragraphes qui
précèdent sont les raisonnements.

### 91.1 Le professeur seul — la cible n'existe pas sans son panel

482 articles, couche 8, **moyenne sur les positions**, 896 canaux, `cache_vf_*.npz` :

| panel | `P_lang` | `P_cont` | **RAPPORT** |
|---|---:|---:|---:|
| 6 langues (de, en, es, fr, it, pt) | 2 381,8 | 4 041,9 | **1,697** |
| de/en/fr | 3 347,7 | 4 405,3 | **1,316** |
| **es/it/pt** | 387,9 | 4 655,4 | **12,001** |
| paire **de–en** (la pire) | 3 372,6 | 5 037,6 | **1,494** |
| paire médiane (15 paires) | — | — | **3,002** |
| paire **es–pt** (la meilleure) | 100,4 | 5 465,1 | **54,428** |

**Étalement pire/meilleure paire : ×8,5.** `P_cont` ne varie que de 15 % entre les panels :
toute la variation vient de `P_lang`.

### 91.2 Le professeur, couche par couche

50 articles × 6 langues, moyenne sur les positions, `traces_couches/` :

| couche | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **RAPPORT** | 0,254 | 0,203 | 0,233 | 0,427 | 0,698 | 1,650 | 1,736 | 1,674 | 1,769 |
| dim. eff. | 14,2 | 16,1 | 18,3 | 22,3 | 32,5 | 37,5 | 37,5 | 34,6 | 35,5 |

Le saut est entre **3 et 5** ; les couches 0 à 2 font *baisser* le rapport. Mais paire par
paire, les paires proches continuent de se séparer jusqu'à la couche 8 (es–pt 23,098 → 48,269).

### 91.3 Le pooling et la dernière position

Mêmes traces, mêmes couches, seule la réduction des positions change :

| pooling | couche 0 | couche 8 |
|---|---:|---:|
| **moyenne** (comparable au §70 et à notre pont) | 0,254 | 1,769 |
| dernière position | 8,044 | 6,275 |

### 91.4 Notre pont, protocole de référence

120 neurones · lecture quadratique · ride 0,03 · graine 5 · masque des canaux vivants ≥ 0,5.

| apprentissage | mesure | fid TEST | notre rapport | professeur | **part** |
|---|---|---:|---:|---:|---:|
| de/en/fr | es/it/pt (hors vivier) | 0,4780 | 1,676 | 12,001 | **14,0 %** |
| es/it/pt | de/en/fr (hors vivier) | 0,4652 | 0,301 | 1,316 | **22,9 %** |
| 6 langues (47 art.) | 6 langues (24 art.) | — | 0,176 | 1,081 | **16,3 %** |

**Notre pire paire au rang 0 est de–en, comme celle du professeur.**

### 91.5 Le discriminant de rang 2 — et l'endroit où il est appris

| appris sur | mesuré sur | hors vivier ? | rang 2 | **part** |
|---|---|---|---:|---:|
| 6 langues | 6 langues | **oui** (articles) | 1,474 | **136,4 %** |
| de/en/fr | 6 langues | **oui** (articles) | 1,368 | **126,6 %** |
| es/it/pt | 6 langues | **oui** (articles) | 0,585 | **54,1 %** |
| es/it/pt | es/it/pt | non (dans-panel) | 38,443 | 320,3 % |
| de/en/fr | de/en/fr | non (dans-panel) | 2,783 | 211,5 % |
| es/it/pt | de/en/fr | oui | 0,411 | **31,2 %** |
| de/en/fr | es/it/pt | oui | 6,610 | **55,1 %** |

**Ce qui décide n'est ni le nombre de langues ni la taille du panel, mais la présence des
paires DIFFICILES dans le panel d'apprentissage.** Et les lignes « dans-panel » ne valent
rien : un projecteur de rang 2 sur 3 langues a 2 directions pour faire coïncider 3 moyennes,
et il les annule.

### 91.6 L'échelle est gratuite — donc les énergies ne mesurent rien

Rang 2 sur le panel 6 langues, amplifié pour amener `P_cont` à celui du professeur :

| | `P_lang` | `P_cont` | RAPPORT |
|---|---:|---:|---:|
| professeur | 2 410,7 | 2 605,5 | 1,081 |
| notre pont, rang 2, brut | 60,5 | 89,2 | 1,474 |
| **notre pont, rang 2, ×5,40** | **1 767,9** (73 %) | **2 605,5** (100 %) | **1,474** |

**Le critère du §62.3 se réduit exactement à « notre rapport ≥ celui du professeur ».**

### 91.7 Transformations de la cible — ce qui se réplique et ce qui ne se réplique pas

| variante | fid (47 art.) | rapport (47 art.) | fid (482 art.) | rapport (482 art.) |
|---|---:|---:|---:|---:|
| A — référence | 0,4910 | 0,232 | 0,4689 | 1,723 |
| **B — cible centrée** | **0,5002** | 1,877 | **0,4751** | 1,400 |
| C — lignes normées | 0,4217 | 31,240 | — | — |

**La fidélité se réplique (+0,0092 puis +0,0062, soit 5 à 7 σ) ; le rapport s'inverse**
(×8,1 puis ×0,81). B **abaisse les deux énergies** ; leur quotient change de signe selon le
panel.

### 91.8 Localité — ce que chaque couche doit au jeton

300 traces (50 articles × 6 langues), **164 775 positions**, fenêtre de 3 jetons, ridge 1,0 :

| couche | 1 | 2 | 3 | 5 | 8 |
|---|---:|---:|---:|---:|---:|
| R²(jeton seul) | 0,6051 | 0,5059 | 0,4139 | 0,2733 | **0,2424** |
| R²(fenêtre de 3) | 0,6436 | 0,5667 | 0,5224 | 0,3604 | **0,3313** |
| **gain** | +0,0385 | +0,0608 | **+0,1085** | +0,0870 | +0,0888 |

Le jeton courant porte **60 %** de la couche 1 et **24 %** de la couche 8. Le gain contextuel
culmine à la **couche 3** — là où le §91.2 situe la construction de la séparation.

### 91.9 Ce qui reste solide, et qui n'a pas bougé

| affirmation | mesure |
|---|---|
| 392 langues UDHR, couches 8+10 | **392/392**, 0 échec |
| 400 unités | **400/400**, 0 échec |
| Wikipedia apparié | **482 articles × 6 langues = 2 892 traces**, 0 échec |
| Couche 8 contre couche 10 | **41 voix contre 0** — TEST 0,6424 contre 0,5960 |
| Ridge optimal | **0,03**, pas 0,3 |
| Croissance + attrition | **147 neurones** — fid appr 0,6464 · VAL 0,6312 · TEST 0,6299 |
| `corr(fidélité, témoin constant)` | **+0,9768** |
| Écart oracle TEST contre VALIDATION | **+0,0975 contre +0,0112** |

### 91.10 La règle, en sept termes

Chaque fois qu'un chiffre de cette session s'est révélé faux à l'usage, la cause était la
même : **un choix non déclaré**. Les sept formes rencontrées :

1. **la graine** (§81) — un tirage présenté comme une propriété ;
2. **le panel** (§82) — 12,001 ou 1,697 selon les langues ;
3. **le pooling** (§84.1) — 6,275 ou 1,769 selon la réduction ;
4. **l'ajustement** (§86) — 320 % dans-panel, 31 % hors vivier ;
5. **l'échelle** (§88) — une quantité définie à une transformation gratuite près ;
6. **le rapport variables/points** (§89.4) — +70 % au lieu de +11,7 % ;
7. **la réplication** (§90) — un effet qui change de signe entre deux panels.

> **Avant d'écrire un chiffre : nommer la graine, le panel, le pooling, l'ajustement,
> l'échelle, le rapport variables/points — et se demander sur combien de panels on l'a vu.**

---
