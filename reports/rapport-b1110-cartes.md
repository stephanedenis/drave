# B11.10 — Cartes et ambiguïtés : le codec lit, le dispatcher devinait

> **Ligne de roadmap** : B11.10 · **Date** : 2026-10-29 · **Verdict** : ✅ **mesurée** — le codec lit
> **161/161** cartes ; les coordonnées nues sont désormais **refusées** avec leurs jeux candidats, au lieu
> d'être devinées. Le **69,3 %** souvent cité est le champ `carte` du **parseur natif**, pas le codec.
>
> **Dispositif** : `tools/jeux/codecs/base.py` (garde d'ambiguïté), `tools/jeux/tests/test_codecs.py`
> (27 tests), corpus B5/B7 ; données [`b1110-cartes.json`](b1110-cartes.json).

## La question

Le codec lit-il les cartes, et que fait-il d'une surface qui peut appartenir à plusieurs jeux
(`A1`, `E4`, `d4`, `b6-c5`) ? La fiche B11.10 attendait une extension du codec aux cartes, sur la
base d'un **69,3 %** — chiffre qui vient du champ natif, pas de la couche classique.

## Le dispositif

- **161 items de cartes** du corpus typé ; 8 portent un **contexte RSN** complet, 153 sont lus sans
  contexte (le codec rend alors une carte, avec l'ambiguïté « position requise pour valider »).
- **4 surfaces ambiguës** : `A1` (morpion/échecs/dames/go), `E4` et `d4` (échecs/go), `b6-c5`
  (échecs/dames).
- **Avant** : `lit(surface)` sans jeu laissait le dispatcher choisir le codec le plus confiant.
- **Après** : une coordonnée nue, ou deux cases séparées par un tiret, est **refusée** quand ni le
  jeu ni le contexte ne sont donnés ; l'erreur nomme les jeux candidats. Avec un jeu explicite, le
  codec lit comme avant.
- **Contrôles** : `e2e4` (coup d'échecs, sans tiret) et `2D` (carte) ne sont pas touchés ; la porte
  des jeux complète le dispositif.

## Ce qui est mesuré

| mesure | avant | après |
|---|---:|---:|
| codec cartes, code exact | **161 / 161** | **161 / 161** |
| `A1` sans jeu | morpion, case 0 | **refus** (4 jeux) |
| `E4` sans jeu | go, point 289 | **refus** (4 jeux) |
| `d4` sans jeu | go, point 288 | **refus** (4 jeux) |
| `b6-c5` sans jeu | dames, chemin `[8, 13]` | **refus** (2 jeux) |
| avec le jeu explicite | — | **4 / 4 routées, 4 / 4 lues** (`E4` = requête de case) |
| `e2e4` | échecs | échecs |
| `2D` | cartes | cartes |

**Lecture.** Le codec n'a **pas** de trou sur les cartes : il lit les 161 items. Le trou était dans
le **dispatcher** : sans jeu, `E4` et `d4` étaient lus comme des points de go, `A1` comme une case
de morpion, `b6-c5` comme un chemin de dames — sans nommer les autres candidats. C'est exactement
la collision que la porte B11.10 demandait de contrôler.

## Les contrôles négatifs

- **Sans jeu** : les quatre surfaces sont refusées, avec `ok = False` et les jeux candidats dans
  `ambiguites` ; aucune ne produit de RSN.
- **Avec jeu** : `A1` → morpion, `E4` → échecs (requête case 36), `d4` → go, `b6-c5` → dames ; **4/4 routées et lues**.
- **Surfaces non ambiguës** : `e2e4` reste un coup d'échecs, `2D` une carte ; le garde ne les touche pas.
- **Porte des jeux** : `exit 0` ; **100 %** au niveau 4, **33/33** paires invariantes, **0 collision**,
  71 langues et les maîtres mesurés.
- **27 tests** de codecs passent, dont les trois nouveaux tests d'ambiguïté.

## Ce qui pourrait le rendre faux

- **161 items synthétiques**, **4 surfaces** choisies : le corpus ne prouve pas que toutes les
  coordonnées du monde réel sont couvertes.
- **8 contextes RSN** seulement : les 153 autres cartes sont lues **sans validation** ; le codec
  peut être exact sur la carte et muet sur la position.
- **Pas de nouvelle mesure du natif** : le **69,3 %** est repris de B11.7 ; il n'est pas reproduit ici.
- **Garde par motif** : une coordonnée nue ou `a1-b2` est refusée ; une surface avec un nom de jeu
  (`E4 au go`) ou un contexte RSN passe par la détection normale. Le garde pourrait refuser une
  notation légitime sans jeu — c'est le prix de l'explicite.
- **Le dispatcher n'est pas un juge sémantique** : il nomme les jeux candidats, il ne dit pas lequel
  est le bon.

## Ce que ça change

**B11.10 est mesurée — et corrige sa prémisse.** Le codec lit les cartes à **100 %** ; le **69,3 %**
est le champ `carte` du **parseur natif** (B11.7). Il n'y a donc **pas** d'extension du codec à
faire pour les cartes. Ce qui reste est le **champ natif** : une tête `carte` entraînée, ou une
route hybride qui envoie les cartes au bloc classique. Les ambiguïtés, elles, sont maintenant
**refusées explicitement** ; le dispatcher ne devine plus.

## Fichiers

- `tools/jeux/codecs/base.py` — garde `_ambiguite_de_surface` et refus dans `lit` sans jeu.
- `tools/jeux/tests/test_codecs.py` — `TestAmbiguites` (3 tests).
- `reports/b1110-cartes.json` — les mesures.
- `reports/rapport-b1110-cartes.md` — cette fiche.
