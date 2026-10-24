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
| [2026-10-13](2026-10-13_attention.md) | `+3,0 %` · `2,1 %` · `+9,3 %` · `+0,9 %` · `+4,1 %` · `+49,2 %` · `482 jetons` · `+2,1 %` · `2 %` · `+49 %` |
| [2026-10-14](2026-10-14_attention.md) | `-6,5 %` · `-4,8 %` |
| [2026-10-15](2026-10-15_attention.md) | `-14,1 %` · `0,019` · `0,096` · `4 couches` |
| [2026-10-16](2026-10-16_attention.md) | `0,0 %` |
| [2026-10-22](2026-10-22_attention.md) | `5%` · `0,042` · `0,466` · `0,810` |

### `memoire` — Mémoire épisodique, consolidation, greffe

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_memoire.md) | `15 %` · `83 %` · `96 %` · `81 %` · `85 %` · `22 %` · `87 %` · `50 %` · `2 jetons` · `0,5 %` · `2048 jetons` · `11 jetons` |
| [2026-10-10](2026-10-10_memoire.md) | `31 %` · `1,000` · `0,913` · `1006 jetons` · `136 jetons` · `50 jetons` · `+12 %` · `÷4` · `0,906` · `0,112` |
| [2026-10-11](2026-10-11_memoire.md) | `15 s` · `4 Go` |
| [2026-10-12](2026-10-12_memoire.md) | `3 couches` |
| [2026-10-13](2026-10-13_memoire.md) | — |
| [2026-10-14](2026-10-14_memoire.md) | `-16,4 %` · `+1,3 %` |
| [2026-10-15](2026-10-15_memoire.md) | `-7,46 %` · `-10,68 %` · `0,035 %` · `0,07 %` · `0,035` · `-7,63 %` · `-5,28 %` · `+0,36 %` · `-22,5 %` · `-7,4 %` · `+1,2 %` |
| [2026-10-16](2026-10-16_memoire.md) | `88,3 %` · `0,701` · `1,015` · `-1,55 %` · `16 jetons` · `-8,75 %` · `-7,47 %` · `-0,58 %` · `+0,33 %` · `16 Go` |
| [2026-10-17](2026-10-17_memoire.md) | `860 s` · `817 s` · `102 s` · `101 s` · `5 ms` · `134,6 ms` · `530 Ko` · `9,8 Mo` |
| [2026-10-18](2026-10-18_memoire.md) | `37,2 %` · `27,8 %` · `10,8 %` · `2,05 %` · `3,3 %` · `2415 paires` · `0,138` · `0,049` · `6,50 %` · `16,3 %` · `85,1 %` · `0,6 %` |
| [2026-10-19](2026-10-19_memoire.md) | `93,2 %` · `0,3 %` · `3397 paires` · `4 paires` |
| [2026-10-21](2026-10-21_memoire.md) | `2832 paires` |
| [2026-10-24](2026-10-24_memoire.md) | — |

### `apprentissage` — Règles locales, hebbien, modulateurs, distillation

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_apprentissage.md) | `5,2 %` · `-12 %` · `−12 %` · `−5,2 %` |
| [2026-10-10](2026-10-10_apprentissage.md) | — |
| [2026-10-11](2026-10-11_apprentissage.md) | `50 %` · `25 %` |
| [2026-10-14](2026-10-14_apprentissage.md) | `46,8 %` · `51,0 %` · `36,9 %` · `25,9 %` · `28 %` · `51 %` |
| [2026-10-15](2026-10-15_apprentissage.md) | `30 %` · `75 %` · `0 %` |
| [2026-10-16](2026-10-16_apprentissage.md) | `+148 %` · `+143 %` · `30,3 %` · `25,7 %` · `51,4 %` · `38,1 %` · `28,0 %` · `17,1 %` · `13,8 %` |
| [2026-10-21](2026-10-21_apprentissage.md) | — |

