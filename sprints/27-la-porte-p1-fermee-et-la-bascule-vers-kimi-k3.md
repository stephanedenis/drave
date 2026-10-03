# Sprint 27 — La porte P1 fermée, les portes auditées, et la bascule vers Kimi-K3

- **Début** : 09:40 · **Fin** : 11:00
- **Objectif** : le bloc partait pour fermer la porte Drave de P1 (les 24 poids de
  connexion, calculés puis jetés — un forward muet) et pour finir la porte de
  correction à ctx 1 024. Il a fait les deux, **et il a changé de cible** : sur
  directive explicite, les modèles périmés sortent du chemin critique et le
  travail se porte sur les meilleurs modèles ouverts, « surtout ceux qui sont
  typiquement trop gros pour l'exécution locale ».
- **Engagement de fin** : dépôt vert, machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. Porte Drave de P1 : elle n'existait pas, elle existe, et elle révèle une structure

Ni le canal ni l'outil n'existaient (`tools/analyse_hc.py` : absent ; aucun
`DRAVE_TRACE_HC`). Les 24 coefficients d'un raccord étaient **calculés puis
jetés**. Le moteur les écrit désormais (`DRAVE_DUMP_COUCHES`, `hc_attn`/`hc_ffn` :
4 `pre` + 4 `post` + 16 `comb`), l'outil les relit, **vérifie la promesse du
Sinkhorn** (l'axe qu'il normalise en dernier : `|Σsrc − 1| = 1,14e-06`) et sort en
erreur sinon. Porte branchée dans `portes.sh` (§7sexies), désormais portée par
**V4.1** (un modèle périmé ne doit pas porter une porte vivante).

**Ce que la mesure a trouvé** (V4-Flash 43 couches + V4.1 40 couches, 4 positions,
**332 matrices**) : les **4 connexions dominantes forment une PERMUTATION dans
332/332 cas** (99 % de la masse) ; l'identité domine (34-42 identités sur 43,
38-39 sur 40) et **9 couches de V4-Flash permutent réellement** (dont la 34,
presque un 4-cycle, masse diagonale 1,03/4). Stabilité entre positions : 0,92
(V4-Flash) et 0,98 (V4.1). Coût d'une simplification en permutation :
**6,4 % d'erreur L2** en moyenne (V4-Flash), 8,2 % (V4.1) — chiffré, pas supposé.

### 2. Les deux portes, auditées phase par phase

`reports/rapport-portes-p0-p9.md` : P0 à P6 et P8 tenues ; **P1 fermée
aujourd'hui** ; **P7** seule porte **impossible** (llama.cpp refuse
`deepseek41`), avec sa condition de sortie ; P9 optionnel, son dernier ajout
*opt-in* et son écart mesuré. Une précision qui change la lecture : pour V4, les
**paires** sont comptées (16,2 G/jeton, avec provenance) mais la part **en
listes est nulle** — le calcul est dense. Les portes de flux sont tenues au sens
du **contrat d'échange**, pas de l'unité de calcul.

### 3. Porte de correction à ctx 1 024 (1 023 positions) — la dernière de V4-Flash

