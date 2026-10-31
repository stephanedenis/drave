# R13 — la décision : rester en octets, parce que le BPE ne gagne pas à octets égaux

> **Ligne de roadmap** : R13 / R1.3 · **Date** : 2026-10-30 · **Verdict** : ✅ **décision
> mesurée — le natif reste en octets** (`vocab = 256`). À budget d'**octets** égal, le BPE perd
> partout : **+0,39 %** (512, deux graines), **+3,92 à +4,09 %** (1024 selon la graine), **+4,22 % / +6,59 %** (anglais).
> Le « gain de 11 % » du pilote était un **artefact de budget** : à pas égaux, le BPE voit deux
> fois plus d'octets.
>
> **Dispositif** : synthèse de six fiches et de six JSON — français (4,4 Mo) et anglais
> (100 Mo), vocabulaires 512 et 1024, deux graines ; comparaison en **bits/octet** à octets vus
> égaux, train/val séparés ; `tools/tokenizer_bpe.py`, `tools/entrainer_native_tokens.py`,
> `tools/r13_anglais.py` ; données [`r13-tokenisation.json`](r13-tokenisation.json),
> [`r13.1-bpe.json`](r13.1-bpe.json), [`r13.1-campagne.json`](r13.1-campagne.json),
> [`r13.2-vocab1024.json`](r13.2-vocab1024.json), [`r13.3-anglais.json`](r13.3-anglais.json),
> [`r13.4-graines.json`](r13.4-graines.json).

## La question

Le natif lit des **octets** : 1 jeton par octet, vocabulaire de 256. Le BPE promet des séquences
**3 à 5 fois plus courtes** sur le latin (R13.0), donc un empan utile plus grand et un coût par
octet plus faible. La question de R13 n'est pas « le BPE compresse-t-il ? » (oui, mesuré) mais
« **à budget égal, le BPE donne-t-il une meilleure qualité par octet ?** » — c'est-à-dire un
**bits/octet** plus bas, même graine, même architecture, même nombre d'octets vus.

## Ce qui est mesuré

Toutes les valeurs sont des **bits/octet de validation**, plus bas = mieux.

| dispositif | bytes | BPE 512 | BPE 1024 | verdict |
|---|---:|---:|---:|---|
| R13.1c français, 10 k / 5 k pas | **1,8021** | 1,8142 | — | BPE **+0,67 %** |
| R13.2 français, 4 k pas | **1,8021** | — | 1,8726 | BPE **+3,92 %** |
| R13.3 anglais 100 Mo | **2,6408** | 2,7522 | 2,8147 | **+4,22 % / +6,59 %** |
| R13.4 français, deux graines | **1,8001** | 1,8071 | 1,8738 | **+0,39 %** (bruit) / **+4,09 %** |

- **Le signe ne s'inverse jamais** : 512 est dans le bruit d'une graine à l'autre (+0,67 % puis
  +0,10 %), 1024 perd nettement et de façon stable.
- **Deux langues** : le français et l'anglais donnent le même signe ; ce n'est pas un artefact
  du corpus français.
- **Deux vocabulaires** : agrandir le vocabulaire (512 → 1024) **aggrave** la perte.
- **Deux graines** : le bruit de graine du modèle octets est de **0,21 %**, plus petit que
  l'effet du 1024.

## Le contrôle négatif, et le piège du budget

Le pilote R13.1 (200/400 pas) trouvait le BPE **meilleur de 11,0 %** — et c'était faux de
budget : à 200 pas BPE contre 400 pas octets, les **octets vus** étaient comparables, mais le
modèle octets était encore **sous-entraîné**. À 10 k pas, le baseline octets descend à 1,8021 et
le gain disparaît : à **pas égaux**, le BPE gagne 9,4 % mais voit **deux fois plus d'octets**.

- **Le budget se compte en octets**, pas en pas ni en jetons : c'est la seule unité commune aux
  deux tokenisations.
- **Le ratio de validation**, pas le ratio global, donne le bits/octet exact (correction
  d'audit : 11,0 % et non 11,9 % au pilote).
- **La réversibilité** est vérifiée avant toute comparaison : un tokenizer qui perd des octets
  est disqualifié (R13.0, sept échantillons, réversible exactement).
- **Le contrôle aléatoire** de R13.0 tombe à 1,63 octet/jeton contre 3,3–5,2 sur du naturel : la
  compression est linguistique, pas mécanique.

## La décision

1. **Le natif reste en octets** pour v0/v1 : `vocab = 256`, aucune dépendance à un tokenizer
   externe, réversibilité triviale, tête d'embedding minimale.
2. **Le BPE n'est pas adopté** : son avantage de longueur (3,4–5,2× sur le latin) ne se
   convertit pas en qualité par octet, et son coût est réel (vocabulaire 512 → **12,45 M**
   paramètres contre **11,81 M** pour les octets, +5,4 %).
3. **R13 est close** ; R1.3 garde la trace de la mesure. N5 (50–100 M) n'est **pas** conditionné
   au BPE : la réouverture se déciderait sur un modèle assez grand pour que la longueur de
   séquence domine, pas sur une préférence d'architecture.

## Ce qui pourrait la rendre fausse

- **Petits modèles, peu de pas** : 10 k pas, 11,8 M de paramètres ; à 50–100 M, le coût de la
  longueur de séquence peut changer le rapport.
- **Deux langues, deux vocabulaires** : arabe, cyrillique et CJK ne sont pas entraînés ici ; le
  gain de longueur y est plus faible (2,8–4,6×), ce qui ne plaide pas pour le BPE, mais ce n'est
  pas mesuré en bits/octet.
- **Un BPE entraîné sur un petit corpus** : un tokenizer de meilleure qualité (plus de données,
  vocabulaire appris sur le domaine) réduirait la perte, sans nécessairement l'annuler.
- **L'empan utile** : à 128 jetons, le BPE voit ~2× plus d'octets que les octets ; le contexte
  natif de 130 octets vaut ~25–40 jetons BPE. La comparaison à **contexte égal** n'est pas faite
  ici — c'est la seule raison qui pourrait rouvrir la décision.

## Fichiers

- `reports/rapport-r13-tokenisation.md` — R13.0, la longueur et la réversibilité.
- `reports/rapport-r13.1-bpe.md`, `rapport-r13.1-campagne.md` — le pilote et le contrôle à
  octets égaux.
- `reports/rapport-r13.2-vocab1024.md`, `rapport-r13.3-anglais.md`, `rapport-r13.4-graines.md` —
  vocabulaire, langue, graines.
- `tools/r13_anglais.py` — le dispositif anglais (R13.3/R13.4).
- `docs/implantation/tokenisation.md` — la spécification et la décision.
