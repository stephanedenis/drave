# Sprint 5 — Refaire la grille avec de VRAIES fenêtres (outil corrigé) et mesurer si le k nécessaire croît avec le contexte (8192 : k=1024 et 2048)

- **Début** : 01:37 · **Fin prévue** : 03:37 (boxing de 120 min)
- **Objectif** : Refaire la grille avec de VRAIES fenêtres (outil corrigé) et mesurer si le k nécessaire croît avec le contexte (8192 : k=1024 et 2048)
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.


## Revue — ce qui est livré, mesuré

Durée : 120 min (boxing 120 min). Commits : 4.

  - `a3691a5` Revue du sprint 5 : la section 8 192 manquait, et « au plus » dépassait la mesure d'un facteur 10
  - `0d50e75` À 8 192 clés, k=1024 (12,5 %) suffit : le k nécessaire croît plus lentement que le contexte (deux points)
  - `508d3d8` Grille refaite sur trois VRAIS textes : k=256 échoue 1 fois sur 3, pas 3 sur 3
  - `ee59519` Pourquoi --lot 1 diffère de --lot 256 : 7e-4 nat par position, top-1 identique partout — c'est une amplification chaotique, pas un chemin faux

**Objectif du sprint** : « Refaire la grille avec de VRAIES fenêtres (outil corrigé)
et mesurer si le k nécessaire croît avec le contexte (8192 : k=1024 et 2048) ».
**Les deux réponses sont là, et la première change la nature de la conclusion.**

### 1. La grille refaite : l'échec est probabiliste, pas systématique

Le correctif de l'outil se voit dans les longueurs de prompt : **4 114 / 4 433 /
4 126** jetons (contre 4 114 trois fois au sprint 4). À 4 096 clés, profondeur 0,5,
`--lot 256` :

| configuration | fenêtre 1 | fenêtre 2 | fenêtre 3 | trouvé |
|---|---|---|---|---|
| attention complète | oui (266,2 s) | oui (280,2 s) | oui (251,1 s) | **3/3** |
| **k = 256** (6,25 %) | NON (240,3 s) | oui (302,2 s) | oui (241,4 s) | **1/3** |
| **k = 1 024** (25 %) | oui (238,9 s) | oui (275,6 s) | oui (265,7 s) | **3/3** |

* l'échec du sprint 3 (« NON au milieu ») était **réel, mais sur un seul texte** ;
* le « 0/3 » du sprint 4 mesurait **trois fois ce même texte** — les trois
  répétitions d'un calcul déterministe ne mesurent rien de plus qu'une ;
* la bonne formulation est un **taux** : dense 3/3, k = 256 **1/3**, k = 1 024 3/3.

Trois tirages restent peu (l'intervalle de confiance d'un 1/3 va de 1 % à 90 %) :
**neuf fenêtres** sont au planning du sprint 6.

### 2. Le k nécessaire NE croît PAS proportionnellement au contexte

| contexte | dense | k = 1 024 | k = 2 048 |
|---|---|---|---|
| 4 096 | 3/3 | 3/3 (25 % du contexte) | — |
| 8 192 | **oui** (1 002,0 s) | **oui** (764,7 s, 12,5 %) | **oui** (755,7 s, 25 %) |

À 8 192 clés, **k = 1 024 suffit** (12,5 % du contexte) là où il en fallait 1 024 à
4 096 clés (25 %) : sur ces deux points, le k nécessaire croît **plus lentement que
le contexte** — exactement ce qu'il faut pour que l'élagage devienne payant à long
contexte. ⚠️ Deux points ne font pas une courbe, et le point de 8 192 est une seule
fenêtre (le taux de 4 096 est, lui, sur trois) : la courbe k(contexte) est au
planning du sprint 6.

### 3. `--lot 1` ≠ `--lot 256` : mesuré, et c'est minuscule

| | perplexité | écart moyen \|ΔNLL\| | accord top-1 |
|---|---|---|---|
| `--lot 1` | 13,1368 | — | — |
| `--lot 256` | 13,1359 | **0,0007** (p90 0,0017, max 0,0068) | **511/511** |