| mesure | llama.cpp | Drave |
|---|---|---|
| perplexité | **5,0061** | **5,0921** (+1,7 %) |
| corrélation moyenne | **0,991443** | |
| top-1 | **957/1 023 (93,5 %)** | |
| tranches | 0,98534 → 0,98934 → **0,99248** (s'améliore) | |
| coût | **2,98 s/jeton** | |

**Elle a d'abord échoué** sur le plancher (position 1009, corrélation 0,8868).
Analyse : cette position a une **NLL nulle des deux côtés**, le même jeton et le
même rang — Pearson ne mesure rien sur une distribution saturée. Quatre des cinq
positions sous 0,95 sont dans ce cas. Critère révisé **avec sa mesure** : les
positions saturées (NLL réf < 0,05) sortent de la corrélation, sont **comptées et
affichées**, et le **top-1 les couvre** (jugé sur toutes). Le cas dégradé
(`--abits 8`) **échoue toujours**.

### 4. La bascule : Kimi-K3 (nouvelle cible), et V4-Flash retiré

Mesuré avant de s'engager :

| fait | valeur |
|---|---|
| GGUF visé | `unsloth/Kimi-K3-GGUF` UD-Q4_K_XL : **1 508,7 Go**, 32 shards |
| architecture | **`kimi-k3`** — inconnue de notre moteur |
| structure | 93 couches · 896 experts dont **16 par jeton** · 1 M de contexte · attention **hybride linéaire** (le texte EST Kimi-Linear) · `situ` |
| experts | **MXFP4** (41,9 Go pour 3 couches) |
| **poids par jeton** | **≈ 35 Go** (2,3 % du modèle) → NVMe 17 s/jeton · disque dur 173 s |
| référence | **llama.cpp amont connaît `kimi-k3`** (`src/models/kimi-k3.cpp` ✓) → **seconde copie construite** (`llama.cpp-k3`, 6 min) |
| téléchargement | **108 Mo/s** → ~4 h (en cours) |

`docs/plan-kimi-k3.md` porte les jalons M1→M8. **V4-Flash est retiré** : copie
NVMe supprimée, porte hc repointée (testée), section 6bis de `portes.sh` marquée
**ARCHIVÉE** — les acquis restent dans les rapports.

## Rétrospective — garder / changer / doute

**Garder.** Chercher l'instrument avant de croire le chiffre : la porte P1
« existait » dans le plan depuis le 02/10 et **aucun outil ne la vérifiait**.
Même schéma que la porte de correction au bloc 22 : une porte qu'on n'exécute pas
n'existe pas.

**Garder (2).** Le test sur données synthétiques **et** sur données réelles : le
piège d'axe (`comb[d + s·hc]` → la destination varie le plus vite) a été trouvé
par le test synthétique, et la lecture de `sinkhorn` a confirmé lequel des deux
axes est garanti. Sans les deux, l'outil accusait le moteur à tort.

**Changer.** Deux fois en deux blocs, un critère a échoué puis a été révisé
(plancher de corrélation). Les deux révisions sont motivées par la mesure, mais
la **répétition** est un signal : un critère posé sur une statistique de queue
(minimum, maximum) sur un échantillon qui grandit finira toujours par échouer.
La règle à retenir : **un critère s'écrit en taux, pas en extremum** — et le
prochain critère sera écrit comme ça du premier coup.

**Changer (2).** J'ai construit la référence d'exécution (llama.cpp `kimi-k3`)
**avant** de savoir si notre moteur saurait lire le fichier : c'est le bon ordre
(la porte d'abord), mais il faut maintenant la même discipline que pour V4.1 —
écrire la spécification depuis le code publié **avant** d'implémenter, sinon on
vérifie notre lecture contre notre lecture.

**Doute.** Les 35 Go de poids par jeton rendent l'exécution locale **impossible
sans réutilisation** : à 2 Go/s (NVMe) c'est 17 s/jeton, et le disque dur est hors
jeu. La question ouverte est donc *mesurable mais non mesurée* : **quelle est la
réutilisation réelle des experts entre jetons** sur ce modèle (16 sur 896, soit
1,8 % par jeton) ? Le cache RAM d'experts a été mesuré **plus lent** sur V4.1, donc
la réponse n'est pas acquise — c'est le jalon M6, et il décide de tout le reste.

**Doute (2).** Le téléchargement de 1,5 To occupe le lien et le disque pendant
~4 h : toute mesure de débit publiée dans ce créneau doit dire que la machine
télécharge. Les chiffres de ce sprint ont été pris avant la bascule, ou sur des
fenêtres où le débit était stable — mais c'est une variable de plus, et elle est
nommée.
