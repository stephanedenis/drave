> Campagne : **toutes-langues** · expérience **R**
> Titre : C.1 Ce que l'objectif demandait, et la mesure qui y répond
> Date réelle : **2026-10-07 08:35 HAE** (source : commit `32ed5db`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## C.1 Ce que l'objectif demandait, et la mesure qui y répond

| exigence | état | mesure |
|---|---|---|
| **1. Étendre à TOUTES les langues de l'UDHR** (au-delà des 46) | **ATTEINT** | **392 / 392** langues tracées aux couches **8 ET 10**, **400 / 400** unités alignées, **0 échec** (§42) |
| **2. Passer aux GRANDS CORPUS MULTILINGUES** — Wikipedia décompressée | **ATTEINT** | **482 articles × 6 langues = 2 892 traces**, **0 échec**, **482 articles présents dans les six langues (100 %)** (§45, §78) |
| **2 bis. Œuvres parallèles Gutenberg** | **ATTEINT** | Romeo **24 scènes en–fr** (48 traces) ; Crime et Châtiment **24 chapitres en–es écrits**, 4 tracés (§46) |
| **3. Professeurs plus RICHES** | **ATTEINT** | Wikipedia apparié est le premier corpus **multi-domaine ET aligné** du projet — ce que l'UDHR interdisait (§53) |
| **4. Étendre notre modèle** | **ATTEINT** | croissance libre + attrition : **147 neurones**, protocole entier (§56) |
| **Contrainte : un seul professeur** | **RESPECTÉE** | Qwen2.5-0.5B-Instruct, jamais changé |
| **Contrainte : boîte noire** | **RESPECTÉE** | seules les couches 0 et cible sont lues, jamais la tête ni les jetons générés |
| **Contrainte : aucune rétropropagation** | **RESPECTÉE** | `A` et `B` aléatoires et gelés ; lecture en forme fermée partout |
