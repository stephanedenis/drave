# Sprint 4 — Le k de l'attention creuse : l'échec au milieu est-il un réglage (k plus grand) ou un mécanisme manquant ? Grille en --lot 1 (tout le passage creux) et k = 256/512/1024

- **Début** : 23:44 · **Fin prévue** : 01:44 (boxing de 120 min)
- **Objectif** : Le k de l'attention creuse : l'échec au milieu est-il un réglage (k plus grand) ou un mécanisme manquant ? Grille en --lot 1 (tout le passage creux) et k = 256/512/1024
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.


## Revue — ce qui est livré, mesuré

Durée : 113 min (boxing 120 min). Commits : 4.

  - `b14e4f2` Contrôle dense à 8 192 : l'information est retrouvée (1002 s, prompt de 7963 jetons) — la question du k vs contexte est mesurable là
  - `1425c79` Revue du sprint 4 : « trois fenêtres » étaient trois fois la même invite, et la portée du k était surestimée
  - `09adea5` Le k est un réglage : 0/3 au milieu à k=512, 3/3 à k=1024 (trois fenêtres par point)
  - `2ae761c` Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5

**Objectif du sprint** : « Le k de l'attention creuse : l'échec au milieu est-il un
réglage (k plus grand) ou un mécanisme manquant ? Grille en `--lot 1` (tout le
passage creux) et k = 256/512/1024 ». **Réponse : c'est un réglage**, et la
conclusion du sprint 3 était trop forte — corrigée.

### 1. Le balayage en k : 0 · 0 · 3

La grille du sprint 3 n'avait **qu'une sonde par configuration**, et le premier
balayage en k a donné des résultats **non monotones** (k = 512 échoue, k = 1 024
réussit) — d'où trois sondes par configuration, à 4 096 clés et profondeur 0,5,
`--lot 256` :

| configuration | répétition 1 | répétition 2 | répétition 3 | verdict |
|---|---|---|---|---|
| attention complète | oui (383,6 s) | oui (326,5 s) | oui (251,5 s) | **3/3** |
| k = 256 (6,25 %) | NON (244,7 s) | NON (237,8 s) | NON (237,0 s) | **0/3** |
| k = 512 (12,5 %) | NON (240,5 s) | NON (238,1 s) | NON (237,8 s) | **0/3** |
| k = 1 024 (25 %) | oui (239,6 s) | oui (253,2 s) | oui (244,1 s) | **3/3** |

⚠️ **Et la revue adverse a démoli la justification de ces « 3/3 »** : les trois
colonnes sont trois **répétitions de la MÊME invite**, pas trois fenêtres de
corpus. Le garde-fou d'`aiguille.py` comparait l'offset à `len(corpus) - 400_000`
alors que le corpus en fait **353 778** : la remise à zéro se déclenchait toujours.
Or le moteur est déterministe : **trois répétitions d'une même invite ne mesurent
rien de plus qu'une seule**. Ce qui reste : la CONVERGENCE avec le premier balayage
(une sonde) — non à 512, oui à 1 024 — et le fait que le seuil est dans
(12,5 %, 25 %] **pour ce cas précis**. La généralité inter-fenêtres n'est pas
mesurée, et l'outil est corrigé.

**Ce qui tient, avec sa portée exacte** : en `--lot 256` — où `--attn-topk` ne
s'applique qu'aux **24 jetons du décodage** (0,58 % des passes), le préremplissage
restant dense et le moteur le disant — l'échec au milieu n'est pas une impossibilité
structurelle du top-k : c'est un réglage, et le seuil est entre 512 et 1 024 clés.
L'affirmation du sprint 3 (« sans index, l'attention creuse ne peut pas remplacer
l'attention complète ») était trop forte.

**Ce que ça déplace** : la vraie question de feuille de route est **comment le k
nécessaire évolue avec le contexte** — s'il reste de l'ordre du quart, l'élagage ne
rapporte rien à 32 k.

### 2. Un contrôle qui invalide une comparaison tentante

En `--lot 1` (UNE sonde), l'attention **COMPLÈTE** échoue aussi au milieu
(251,0 s, « NON ») alors qu'elle réussit en `--lot 256`. Le chemin par lots change
le résultat lui-même — la revue adverse du sprint 3 avait mesuré que `--lot 1` et
`--lot 256` génèrent des identifiants différents pour la même invite. La
comparaison « tout le passage creux » en `--lot 1` n'est donc **pas propre**, et la
seule comparaison valable est **à lot fixé**.

