# Session session- — Ajouter évaluer par langue et documenter

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-9d3b2074-c5f0-4f11-be10-31d317bac657` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 04:33 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 86 |
| Appels d'outils | 103 |
| Fichiers touchés | 6 |
| Commandes | 63 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J11.2 : ajouter `evaluer --par-langue` (le détail fr/en) et le documenter dans `docs/produit/README.md` ; test dans `tools/tests/test_produit.py` ; fiche `reports/rapport-evaluer-langue.md` + JSON, commit.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J11.2 : ajouter `evaluer --par-langue` (le détail fr/en) et le documenter dans `docs/produit/README.md` ; test dan … [91 caractères tronqués]

*103 appels d'outils.* Actions notables :

- bash — Show working dir and git status
- bash — List key directories
- bash — Find evaluer/produit files
- bash — Search evaluer in produit README
- bash — Find evaluer in drave.py
- bash — Read start of test_produit
- bash — Read evaluer implementation
- bash — Read CLI args of drave.py
- bash — Read evaluateur_gold.py part 1
- bash — Search langue in evaluateur_gold
- bash — Search J11.2 references
- bash — Read rest of evaluer_bloc
- bash — Read existing per-language report
- bash — Inspect plan.json structure
- … et 78 autres

**Synthèse produite :**

**J11.2 terminé et committé** — `09e54143`

\## Ce qui a été ajouté

- **`evaluer --par-langue`** dans [`tools/drave.py`](tools/drave.py) : rejoue la même mesure sur les sous-golds **fr** et **en**, en texte (`PAR LANGUE`) et en JSON (`par_langue`), avec un **contrôle négatif recalculé par langue**.
- **Documentation** dans [`docs/produit/README.md`](docs/produit/README.md) : § 3.3 (sortie actuelle + bloc par langue + lecture), § 7 (syntaxe et tableau des options), lien vers la fiche.
- **Tests** dans [`tools/tests/test_produit.py`](tools/tests/test_produit.py) : `TestParLangue` (JSON, texte, non-régression de la mesure globale, cohérence des comptes). **18 tests OK**.
- **Fiche + JSON** : [`reports/rapport-evaluer-langue.md`](reports/rapport-evaluer-langue.md), [`reports/evaluer-langue.json`](reports/evaluer-langue.json).
- **État/roadmap** : `en-cours` et `roadmap` à jour, J11.2 marqué, suite = J11.3–J11.4.

\## Les chiffres

| langue | phrases | tokens | POS | F1 | attachement | top-k |
|---|---:|---:|---:|---:|---:|---:|
| **fr** | 402 | 2 031 | **0,8159** | **0,7475** | **151/151** | 0,9868 |
| **en** | 210 | 1 148 | **0,9451** | **0,8656** | **87/88** (span 87/87) | 0,9886 |
| global | 612 | 3 179 | 0,8625 | **0,7902** | **238/239** | 0,9874 |

**Contrôle négatif** : cible exacte au hasard **1,99 %** (fr), **2,27 %** (en), **1,67 %** (tout), graine 0.

**Le point de méthode** : l'anglais est devant, mais son gold est **100 % réel** quand le français ajoute **160 synthétiques**. Sur le réel seul l'écart tient (POS 0,9451 contre 0,8408 ; F1 0,8656 contre 0,7258), donc il reste **confondu avec la source** — la fiche le dit explicitement.

\## Vérifications

- `python3 tools/drave.py evaluer --par-langue` → **PL-0**
- `python3 tools/tests/test_produit.py` → **OK**, 18 tests
- `bash tools/porte-produit.sh` → **verte**, 183/183 autotest
- Revue de documentation, tableaux, schémas, journal, budget T0 (3 994/4 000) → **verts**

Les modifications préexistantes hors périmètre (`reports/INDEX.md`, `tools/chantier/plan.json`, `tools/structures`, etc.) n'ont pas été touchées.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_produit.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-evaluer-langue.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 11 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Show working dir and git status
- **T1** List key directories
- **T1** Find evaluer/produit files
- **T1** Search evaluer in produit README
- **T1** Find evaluer in drave.py
- **T1** Read start of test_produit
- **T1** Read evaluer implementation
- **T1** Read CLI args of drave.py
- **T1** Read evaluateur_gold.py part 1
- **T1** Search langue in evaluateur_gold
- **T1** Search J11.2 references
- **T1** Read rest of evaluer_bloc
- **T1** Read existing per-language report
- **T1** Inspect plan.json structure
- **T1** Find J11.2 task in plan
- **T1** Read produit README beginning
- **T1** Read produit README evaluer section
- **T1** Search J11.2 in docs/plan/journal
- **T1** Search git history for J11
- **T1** Read roadmap and week plan around J11
- **T1** Read reports index
- **T1** Read rest of tests and product gate
- **T1** Language distribution of golds
- **T1** Read README sections 3.3-4
- **T1** Show J11.1 commit files
- **T1** Read J11.1 report style
- **T1** Read current state lines
- **T1** See J11.1 state/roadmap diff
- **T1** Run evaluer --par-langue
- **T1** Inspect per-language JSON metrics
- **T1** Measure per language and source
- **T1** Run product smoke tests
- **T1** Compile and test --gold per language
- **T1** Get current gold evaluation output
- **T1** Inspect doc review tool
- **T1** Print selected numbers for JSON
- **T1** Generate evaluer-langue JSON
- **T1** Generate evaluer-langue JSON fixed
- **T1** Compute combined real subset metrics
- **T1** Inspect task schema/status
- … et 23 autres

## 4. Mesures et résultats marquants

- **T1** `| **français** | 151 | **117** (77,5 %) | 113 | 114 | **0,9658** |`
- **T1** `| **anglais** | 88 | **28** (31,8 %) | 28 | 28 | **1,0000** |`
- **T1** `- **La couverture anglaise est le trou** : 28 labels sur 88 cibles (31,8 %) contre 77,5 % en`
- **T1** `| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |`
- **T1** `1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat`
- **T1** `aléatoire** dans les listes donne **42,14 %** de top-1 — et la **permutation des cibles**`
- **T1** `**1,997/220 = 0,908 %** ; les deux donnent p = 0. Un chiffre sans sa contre-épreuve n'est pas un`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)`
- **T1** `SYNTAGMES   F1 75.33 %  (P 72.39 % / R 78.53 %)`
- **T1** `tête      F1 86.40 %  (P 85.19 % / R 87.65 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.04 %  · attachement 93.31 % de couverture`
- **T1** `ATTACHEMENT exact 98.74 % · couverture 99.16 % · exact sur span 99.58 % · top-k 98.33 %`
- **T1** `tête      couverture 100.00 % · top-k 99.16 %`
- **T1** `PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %`
- **T1** `FRACTION SÉMANTIQUE 54.76 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)`
- **T1** `**Lecture.** `exact 98.33 %` est le **rendement** (235/239 cibles) ; `exact sur span 99.58 %` est`
- **T1** `le gold gelé 602 (F1 65,11 %, POS 85,32 %). La commande sort **0** : elle ne teste pas la cascade`
- **T1** `| **cache du chunker** | **×138,7** à 160 répétitions (9 817,7 → 70,8 ms) | banc de texte **répété**, chemin chunker |`
- **T1** `| **cache, chemin par défaut** | ×5,8 à 20 répétitions, puis **×1,0** à 80 et 160 | S domine le coût |`
- **T1** `| **cache, corpus réel** | **×1,2** | phrases réelles, 6,1 tokens/phrase |`
- **T1** `**Ce que le ×139 veut dire — et ne veut pas dire.** C'est la suppression du **O(n²)** du chunker`
- **T1** `réel, le gain est **×1,2** ; sur le chemin par défaut, **×1,0** à 80 et 160 répétitions. Annoncer`
- **T1** `« ×139 plus rapide » sans la condition serait faux. Ce que le cache garantit, c'est que les`
- **T1** `SYNTAGMES   F1 58.93 %  (P 63.19 % / R 55.22 %)`
- **T1** `tête      F1 73.92 %  (P 81.36 % / R 67.72 %)`
- **T1** `| **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `| [rapport-a83d-lot-threads.md](rapport-a83d-lot-threads.md) | A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread |`
- **T1** `| [rapport-autotest-parallele.md](rapport-autotest-parallele.md) | B13 — la vérification parallèle : 183/183 en 1 min 54 (×2,4) |`
- **T1** `| [rapport-speculatif-reflexe.md](rapport-speculatif-reflexe.md) | Le réflexe propose, le cerveau vérifie — acceptation 2 à 30 % (le cerveau non entraîné : 0 %) |`
- **T1** `| [rapport-vitesse-v41.md](rapport-vitesse-v41.md) | Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé |`
- **T1** `fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%`
- **T1** `mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `sont inchangés ; les **2 unités** et **61,5 %** du texte aussi.`
- **T1** `segments du groupe 0 portent `meta.partition` (`membres: 3` ; rang 1 = REL longue, rang 2 = GV,`
- **T1** `rang 3 = REL courte) et `meta.alternative` avec les deux autres. La doc le dit maintenant au § 2.`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../r`
- **T1** `+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../r`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p`
- **T1** `SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)`
- **T1** `tête      F1 90.29 %  (P 92.61 % / R 88.08 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture`
- **T1** `ATTACHEMENT exact 99.58 % · couverture 99.58 % · exact sur span 100.00 % · top-k 98.74 %`
- **T1** `POS 94.51 % (fermé 98.30 %, ouvert 90.54 %) · SYNTAGMES F1 86.56 % (tête 95.27 %)`
- **T1** `ATTACHEMENT exact 98.86 % · couverture 98.86 % · top-k 98.86 % · PRAGMATIQUE acte 99.52 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 2.27 % (graine 0, 88 cibles)`
- **T1** `POS 81.59 % (fermé 90.92 %, ouvert 73.25 %) · SYNTAGMES F1 74.75 % (tête 87.33 %)`
- **T1** `ATTACHEMENT exact 100.00 % · couverture 100.00 % · top-k 98.68 % · PRAGMATIQUE acte 99.75 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.99 % (graine 0, 151 cibles)`
- **T1** `POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.14 %)`
- **T1** `SYNTAGMES   F1 78.82 %  (P 78.18 % / R 79.46 %)`
- **T1** `tête      F1 90.25 %  (P 92.34 % / R 88.26 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.27 %  · attachement 92.05 % de couverture`
- **T1** `ATTACHEMENT exact 97.91 % · couverture 97.91 % · exact sur span 100.00 % · top-k 97.07 %`
- **T1** `tête      couverture 100.00 % · top-k 99.15 %`
- **T1** `PRAGMATIQUE acte 99.67 % · négation 97.67 % · modalité 98.84 % · double sens 94.35 %`
- **T1** `FRACTION SÉMANTIQUE 54.96 %`
- **T1** `**521/532** étiquetées Glottolog), le top-1 de voisinage est de la même famille **66,1 %** (hasard`
- **T1** `10,3 %) et de la même branche **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout est au hasard**`
- **T1** `(famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %) ; dans la même écriture, la famille monte à`
- **T1** `**69,8 %** et la sœur à **27,8 %**. Le retrieval parallèle 30 articles le chiffre : sur les **25`
- **T1** `[still running after 60000ms; moved to background job bash-59]`

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : /home/stephane/Data13TB/stephane/GitHub/Qtrinet MM journal/2026-11-14/README.md MM journal/2026-11-14/docs.md MM journal/2026-11-14/memoire.md MM journal/2026-11-14/mesures.md MM journal/2026-11-14/po
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 32, in <module>   File "<stdin>", line 22, in resume KeyError: 'controle_negatif' [exit code: 1]
- **T1** : total 24 drwxr-xr-x. 1 stephane stephane   90 14 nov 01:58 . drwxr-xr-x. 1 stephane stephane  972 14 nov 00:51 .. -rw-r--r--. 1 stephane stephane 3205 14 nov 04:31 docs.md -rw-r--r--. 1 stephane steph
- **T1** : diff --git a/journal/2026-11-14/README.md b/journal/2026-11-14/README.md index a5012ccd..4d99d6bb 100644 --- a/journal/2026-11-14/README.md +++ b/journal/2026-11-14/README.md @@ -5,22 +5,22 @@  > le b
- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r

## 6. Commits

- J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ" -m "evaluer --par-langue rejoue la même mesure sur les deu

