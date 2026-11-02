# A2.6 / A8.3 — le lot sur le disque : il accélère le calcul, il ne divise pas les lectures

> **Verdict.** Sur un modèle **dense** de 0,5 Go (Qwen2.5-0.5B-Q8), avec l'**éviction du cache**
> (`posix_fadvise(DONTNEED)`) : le lot **ne divise pas** les lectures du disque — **503 Mio** au lot 1,
> **502 Mio** aux lots 2, 4 et 8 (le modèle est lu une fois, quel que soit le lot). Le lot
> **accélère le calcul** : **24,0 → 30,5 tok/s** (+27 %) dès le lot 2, et le temps mural passe de
> **12,04 s à 9,96 s**. La **PPL** ne bouge presque pas : **15,8452** (lot 1) → **15,8443** (lot 2+),
> soit **−0,006 %**.
>
> **Date** : 2026-11-01. **Lignes** : A2.6 (ordonnanceur) et A8.3 (le lot). **Machine** : CPU seul.
> **Dispositif** : `tools/mesure_lot_disque.sh`, 192 jetons (les 85 626 jetons de
> `data/wikitext2_test.txt`), ctx 512, 20 fils, cache du modèle évincé avant chaque lot.

## 1. La question

A2.6 : « réduire le lot » — le lot réduit-il les lectures du disque ? A8.3c avait montré, sur le
français en f32, que le lot déplace la PPL à lui seul (61,9920 au lot 1, 60,8135 au lot ≥ 2). Ici :
le lot, sur l'**anglais**, en **Q8**, sur un modèle **dense**.

## 2. Ce qui est mesuré

| lot | PPL | lus (Mio) | mur (s) | tok/s |
|---:|---:|---:|---:|---:|
| **1** | 15,8452 | **503** | 12,04 | 24,0 |
| **2** | 15,8443 | **502** | 10,38 | 30,5 |
| **4** | 15,8443 | **502** | 10,18 | 30,0 |
| **8** | 15,8443 | **502** | 9,96 | 30,5 |

**Le lot ne divise pas les lectures.** Le modèle de 0,5 Go est lu une fois ; les activations de 192
jetons sont négligeables devant lui. Le lot ne fait pas partager de lectures : il n'y a rien à
partager dans un modèle dense.

**Le lot accélère le calcul.** Dès le lot 2, le préremplissage passe de 24,0 à 30,5 tok/s (+27 %)
et le temps mural de 12,04 s à 9,96 s (lot 8). C'est le gain des sommes groupées, pas du disque.

**La PPL bouge à peine.** 15,8452 → 15,8443 (−0,006 %) : le lot 2+ est **stable** et le lot 1
diffère ; l'écart de 1,9 % d'A8.3c (le français, f32) ne se retrouve pas ici (l'anglais, Q8). Le
lot 2+ peut être assumé comme **référence distincte** ; le lot 1 reste le chemin jeton par jeton.

## 3. La leçon pour A2.6

- **« Réduire le lot » est inutile** pour les lectures denses : le lot ne les divise pas. Le lot ≥ 2
  est **à garder** pour le calcul (le +27 %).
- Le lot ne partagerait des lectures que là où des **matrices d'experts** sont lues par plusieurs
  jetons du même lot : c'est le **MoE** (A6.2), toujours bloqué faute de modèle routé local.
- Le prochain pas d'A2.6 reste les **experts et la tête** ; le placement KV (×1,93 / ×5,8 à 8 k)
  tient.

## 4. Ce qui pourrait être faux

- **Un seul modèle, un seul prompt** : le 0,5B dense, l'anglais, 192 jetons. Un modèle plus gros
  lirait des activations plus lourdes ; un MoE lirait des experts partagés — c'est là que le lot
  pourrait diviser les lectures.
- **La charge de la machine** (8 à 15 pendant la mesure) : les temps muraux incluent la contention ;
  les lectures, elles, sont stables (503/502).
- **La PPL à 192 jetons** : ce n'est pas la PPL du corpus ; l'écart de lot (0,006 %) est un ordre de
  grandeur, pas une mesure de qualité.
- **L'éviction** : elle garantit le disque froid ; sans elle, le cache de pages aurait menti (c'était
  le défaut du protocole précédent).

## Fichiers

- `tools/mesure_lot_disque.sh` — le dispositif (éviction + lots + lectures).
- `reports/a26-lot-disque.json` — les quatre mesures et le verdict.
- `/tmp/a26-lot-journal.txt` — le journal horodaté (local).