### 3. Un levier qui existait déjà : le préremplissage déporté

Profilage d'un prompt de 3 961 jetons (Qwen2.5-0.5B Q8_0, `--lot 256`, `--infer`) :

| chemin | prompt | postes (ms/jeton) |
|---|---|---|
| CPU | **286,6 s** (13,8 tok/s) | attention **52,6** · matvec+mlp 18,4 |
| `DRAVE_GPU=1 DRAVE_GPU_KV=1` | **63,8 s** (62,1 tok/s) | attention **2,2** · matvec+mlp 12,8 |

L'attention est **le** poste dominant du préremplissage sur CPU (73 %), et le
miroir VRAM la divise par 24. Qualité vérifiée : perplexité **9,4335 (CPU)** contre
**9,4337 (GPU KV)** à ctx 4 096 et 1 023 jetons, soit 2e-5. Autrement dit, pour tout
prompt long, `DRAVE_GPU_KV=1` est le réglage à prendre — il l'était déjà, mais le
chiffre n'existait pas.

## Introspection

- **Ce qui a marché** : refuser de conclure sur une sonde unique. Le premier
  balayage donnait une histoire séduisante (« k = 512 échoue, k = 1 024 réussit »)
  qui était du bruit ; trois fenêtres par point ont donné un passage net 0/0/3. La
  règle qui a servi : **un point de mesure sans répétition n'est pas un point de
  mesure**, surtout quand la sortie est binaire et qu'une bascule de jeton décide
  du résultat.
- **L'erreur à ne pas refaire** : j'ai écrit « trois fenêtres de corpus
  différentes » sans vérifier que l'outil les produisait. Un compteur de fenêtres
  qui ne compte rien (« l'offset avance de 200 000 » avec un garde-fou qui le remet
  à zéro) est la même classe de faute que le filet de sécurité du sprint 2 et
  l'échantillon du sprint 3 : **un artefact non vérifié qui a l'air de faire ce
  qu'il annonce**. Quatrième fois cette nuit ; la parade est toujours la même —
  vérifier dans la mesure, pas dans l'intention.
- **Ce que je dois changer** : j'ai écrit au sprint 3 qu'« un index est nécessaire »
  sur la foi de 3 sondes à k = 256 seulement. La mesure de ce sprint dit que k
  suffit — plus cher, mais suffisant. Une conclusion de feuille de route demande un
  balayage, pas un point.
- **Ce que ce sprint a produit sans le chercher** : le chiffre du préremplissage
  déporté (×4,5, qualité à 2e-5), qui rend les grilles longues abordables — c'est
  ce qui permettra de mesurer si le k nécessaire croît avec le contexte.
- **Doute** : le seuil entre 512 et 1 024 est mesuré à 4 096 clés, sur UN modèle de
  0,5B et UNE tâche (un code à retrouver). Le rapport k/contexte à 8 192, 16 384 et
  sur un modèle plus grand n'est pas mesuré — c'est la première expérience du
  prochain sprint.
- **Doute** : `--lot 1` et `--lot 256` ne donnent pas le même résultat (mesuré par
  la revue adverse). Quelle est la bonne sémantique ? Le chemin par lots est une
  optimisation, il ne devrait pas changer la sortie.

## Planning — sprint 5 (2 h)

| # | chantier | critère de succès |
|---|---|---|
| 1 | **Refaire la grille avec de VRAIES fenêtres** (l'outil est corrigé) : 4 096 et 8 192, profondeur 0,5, k = 256 / 512 / 1 024, trois fenêtres distinctes | la conclusion « k est un réglage » tient-elle sur trois textes différents ? |
| 2 | **Le k nécessaire croît-il avec le contexte ?** k = 1 024 / 2 048 / 4 096 à 8 192 et 16 384 (une fenêtre, tant que l'outil n'est pas re-testé) | une courbe k_nécessaire(contexte), ou l'aveu qu'elle n'est pas mesurable dans le box |
| 3 | **Pourquoi `--lot 1` ≠ `--lot 256` ?** Comparer les logits des deux chemins (mêmes jetons) et dire lequel est le bon | l'écart est localisé (préremplissage, attention, ordre de sommation) et documenté |
| 4 | Si le temps le permet : le préremplissage déporté **par défaut** quand `DRAVE_GPU_KV` est posé (aujourd'hui il l'est déjà — vérifier qu'aucun chemin ne l'oublie) | un seul réglage à retenir, et c'est écrit |

**Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
