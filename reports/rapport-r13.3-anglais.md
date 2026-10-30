# R13.3 — anglais 100 Mo : le BPE perd encore à octets égaux

> **Ligne de roadmap** : R13.3 · **Date** : 2026-10-30 · **Verdict** : ⛔ **négatif confirmé** —
> sur l’anglais, à budget d’octets égal, BPE 512 fait **2,7522** et BPE 1024 **2,8147** bits/octet
> contre **2,6408** pour bytes : ils perdent **4,2 %** et **6,6 %**. Le signe est le même qu’en
> français ; ce n’est pas un artefact du corpus.
>
> **Dispositif** : tokenizers 512/1024 entraînés sur `corpus_en.txt` (100 276 153 octets), val
> `corpus_en_val.txt` (2 032 162 octets), bytes 10 k, BPE 512 5 k, BPE 1024 4 k (octets vus
> égaux), même graine/architecture ; données [`r13.3-anglais.json`](r13.3-anglais.json).

## Ce qui est mesuré

| modèle | pas | PPL val | bits/octet val | écart |
|---|---:|---:|---:|---:|
| bytes | 10 000 | **6,2366** | **2,6408** | — |
| BPE 512 | 5 000 | 26,4523 | 2,7522 | **+4,22 %** |
| BPE 1024 | 4 000 | 52,6075 | 2,8147 | **+6,59 %** |

- **Validation séparée** : tokenizers entraînés sur le train, évalués sur `corpus_en_val`.
- **Octets vus** : bytes 10,24 M ; BPE 512 5,12 M jetons ×1,7169 = 8,79 M octets (val ratio)
  — le contrôle exact est le ratio de **train** ; les deux restent dans la même décade.
- **Deux vocabulaires** perdent : 512 et 1024.

## Le contrôle négatif

- **Même val** (2 032 162 octets), même graine, même architecture.
- **Train/val séparés** : pas de fuite du tokenizer.
- **Français + anglais** : le BPE perd dans les deux langues à octets égaux.
- **Deux vocabulaires** : le signe ne dépend pas de 512.
- **La précision par jeton** (27,1 % BPE contre 46,3 % bytes) n’est pas comparable ; seul le
  bits/octet l’est.

## Ce qui pourrait le rendre faux

- **Une graine**, 10 k/5 k/4 k pas ; pas la convergence.
- **Anglais 100 Mo** ; le ratio val est plus faible que le train (1,7169 contre 1,8976), donc le
  budget d’octets du BPE 512 est légèrement sous 10,24 M — défavorable au BPE, mais l’écart est
  de 4,2 %, pas 14 %.
- **Le corpus anglais** n’est pas du texte naturel contrôlé ; il peut favoriser bytes.
- **Pas de deuxième graine** : le bruit n’est pas chiffré.

## Ce que ça change

R13.3 **renforce la condition** : à octets égaux, le BPE 512/1024 perd en français **et** en
anglais. La prochaine mesure est une **deuxième graine** et plus de pas, pas une adoption.

## Fichiers

- `reports/r13.3-anglais.json` — les mesures.
- `reports/rapport-r13.3-anglais.md` — cette fiche.
