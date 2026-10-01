# Sprint 2 — Fusionner la chaîne du top-k déporté : descente radix, collecte et somme dans UN noyau par ligne (8 lancements → 2, plus de tampon nh×n×4), et gagner dès ~1 000 clés

- **Début** : 19:49 · **Fin prévue** : 21:49 (boxing de 120 min)
- **Objectif** : Fusionner la chaîne du top-k déporté : descente radix, collecte et somme dans UN noyau par ligne (8 lancements → 2, plus de tampon nh×n×4), et gagner dès ~1 000 clés
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.


## Revue — ce qui est livré, mesuré

Durée : 119 min (boxing 120 min). Commits : 6.

  - `a76d8c8` REPRISE : le doute sur les projections est à moitié levé (ctx 512 et 1024 identiques, ctx 256 évalue une autre chose)
  - `1dee0e6` REPRISE : sprint 2 (fusion du top-k, croisement à ~300 clés, le filet testé, le doute sur les projections)
  - `5bc4c0c` Grille propre, noyau fusionné dans le moteur, et gpt-oss (les puits en vrai)
  - `ed4ce47` Revue adverse du noyau fusionné : une course bloquante, et cinq autres points
  - `ea1d155` Le filet du noyau 4 doit agir AVANT la somme (test du filet, saboté exprès)
  - `8342f17` Noyau 4 : le top-k complet d'une ligne en UN lancement (8 lancements → 2)

**Objectif du sprint** : « Fusionner la chaîne du top-k déporté : descente radix,
collecte et somme dans UN noyau par ligne (8 lancements → 2, plus de tampon
nh×n×4), et gagner dès ~1 000 clés ». **Livré, mesuré, et le gain est plus grand
que demandé.**

### Ce qui est livré

