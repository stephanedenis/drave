# A7.9 — le cache KV à distance coûte 24,6 ko par jeton

> **Objet.** A7.6 exécute une couche à distance mais **ne transfère pas le cache KV** (prefill).
> Ici on mesure le **cache seul** : couche 12 de Qwen 0.5B, 2 têtes KV, head_dim 64, f32.

## Résultats (64 jetons)

| mesure | valeur |
|---|---:|
| octets du cache | **65 548 o** |
| par jeton | **1 024,19 o** |
| fidélité | **exacte** |
| messages identiques | **5 / 5** |
| latence loopback | **0,179 ms** |
| ratio KV / hidden A7.6 (une couche) | **0,249** |
| **24 couches, par jeton** | **24 580 o** |
| **24 couches, 4 096 jetons** | **96,0 Mio** |

## Lecture

- Le cache KV d'**une couche** pèse **1 024 o/jeton**, soit **0,25×** le hidden d'A7.6 (4 105 o).
- Mais les **24 couches** cumulent **24 580 o/jeton** : **6×** le hidden, **96 Mio** pour 4 096 jetons.
- Le transport est **fidèle** et rapide en loopback (**0,18 ms**), mais le **volume** domine.
- **A7.6 évitait ce coût** en restant en **prefill** (`use_cache=False`).

## Verdict

**A7.9 est un négatif pour le transfert naïf du KV** : à 24 couches, le cache coûte **6×** le hidden
par jeton et **96 Mio** pour 4 096 jetons. Il faut **garder le KV côté serveur** (état persistant),
ou le **quantifier** (int8 → 24 Mio), pas le renvoyer à chaque pas.

## Limites

- **Cache synthétique** : la forme est celle de la couche 12, pas un vrai décodage autoregressif.
- **Une couche** mesurée ; l'extrapolation à 24 suppose des couches identiques.
- **Loopback** seulement ; pas de WAN.
- Le coût CPU du (dé)codage n'est pas compté.

## Fichiers

- Code : [`tools/kv_reseau.py`](../tools/kv_reseau.py).
- Test : [`tools/cerveau/tests/test_kv_reseau.py`](../tools/cerveau/tests/test_kv_reseau.py).
- JSON : [`kv-reseau.json`](kv-reseau.json).