### `distribue` — Régions, flux, protocoles, budgets, pannes

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_distribue.md) | `255 jetons` · `1,842` · `3,4 ms` · `×128` · `24 couches` · `59,0790` · `9 %` |
| [2026-10-10](2026-10-10_distribue.md) | `0,992` · `0,681` · `1,000` · `49 %` · `14,8 ms` · `40 %` · `7 ms` · `50 ms` · `50,2 ms` · `256 jetons` · `255 jetons` · `5,3719` |
| [2026-10-11](2026-10-11_distribue.md) | `10 %` · `25 %` · `36 %` · `÷3,8` · `3,8 paires` · `−36 %` |
| [2026-10-12](2026-10-12_distribue.md) | `91 %` · `11,72 ms` · `1,05 ms` · `0,27 ms` |
| [2026-10-13](2026-10-13_distribue.md) | `16 couches` · `0,7 %` |
| [2026-10-14](2026-10-14_distribue.md) | `-5,6 %` · `-10,0 %` |
| [2026-10-15](2026-10-15_distribue.md) | `128 jetons` · `0,274` |
| [2026-10-16](2026-10-16_distribue.md) | `110,2 %` |
| [2026-10-17](2026-10-17_distribue.md) | `0,0097` · `0,0087` · `20 %` · `451 Ko` · `375 Ko` · `82,2 %` · `68 %` · `1,33 %` · `84 %` · `-44,6 %` · `-52,9 %` · `1,5046` |
| [2026-10-20](2026-10-20_distribue.md) | `92,5 %` · `96,2 %` · `0,5 %` · `2,0 %` · `8,8 %` |
| [2026-10-21](2026-10-21_distribue.md) | `-8,9 %` · `2,2 %` · `-11,1 %` · `81 Go` · `1186 paires` · `16 Go` · `256 jetons` · `30950 paires` · `2832 paires` · `33 %` · `0,855` · `0,865` |
| [2026-10-22](2026-10-22_distribue.md) | `13394 paires` · `0,586` · `0,592` · `0,773` · `0,751` · `0,456` · `0,534` · `0,505` · `0,742` · `5%` · `0,042` · `0,451` |

### `modele` — Modèles, entraînement, parcimonie, biologie

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_modele.md) | `+6,7 %` · `+8,0 %` · `+1,0 %` · `+3,8 %` · `÷3,7` · `1 %` · `÷2` · `50 %` · `6 %` · `+1 %` |
| [2026-10-10](2026-10-10_modele.md) | `5,8 %` · `2,3431` · `2,3215` · `2,2729` · `2,3838` · `2,5188` · `24 couches` · `−11,5 %` · `8000 états` · `8188 états` · `×540` · `×59` |
| [2026-10-11](2026-10-11_modele.md) | `1 %` · `5,8 %` · `+9,4 %` · `+18,4 %` · `÷4,3` · `÷7,9` · `9 %` · `25 %` · `89,18 %` · `9,4 %` · `21 %` · `10 %` |
| [2026-10-12](2026-10-12_modele.md) | `3 couches` |
| [2026-10-13](2026-10-13_modele.md) | `19 %` · `16 couches` |
| [2026-10-14](2026-10-14_modele.md) | `÷1,47` · `÷1,24` · `÷1,19` · `÷1,32` · `÷1,83` |
| [2026-10-15](2026-10-15_modele.md) | `9,6706` · `-10,80 %` · `-7,21 %` · `-0,65 %` · `-0,04 %` · `0,71 %` · `32 couches` |
| [2026-10-16](2026-10-16_modele.md) | `77,5 %` · `49,0 %` · `44,8 %` · `128 jetons` · `24,9 %` · `25,7 %` · `30,3 %` · `51,4 %` · `0,1387` · `25 %` · `4,8948` · `-73 %` |
| [2026-10-17](2026-10-17_modele.md) | `1,33 %` · `-4,7 %` · `+10,8 %` · `-53 %` · `-7,6 %` · `-26 %` · `2,6504` · `69,0 %` · `2,6097` · `60 %` · `56 %` · `87,7 %` |
| [2026-10-18](2026-10-18_modele.md) | `16,3 %` · `14,4 %` · `6,50 %` · `85,1 %` · `96 %` · `-87 %` · `-10 %` |
| [2026-10-19](2026-10-19_modele.md) | — |
| [2026-10-20](2026-10-20_modele.md) | `1,33 %` · `96 %` · `5 ms` |
| [2026-10-21](2026-10-21_modele.md) | `0,933` · `0,733` · `0,467` · `0,133` · `0,0001` · `0,067` · `50 %` · `0,865` · `0,125` |
| [2026-10-22](2026-10-22_modele.md) | `0,592` · `0,610` · `0,751` · `0,453` · `0,502` · `0,542` · `0,481` · `0,589` · `0,627` · `0,576` · `0,364` · `0,250` |

