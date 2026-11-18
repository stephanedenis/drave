# Les plans de travail par fenêtre tarifaire — l'API à tarif réduit, le local au plein tarif

> **Le principe.** DeepSeek applique un **tarif réduit** pendant la fenêtre **UTC 16:30 → 00:30**
> (la Chine 00:30 → 08:30), et un tarif plein le reste du temps. Pour le Canada (EST, UTC−5),
> la fenêtre remisée tombe **11:30 → 19:30** — c'est-à-dire **l'après-midi de travail** ; la
> fenêtre pleine couvre **19:30 → 11:30** (la nuit et le matin).
>
> **La règle.** On place les tâches **qui appellent l'API** dans la fenêtre remisée, et on garde
> **une file de tâches locales** (GPU, CPU, docs, tests) pour la fenêtre pleine — de sorte que
> **rien n'attende** et que le coût API soit minimal.

## 1. Les deux fenêtres (heure du Canada, EST)

| fenêtre | heures (EST) | heures (Chine) | tarif | ce qu'on y fait |
|---|---|---|---|---|
| **remisée** | **11:30 → 19:30** | 00:30 → 08:30 | **−50 %** (chat) / **−75 %** (raisonneur) | **tout ce qui appelle l'API** : le tagger, la distillation, les sorties de modèle |
| **pleine** | **19:30 → 11:30** | 08:30 → 00:30 | plein | **tout ce qui est local** : l'entraînement GPU, les bancs, les tests, les docs, les portes |

**Les week-ends** : DeepSeek applique le tarif réduit **toute la journée** les samedis et dimanches
(la mesure de la presse, à revérifier sur la page officielle). **La règle locale** : le samedi et
le dimanche, la fenêtre remisée couvre **toute la journée** — on y place les gros lots d'API.

## 2. Les plans par chantier

| chantier | la fenêtre remisée (l'API) | la fenêtre pleine (le local) |
|---|---|---|
| **B / B13 — le produit** | le **tagger** sur les textes réels (`--tagger`), les sorties du modèle pour la distillation, les exemples de la doc | les **tests**, le CLI, le schéma, la doc, la porte produit |
| **R — le lecteur** | le tagger sur le gold 612, les mesures de PPL par API | les mesures locales (le gold, le parseur), les conventions |
| **N — le natif** | la **distillation** (l'API → le natif), les données d'instruction, les paires | l'**entraînement GPU** (le 100 M, le 30 k), le banc de génération, le cache KV |
| **A — le moteur** | *(rien : local uniquement)* | les kernels GPU, le FPGA, la dispersion, les mesures |
| **S — les structures** | *(rien : local)* | le générateur, la page, les verdicts |
| **D — les données** | l'OCR ou l'étiquetage **si** l'API est le meilleur chemin (à mesurer) | le corpus, le nettoyage, le dédoublonnage |
| **L — le bloc langue** | *(rien : local)* | les règles, les tests, le lexique |

**Les trois chantiers qui gagnent le plus à la fenêtre remisée** : **N** (la distillation est
gourmande en tokens), **R** (le tagger), **B13** (les sorties de modèle). Les autres sont
**locaux par nature** — c'est déjà la bonne nouvelle : la fenêtre pleine ne les ralentit pas.

## 3. La journée type

| heure (EST) | fenêtre | la file |
|---|---|---|
| 08:00 → 11:30 | **pleine** | le local : le GPU (l'entraînement), les tests, les docs, les portes |
| **11:30 → 19:30** | **remisée** | **l'API** : le tagger, la distillation, les sorties ; le local en parallèle (le GPU) |
| 19:30 → 08:00 | **pleine** | le local : les longs runs GPU, les passes, le rangement |

**La file « jamais en attente »** : chaque chantier a **deux files** — une **API** (pour la
fenêtre remisée) et une **locale** (pour la pleine). Si la fenêtre bascule et que la file API est
vide, on prend la locale ; si la locale est vide, on prend l'API (mais seulement en remisée).

## 4. Ce qui est déjà en place

- Le **tagger** (`--tagger`) : il appelle l'API ; c'est la tâche API de référence.
- L'**entraînement GPU** (`entrainer_native --amp --device cuda`) : le local de référence.
- Les **bancs** (génération, grammaticalité, PPL) : locaux.
- Le **cache** du client DeepSeek (`data/deepseek/cache/`) : il évite de payer deux fois le même
  texte — un appel déjà fait en remisée reste gratuit en pleine.

## 5. Les limites

- **Les heures exactes** : la fenêtre remisée est celle de la **documentation officielle**
  DeepSeek ; elle peut changer — **la vérifier** avant un gros lot (la page `api-docs.deepseek.com`,
  la section « pricing »).
- **Le week-end** : la mesure de presse (le 17/11) est à confirmer sur la page officielle.
- **La qualité** : un lot d'API en remisée n'est pas plus mauvais ; c'est le **même** modèle.
- **Les tâches locales ne paient pas** : elles consomment le GPU/CPU de la machine — le vrai
  coût, c'est le temps (et l'électricité), pas les tokens.
