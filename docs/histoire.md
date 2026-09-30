# Histoire du projet, et le renommage

Ce document est là pour une raison précise : **le 30 septembre 2026, le projet a
changé de nom, partout, d'un coup.** Renommer efface des traces ; ce fichier est
la trace qu'on ne voulait pas perdre.

## 1. Le projet a eu trois âges

| âge | ce qu'il était | où c'est écrit |
|---|---|---|
| **Qtrinet** (origine) | inférence de LLM en ternaire / multi-bits sur un cluster de cartes **Stratix V** (Microsoft Storey Peak), 100 % logique, sans DSP. Le cahier des charges d'origine est **conservé tel quel** : [`Qtrinet-bootstrap.md`](../Qtrinet-bootstrap.md) — c'est un document daté, il n'est pas réécrit | `Qtrinet-bootstrap.md`, `README.md` §« Écarts avec le CDC » |
| **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Representation*). Le prototype C mesure **7,79 G événements/s**, le croisement push/pull est mesuré à **10 % de densité** | `reports/rapport-cpu-aer.md`, `reports/rapport-croisement-push-pull.md`, `reports/rapport-encodage.md` |
| **Drave** (aujourd'hui) | le moteur Rust qui exploite cette représentation sur CPU, GPU et FPGA, avec le contexte long (KV paginé, MLA, vision) et la distribution en ligne de mire | `docs/vision.md` |

Le nom **Qtrinet** appartenait au premier âge : il évoquait un réseau ternaire, une
puce, un banc de cartes. Ce que le projet est devenu ne se raconte plus comme ça.

## 2. Le nom

**Drave** : *stream of logs* — le flux des listes. Et, en français d'ici, la
**drave** : ces billots confiés à la rivière au printemps, guidés de l'estacade
jusqu'à la scierie. Le mot porte les trois propriétés du moteur : il **coule**
(les listes avancent), il se **répartit** (les billots se séparent aux fourches),
il se **surveille** (on compte, on trie, on redirige).

## 3. Ce qui a changé le 2026-09-30, et ce qui n'a pas changé

**Changé, partout** (61 fichiers de contenu, plus les chemins) :

| avant | après |
|---|---|
| crate `qtrinet-core/` | `drave-core/` |
| binaire `qtrinet-core` | **`drave`** |
| noyaux `gpu/qtrinet_gpu.cu` / `.ptx` | `gpu/drave_gpu.cu` / `.ptx` |
| variables `QT_*` | **`DRAVE_*`** (voir le tableau ci-dessous) |
| « Qtrinet » dans les rapports et les documents | « Drave » |

**Pas changé, volontairement** :

* `journal/` — les sessions archivées gardent ce qui a été dit ce jour-là. Un
  journal réécrit n'est plus un journal ;
* `Qtrinet-bootstrap.md` — le cahier des charges d'origine, tel quel ;
* l'historique Git — les commits anciens gardent leurs messages.

## 4. Migrer un script ou une tâche planifiée

Les anciennes variables **ne font plus rien** (elles ne sont pas des alias) : le
moteur prévient et s'arrête là plutôt que de laisser croire qu'une option est
active.

| ancien | nouveau |
|---|---|
| `QT_GPU` | `DRAVE_GPU` |
| `QT_GPU_TETE` | `DRAVE_GPU_TETE` |
| `QT_GPU_KV` | `DRAVE_GPU_KV` |
| `QT_GPU_EXPERTS`, `QT_GPU_EXPERTS_GO` | `DRAVE_GPU_EXPERTS`, `DRAVE_GPU_EXPERTS_GO` |
| `QT_KV_BITS`, `QT_KV_F16` | `DRAVE_KV_BITS`, `DRAVE_KV_F16` |
| `QT_YARN`, `QT_YARN_NON`, `QT_YARN_MSCALE`, `QT_YARN_RAMPE` | `DRAVE_YARN*` |
| `QT_BANC_KV_*` | `DRAVE_BANC_KV_*` |
| `QT_HARMONY_TRACE`, `QT_Q8_BLOCS`, `QT_SANS_EMPRUNT`, `QT_VISION_TEXTE` | `DRAVE_*` |

Et les chemins : `qtrinet-core/target/release/qtrinet-core` devient
**`drave-core/target/release/drave`**.

Ce qui vit **hors du dépôt** et doit être mis à jour à la main : les scripts
personnels (par exemple dans `/tmp`), une éventuelle tâche `crontab`, et le
crochet Git s'il pointait vers un chemin absolu — celui du dépôt
(`.git/hooks/pre-commit`) appelle `tools/archive_sessions.py` en chemin relatif
et n'a pas eu besoin d'être touché.

## 5. Une leçon de méthode, gardée ici

Le renommage a été fait « tout, tout de suite », y compris dans les rapports
datés. C'est un choix : la cohérence de lecture compte plus que la fidélité
littérale des textes — à une exception près, le journal, qui est la mémoire
brute, et le CDC, qui est la pièce d'origine. Ce document existe pour que la
question « pourquoi ce projet s'appelait-il Qtrinet ? » ait une réponse, et pour
que les vieux scripts aient une table de conversion au lieu d'un mystère.
