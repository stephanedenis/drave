# Thèmes du journal

> Généré par `tools/journal_auto.py` — c'est la **règle de classement** des fichiers
> `journal/AAAA-MM-JJ_<thème>.md`. Un commit (ou une étape de session) est classé par
> le **premier** thème dont un mot-clé apparaît dans son texte ; à défaut, par les
> **chemins** touchés ; à défaut, en `divers`. Pour changer le classement, éditer la
> table `THEMES` du script et relancer : rien d'autre n'est à toucher.

| thème | ce qu'il couvre | mots-clés | chemins |
|---|---|---|---|
| `attention` | Attention, fenêtre, puits | attention, fenêtre, fenetre, puits, sinks, attn-, softmax, swa |  |
| `memoire` | Mémoire épisodique, consolidation, greffe | mémoire, memoire, épisodique, episodique, greffe, consolid, rappel, indice, magasin, c6, c7, clé, cle | episodique.rs |
| `apprentissage` | Règles locales, hebbien, modulateurs, distillation | hebb, décorrélation, decorrelation, modulateur, nouveauté, nouveaute, règle locale, regle locale, apprentissage, distill, impulsion, décharge, decharge, spiking, log-normal, élagage appris, k-wta appris |  |
| `distribue` | Régions, flux, protocoles, budgets, pannes | topologie, région, region, nœud, noeud, flux, bus, latence, budget, panne, registre, trace, protocole, v7, v8, paires, message, gigue, réparti, reparti, relais, découpage, decoupage, lien | topologie.rs, trace_globale.rs, bus.rs, flux.rs |
| `modele` | Modèles, entraînement, parcimonie, biologie | modèle, modele, entraîn, entrain, parcimonie, poids, échelle, echelle, biolog, e1, e2, e3, e4, e5, e6, e7, e8, e9 | entrainer_moteur.py, biologie |
| `moteur` | Moteur : chargement, calcul, listes, quantification | moteur, gguf, listes, quantif, noyau, gpu, threads, mmap, lots, profil, débit, debit | gguf.rs, model.rs, main.rs |
| `mesures` | Campagnes et mesures | campagne, mesure, perplexité, perplexite, carte, banc, benchmark, aiguille | reports/ |
| `portes` | Portes et vérifications | porte, portes, vérification, verification, tests, gate | tools/porte-, toutes-les-portes |
| `docs` | Documentation, état, conventions | document, doc, readme, glossaire, rangement, convention, état, etat, journal, organisation, manques | docs/, README.md |
| `outils` | Outils et harnais | outil, script, harnais, hook, générateur, generateur | tools/ |
| `divers` | Ce qui ne rentre dans aucun thème | — | — |

## L'évolution, thème par thème

Chaque thème liste ses journées, dans l'ordre, avec les chiffres que la journée a
produits : c'est la vue « d'un jour à l'autre » que les noms `jour_thème` rendent
possible (`ls journal/*_<thème>.md`).

### `attention` — Attention, fenêtre, puits

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_attention.md) | `× 128` |
| [2026-10-10](2026-10-10_attention.md) | `512 jetons` · `+12 %` · `+0,33 %` · `+40 %` · `+2,0 %` · `−6,7 %` · `−1,4 %` · `256 jetons` · `÷2,67` · `2048 jetons` · `10,4046` · `10,3703` |
| [2026-10-11](2026-10-11_attention.md) | `5,8 %` |
| [2026-10-13](2026-10-13_attention.md) | — |

### `memoire` — Mémoire épisodique, consolidation, greffe

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_memoire.md) | `15 %` · `83 %` · `96 %` · `81 %` · `85 %` · `22 %` · `87 %` · `50 %` · `2 jetons` · `0,5 %` · `2048 jetons` · `11 jetons` |
| [2026-10-10](2026-10-10_memoire.md) | `31 %` · `1,000` · `0,913` · `1006 jetons` · `136 jetons` · `50 jetons` · `+12 %` · `÷4` · `0,906` · `0,112` |
| [2026-10-11](2026-10-11_memoire.md) | `15 s` · `4 Go` |
| [2026-10-12](2026-10-12_memoire.md) | `3 couches` |

### `apprentissage` — Règles locales, hebbien, modulateurs, distillation

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_apprentissage.md) | `5,2 %` · `-12 %` · `−12 %` · `−5,2 %` |
| [2026-10-10](2026-10-10_apprentissage.md) | — |
| [2026-10-11](2026-10-11_apprentissage.md) | `50 %` · `25 %` |

