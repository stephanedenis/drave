# Session f2de810a — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `f2de810a-b765-444d-b3cc-d8fce1ba2105` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 15:03 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 56 |
| Appels d'outils | 63 |
| Fichiers touchés | 0 |
| Commandes | 35 |
| Sous-agents | 4 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust — dossier `drave-core/` — qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).  TÂCHE : dépouille EXHAUSTIVEMENT, avec l'outil read (lecture complète) : 1. les 9 fichiers de `sprints/` (01-premier-des-trois-noyaux-g … [3116 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en … [3396 caractères tronqués]

*63 appels d'outils.* Actions notables :

- bash — List files and line counts
- sous-agent — Extract Rust CLI flags part 1
- sous-agent — Extract Rust flags part 2
- sous-agent — Extract Python tool headers
- sous-agent — Extract shell script headers
- read
- bash — Read sprint 9 and list repo root/docs/reports
- bash — Grep long() CLI definitions
- bash — Count all DRAVE_ env vars repo-wide
- bash — List literal --flags in Rust sources
- bash — List --flags in tools
- bash — Locate argument parser in main.rs
- bash — Inspect top-level src and drave-core layout
- bash — Explore main.rs parser structure
- … et 28 autres

**Synthèse produite :**

⏵ Livrable transmis au parent ; reproduction intégrale ci-dessous

\## A. Termes, sigles et drapeaux