Ce n'est pas un chemin faux : c'est une **amplification chaotique** (7e-4 nat par
position suffit à changer un jeton greedy après quelques dizaines de pas, et une
réponse qui doit contenir un code ne pardonne pas un jeton). Toute comparaison de
qualité doit donc se faire **à lot fixé** — ce que les grilles de ce sprint font.

### 4. Revue adverse : deux écarts graves — dont une mesure publiée dans un commit et absente des fichiers

1. **La mesure à 8 192 n'existait dans aucun artefact.** Le sujet du commit
   `0d50e75` annonçait « k = 1 024 suffit, le k nécessaire croît plus lentement que
   le contexte »… et la section correspondante n'avait jamais été écrite dans le
   rapport (le patch avait échoué en silence, et le rapport disait encore « 8 192
   non mesuré »). C'est la cinquième fois cette nuit qu'un artefact promet ce qu'il
   ne fait pas — et la première fois que la promesse est dans un message de commit.
   Section écrite, avec sa portée : deux sondes, UNE fenêtre chacune, **aucun k en
   échec** (donc une borne supérieure, pas un seuil localisé).
2. **« 7e-4 nat par position AU PLUS »** — contredit par le tableau deux lignes plus
   haut (max 0,0068) : c'est la MOYENNE. Corrigé.
3. Le garde-fou d'offset de l'outil comparait à **20 000 fixes** alors que le besoin
   vaut `int(ctx×4.2)+400` : à 16 384 (prévu au planning !) la fenêtre serait
   revenue à 0 en silence, et un corpus court rejouait la même invite — le bug
   d'origine, réintroduit. Corrigé : le pas vaut désormais le BESOIN, donc les
   fenêtres sont **contiguës et non recouvrantes** (une vingtaine disponibles au
   lieu de trois), et l'outil **avertit** quand il y a moins de fenêtres que de
   sondes.
4. Mineurs : 13,1368 est la sortie du moteur (13,1367 pour le comparateur) ;
   « 4 114 trois fois » → « 4 114 aux douze sondes ».

## Introspection

- **Ce qui a marché** : corriger l'outil AVANT de refaire la grille. La revue adverse
  du sprint 4 avait trouvé que « trois fenêtres » étaient trois fois la même invite ;
  le correctif (marge calculée sur la taille réelle du corpus) a immédiatement
  changé le résultat — 1/3 au lieu de 0/3.
- **La leçon qui se répète** : quatre fois cette nuit, un artefact a fait ce qu'il
  annonçait sans le faire (le filet de sécurité, l'échantillon de logits, le grep de
  chaîne d'appels, le décalage de fenêtre). Chaque fois, la vérification a coûté
  quelques minutes et a changé une conclusion. La règle à garder : **vérifier
  l'instrument avant de croire la mesure**.
- **Ce que je dois changer** : j'ai écrit deux conclusions de feuille de route
  (« un index est nécessaire », puis « l'échec est systématique à k ≤ 512 ») sur des
  échantillons de un et trois tirages du même texte. Une conclusion sur un taux
  demande un taux : neuf fenêtres minimum, et l'intervalle de confiance écrit à côté.
- **Doute** : le taux de 1/3 à k = 256 est mesuré sur un modèle de 0,5B et une tâche
  (retrouver un code de 8 caractères). Rien ne dit qu'un modèle plus grand, ou une
  tâche moins binaire, donne le même taux.
- **Doute** : à 8 192, une seule fenêtre par configuration. Le « k = 1 024 suffit »
  est un point, pas une courbe.

## Planning — sprint 6 (2 h)

| # | chantier | critère de succès |
|---|---|---|
| 1 | **Neuf fenêtres** à 4 096, profondeur 0,5 : dense, k = 256, k = 1 024 (avec `--gpu-kv`, mesuré ×3,3 : 76 s par sonde au lieu de 250) | un taux avec son intervalle, au lieu d'un verdict binaire |
| 2 | **La courbe k(contexte)** : 8 192 et 16 384, k = 1 024 / 2 048 / 4 096, deux fenêtres | deux points de plus, assez pour dire si le rapport k/contexte décroît |
| 3 | Si le temps le permet : préremplissage déporté pour les sondes longues (×4 mesuré) afin que le point 2 tienne dans le box | 16 384 mesuré, pas seulement 8 192 |

**Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
