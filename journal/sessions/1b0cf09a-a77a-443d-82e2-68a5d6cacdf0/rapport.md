# Session 1b0cf09a — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `1b0cf09a-a77a-443d-82e2-68a5d6cacdf0` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:22 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 99 |
| Appels d'outils | 100 |
| Fichiers touchés | 4 |
| Commandes | 77 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **valider le cache du chunker** proposé par la fiche `reports/rapport-cout-chunker.md` (O(n²) confirmé, cache ×11,6 à 160 tokens) — sans modifier le code du dépôt.  Contexte : `tools/bloc_linguistique.py`, classe `Heuristique` : `analyser` appelle `self._syntagmes_simple(texte, lg)` à l'in … [1794 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **valider  … [2074 caractères tronqués]

*100 appels d'outils.* Actions notables :

- bash — Check repo status and branch
- bash — List reports and file sizes
- read
- bash — Hash and diff of the linguistic block
- bash — Locate key functions in the source
- bash — Read top of linguistic block
- bash — Read rest of analyser and next classes
- bash — Read Heuristique class init
- bash — Inspect gold evaluation corpus loader
- bash — Load 612-sentence corpus and stats
- bash — Inspect pensee JSON schema
- bash — Top-level structure of pensee file
- bash — Inspect key sections of pensee JSON
- bash — Inspect default-path long points
- … et 73 autres

**Synthèse produite :**

✅ **Cache validé.** Deux fichiers neufs, non committés, aucun fichier existant modifié :

- [`reports/rapport-cache-chunker.md`](reports/rapport-cache-chunker.md) — protocole, temps, complexité, égalité, contrôles négatifs, limites, diff complet.
- [`reports/pensee-cache-chunker.json`](reports/pensee-cache-chunker.json) — données structurées.

\## Facteur de gain (mesures sur `6e8430…`, snapshot de la fiche)

| mesure | résultat |
|---|---|
| cache complet C2 (chunking + verbes), chunker, 160 tokens | **×11,0** (9 passes), **×12,2** (15 passes) — fiche ×11,6, confirmé à ±10 % |
| idem, 320 tokens | **×18,1-19,5** (fiche ×16,9) |
| idem, 640-1 280 tokens | **×29-37** |
| défaut S, 160 / 320 tokens | **×2,06** / **×2,61-2,83** |
| corpus 612 phrases | **×1,25** chunker, **×1,03** défaut |
| mémoïsation seule C1 (`_syntagmes_simple`) | ×5,1 à 160, ×6,9 à 320 ; défaut ×1,02-1,07 |

**Nuance importante :** le ×11,6 n'est pas obtenu par la seule mémoïsation du chunker (×5,1). Il faut aussi le cache des verbes de GV (C2) ; sur le défaut, c'est même lui qui porte tout le gain, le 2→1 chunking ne valant que 2-4 %.

\## Égalité : **OUI**

- C1, C2 et OFF : **612/612** sur les deux chemins (chunker seul et défaut S).
- **42/42** sur 7 longueurs × 2 chemins.
- Patch hoisté réel : **612/612 + 14/14**, **1 seul chunking** par analyse.
- Comparateur sensible : cache falsifié détecté (113/612 chunker, 290/612 défaut) ; cache bien recréé à chaque `analyser`.

\## Correctif exact à appliquer (contre `6e8430…`)

Hoister `simples`/`gvs_simple`/`cache_gv` après le calcul de `verbes` (après 855), supprimer les re-chunkings **861, 919, 928**, remplacer **914** par `for s in simples`, utiliser `gvs_simple` en **916/922**, poser `gvs_u = gvs_s + gvs_simple` (**929-930**), passer `cache_gv` en **887/895/899/935/940**, ajouter `_verbe_gv` après **658**, ajouter `cache_gv=None` aux signatures **662/689**, remplacer `_verbe_dans` par `_verbe_gv` en **681/685/701**. Le diff complet est au § 8.2 ; il s'applique proprement (fichier patché sha256 `5639a376…`).