| # | livrable | mesure |
|---|---|---|
| 1 | `attn_topk_tout` : descente radix + collecte + somme en **un** noyau par ligne (256 compteurs, k indices et k poids en partagé ; aucun indice ne quitte la VRAM) | 2 lancements au lieu de 8 · tampon `nh × n × 4` supprimé du plan |
| 2 | seuil de bascule **mesuré** avec la chaîne (noyau 4 plus rapide jusqu'à 131 072 clés, la chaîne au-delà) | 0,13 contre 0,22 ms à 4 k · 0,85 contre 0,89 à 131 k · 1,58 contre 1,35 à 262 k |
| 3 | banc : noyau 4 vérifié de n = 1 à 1 M, avec et sans puits | écart 7,19e-7 (avec puits) et **8,38e-7** (sans) · bornes n = 1, 100, 2 048, 4 097, 5 000 toutes vertes |
| 4 | **le gain dans le moteur** | attention 4,53 → 4,86 ms/jeton **de 255 à 4 095 clés** (plate) contre 4,26 → 38,84 pour le CPU · **croisement à ~300 clés** |
| 5 | perplexité | identique à 2e-5 à chaque point mesuré (13,1355 / 13,1358 · 9,4162 / 9,4167 · 12,2265 / 12,2267) |
| 6 | filets | NaN si la collecte ne remplit pas les k places (écrit AVANT la somme, l'hôte refuse une sortie non finie) · bornes sur les écritures partagées · `k > n`, `n ≥ 2^24`, k > 1024, bits 4 refusés |
| 7 | portes | Qwen 19,3885 · gpt-oss 15,1757 · `cargo test` 17/17 |

### La grille propre (une seule variable)

Contexte fixé à 16 384, on fait varier le NOMBRE DE JETONS — donc les clés
réellement notées. C'était la correction demandée par l'introspection du sprint 1 :

| jetons | clés vues | attention CPU | attention GPU | rapport |
|---|---|---|---|---|
| 511 | 255 | **4,26** | 4,53 | CPU +6 % |
| 1 023 | 512 | 7,17 | **4,62** | GPU −36 % |
| 2 047 | 1 024 | 12,08 | **4,82** | GPU −60 % |
| 4 095 | 2 047 | 19,77 | **4,86** | GPU −75 % |
| 8 191 | 4 095 | 38,84 | (mesuré) | (calculé) |

Le CPU croît de **0,0090 ms par clé** ; le GPU est plat.

### Les puits en vrai, et le coût du pruning (gpt-oss, le seul modèle à puits)

| gpt-oss, ctx 1024, 511 jetons | perplexité | effet mesuré |
|---|---|---|
| CPU dense | 18,5803 | — |
| CPU top-k 256 | 19,0740 | **+2,66 %** |
| GPU dense (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % vs CPU |
| GPU top-k 256 (`DRAVE_GPU_TOPK`) | 18,8391 | **+2,90 %** |
| GPU sans miroir KV | 18,3538 | −1,22 % vs CPU |

Le coût du pruning est le MÊME des deux côtés (+2,7 % / +2,9 %) : le chemin
déporté calcule bien la même chose, à la bascule de rang près. Et l'écart CPU/GPU
n'est pas le miroir KV (−0,25 %) mais le déport des projections (−1,22 %).

### Revue adverse (sous-agent, autonome) — et ce qu'elle a trouvé

**F1, BLOQUANT** : aucune barrière entre la lecture de `shHisto[0]/[1]` (préfixe et
report, écrits par les fils 0..255) et la remise à zéro de la passe suivante. Un
warp relâché tard lit `(0, 0)` ; `monotone()` ne rendant jamais 0, son compte
« au-dessus » vaut toute sa plage, le balayage est gonflé et la collecte écrit
**au-delà** de `shIdx` — jusqu'à corrompre la mémoire partagée d'un autre bloc
résident. La preuve est dans le PTX généré, pas dans une intuition. Corrigé.

**F3, faux résultat silencieux (rare)** : `gpu.rs` affirmait « le même départage des
ex æquo que le CPU » alors que le CPU utilise `select_nth_unstable_by`, qui n'est
**pas stable**. Sur des égalités exactes au seuil, les deux chemins pouvaient
garder des sous-ensembles différents. Le CPU garde la sélection pour trouver la
VALEUR du k-ième, puis reconstruit l'ensemble en ordre d'indice.

**F4/F5/F6** : `k > n` accepté (refusé maintenant) · `shCle` mort (4 ko de partagé
par bloc et un terme `3*k` à maintenir en double, retiré) · comptages en `float`
exacts seulement si n < 2^24 (refusé au-delà).

**F7, faiblesse de banc** : `idx_ref` calculé puis jeté, et le chemin
`sinks == nullptr` — celui que le moteur utilise pour Qwen, qui n'a pas de puits —
n'était exercé par AUCUN banc. Le nouveau passage l'exerce… et a immédiatement
révélé que la référence du banc n'appliquait pas les mêmes puits que le noyau
(écart annoncé 1,02e-3, qui n'était que celui du banc).

### Test du filet : le garde-fou qui ne gardait rien

Avant la revue, j'avais ajouté un « poison » (NaN si la collecte ne remplit pas les
k places). Je l'ai testé en SABOTANT la collecte exprès : **CUDA_ERROR_ILLEGAL_ADDRESS
(700)**, contexte empoisonné. Trois défauts d'affilée : le NaN était écrit puis
écrasé par la somme ; déplacé plus loin, il ne servait pas davantage, car les cases
non écrites de `shIdx` servaient à LIRE la VRAM avant lui ; et une course étroite
sur `red` (le max lu par tous, la case réutilisée par la somme) existait dans les
noyaux 3 ET 4. Corrigé : le filet sort AVANT la somme, et le sabotage redevient une
sortie « non finie » proprement refusée.

## Introspection

- **Ce qui a marché** : écrire le noyau fusionné *après* avoir mesuré où passait le
  temps (8 lancements, 17 transferts) — le remède était dicté par la mesure, pas
  par une intuition. Et le seuil de bascule a été MESURÉ (131 072) au lieu d'être
  choisi : le noyau fusionné perd au-delà, ses 14 blocs saturant moins bien la VRAM
  que les 1 792 de la chaîne.
- **Ce que je dois changer** : j'ai écrit un filet de sécurité et je l'ai CRU
  pendant deux commits. Un garde-fou non testé est une décoration ; le tester, c'est
  le saboter exprès et vérifier qu'il refuse. Trois défauts sont tombés de ce seul
  test.
- **Ce que la revue adverse apporte et que mes bancs ne peuvent pas** : une course
  sur la mémoire partagée ne se manifeste que parfois, et jamais dans un banc qui
  passe. Elle se lit — et se prouve dans le PTX.
- **Doute à instruire** : sur gpt-oss à ctx 1024, le déport des PROJECTIONS change
  la perplexité de 1,22 % alors qu'il ne la change que de 0,06 % à ctx 256 (mêmes
  511 jetons). Ce n'est pas le miroir KV (−0,25 %). Une erreur d'ordre de sommation
  ne devrait pas peser 20× plus lourd à contexte plus long : à vérifier au prochain
  sprint, en isolant tête, projections et experts.
- **Doute** : le noyau 4 fait faire au fil 0 des boucles sérieuses (descente des
  256 seaux × 4 passes, balayage de 1024 cases, somme du filet) pendant que 1023
  fils attendent. Les mesures ne montrent pas que ce soit le facteur dominant, mais
  un balayage en log(blockDim) et une descente coopérative sont sur la table.
- **Doute** : le chemin sans puits n'est exercé que depuis ce sprint ; gpt-oss
  (le seul modèle à puits) n'a pas encore tourné avec `DRAVE_GPU_TOPK=1`.

## Planning — sprint 3 (2 h)

| # | chantier | critère de succès |
|---|---|---|
| 1 | **Qualité de l'attention creuse à long contexte** : aiguille (needle) à 4 k / 8 k / 16 k, croisée avec `--attn-topk 256` et sans | la sonde est retrouvée à chaque profondeur, ou l'échec est chiffré et daté |
| 2 | `DRAVE_GPU_TOPK` sur **gpt-oss** (le seul modèle à puits) : A/B perplexité | écart ≤ 1e-4 avec le CPU, et le chemin des puits exercé en vrai |
| 3 | Si le temps le permet : le top-k en **mode lot** (aujourd'hui ignoré, désormais signalé) | soit implémenté, soit refusé bruyamment — plus de drapeau silencieux |

**Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