**Protocole de flux (DRVF)**
- **DRVF** — Format binaire de trace/échange d'activations : en-tête `"DRVF"` + u16 version + u32 n_layer + u32 hidden, listes (couche, position, n_actifs, échelle) et paires, sentinelle `0xFFFF` ; écrit par `model.rs:1502` (`b"DRVF"`), lu `model.rs:1644-1649`, spécifié `tools/flux_codec.py:16-31`, `tools/analyse_flux.py:24-33` ; terme de protocole/format.
- **DRVF v1 / v2 / v3** — Versions du fichier de trace : v1 paires `(u32 indice, i16 valeur)`, v2 écarts u8 + i16 (255 = indice absolu u16), v3 blocs i8 + échelle f16 par bloc de 32 (`DRAVE_TRACE_BLOCS`) ; `tools/flux_codec.py:28-36` (VERSION=2 écrit, lit 1/2/3), `model.rs:1507,1649` ; format.
- **DRVF v5** — Version du protocole de TRANSPORT TCP (≠ version du fichier) : en-tête de 79 octets, magie `0x44525631` (« DRV1 ») ; `main.rs:1893,1906,1941` (`MAGIE_FLUX`, `VERSION_FLUX=5`, `TAILLE_TETE`), `docs/format-flux.md:92-114` ; protocole.
- **mode 0 / MODE_DENSE** — Vecteur dense f32 (4 octets/canal) ; `main.rs:1908`, `tools/pair_factice.py:17` ; mode de protocole.
- **mode 1 / MODE_LISTE** — Liste creuse quantifiée : indice u16 + valeur i16 + une échelle (émis par `--flux-liste`) ; `main.rs:1912`, `tools/pair_factice.py:17` ; mode de protocole.
- **mode 2 / MODE_BLOCS** — Liste à échelle par bloc de 32 canaux : indice u16, valeur i8, échelle f32 par bloc (émis par `--flux-blocs`) ; `main.rs:1917`, `tools/pair_factice.py:18` ; mode de protocole.
- **mode 3 / MODE_LOT** — n états × hidden en f32 dense dans un seul flux (préremplissage réparti) ; `main.rs:1923`, `docs/format-flux.md:112` ; mode de protocole.
- **mode 4 / MODE_LOT_LISTES** — Lot d'états, chacun encodé comme le mode 2, auto-délimité ; `main.rs:1930` (« ≈1 530 octets/jeton, ÷2,3 »), `main.rs:2616-2622` ; mode de protocole.
- **TAILLE_TETE = 79** — Octets de l'en-tête de flux (règles d'activation comprises) ; `main.rs:1941`, `tools/pair_factice.py:15` ; constante.
- **PLAFOND_FLUX = 256 Mo** — Plafond d'allocation pilotée par le réseau (règle R4 de `docs/plan-prefill-reparti.md`) ; `main.rs:2002` ; constante.
- **Act** — Réglages d'activation voyageant dans chaque en-tête (levels, thresh, topk, renorm, topk_proj[7], attn/qk/moe top-k) ; `main.rs:1945-1978` ; structure de protocole.
- **pair / paire (indice, valeur)** — Unité de contenu d'une liste creuse, et « pair » = pair distant du protocole (`--ppl-reparti`) ; `t
… [43750 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Sous-agents lancés

- tour 1 — Extract Rust CLI flags part 1
- tour 1 — Extract Rust flags part 2
- tour 1 — Extract Python tool headers
- tour 1 — Extract shell script headers

### Commandes exécutées (échantillon)

- **T1** List files and line counts
- **T1** Read sprint 9 and list repo root/docs/reports
- **T1** Grep long() CLI definitions
- **T1** Count all DRAVE_ env vars repo-wide
- **T1** List literal --flags in Rust sources
- **T1** List --flags in tools
- **T1** Locate argument parser in main.rs
- **T1** Inspect top-level src and drave-core layout
- **T1** Explore main.rs parser structure
- **T1** Find usage/help text in main.rs
- **T1** List env::var call sites in Rust
- **T1** Investigate ambiguous DRAVE vars
- **T1** Identify flux protocol modes 1-4
- **T1** Read flux format mode table
- **T1** Check flux constants and portes comment
- **T1** Check existence of paths cited in sprints
- **T1** Check other arg parsers
- **T1** List enums and consts in Rust
- **T1** Check attn-topk lot behaviour and KvCache::assurer
- **T1** Locate assurer functions
- **T1** Check livelock fixes
- **T1** Count tests and check cited lines
- **T1** Locate hardware terminology
- **T1** Locate ALM and M20K references
- **T1** Locate remaining jargon terms
- **T1** Check lora, porte de correction, MTP
- **T1** Inspect materiel, Gating, formats statics
- **T1** Cross-check engram figures
- **T1** Read heavy model manifest
- **T1** Verify existence of cited files
- **T1** Check porte de correction, greffon, E8M0
- **T1** List glossary entries
- **T1** List rest of glossary entries
- **T1** Verify density figure and misc
- **T1** Check hard-coded Drave path existence

## 4. Mesures et résultats marquants

- **T1** `./docs/roadmap.md:30:| 1.4 | **Écart int8 résiduel** (+3,0 % contre +0,8 % chez llama.cpp à 8 192) | ✅ | **attribué** : tout l'écart est dans les CLÉS (clés f32 + valeurs int8 = +0,023 % ; l'inverse =`
- **T1** `réelle de 512 jetons : 132 396 736 octets en v1, **66 370 408** en v2 (−49,87 %),`
- **T1** `133:f32 dense (3,5 ko par jeton) ; le lot en LISTES est le mode 4 (1,5 ko par jeton,`
- **T1** `jetons, 16 par lot, seuil 0,01 : **1,5 ko par jeton au lieu de 3,5** (÷2,3) pour`
- **T1** `f32 dense (3,5 ko par jeton) ; le lot en LISTES est le mode 4 (1,5 ko par jeton,`
- **T1** `drave-core/src/gpu.rs:639:    /// pèse 14,7 Mo sur le bus PCIe, et 56 Mo à 1 M : la mesurer séparément est`
- **T1** `drave-core/src/main.rs:3981:/// cette machine : CPU 14–25 Go/s, PCIe x8 6,5 Go/s, NVLink 25,78 Go/s,`
- **T1** `drave-core/src/main.rs:4028:                        else { "GPU (PCIe 6,5 Go/s)" };`
- **T1** `drave-core/src/main.rs:4105:    for (nom, debit) in [("RAM 20 Go/s", 20.0), ("PCIe 6,5", 6.5), ("NVLink 25,8", 25.78),`
- **T1** `drave-core/src/materiel.rs:51:    /// Liens NVLink actifs : 25,8 Go/s sur cette machine, soit 2× le PCIe.`
- **T1** `drave-core/src/materiel.rs:339:            raisons.push("NVLink détecté (25,8 Go/s, 2× le PCIe) : les échanges \`
- **T1** `docs/comparaison-spiking.md:59:| Arithmétique | ET logique + **AC** (accumulation) | MAC (mais décalages+additions validés, 0 DSP sur FPGA) |`
- **T1** `docs/comparaison-spiking.md:63:| Énergie par opération | E_AC = 0,9 pJ contre E_MAC = 4,5 pJ (Horowitz) | 8,3 nJ/événement (FPGA, **projeté** : 4,83 G évts/s, limite DDR3) contre 57 nJ (CPU, **mesuré*`
- **T1** `docs/convertisseur.md:91:| DDR3 de la carte FPGA | 9,66 Go/s | lecture de listes |`
- **T1** `docs/convertisseur.md:93:| PCIe x8 (gen 3) | 6,5 Go/s | transfert CPU↔GPU |`
- **T1** `docs/programme-recherche.md:58:| Carte FPGA | PE vérifié sur 309 020 événements réels, synthétisé (176 ALMs, 0 DSP), lecteur DDR3 vérifié de bout en bout |`
- **T1** `reports/bilan-multi-materiel.md:66:3. **Pas de multiplieur requis.** Le PE atteint 112,5 MHz avec 176 ALMs **et zéro`
- **T1** `reports/bilan-multi-materiel.md:67:   DSP**, contre 115 ALMs et 1 DSP avec multiplieur — et **pas un hertz d'écart**.`
- **T1** `reports/bilan-multi-materiel.md:95:| « 27 PE suffisent, 3 % de la logique » | **Corrigée** — en comptant le lecteur : 51 voies, 41 % de la logique et 41 % de la M20K |`
- **T1** `reports/rapport-cpu-aer.md:11:  (accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) ;`
- **T1** `reports/rapport-eparsite.md:64:4. **Le vrai obstacle n'est pas le poids, c'est l'activation** : un événement n'existe que si le poids *et* l'activation sont non nuls (ici 13.9 % d'événements réels). R`
- **T1** `reports/rapport-minimal.md:81:5. **Tout le projet est borné par la DDR3**, pas par le calcul : à 124 MHz il ne faut que ~312 voies de MAC (≈ 9 400 ALM, 5 % du FPGA) pour saturer les 9,66 Go/s. 96 % du`
- **T1** `docs/histoire.md:12:| **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Rep`
- **T1** `docs/plan-deepseek41-complet.md:70:| tables d'engram | 10 000 entrées en **219–524 ms**, 2,6 Mo touchés par table, **120 Mo de RSS** pour 365,7 Go |`
- **T1** `415:**Patch · ViT · projecteur (mmproj)** — Un *patch* est un carré d'image (14 × 14`
- **T1** `=== 22 % ===`
- **T1** `tools/analyse_flux.py:8:  croisement mesuré est à ~22 % de densité) — mais elle se prend PAR COUCHE, pas`
- **T1** `drave-core/src/model.rs:984:        // scalaire dense (pull). Le croisement mesuré est à 22 %`
- **T1** `drave-core/src/model.rs:1485:    /// canaux, ~22 % plus petit, avec perte).`
- **T1** `drave-core/src/model.rs:1505:        // f16 par bloc de 32 canaux (l'étude de compacité annonce −22 % de plus,`
- **T1** `drave-core/src/model.rs:1779:    /// push/pull de 22 % arbitre (`reports/rapport-croisement-push-pull.md`).`
- **T1** `drave-core/src/model.rs:1845:    /// deux architectures se croisent à **22 %** de densité`
- **T1** `drave-core/src/model.rs:5531:                        // 0,13 contre 0,22 ms à 4 k clés, 0,85 contre 0,89 à 131 k —`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : === long("...") occurrences ===  === count long( === drave-core/src/clusters.rs:0 drave-core/src/engine.rs:0 drave-core/src/formats.rs:0 drave-core/src/gguf.rs:0 drave-core/src/gpu.rs:0 drave-core/src