### `moteur` — Moteur : chargement, calcul, listes, quantification

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_moteur.md) | `8,6 Mo` · `243 Mo` · `8 jetons` · `8 Mo` |
| [2026-10-10](2026-10-10_moteur.md) | `+3,0 %` · `0,283` · `0,399` · `-20 %` · `86 Gio` · `÷4` · `×78` |
| [2026-10-11](2026-10-11_moteur.md) | `8,5 %` |
| [2026-10-12](2026-10-12_moteur.md) | `26,95 s` · `7,36 s` · `6,85 s` · `0,60 s` · `-53 %` · `3,65 s` · `×42` · `1230 Mo` |
| [2026-10-13](2026-10-13_moteur.md) | `2,4 s` · `0,88 Mo` · `601.03ms` · `3,40 s` · `6,22 Go` · `-11,6 %` |
| [2026-10-14](2026-10-14_moteur.md) | `÷1,19` · `÷1,32` · `÷1,83` · `14,2342` |
| [2026-10-15](2026-10-15_moteur.md) | `0,71 %` · `66,6 %` · `0,00 %` · `0,9972` · `10 %` · `-7,47 %` · `-16,11 %` · `-7,63 %` · `-15,93 %` · `-4,0 %` · `-7,4 %` · `-8,7 %` |
| [2026-10-16](2026-10-16_moteur.md) | — |
| [2026-10-17](2026-10-17_moteur.md) | `69,0 %` · `87,8 %` |
| [2026-10-18](2026-10-18_moteur.md) | — |
| [2026-10-21](2026-10-21_moteur.md) | — |
| [2026-10-22](2026-10-22_moteur.md) | — |

### `mesures` — Campagnes et mesures

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_mesures.md) | `392 fibres` · `79 Kio` · `+1 %` · `+4 %` · `+22 %` · `÷4` · `÷8` · `÷15` · `50 %` · `25 %` · `12,5 %` · `2 %` |
| [2026-10-10](2026-10-10_mesures.md) | `-20 %` · `-8 %` · `512 jetons` · `4096 jetons` · `56,7642` · `10 %` · `×36` · `128 jetons` · `31 jetons` · `24 couches` |
| [2026-10-11](2026-10-11_mesures.md) | — |
| [2026-10-12](2026-10-12_mesures.md) | `3,40 s` · `3,70 s` · `6,22 Go` · `10,90 Go` · `×3,8` · `7,45 Go` |
| [2026-10-13](2026-10-13_mesures.md) | `16 couches` · `2,3 s` · `3,05 s` · `16,96 %` · `0,63 %` · `5,5 s` · `32 jetons` · `33,9093` · `33,6967` · `2121 Mo` |
| [2026-10-14](2026-10-14_mesures.md) | `10 s` |
| [2026-10-15](2026-10-15_mesures.md) | `0,345` · `6,7487` · `0,921` · `0,817` · `-7,85 %` · `-14 %` · `-14,5 %` · `-10,9 %` · `51,0 %` · `22,1 %` · `-0,95 %` · `-0,82 %` |
| [2026-10-16](2026-10-16_mesures.md) | `654 Mio` · `1086 Mio` · `72,0 %` · `0,9972` · `0,5 %` · `39,3 %` · `0,0 %` · `4 %` |
| [2026-10-17](2026-10-17_mesures.md) | `5,9 %` · `9,8 %` · `1,1 %` · `76,5 %` · `75,9 %` · `104,3 %` · `87,0 %` |
| [2026-10-18](2026-10-18_mesures.md) | `-17 %` · `-2 %` · `30,7 %` · `22,0 %` · `15,2 %` · `3,3 %` · `87,5 %` · `50 %` · `6,2 %` |
| [2026-10-19](2026-10-19_mesures.md) | `150 Ko` · `100 %` · `5 %` · `10 %` · `41 %` · `30 %` |
| [2026-10-20](2026-10-20_mesures.md) | — |
| [2026-10-21](2026-10-21_mesures.md) | `-1,15 %` · `-27 %` · `25 %` · `0,827` · `0,940` · `0,821` · `0,939` · `0,933` · `0,995` · `0,003` · `2,2 %` · `0,5 %` |
| [2026-10-22](2026-10-22_mesures.md) | `0,364` · `0,375` · `0,511` · `0,273` · `0,318` · `0,386` · `0,284` · `33,3 %` · `0,502` · `0,576` · `0,592` · `0,966` |

