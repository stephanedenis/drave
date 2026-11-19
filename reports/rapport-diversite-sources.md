# La diversité du corpus : les sources ne se laissent pas moissonner (503 Gutenberg, Wikisource à transclusions)

> **Ligne de roadmap** : N (le palier 1) / D · **Date** : 2026-11-19 · **Verdict** : ⚠️ **bloqué par
> les sources** — les deux voies essayées ne rendent pas de texte exploitable sans un travail de
> moissonnage dédié : **Gutenberg répond 503** (blocage/limite), et **Wikisource FR** est joignable
> (l'API répond, catégories et révisions) mais ses pages sont des **portails à transclusions** :
> sur 40 membres de `Catégorie:Contes`, 6 pages seulement ne sont pas des homonymies, et elles
> pèsent **1 241 octets bruts** en tout (127 après nettoyage) — le texte est dans des sous-pages
> transcluses (`{{:…}}`), qu'un simple nettoyeur ne résout pas.
>
> **Dispositif** : `curl` (Gutenberg, Wikipédia, GitHub), l'API MediaWiki de `fr.wikisource.org`
> (`categorymembers`, `revisions`), `tools/collecter_wikisource.py` (écrit, non retenu) · mesure du
> 19/11 vers 10 h.

## Les mesures

| source | réponse | ce qui bloque |
|---|---|---|
| `gutenberg.org` | **503** | blocage/limite — aucune page rendue |
| `fr.wikipedia.org` | 301 (joignable) | — |
| `github.com` | 200 | — |
| `fr.wikisource.org` API | 200, mais **intermittente** (des lots reviennent vides) | limite de débit |
| `Catégorie:Romans` (20 pages) | 84 sous-pages, **0 gardée** ≥ 3 000 o | ce sont des portails/éditions sériées |
| `Catégorie:Contes` (40 pages) | 6 pages non-homonymes, **1 241 o bruts** | textes transclus (`{{:…}}`), non résolus |

## Ce que ça veut dire

La réserve locale de français hors Wikipédia reste ce que l'inventaire du 18/11 avait mesuré :
**≈ 0,1 Go** (littérature 15,3 Mo, `corpus_fr` 3,2 Mo, dépôt 4,8 Mo, ~72 Mo de FR dans les PDF).
Pour aller au-delà, il faut **un moissonneur dédié** :
- soit un **dump Wikisource** (l'export XML complet, plusieurs Go) + un résolveur de transclusions ;
- soit un **catalogue Gutenberg** (le miroir `gutenberg.org/cache` ou un miroir GitHub) avec un
  délai et un `User-Agent` conformes à leur politique ;
- soit des corpus de livres déjà constitués (licences à vérifier une par une).

Ce n'est pas une impasse technique : c'est un **chantier** (moissonnage + licences + nettoyage) qui
ne tient pas dans une session de mesure. Il est nommé, il attend.

## Ce qui n'a pas été fait

- **Aucun texte n'a été ajouté au corpus** : rien n'est promu, rien n'est épinglé.
- `tools/collecter_wikisource.py` (écrit, testé sur deux catégories) **n'est pas retenu** : il ne
  résout pas les transclusions. Il est committé comme **point de départ** (le résolveur de
transclusions est le travail suivant), et l'état le dit bloqué.

## Voir aussi

- [l'inventaire des données](rapport-donnees-inventaire.md) · [le corpus v2](rapport-corpus-v2.md) ·
  [le nettoyage](rapport-nettoyage-corpus.md) · [le plan natif](../docs/pilotage/natif-plan.md)