⚠️ Le fichier committé dans HEAD (`5640809e`) est un patch **partiel** : le chemin défaut garde deux chunkings (lignes 875 et 947). L'arbre courant a encore bougé depuis (`64b7c520…`) : relire la note d'état § 2.1/§ 8.3 avant d'appliquer. **Rien n'a été committé.**

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/bench_cache_chunker.py` | 1 | 0 |
| `/tmp/gen_pensee.py` | 1 | 0 |
| `/tmp/rapport_body.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cache-chunker.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Check repo status and branch
- **T1** List reports and file sizes
- **T1** Hash and diff of the linguistic block
- **T1** Locate key functions in the source
- **T1** Read top of linguistic block
- **T1** Read rest of analyser and next classes
- **T1** Read Heuristique class init
- **T1** Inspect gold evaluation corpus loader
- **T1** Load 612-sentence corpus and stats
- **T1** Inspect pensee JSON schema
- **T1** Top-level structure of pensee file
- **T1** Inspect key sections of pensee JSON
- **T1** Inspect default-path long points
- **T1** Environment and CPU information
- **T1** Read gold evaluation attachment logic
- **T1** Smoke-test cache equality on 30 sentences
- **T1** Re-check current source around analyser
- **T1** Inspect concurrent modification and HEAD snapshot hash
- **T1** Check RACINE usage and generator path deps
- **T1** Read remainder of concurrent patch
- **T1** Freeze HEAD snapshot of the block
- **T1** Check new commit and file state
- **T1** Switch bench to frozen HEAD snapshot
- **T1** Smoke-test equality against frozen snapshot
- **T1** Run full cache validation benchmark
- **T1** Check target files do not exist
- **T1** Read existing fiche limits for context
- **T1** Check benchmark progress and load
- **T1** Read benchmark summary output
- **T1** Inspect long-text and complexity results
- **T1** Generate and inspect exact patch on /tmp copy
- **T1** Locate duplicate return statement
- **T1** Inspect all GV verb calls
- **T1** Fix patch anchor and regenerate diff
- **T1** Write OFF re-measure and real patch benchmark
- **T1** Fix fabric and equality loop bugs
- **T1** Run OFF re-measure and real patch benchmark
- **T1** Read patch benchmark error
- **T1** Fix lambda keyword and rerun patch benchmark
- **T1** Generate markdown tables from benchmark JSON
- … et 37 autres

## 4. Mesures et résultats marquants

