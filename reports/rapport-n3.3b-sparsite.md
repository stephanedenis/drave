# N3.3b — `kwta` et `top_k` agissent séparément

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ✅ **N3.3b tenu** — trois
> DRVM de mêmes poids (graine 7, 113 292 paramètres) ne diffèrent que par un paramètre :
> `kwta` seul change la génération, `top_k` seul la change aussi, et A est déterministe.
> N3.3a changeait les deux ensemble ; N3.3b les sépare.
>
> **Dispositif** : `tools/porte-n3-sparsite.sh`, `--drvm-generate` ; données
> [`n3.3b-sparsite.json`](n3.3b-sparsite.json).

## Ce qui est mesuré

| modèle | `top_k` | `kwta` | sortie |
|---|---:|---:|---|
| **A** | 2 | 0,5 | référence, 27 octets |
| **B** | 2 | **0,25** | **différente** (kwta seul) |
| **C** | **3** | 0,5 | **différente** (top_k seul) |

A deux fois est **identique** ; les trois modèles ont **113 292** paramètres (mêmes poids).

## Le contrôle négatif

- **A deux fois** : identique — la génération n’est pas un tirage.
- **A contre B** : `kwta` seul change la sortie — la sparsité agit.
- **A contre C** : `top_k` seul change la sortie — le nombre d’experts agit.
- **Mêmes paramètres** : la différence ne vient pas d’une capacité différente.

## Ce qui pourrait le rendre faux

- **Modèle synthétique** : la porte prouve la **sensibilité**, pas la **justesse**.
- **Config, pas comptage** : le nombre d’experts/canaux actifs n’est pas lu dans le moteur.
- **Un prompt, une graine**.
- **`kwta` et `top_k` sont testés à deux valeurs** ; une non-linéarité plus fine échapperait.

## Ce que ça change

N3.3b est **fait** au niveau configuration. N3.3c (comptage direct des experts/canaux
actifs) reste ; N3.2b (seuil de confiance) et la porte de composition aussi.

## Fichiers

- `tools/porte-n3-sparsite.sh` — la porte.
- `reports/n3.3b-sparsite.json` — les mesures.
- `reports/rapport-n3.3b-sparsite.md` — cette fiche.
