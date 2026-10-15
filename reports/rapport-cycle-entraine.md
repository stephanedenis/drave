# C2 bis — le cycle ENTRAÎNÉ : ×228 au pas 4, mais il dégrade encore (et le moteur le confirme)

> Campagne : **cerveau** · expérience : la suite directe de `reports/rapport-cycle-c2.md` — le
> cycle non entraîné **divergeait** (14,65 → 2 988 en quatre pas). La note demandait : « un cycle
> entraîné vaut-il mieux qu'une passe ? »
> Verdict : **l'entraînement dompte la divergence, il ne rend pas la boucle utile.** Sur les
> morceaux de test, le pas 4 passe de **15 868,54** (non entraîné) à **52,24** (entraîné) — un
> facteur **228** — mais la trajectoire entraînée **dégrade encore** à chaque pas (18,40 → 22,61 →
> 32,56 → 52,24, soit ×1,4 par pas) et **ne bat jamais une passe** (18,40). Le **moteur** le
> confirme sur son propre découpage : 15,66 → 18,71 · 427,87 → 23,54 · 4 088,44 → 35,57 ·
> 14 226,12 → **62,48**, même forme, mêmes conclusions.
> Date réelle : **2026-10-15 00 h 05-00 h 50 HAE** (heure lue sur la machine)
> Protocole : `tools/cycle_entraine.py` (nouveau) — cycle à deux régions (coupe 12/24), T = 4 pas,
> LoRA rang 8 sur les **24 couches**, objectif = **somme des pertes des quatre pas**, 10 époques,
> époque choisie sur un morceau de validation, fenêtre de 512 jetons · confirmation moteur :
> `tools/derouler.py` sur `--topologie /tmp/c2/cycle.json` avec le LoRA **fusionné**
> (`tools/exporter_gguf_dense.py`, 96 projections).

## 1. La trajectoire, avant et après

| pas | non entraîné (torch) | **entraîné (torch)** | non entraîné (moteur) | **entraîné (moteur)** |
|---:|---:|---:|---:|---:|
| 1 | 15,42 | **18,40** | 15,66 | **18,71** |
| 2 | 355,03 | **22,61** | 427,87 | **23,54** |
| 3 | 4 057,04 | **32,56** | 4 088,44 | **35,57** |
| 4 | 15 868,54 | **52,24** | 14 226,12 | **62,48** |

Ce que ça dit :

* **l'entraînement change la NATURE de la boucle** : la divergence est **géométrique** (×23, ×11,
  ×3,9 par pas) avant, et devient **lente** (×1,23, ×1,44, ×1,60) après. À quatre pas, le facteur
  est de **228 à 304** selon le découpage — c'est le résultat le plus net de cette fiche ;
* **mais la boucle ne converge pas, et elle n'aide pas** : chaque pas coûte ~40 % de perplexité de
  plus que le précédent, et le pas 1 (une passe, 18,40) reste le meilleur. Un cycle entraîné est
  donc, à ce budget, **un mécanisme de temps qui ne rend pas le résultat meilleur** — il rend une
  **trajectoire** (ce que le plan demandait) et il la rend **utilisable** (bornée, déterministe,
  ×228 plus proche) ;
* **le pas 1 paie le prix de l'entraînement** : 15,42 (non entraîné) contre 18,40 (entraîné) — le
  LoRA apprend la boucle **au détriment** de la passe unique. C'est cohérent avec l'objectif
  (somme des quatre pas) et c'est dit : on ne peut pas, à ce budget, optimiser les deux à la fois ;
* **le moteur est plus pessimiste à chaque pas** (18,7 · 23,5 · 35,6 · 62,5 contre 18,4 · 22,6 ·
  32,6 · 52,2) : l'écart passe de **+1,7 %** au pas 1 à **+19,6 %** au pas 4. C'est la
  **quantification Q8_0 qui s'amplifie dans la boucle** — chaque pas réinjecte l'état du pas
  précédent, donc l'erreur de quantification se compose au lieu de se dissiper. Un cycle est un
  **amplificateur d'erreur**, et c'est mesuré.

## 2. Ce que ça change pour le cerveau

* **la récurrence n'est pas un levier de qualité** — c'est la troisième fois que ce dépôt le
  mesure, et la plus complète : la récurrence locale dégrade (« un écho, pas une mémoire »), la
  récurrence linéaire de 64 canaux plafonne (R² +0,104), et un cycle **entraîné** reste en dessous
  d'une passe (52,24 contre 18,40 au pas 4) pour **quatre fois le calcul** ;
* **ce qu'un cycle sait faire, en revanche, est du TEMPS** : une trajectoire bornée et
  déterministe, contrôlable (N pas), dont chaque pas est une transformation de l'état précédent —
  c'est-à-dire un substrat pour de l'**oscillation**, de l'**accumulation** ou du **maintien**
  d'activité, pas pour du raffinement de prédiction à ce budget ;
* **la piste qui reste, et elle est nommée** : entraîner la boucle avec un objectif de
  **point fixe** (le pas N doit rejoindre une cible, pas prédire), ou avec un objectif **pondéré**
  (le dernier pas seul) — la fiche ne les a pas essayés, et le § 4 le dit.

## 3. Ce que cette fiche ne dit pas

* **un seul objectif d'entraînement** (somme des pertes des quatre pas) : le dernier pas seul, ou
  une pondération décroissante, n'est pas mesuré — c'est la variable la plus prometteuse, et elle
  est facile à essayer ;
* **un seul budget** (10 époques, 8 morceaux de 512 jetons) : la courbe « plus d'entraînement »
  n'est pas faite — au fil des époques, la validation descend (56,7 → 49,8) puis remonte (66,7,
  77,8, 87,5) : le meilleur est **milieu de courbe**, et c'est le surapprentissage qui parle ;
* **une seule coupe** (12/24) et un seul T (4) : couper ailleurs change la nature des deux
  « régions » (le plan le dit : le facteur limitant est le chemin court) ;
* **rien n'est mesuré sur une tâche** : la perplexité n'est pas une capacité. Un cycle qui
  *rafraîchit* une réponse au fil des pas (poursuite, délibération) demanderait un protocole à
  cible, qui n'existe pas encore dans ce dépôt ;
* **le coût n'est pas comparé à budget égal** : quatre pas = quatre passes. La comparaison honnête
  serait « un cycle de 4 pas » contre « un modèle 4 fois plus gros/plus entraîné » — et elle n'est
  pas faite.
