# A8.0 — `porte-cycle-c2` épingle la PPL de référence : 14,6496

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **neuvième porte
> épinglée** — la PPL directe du cycle C2 est ancrée, et le pas 1 reste exact. A8.0 reste
> **partielle** : 9 portes sur 33.
>
> **Dispositif** : `tools/porte-cycle-c2.sh`, Qwen2.5-0.5B Q8_0, 128 jetons, 4 pas ;
> référence **14,6496**, tolérance **5e-4** ; données [`a80-porte-cycle-c2.json`](a80-porte-cycle-c2.json).

## Ce qui est mesuré

| mesure | valeur |
|---|---:|
| PPL directe (un seul tenant) | **14,6496** |
| pas 1 du cycle | **14,6496** |
| trajectoire 4 pas | 14,6496 → 275,5153 → 940,2153 → 2 988,4562 |
| λ mesuré | **488,82** |

La porte **exit 0** : chaîne exacte, pas 1 exact, cycle borné et annoncé, coût publié, trajectoire
déterministe, divergence bornée et λ mesuré.

## Le contrôle négatif

La condition est numérique : `abs(ppl - 14,6496) <= 5e-4 × 14,6496`. Un décalage de **10 %** est
refusé par la même expression. Le contrôle porte sur la valeur, pas sur les égalités internes.

## Ce qui pourrait le rendre faux

- **Un seul modèle** ; 128 jetons ; 4 pas.
- **Le cycle non entraîné diverge** (λ = 488,82) : c’est le résultat, pas une qualité.
- **La trajectoire** est déterministe sur cette machine, pas nécessairement sur une autre.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **8/33** à **9/33** portes épinglées. A8.3b est mesuré (trois régimes) et A8.3
reste **opt-in** ; la prochaine porte PPL est `porte-profondeur-routee` (longue) ou
`porte-reflexe`.

## Fichiers

- `tools/porte-cycle-c2.sh` — PPL de référence épinglée.
- `reports/a80-porte-cycle-c2.json` — les mesures.
- `reports/rapport-a80-porte-cycle-c2.md` — cette fiche.
