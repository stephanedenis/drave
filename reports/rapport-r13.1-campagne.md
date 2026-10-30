# R13.1c — à octets égaux, le BPE ne gagne plus

> **Ligne de roadmap** : R13.1 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **le gain de 11 % ne
> survit pas au contrôle à octets égaux** — à 10 k pas, bytes **1,8021** contre BPE **1,6332**
> bits/octet (BPE **−9,4 %**), mais le BPE a vu **2× plus d’octets**. À octets égaux (BPE 5 k),
> BPE **1,8142** contre bytes **1,8021** : le BPE **perd 0,7 %**. R13.1 repasse en **condition**.
>
> **Dispositif** : tokenizer 512 entraîné sur `corpus_fr_train` seulement, val `corpus_fr_val`
> (231 694 octets, 118 650 jetons), mêmes graine/architecture, 10 k pas ; données
> [`r13.1-campagne.json`](r13.1-campagne.json).

## Ce qui est mesuré

| modèle | pas | PPL val | bits/octet val | octets vus |
|---|---:|---:|---:|---:|
| bytes | 10 000 | **3,4872** | **1,8021** | 10,24 M |
| BPE 512 | 10 000 | 9,1218 | **1,6332** | 20,25 M |
| BPE 512 | 5 000 | ~12 | **1,8142** | 10,13 M |

- **À pas égaux** : BPE **−9,37 %**.
- **À octets égaux** : BPE **+0,67 %** (il perd).
- **Validation séparée** : le tokenizer n’a jamais vu `corpus_fr_val`.

## Le contrôle négatif

- **Même val** (231 694 octets) pour les trois ; bits/octet exact, pas un ratio global.
- **5 k BPE ≈ 10 k bytes** en octets vus (10,13 M contre 10,24 M, écart 1,1 %).
- **Même graine, architecture, évaluation** ; seul le tokenizer change.
- **Le pilote 200/400 pas** (11,0 %) est **sous-entraîné** : à 10 k bytes, le baseline bytes
  descend à 1,8021 et le gain disparaît à octets égaux.

## Ce qui pourrait le rendre faux

- **Français, vocab 512, 10 k pas, une graine**.
- **La précision par jeton** n’est pas comparable (44,1 % BPE contre 64,9 % bytes) : elle ne dit
  rien du bits/octet.
- **Le BPE voit plus de contexte** à seq 128 (253 octets contre 128).
- **10 k pas** n’est pas la convergence ; à 1024/anglais/plus de pas, le signe peut changer.

## Ce que ça change

R13.1 n’est **pas** une victoire du BPE à octets égaux. Le pilote 11 % était réel à son budget,
mais il ne se reproduit pas quand le baseline bytes reçoit le même nombre d’octets. **R13 repasse
en condition** ; la prochaine mesure est vocab 1024, anglais 100 Mo, plus de pas — pas un adoption
sur la foi du pilote.

## Fichiers

- `reports/r13.1-campagne.json` — les mesures.
- `reports/rapport-r13.1-campagne.md` — cette fiche.
