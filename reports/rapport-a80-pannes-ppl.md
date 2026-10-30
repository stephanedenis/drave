# A8.0 — `porte-pannes` épingle la PPL nominale : 33,0156

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-30 · **Verdict** : ✅ **dix-neuvième porte
> épinglée** — la PPL nominale est ancrée à **33,0156** (tolérance 5e-4), et les deux pannes ne
> rendent **aucune** PPL. A8.0 passe à **19/33**.
>
> **Dispositif** : `tools/porte-pannes.sh`, Qwen2.5-0.5B Q8_0 ; données
> [`a80-pannes-ppl.json`](a80-pannes-ppl.json).

## Ce qui est mesuré

| cas | résultat |
|---|---|
| nominal | code 0, PPL **33,0156** |
| pair tué | pas **102**, **375 768** octets, code **7**, aucune PPL |
| pair absent | **1 s**, code **7**, aucune PPL |

## Le contrôle négatif

- **PPL nominale** : `abs(ppl - 33,0156) <= 5e-4 × 33,0156`.
- **Pair tué/absent** : aucune perplexité, code 7 — une PPL partielle serait refusée.
- **La panne nomme** région, pas et octets.

## Ce qui pourrait le rendre faux

- **Un seul modèle** ; le pas/octets de panne varie (95/349 980 dans une exécution antérieure,
  102/375 768 ici).
- **5e-4** attrape 0,05 %, pas 0,01 %.
- **La PPL nominale** dépend du corpus et de la quantification.

## Ce que ça change

A8.0 : **19/33**. `porte-pannes` n’est plus seulement « présence » : elle ancre une valeur.
Voir l’audit final [`rapport-a80-audit-final.md`](rapport-a80-audit-final.md).

## Fichiers

- `tools/porte-pannes.sh` — pin.
- `reports/a80-pannes-ppl.json` — les mesures.
- `reports/rapport-a80-pannes-ppl.md` — cette fiche.
