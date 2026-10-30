# R13.4 — deux graines : le BPE 512 est dans le bruit, le 1024 perd

> **Ligne de roadmap** : R13.4 · **Date** : 2026-10-30 · **Verdict** : ⛔ **pas de gain à octets
> égaux** — sur deux graines, BPE 512 est à **+0,39 %** (dans le bruit : +0,67 % puis +0,10 %)
> et BPE 1024 à **+4,09 %** contre bytes. Le signe négatif est stable ; l’ampleur du 512 ne l’est pas.
>
> **Dispositif** : mêmes ids/val/architecture que R13.1c, graines 1 et 2 ; bytes 10 k, BPE 512 5 k,
> BPE 1024 4 k ; données [`r13.4-graines.json`](r13.4-graines.json).

## Ce qui est mesuré

| modèle | graine 1 | graine 2 | moyenne | écart moyen |
|---|---:|---:|---:|---:|
| bytes | 1,8021 | 1,7982 | **1,8001** | — |
| BPE 512 | 1,8142 | 1,8000 | **1,8071** | **+0,39 %** |
| BPE 1024 | 1,8726 | 1,8750 | **1,8738** | **+4,09 %** |

- **BPE 512** : +0,67 % à la graine 1, +0,10 % à la graine 2 ; la moyenne est positive mais
  l’écart entre graines (0,78 %) est plus grand que l’effet.
- **BPE 1024** : +3,91 % et +4,27 % ; l’effet est stable et clairement négatif.
- **Bytes** : 1,8021 / 1,7982 ; le bruit de graine est de **0,21 %**.

## Le contrôle négatif

- **Mêmes données, même val, même architecture** ; seule la graine change.
- **Deux vocabulaires** : 512 dans le bruit, 1024 négatif stable.
- **Le signe** ne s’inverse pas ; l’ampleur du 512, oui.
- **La précision par jeton** n’est pas utilisée pour comparer.

## Ce qui pourrait le rendre faux

- **Deux graines** ne donnent pas un intervalle de confiance.
- **Français seulement** ; l’anglais (R13.3) est négatif aussi, mais une graine.
- **10 k/5 k/4 k pas** ; pas la convergence.
- **Le BPE 512** pourrait être neutre plutôt que négatif ; il n’est **pas** un gain.

## Ce que ça change

R13.4 **ferme la question du bruit** : le BPE 512 n’a pas de gain reproductible à octets égaux ;
le 1024 perd. R13 reste en **condition** ; la prochaine mesure est multilingue, pas une adoption.

## Fichiers

- `reports/r13.4-graines.json` — les mesures.
- `reports/rapport-r13.4-graines.md` — cette fiche.
