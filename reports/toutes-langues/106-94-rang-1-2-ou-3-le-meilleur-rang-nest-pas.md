> Campagne : **toutes-langues** · expérience **94**
> Titre : 94. RANG 1, 2 OU 3 : le meilleur rang n'est pas celui du meilleur chiffre
> Date réelle : **2026-10-07 13:35 HAE** (source : commit `d186466`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 94. RANG 1, 2 OU 3 : le meilleur rang n'est pas celui du meilleur chiffre

### 94.1 L'hypothèse que je m'étais faite, et sa réfutation

Le §93.4 terminait sur une hypothèse, écrite noir sur blanc : *« le premier axe est stable, le
second ne l'est pas — un discriminant de **rang 1** donnerait-il l'essentiel du gain ? Un axe
stable et calculable en forme fermée vaut mieux qu'un plan dont la moitié dépend d'un
tirage. »*

**C'était plausible, et c'est faux.** Six graines, même protocole, même panel que le §93,
rangs 1, 2 et 3 :

| rang | moyenne | écart-type | **min** | max | étalement |
|---|---:|---:|---:|---:|---:|
| **1** | 112,3 % | 19,7 % | **75,2 %** | 135,0 % | ×1,80 |
| **2** | **133,7 %** | 20,6 % | **99,1 %** | **163,2 %** | ×1,65 |
| **3** | 121,6 % | **12,2 %** | **104,7 %** | 143,1 % | **×1,37** |

Le rang 1 est le **moins bon des trois**, et de loin : sa moyenne est la plus basse
(112,3 %) et son minimum tombe à **75,2 %** — un tirage sur six **perd** contre le professeur
d'un quart. Le premier axe est stable, mais **il ne suffit pas** : la séparation fine demande
bien plus d'une direction.

### 94.2 Le résultat utile, et il est contre-intuitif

**Le rang 3 est le seul qui ne perd jamais.** Sur six tirages indépendants :
**minimum 104,7 %**, c'est-à-dire que **les six dépassent le professeur**, avec l'écart-type
le plus faible (12,2 % contre 20,6 % au rang 2) et l'étalement le plus serré (×1,37).

**Le rang 2 a la meilleure moyenne (133,7 %) mais le pire minimum (99,1 %).** Un seul tirage
sur six l'amène au niveau du professeur, pas au-dessus.

**Le compromis, chiffré** : passer du rang 2 au rang 3 coûte **12 points de moyenne**
(133,7 % → 121,6 %) et achète **une garantie** — le minimum monte de 99,1 % à 104,7 % et
l'écart-type baisse de 40 %. Pour un déploiement, où l'on ne choisit pas son tirage,
**c'est le rang 3 qu'il faut garder.**

### 94.3 Pourquoi le rang 3 est plus stable que le rang 2

Une explication, et elle est cohérente avec le §93.3 : les deux premiers axes sont **le plan
où se joue la séparation**, et le second y est instable (angles jusqu'à 50,6°). Un
projecteur de rang 2 qui s'appuie sur un axe instable hérite de son instabilité. Le
troisième axe, lui, **moyenne** les fluctuations : le sous-espace de dimension 3 est moins
sensible au basculement d'un axe que le sous-espace de dimension 2, parce qu'il en contient
un de plus pour rattraper.

**Ce n'est pas une preuve, c'est une lecture** — et elle suggère une mesure qui n'a pas été
faite : **la stabilité du sous-espace de rang 3 en fonction de la graine**. Le §93.3 ne l'a
mesurée qu'aux rangs 2 et 5, et le rang 5 est déjà trop grand pour que `C_lang` (rang ≤ 5
sur 6 langues) soit bien estimé.

### 94.4 Ce que le mandat demandait, et où l'on en est

Le mandat exige que chaque affirmation porte **sa fidélité d'entraînement, sa fidélité de
TEST, son invariance inter-langue, sa pire paire et sa TAILLE de réseau**. Le tableau du
§94.2 porte la taille (120 neurones), le rang du projecteur (1, 2, 3), et une distribution
sur six tirages. Ce qui manque encore, et c'est nommé :

- **la fidélité de TEST** pour chaque rang — la projection change la sortie, donc la
  fidélité ; elle n'a pas été remesurée ici ;
- **la pire paire** pour chaque rang — le §92 l'a donnée pour le rang 2 seulement ;
- **la stabilité du sous-espace de rang 3** (§94.3).

Ces trois mesures sont les suivantes, et elles sont toutes les trois accessibles avec les
outils déjà écrits.

---
