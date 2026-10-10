> Campagne : **toutes-langues** · expérience **01**
> Titre : 1. Le périmètre, inventorié
> Date réelle : **2026-10-05 23:50 HAE** (source : commit `1424c5d`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 1. Le périmètre, inventorié

| corpus | contenu | parallèle ? |
|---|---|---|
| **UDHR** | **392 langues × 10 unités** | **oui**, aligné |
| Wikipedia | 81 Go, 6 langues, 65 589 fichiers de 150 articles | **non** |
| Gutenberg | 40 œuvres, 6,6 M mots | **3 paires** : Dostoïevski en/es, Dumas en/fr, Shakespeare en/fr |

**Wikipedia n'est pas parallèle, et c'est vérifié** : sur 400 articles par langue
dans six langues, **aucun titre commun** — les dumps sont triés par titre et chaque
langue commence ailleurs. L'alignement par titre ne donnerait qu'une poignée de
noms propres. D'où la division assumée :

- **richesse** (fidélité, transfert) → UDHR complet, Romeo, Wikipedia ;
- **invariance** (contenu apparié) → UDHR, Romeo.

---