- **T1** `"V1": "_syntagmes_simple m\u00e9mo\u00efs\u00e9 par (texte, langue) dans une sous-classe locale",`
- **T1** `"textes_longs_20_320": "V1, V2 et OFF identiques à l’original sur les 5 longueurs × 2 chemins"`
- **T1** `"Base synthétique A (« est sur le toit ») : le GV a pour tête l'auxiliaire « est » ; _cible_proche le saute et scanne tous les GV. C'est un cas défavorable réel (copules), mais il amplifie le coût. Av`
- **T1** `"Corpus court : 6,13 tokens _mots/phrase, 1,10 segment, 0,19 GV. Le gain corpus est faible (×1,18-1,22 chunker, ×0,97-1,07 défaut) ; le O(n²) ne mord pas sur le gold actuel.",`
- **T1** `"Bruit de mesure : Xeon partagé, temps CPU, 3-11 passes ; l'OFF varie de ×0,90 à ×1,13 selon le point (médiane ×1,00). Les facteurs à ±10 % près.",`
- **T1** `| original | 245.3 | ×1.000 | 400.8 | 395.2 | ×1.000 | 645.8 |`
- **T1** `| C1 | 198.0 | ×1.239 | 323.6 | 388.3 | ×1.018 | 634.5 |`
- **T1** `| C2 | 196.1 | ×1.251 | 320.4 | 385.1 | ×1.026 | 629.2 |`
- **T1** `| OFF | 275.6 | ×0.890 | 450.4 | 398.4 | ×0.992 | 650.9 |`
- **T1** `| 20 | 6 | 2 | 1.64 | 0.88 | 0.71 | 1.67 | ×1.88 | ×2.32 | ×0.98 |`
- **T1** `| 40 | 12 | 4 | 4.97 | 2.38 | 1.40 | 4.99 | ×2.09 | ×3.55 | ×1.00 |`
- **T1** `| 80 | 24 | 8 | 16.19 | 4.26 | 2.50 | 16.44 | ×3.80 | ×6.46 | ×0.99 |`
- **T1** `| 160 | 48 | 16 | 57.74 | 11.27 | 5.25 | 62.02 | ×5.12 | ×11.00 | ×0.93 |`
- **T1** `| 320 | 96 | 32 | 233.47 | 33.80 | 12.00 | 241.33 | ×6.91 | ×19.46 | ×0.97 |`
- **T1** `| 640 | 192 | 64 | 925.09 | 119.60 | 31.70 | 919.54 | ×7.74 | ×29.18 | ×1.01 |`
- **T1** `| 1280 | 384 | 128 | 3740.44 | 426.46 | 100.93 | 3657.45 | ×8.77 | ×37.06 | ×1.02 |`
- **T1** `| 20 | 6 | 2 | 2.02 | 1.95 | 1.60 | 2.03 | ×1.03 | ×1.26 | ×0.99 |`
- **T1** `| 40 | 12 | 4 | 4.04 | 3.90 | 2.92 | 4.10 | ×1.04 | ×1.39 | ×0.99 |`
- **T1** `| 80 | 24 | 8 | 14.88 | 12.54 | 6.03 | 14.09 | ×1.19 | ×2.47 | ×1.06 |`
- **T1** `| 160 | 48 | 16 | 27.88 | 27.27 | 13.55 | 30.76 | ×1.02 | ×2.06 | ×0.91 |`
- **T1** `| 320 | 96 | 32 | 91.33 | 89.07 | 35.04 | 90.22 | ×1.03 | ×2.61 | ×1.01 |`
- **T1** `| 640 | 192 | 64 | 344.96 | 321.58 | 103.40 | 317.65 | ×1.07 | ×3.34 | ×1.09 |`
- **T1** `| 1280 | 384 | 128 | 1161.80 | 1164.81 | 318.29 | 1188.64 | ×1.00 | ×3.65 | ×0.98 |`
- **T1** `| original | 245,3 | ×1,000 | 400,8 | 395,2 | ×1,000 | 645,8 |`
- **T1** `| C1 (chunking seul) | 198,0 | ×1,239 | 323,6 | 388,3 | ×1,018 | 634,5 |`
- **T1** `| C2 (chunking + verbes) | 196,1 | ×1,251 | 320,4 | 385,1 | ×1,026 | 629,2 |`
- **T1** `| OFF (caches off) | 275,6 | ×0,890 | 450,4 | 398,4 | ×0,992 | 650,9 |`
- **T1** `| 20 | 6 | 2 | 1,64 | 0,88 | 0,71 | 1,67 | ×1,88 | ×2,32 | ×0,98 |`
- **T1** `| 40 | 12 | 4 | 4,97 | 2,38 | 1,40 | 4,99 | ×2,09 | ×3,55 | ×1,00 |`
- **T1** `| 80 | 24 | 8 | 16,19 | 4,26 | 2,50 | 16,44 | ×3,80 | ×6,46 | ×0,99 |`
- **T1** `| 160 | 48 | 16 | 57,74 | 11,27 | 5,25 | 62,02 | ×5,12 | ×11,00 | ×0,93 |`
- **T1** `| 320 | 96 | 32 | 233,47 | 33,80 | 12,00 | 241,33 | ×6,91 | ×19,46 | ×0,97 |`
- **T1** `| 640 | 192 | 64 | 925,09 | 119,60 | 31,70 | 919,54 | ×7,74 | ×29,18 | ×1,01 |`
- **T1** `| 1280 | 384 | 128 | 3740,44 | 426,46 | 100,93 | 3657,45 | ×8,77 | ×37,06 | ×1,02 |`
- **T1** `| 20 | 6 | 2 | 2,02 | 1,95 | 1,60 | 2,03 | ×1,03 | ×1,26 | ×0,99 |`
- **T1** `| 40 | 12 | 4 | 4,04 | 3,90 | 2,92 | 4,10 | ×1,04 | ×1,39 | ×0,99 |`
- **T1** `| 80 | 24 | 8 | 14,88 | 12,54 | 6,03 | 14,09 | ×1,19 | ×2,47 | ×1,06 |`
- **T1** `| 160 | 48 | 16 | 27,88 | 27,27 | 13,55 | 30,76 | ×1,02 | ×2,06 | ×0,91 |`
- **T1** `| 320 | 96 | 32 | 91,33 | 89,07 | 35,04 | 90,22 | ×1,03 | ×2,61 | ×1,01 |`
- **T1** `| 640 | 192 | 64 | 344,96 | 321,58 | 103,40 | 317,65 | ×1,07 | ×3,34 | ×1,09 |`
- **T1** `| 1280 | 384 | 128 | 1161,80 | 1164,81 | 318,29 | 1188,64 | ×1,00 | ×3,65 | ×0,98 |`
- **T1** `| chunker 160 | 68,31 | 13,04 | 5,61 | 65,38 | ×5,24 | ×12,17 | ×1,04 |`
- **T1** `| chunker 320 | 251,12 | 37,95 | 13,85 | 254,06 | ×6,62 | ×18,13 | ×0,99 |`
- **T1** `| défaut 80 | 10,59 | 10,36 | 6,39 | 10,79 | ×1,02 | ×1,66 | ×0,98 |`
- **T1** `| défaut 160 | 32,96 | 31,80 | 17,27 | 32,90 | ×1,04 | ×1,91 | ×1,00 |`
- **T1** `| défaut 320 | 98,61 | 98,37 | 34,82 | 101,26 | ×1,00 | ×2,83 | ×0,97 |`
- **T1** `| chunker 20 | 2,33 | 0,89 | ×2,61 | 1/1 |`
- **T1** `| défaut 20 | 2,04 | 1,59 | ×1,28 | 1/1 |`
- **T1** `| chunker 40 | 4,94 | 1,22 | ×4,04 | 1/1 |`
- **T1** `| défaut 40 | 4,27 | 2,93 | ×1,46 | 1/1 |`
- **T1** `| chunker 80 | 16,17 | 2,35 | ×6,89 | 1/1 |`
- **T1** `| défaut 80 | 10,02 | 6,03 | ×1,66 | 1/1 |`
- **T1** `| chunker 160 | 66,25 | 5,15 | ×12,86 | 1/1 |`
- **T1** `| défaut 160 | 28,01 | 13,45 | ×2,08 | 1/1 |`
- **T1** `| chunker 320 | 266,21 | 13,18 | ×20,19 | 1/1 |`
- **T1** `| défaut 320 | 93,05 | 37,12 | ×2,51 | 1/1 |`
- **T1** `| chunker 640 | 964,39 | 41,40 | ×23,30 | 1/1 |`
- **T1** `| défaut 640 | 339,03 | 102,59 | ×3,30 | 1/1 |`
- **T1** `| chunker 1280 | 3809,82 | 86,19 | ×44,20 | 1/1 |`
- **T1** `| défaut 1280 | 1118,99 | 313,06 | ×3,57 | 1/1 |`
- **T1** `verdict: Cache VALIDÉ. Le O(n²) du chemin chunker est confirmé : 1+2·S appels à _syntagmes_simple (97/193/769 à 160/320/1 280 tokens), pente log-log 1,71-2,00, doublement 160→320 ×3,68 (re-mesure 15 p`
- **T1** `# Cache du chunker — validation indépendante : ×11,0 à 160 tokens, égalité 612/612`
- **T1** `> pente 1,71-2,00). La mémoïsation seule de `_syntagmes_simple` donne **×1,24 sur le corpus et`
- **T1** `> ×5,1/×6,9 à 160/320** ; le cache complet de la fiche (chunking + verbes de GV) donne **×11,0 à`
- **T1** `> 160** (re-mesure ×12,2 ; fiche ×11,6), **×18,1-19,5 à 320**, et **×2,06/×2,61** sur le défaut.`
- **T1** `> Égalité stricte : **612/612** sur les deux chemins et **42/42** sur 7 longueurs × 2 chemins ;`
- **T1** `> La fiche ×11,6 est confirmée à ±10 % près ; le cache ne linéarise pas (pente 1,42-1,52).`
- **T1** `que la mémoïsation de `_syntagmes_simple`, le défaut reste à ×1,02-1,07.`
- **T1** `- **OFF vs original, corpus chunker** : 275,6 ms contre 245,3 ms dans la série 9 passes (×0,89),`
- **T1** `mais **236,5 ms contre 229,7 ms** dans la re-mesure 11 passes (×0,97) ; l'écart de la première`
- **T1** `série est un épisode de charge. Le résidu +3-5 % est le surcoût des frames Python de la`
- **T1** `- **OFF vs original, longueurs** : ratios ×0,91 à ×1,09 (chunker et défaut), médiane proche de`
- **T1** `1,00. OFF ne montre **jamais** le gain de C2 (×2,3 à ×37 selon le point).`
- **T1** `cache des verbes en porte l'essentiel), mais le 2→1 manque : environ 2-4 % sur le défaut, pas de`
- **T1** `quoi changer le ×2. À appliquer sur `6e8430…` ou à fusionner avec ce patch partiel.`
- **T1** `coût et le gain défaut. Avec la base B à verbe plein, la fiche mesure ×1,07-1,13 : ne pas lire`
- **T1** `×2,0 comme universel.`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : False C1 egal True n_etq 18 [stderr] Traceback (most recent call last):   File "<stdin>", line 9, in <module>   File "/tmp/bench_cache_chunker.py", line 84, in analyser     return super().analyser(tex
- **T1** : diff exit=1 [stderr] Traceback (most recent call last):   File "/tmp/appliquer_correctif.py", line 93, in <module>     rem('return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)',     ~~
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 104, in <module> KeyError: 'sensibilite' [exit code: 1]
- **T1** : pipes échappés: 0 tableaux: 9 tous cohérents [stderr] Traceback (most recent call last):   File "<stdin>", line 23, in <module>   File "<stdin>", line 18, in num ValueError: could not convert string t

