# R13.2 — vocab 1024 : le BPE perd encore plus à octets égaux

> **Ligne de roadmap** : R13.2 · **Date** : 2026-10-29 · **Verdict** : ⛔ **négatif** — à budget
> d’octets égal, BPE 1024 fait **1,8726** bits/octet contre **1,8021** pour bytes : il **perd
> 3,9 %**. Le vocab 512 perdait 0,7 % ; augmenter le vocabulaire n’aide pas ici.
>
> **Dispositif** : tokenizer 1024 sur `corpus_fr_train`, val `corpus_fr_val` (231 694 octets,
> 94 463 jetons), 4 k pas (≈ 10,16 M octets vus), même graine/architecture ; données
> [`r13.2-vocab1024.json`](r13.2-vocab1024.json).

## Ce qui est mesuré

| modèle | pas | PPL val | bits/octet val | octets vus |
|---|---:|---:|---:|---:|
| bytes | 10 000 | 3,4872 | **1,8021** | 10,24 M |
| BPE 512 | 5 000 | ~12 | 1,8142 | 10,13 M |
| **BPE 1024** | 4 000 | 24,1360 | **1,8726** | 10,16 M |

- **BPE 1024** : **+3,92 %** par rapport à bytes.
- **BPE 512** : +0,67 %.
- Le vocabulaire plus grand ne compense pas le budget d’octets.

## Le contrôle négatif

- **Même val**, même graine, même architecture ; bits/octet exact.
- **4 k BPE1024 ≈ 10 k bytes** en octets vus (10,16 M contre 10,24 M, écart 0,8 %).
- **Deux vocabulaires** (512 et 1024) perdent à octets égaux : le signe ne dépend pas d’un choix
  de vocabulaire.
- **La précision par jeton** (32,8 %) n’est pas comparable ; seul le bits/octet l’est.

## Ce qui pourrait le rendre faux

- **Français, 4 k pas, une graine** ; pas la convergence.
- **Le tokenizer** est entraîné sur le train, mais le corpus reste petit (4,4 Mo).
- **Pas d’anglais** ; le arabe/cyrillique pourraient changer.
- **La PPL par jeton** n’est pas la qualité.

## Ce que ça change

R13.2 est **négatif** : à octets égaux, 512 et 1024 perdent. La condition R13 reste ; la prochaine
mesure est l’anglais 100 Mo, plus de pas et une deuxième graine — pas une adoption.

## Fichiers

- `reports/r13.2-vocab1024.json` — les mesures.
- `reports/rapport-r13.2-vocab1024.md` — cette fiche.