### `distribue` — Régions, flux, protocoles, budgets, pannes

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_distribue.md) | `255 jetons` · `1,842` · `3,4 ms` · `×128` · `24 couches` · `59,0790` · `9 %` |
| [2026-10-10](2026-10-10_distribue.md) | `0,992` · `0,681` · `1,000` · `49 %` · `14,8 ms` · `40 %` · `7 ms` · `50 ms` · `50,2 ms` · `256 jetons` · `255 jetons` · `5,3719` |
| [2026-10-11](2026-10-11_distribue.md) | `10 %` · `25 %` · `36 %` · `÷3,8` · `3,8 paires` · `−36 %` |
| [2026-10-12](2026-10-12_distribue.md) | `91 %` · `11,72 ms` · `1,05 ms` · `0,27 ms` |

### `modele` — Modèles, entraînement, parcimonie, biologie

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_modele.md) | `+6,7 %` · `+8,0 %` · `+1,0 %` · `+3,8 %` · `÷3,7` · `1 %` · `÷2` · `50 %` · `6 %` · `+1 %` |
| [2026-10-10](2026-10-10_modele.md) | `5,8 %` · `2,3431` · `2,3215` · `2,2729` · `2,3838` · `2,5188` · `24 couches` · `−11,5 %` · `8000 états` · `8188 états` · `×540` · `×59` |
| [2026-10-11](2026-10-11_modele.md) | `1 %` · `5,8 %` · `+9,4 %` · `+18,4 %` · `÷4,3` · `÷7,9` · `9 %` · `25 %` · `89,18 %` · `9,4 %` · `21 %` · `10 %` |
| [2026-10-12](2026-10-12_modele.md) | `3 couches` |

### `moteur` — Moteur : chargement, calcul, listes, quantification

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_moteur.md) | `8,6 Mo` · `243 Mo` · `8 jetons` · `8 Mo` |
| [2026-10-10](2026-10-10_moteur.md) | `+3,0 %` · `0,283` · `0,399` · `-20 %` · `86 Gio` · `÷4` · `×78` |
| [2026-10-11](2026-10-11_moteur.md) | `8,5 %` |
| [2026-10-12](2026-10-12_moteur.md) | `26,95 s` · `7,36 s` · `6,85 s` · `0,60 s` · `-53 %` · `3,65 s` · `×42` · `1230 Mo` |
| [2026-10-13](2026-10-13_moteur.md) | `601.03ms` · `3,40 s` · `6,22 Go` · `-11,6 %` |

### `mesures` — Campagnes et mesures

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_mesures.md) | `392 fibres` · `79 Kio` · `+1 %` · `+4 %` · `+22 %` · `÷4` · `÷8` · `÷15` · `50 %` · `25 %` · `12,5 %` · `2 %` |
| [2026-10-10](2026-10-10_mesures.md) | `-20 %` · `-8 %` · `512 jetons` · `4096 jetons` · `56,7642` · `10 %` · `×36` · `128 jetons` · `31 jetons` · `24 couches` |
| [2026-10-11](2026-10-11_mesures.md) | — |
| [2026-10-12](2026-10-12_mesures.md) | `3,40 s` · `3,70 s` · `6,22 Go` · `10,90 Go` · `×3,8` · `7,45 Go` |
| [2026-10-13](2026-10-13_mesures.md) | `2121 Mo` |

### `portes` — Portes et vérifications

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_portes.md) | — |
| [2026-10-10](2026-10-10_portes.md) | `13 s` · `136 jetons` · `0,509` · `37,8 %` · `173,0196` · `2048 jetons` · `388 s` · `1 s` · `0 jeton` · `×633` |
| [2026-10-11](2026-10-11_portes.md) | `8 s` · `25 %` · `78 %` · `÷3,8` · `1 %` · `÷7,9` |
| [2026-10-12](2026-10-12_portes.md) | `3995 Mo` |
| [2026-10-13](2026-10-13_portes.md) | — |

### `docs` — Documentation, état, conventions

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_docs.md) | `+2,8 %` · `+25,4 %` · `392 fibres` · `16 couches` |
| [2026-10-10](2026-10-10_docs.md) | `25 s` · `3565 s` · `3525 s` · `45 s` · `43,1 %` · `296 Ko` · `4,0 %` · `×1,05` · `×633` |
| [2026-10-12](2026-10-12_docs.md) | `-91 %` · `60 s` |
| [2026-10-13](2026-10-13_docs.md) | — |

### `divers` — Ce qui ne rentre dans aucun thème

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_divers.md) | `×1,52` · `256 jetons` · `12,5 %` · `+6,7 %` · `+1,0 %` · `0,6 s` · `+7,8 %` · `÷2` · `2 fibres` · `224 fibres` |
| [2026-10-10](2026-10-10_divers.md) | `400 s` · `0,509` · `3,7 %` · `−11,5 %` · `−4,5 %` · `512 jetons` · `50 ms` · `50,2 ms` · `−20 %` · `−8 %` · `10 ms` · `9,4341` |
| [2026-10-11](2026-10-11_divers.md) | `77,7 %` · `×2` · `83,9 %` · `26 %` |
| [2026-10-12](2026-10-12_divers.md) | — |
