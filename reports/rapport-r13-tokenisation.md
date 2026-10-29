# R13.0 — BPE : 3,4 à 5,2 octets par jeton, réversible ; la PPL reste à mesurer

> **Ligne de roadmap** : R1.3 / R13 · **Date** : 2026-10-29 · **Verdict** : 🔬 **pré-mesure** —
> le BPE réduit la longueur de **3,4 à 5,2×** sur le latin et reste **réversible** ; le contrôle
> aléatoire tombe à **1,63 octet/jeton**. La **PPL à budget égal** n’est pas mesurée : R13 reste
> **ouverte**.
>
> **Dispositif** : tokenizer Qwen2.5-0.5B (BPE byte-level, 151 936 jetons), `--tokenize` du moteur ;
> échantillons de 200 lignes (anglais, français, multilingue, arabe, cyrillique, CJK) et un
> contrôle aléatoire ; données [`r13-tokenisation.json`](r13-tokenisation.json).

## Ce qui est mesuré

| échantillon | octets | jetons BPE | octets/jeton | jetons/mot | réversible |
|---|---:|---:|---:|---:|---|
| anglais | 47 214 | 9 146 | **5,16** | 1,34 | ✅ |
| français | 14 304 | 4 250 | **3,37** | 1,77 | ✅ |
| multilingue | 12 632 | 3 444 | **3,67** | 1,76 | ✅ |
| arabe | 12 575 | 4 444 | **2,83** | 4,03 | ✅ |
| cyrillique | 16 809 | 6 038 | **2,78** | 5,80 | ✅ |
| CJK | 6 445 | 1 402 | **4,60** | — | ✅ |
| **aléatoire** | 16 804 | 10 321 | **1,63** | 51,6 | ✅ |

- Les octets sont le **plancher** : 1 jeton par octet. Le BPE divise la séquence par **3,4–5,2**
  sur le latin, **2,8** sur l’arabe/cyrillique, **4,6** sur le CJK (3 octets par caractère).
- Le contrôle aléatoire à **1,63** montre que le gain est **linguistique**, pas mécanique : un texte
  sans régularité ne se compresse presque pas.
- La réversibilité est **exacte** sur les sept échantillons (le moteur reconstruit le texte).
- Pour le CJK, `jetons/mot` n’a pas de sens (pas d’espaces) ; seul `octets/jeton` compte.

## Les contrôles négatifs

- **Octets** : 1 jeton/octet, la référence basse.
- **Aléatoire** : 1,63 octet/jeton, contre 3,3–5,2 sur le naturel : la compression chute.
- **Réversibilité** : `--tokenize` reconstruit le texte identique ; un tokenizer qui perd des
  octets serait disqualifié avant la PPL.
- **Scripts non latins** : le BPE garde un gain, mais plus faible (2,8–4,6) ; une décision
  « latin seulement » serait fausse.

## Ce que ça ne dit pas

- **Pas de PPL** : le modèle natif est en octets ; le tokenizer Qwen est un autre modèle. Comparer
  les PPL des deux ne mesurerait pas la tokenisation, mais deux modèles.
- **Pas de coût complet** : le vocabulaire BPE fait **151 936** entrées contre **256** octets ;
  l’embedding, la mémoire et le temps par pas ne sont pas chiffrés ici.
- **Pas d’empan utile** : 130 octets de contexte natif valent ~25–40 jetons BPE selon la langue ;
  l’effet sur l’aiguille native n’est pas mesuré.
- **Échantillons** : 200 lignes par langue, un seul tokenizer.

## Ce que ça change

La **longueur** n’est plus une intuition : le BPE divise la séquence par 3–5 sur le latin, 2,8 sur
l’arabe/cyrillique. Mais R13 est une décision de **qualité à budget égal** : il faut un **modèle
natif BPE** (ou un student BPE) et une PPL/bits-par-octet, pas seulement un comptage de jetons.
R13 reste **ouverte** ; la pré-mesure est faite.

## Fichiers

- `reports/r13-tokenisation.json` — les mesures.
- `reports/rapport-r13-tokenisation.md` — cette fiche.