### `portes` — Portes et vérifications

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_portes.md) | — |
| [2026-10-10](2026-10-10_portes.md) | `13 s` · `136 jetons` · `0,509` · `37,8 %` · `173,0196` · `2048 jetons` · `388 s` · `1 s` · `0 jeton` · `×633` |
| [2026-10-11](2026-10-11_portes.md) | `8 s` · `25 %` · `78 %` · `÷3,8` · `1 %` · `÷7,9` |
| [2026-10-12](2026-10-12_portes.md) | `3995 Mo` |
| [2026-10-13](2026-10-13_portes.md) | — |
| [2026-10-14](2026-10-14_portes.md) | — |
| [2026-10-15](2026-10-15_portes.md) | `0,71 %` · `31 couches` · `-7,21 %` · `-4,86 %` · `-7,85 %` · `-6,78 %` · `-14,54 %` · `-10,31 %` · `0,921` · `0,817` |
| [2026-10-16](2026-10-16_portes.md) | `42,1 %` · `68,8 %` · `78 %` · `4 jetons` |
| [2026-10-17](2026-10-17_portes.md) | `13,2 Mo` · `15,7 Mo` · `1,7 %` · `0,101` · `80,3 %` · `16 jetons` |

### `docs` — Documentation, état, conventions

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_docs.md) | `+2,8 %` · `+25,4 %` · `392 fibres` · `16 couches` |
| [2026-10-10](2026-10-10_docs.md) | `25 s` · `3565 s` · `3525 s` · `45 s` · `43,1 %` · `296 Ko` · `4,0 %` · `×1,05` · `×633` |
| [2026-10-12](2026-10-12_docs.md) | `-91 %` · `60 s` |
| [2026-10-13](2026-10-13_docs.md) | `+2,1 %` · `+49,2 %` |
| [2026-10-14](2026-10-14_docs.md) | — |
| [2026-10-15](2026-10-15_docs.md) | `66,6 %` · `0,7804` |
| [2026-10-16](2026-10-16_docs.md) | `87,0 %` · `49,3 %` · `76,9 %` · `88 %` |
| [2026-10-17](2026-10-17_docs.md) | `53,6 %` · `69,0 %` · `2,6097` · `0,3 %` · `3,3 %` · `13,1 %` · `21,4 %` · `9,4 %` · `0,1161` · `0,0925` · `0,0779` · `0,0087` |
| [2026-10-18](2026-10-18_docs.md) | `97,1 %` · `100 %` · `30 %` · `52 %` · `96,4 %` · `96 %` · `24 %` |
| [2026-10-19](2026-10-19_docs.md) | `46 %` · `9,3 Ko` · `5,0 Ko` |
| [2026-10-22](2026-10-22_docs.md) | — |

### `outils` — Outils et harnais

| jour | chiffres du jour |
|---|---|
| [2026-10-13](2026-10-13_outils.md) | — |
| [2026-10-15](2026-10-15_outils.md) | `-7,92 %` |
| [2026-10-16](2026-10-16_outils.md) | — |
| [2026-10-17](2026-10-17_outils.md) | `37 %` · `37,5 %` |

### `divers` — Ce qui ne rentre dans aucun thème

| jour | chiffres du jour |
|---|---|
| [2026-10-09](2026-10-09_divers.md) | `×1,52` · `256 jetons` · `12,5 %` · `+6,7 %` · `+1,0 %` · `0,6 s` · `+7,8 %` · `÷2` · `2 fibres` · `224 fibres` |
| [2026-10-10](2026-10-10_divers.md) | `400 s` · `0,509` · `3,7 %` · `−11,5 %` · `−4,5 %` · `512 jetons` · `50 ms` · `50,2 ms` · `−20 %` · `−8 %` · `10 ms` · `9,4341` |
| [2026-10-11](2026-10-11_divers.md) | `77,7 %` · `×2` · `83,9 %` · `26 %` |
| [2026-10-12](2026-10-12_divers.md) | — |
