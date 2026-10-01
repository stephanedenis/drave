# Sprint 6 — Le TAUX de récupération de l'attention creuse : neuf fenêtres à 4096 (dense, k=256, k=1024) et le troisième point de la courbe k(contexte) à 16384

- **Début** : 03:38 · **Fin prévue** : 05:38 (boxing de 120 min)
- **Objectif** : Le TAUX de récupération de l'attention creuse : neuf fenêtres à 4096 (dense, k=256, k=1024) et le troisième point de la courbe k(contexte) à 16384
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.


## Revue — ce qui est livré, mesuré

Durée : 120 min (boxing 120 min). Commits : 4.

  - `45a0c44` Le « ralentissement » est un LIVELOCK : KvCache::assurer boucle sans fin si besoin > ctx (model.rs:1117)
  - `361c186` Nuance : le facteur de ralentissement est un minorant (les deux exécutions à ctx 4608 n'ont jamais fini ; la même fenêtre rend en 85,1 s à ctx 5120)
  - `e4b3ebc` Le taux par fenêtre : 9 fenêtres contiguës, 8/9 en attention complète, et le mur du préremplissage
  - `783f1f9` Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384

**Objectif du sprint** : « Le TAUX de récupération de l'attention creuse : neuf
fenêtres à 4 096 (dense, k = 256, k = 1 024) et le troisième point de la courbe
k(contexte) à 16 384 ». **Le taux est mesuré pour l'attention complète, la série
creuse a buté sur un mur de performance — et ce mur est le résultat du sprint.**

### 1. Le taux, et pourquoi il fallait des fenêtres vraiment distinctes

Neuf fenêtres **contiguës** — l'outil corrigé au sprint 5 les produit et le dit
(« fenêtres distinctes utilisées : 9 sur 9 ») — à 4 096 clés, profondeur 0,5, avec
le préremplissage déporté (75 s par sonde au lieu de 250) :

| fenêtre | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| jetons du prompt | 4114 | 3996 | **4731** | 4664 | 4096 | 4046 | 4152 | 4013 | 4081 |
| attention complète | oui | oui | **NON** | oui | oui | oui | oui | oui | oui |
| k = 256 (GPU) | **NON** | (non mesuré) | | | | | | | |

**Le contrôle dense est à 8/9, pas 9/9** : la fenêtre 3 (la plus longue, 4 731
jetons) échoue même sans élagage. C'est une information sur le protocole (il a une
difficulté propre) et une règle de méthode : une comparaison de qualité doit être
**appariée** (même fenêtre, deux chemins), pas un taux global. Sur la fenêtre 1, le
couple est net : **dense oui, k = 256 NON**, mêmes réglages, seul l'élagage change.

### 2. Le mur, et c'est un résultat

Avec `--attn-topk`, le PRÉREMPLISSAGE perd l'accélération GPU : le chemin groupé du
lot exige `attn_topk == 0`, donc chaque sonde repasse de **75 s à 246 s** (mesuré).
Neuf sondes × 246 s ne tiennent pas dans un box — la grille complète du taux demande
d'**implémenter le top-k dans le chemin par lots**. C'est le chantier que la mesure
désigne, et il est au planning.

### 3. Un piège du MOTEUR, trouvé parce qu'une sonde a duré 23 minutes

La fenêtre 3 tokenise à 4 731 jetons là où la cible était 4 096, et l'outil passait
`--ctx 4608`. Le moteur **ne l'a pas refusé** : les deux exécutions de cette fenêtre
ont été tuées après **13 et 23 minutes** sans finir, là où la MÊME fenêtre rend en
**85,1 s** avec `--ctx 5120` (marge portée à `ctx + 1024`). Le « facteur 10 à 20 »
est donc un minorant observé, pas une mesure : ces exécutions n'ont jamais terminé.
Le moteur reste à corriger — un prompt plus long que le contexte devrait être
tronqué proprement ou refusé.

⚠️ **Et ce n'est pas un ralentissement, c'est un LIVELOCK** : la relecture ciblée a
trouvé le mécanisme — `KvCache::assurer` fait
`while cap < besoin { cap = (cap * 2).min(self.ctx) }` (`model.rs:1117`), qui ne
termine JAMAIS si `besoin > ctx`. Le même défaut avait été corrigé côté GPU au
sprint 2 (`kv_assurer`) ; le chemin CPU est resté. Premier chantier du sprint 7.

C'est la sixième fois de la nuit qu'un artefact fait autre chose que ce qu'il
annonce, mais la première fois que c'est le MOTEUR et pas mes instruments. Elle a
coûté 40 minutes de box avant d'être comprise : j'ai d'abord soupçonné la charge
machine, puis le GPU, avant de compter les jetons des fenêtres — la mesure qui
tranche était à un `--tokenize` de distance.

## Introspection

- **Ce qui a marché** : compter les jetons de chaque fenêtre pour expliquer un
  ralentissement inexpliqué. La cause n'était ni la charge, ni le GPU, ni l'outil :
  c'était un prompt plus long que le contexte, et le moteur qui ne le dit pas.
- **Ce que je dois changer** : j'ai passé 40 minutes à contourner un symptôme
  (relancer la grille, changer les options) avant de mesurer la grandeur qui
  clochait. La règle : **devant un temps anormal, mesurer les entrées avant de
  suspecter la machine**.
- **Ce que la nuit aura appris sur la mesure** : six artefacts ont promis ce qu'ils
  ne faisaient pas (garde-fou jamais déclenché, échantillon lu comme un accord
  global, grep qui ne suit pas la chaîne d'appels, décalage de fenêtre remis à zéro,
  section annoncée dans un commit mais absente du rapport, et un moteur qui ralentit
  au lieu de refuser). Chacun a été trouvé et corrigé dans son box, et chacun a
  changé une conclusion.
- **Doute** : le taux creux reste inconnu (1 fenêtre mesurée, un échec). La grille
  complète est au planning, mais elle ne tiendra qu'avec le top-k dans le lot.
- **Doute** : la fenêtre 3 échoue en dense — est-ce sa longueur, son contenu, ou la
  position de l'aiguille ? Non départagé.

## Planning — sprint 7 (2 h)

| # | chantier | critère de succès |
|---|---|---|
| 1 | **Le livelock du contexte** (`model.rs:1117`, boucle infinie si `besoin > ctx`) | un prompt plus long que le contexte est **tronqué ou refusé en le disant**, et le processus ne boucle plus |
| 2 | **Le top-k dans le chemin par lots** (le mur mesuré à 246 s/sonde) | une sonde creuse à 4 096 clés repasse sous 100 s |
| 3 | Si le temps le permet : la grille du taux (9 fenêtres × k = 256) avec le chemin réparé | un taux apparié dense vs k = 256 |

**Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
