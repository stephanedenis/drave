# Session session- — Coordination A : rapport J4.4

> **Journaux :** [le jour](../../2026-11-13/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-11d99e1c-be38-4727-9c7a-013846234567` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-13 22:41 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 100 |
| Appels d'outils | 145 |
| Fichiers touchés | 2 |
| Commandes | 121 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J4.4 : la coordination A — A6.2 est libre (le MoE local 18 Go existe ; le blocage est la résidence mono-GPU) et A8.3b2 est nommée. **Ne modifie rien dans A** (ni natifs, ni données). Fiche `reports/rapport-coordination-a.md` + JSON : l'état des deux lignes, les commandes, les décisions à prendre.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J4.4 : la coordination A — A6.2 est libre (le MoE local 18 Go existe ; le blocage est la résidence mono-GPU) et A8 … [183 caractères tronqués]

*145 appels d'outils.* Actions notables :

- bash — List repo root and recent commits
- bash — List reports and journal
- bash — Search references to A6.2, A8.3b2, J4.4
- bash — Roadmap lines A6 A8 J4
- read
- bash — Backlog A6/A8 files and J4 plan
- bash — Read autonomous week plan
- bash — Find J4 coordination task files
- bash — Read chantier plan JSON
- bash — Read coordination S and R reports
- bash — Read A6.2 backlog
- bash — Read A8.3b decision report and JSON
- bash — List coordination reports and model dirs
- bash — Read N2 coordination report/JSON
- … et 129 autres

**Synthèse produite :**

Tâche J4.4 terminée. Deux fichiers neufs, **aucune modification de A** (`drave-core/`, `data/`, `work/` intacts) :

- `reports/rapport-coordination-a.md` (474 lignes)
- `reports/rapport-coordination-a.json` (328 lignes, JSON valide)

\## Ce que la fiche établit

**A6.2 est libre, pas bloquée.**
- MoE local : `$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf`, **18 556 686 752 o**, **17,28 GiB**, `sha256 6c997b8a…`.
- `bash tools/porte-echange-experts.sh` → **exit 0**, réf. **54,5202** à `N=16`, **768** décisions, routage propre identique, routage étranger **36 074,9497**.
- `--ppl --ctx 512 --limit 32` → **37,2013** reproduit.
- Le blocage est bien la **résidence mono-GPU 16 Go**. Précision ajoutée : le cache VRAM d'experts (`DRAVE_GPU_EXPERTS`) n'est câblé que pour **MXFP4** ; le Q4_K n'y entre pas, même avec 32 Go. Le noyau GPU Q4_K est mesuré (0,171 ms/expert) mais non branché en production.
- Les mesures existantes montrent que le « ÷10 » est tenu **en octets lus au lot 192** (÷15,51), pas au lot 64 (÷7,08), ni en temps (×1,58). Le routage **appris** reste à mesurer.

**A8.3b2 est nommée mais hors du graphe.**
- Nommée dans `rapport-a83b-decision.md`, `a83b-decision.json`, `rapport-etat-a.md` et `semaine-autonome.md` ; absente de `backlog/index.md`, `dependances.md`, `roadmap.md` et `en-cours.md`.
- `LOT=4 bash tools/porte-flux.sh` → **exit 0** (60,8135 / 60,5427) ; `DRAVE_PERTE_MAX=1 LOT=4` → **exit 0** (62,7357 / 64,9228).
- **Correction importante** : `LOT=1 bash tools/porte-flux.sh` → **exit 1**, et c'est normal : les pins des modes 3/4 sont ceux du lot ≥ 2. `LOT=1/4` n'est donc pas un A/B valide. L'A/B manuel `--ppl-reparti` donne bien **61,9920** (lot 1) et **60,8135** (lot 4), découpage neutre.
- Les points d'instrumentation sont listés à `model.rs:5967` (`forward_lot`), `:6085`, `:6110`, `:6328`, `:6352`, `:6523`, `engine.rs:708/726`, et la règle 1 % est une règle **KV** (`model.rs:4711`), pas d'activation.

\## Décisions proposées

**D1** requalifier A6.2 dans les docs ; **D2** définir la métrique du ÷10 (octets lus, lot 192) ; **D3** mesurer en offload CPU maintenant, cache Q4_K plus tard ; **D4** écrire `rapport-a62-moe.md` ; **D5** nommer A8.3b2 dans le graphe ; **D6** réparer le harnais `LOT=1` ; **D7** trancher une référence vs deux par chemin ; **D8** laisser A8.3 opt-in.

\## Vérifications

- `python3 tools/verifie_backlog.py` → **exit 0**, frontière `(3) : A2.6, N2, N4`.
- `python3 tools/revue_documentation.py` → **exit 1**, uniquement les **2 
… [262 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md` | 1 | 16 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.json` | 1 | 3 |

### Commandes exécutées (échantillon)

- **T1** List repo root and recent commits
- **T1** List reports and journal
- **T1** Search references to A6.2, A8.3b2, J4.4
- **T1** Roadmap lines A6 A8 J4
- **T1** Backlog A6/A8 files and J4 plan
- **T1** Read autonomous week plan
- **T1** Find J4 coordination task files
- **T1** Read chantier plan JSON
- **T1** Read coordination S and R reports
- **T1** Read A6.2 backlog
- **T1** Read A8.3b decision report and JSON
- **T1** List coordination reports and model dirs
- **T1** Read N2 coordination report/JSON
- **T1** Read C9 expert exchange report
- **T1** Summaries of expert-related reports
- **T1** Check MoE path and porte script
- **T1** Locate forward_lot implementations
- **T1** Read expert and flux gates
- **T1** Read prefill and clustering reports
- **T1** Find A8.3b2 artifacts
- **T1** Read forward_lot code
- **T1** Check git status, GPU, RAM, model file
- **T1** Locate batch quantization and MoE code
- **T1** Find LOT commands and CLI option
- **T1** Read A8.3b lot report/JSON
- **T1** Find LOT env usage and CLI
- **T1** Check lot handling in gates
- **T1** Find quantization variables in model
- **T1** Read MoE portion of forward_lot
- **T1** Read remaining MoE batch code
- **T1** Locate quantization and GEMM functions
- **T1** Find quantifier definitions and calls
- **T1** Read quantization and GEMM code
- **T1** Read token-path MoE code
- **T1** Find activation quantization defaults
- **T1** Find CLI activation options
- **T1** Find 1% loss rule implementation
- **T1** Read coupe and pont gates
- **T1** Read DRAVE_PERTE_MAX rule
- **T1** Check binary and token files
- … et 81 autres

## 4. Mesures et résultats marquants

- **T1** `9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`
- **T1** `./reports/rapport-a26-bilan.md:32:**testée**. La suite est **A6.2** (bloqué) ou **A8.3a** (épingler le régime 1 %), pas un nouveau`
- **T1** `./reports/rapport-etat-a.md:48:| **A6** apprendre des flux | ✅ / ⏳ **A6.2 mal classé** | A1, A2 | hebbien +**3,0 %**, produits **+0,0045** de R² ; **0 neurone mort** sur 116 736 ; 63 % < 0,1 % ; top 1`
- **T1** `./reports/rapport-etat-a.md:60:| **A2.6** | **partiel, libre (P2)** | A2 acquis ; **pas** A6.2 pour les experts ; tête décidée | KV ×1,93/×5,8 ; lot **503/502 Mio**, **24,0 → 30,5 tok/s** (+27 %), PPL`
- **T1** `./reports/rapport-etat-a.md:162:| **A6.2** | **oui** | MoE local 18 Go, 2×16 Go VRAM, 125 Go RAM ; trace et imposition du routage existent ; le MoE tourne en offload/CPU, le blocage « 16 Go » est une `
- **T1** `30:| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; `
- **T1** `98:[A1–A8] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `99:[A8.0/A8.3a] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `100:[A8.3b/c] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `148:| **A2** | placer sur une machine : [KV](../theorie/glossaire/entrees/kv.md) paginé, [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md), [top-k](../theorie/glossaire/ent`
- **T1** `154:| **A8** | l'ordonnanceur place **et** perte : `choisir_avec_perte` | ✅ **opt-in** ; 6 portes épinglées, A8.3 **échoue** (−5,9 % … +19,5 %) | **A8.3c/d** : le lot change la PPL, pas les threads ; `
- **T1** `(R² 0,30) — la surface capte l'époque ; tout test de style contrôle la date, tout test de famille`
- **T1** `| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |`
- **T1** `> IC95 bootstrap par phrase **[+7,23 ; +9,74]**, McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. La règle`
- **T1** `(15 Mo). La clé de cache est un sha256 de `modèle + messages + température + max_tokens` ; les`
- **T1** `| `7a45325f` — la ponctuation a une POS (`PONCT`) | 85,00 → 85,75 % | **+25** |`
- **T1** `| `6b976cb1` — R4-FR filtré (adjectif connu ou suffixe) | 85,75 → 85,84 % | **+3** |`
- **T1** `| `c43dd5cc` — la règle « que » (pronom après un nom) | 85,84 → 86,25 % | **+13** |`
- **T1** `| **total** | **85,00 → 86,25 %** | **+40** |`
- **T1** `| appels | ~1 200 | **1 218** | +1,5 % |`
- **T1** `| tokens | ~360 000 | **358 962** | −0,3 % |`
- **T1** `| durée | ~20 min | **20 min 59 s** (1 259,2 s) | +5 % |`
- **T1** `| latence moyenne / appel | 0,94 s (run 432) | **1,033 s** | +10 % |`
- **T1** `**27 326 tokens de sortie** (totaux à ±0,5 % près, six prompts dupliqués).`
- **T1** `> le signe du mélange 1 % bascule avec le **chemin lot binaire** (lot 1 contre lot ≥ 2), pas`
- **T1** `| 1 % | **58,3200** | **62,7357** | **62,7357** |`
- **T1** `- Le signe **bascule avec le chemin** : f32 lotte mieux, 1 % lotte moins bien.`
- **T1** `- **18 portes PPL épinglées**, mais seulement **3** ont un régime 1 % dual (flux, pont, coupe).`
- **T1** `2. donner un régime 1 % **dual** aux 18 portes épinglées ;`
- **T1** `"protocole": "validation data/corpus_propre/val.txt, fenêtres Van der Corput dans les chunks de 8192, 8 lots × 16 fenêtres",`
- **T1** ``data/corpus_propre/train.txt`, 8 000 pas × 8 × 512, graine 1, sha256 du `.pt``
- **T1** `Corput dans les chunks de 8 192, 8 lots × 16 fenêtres) :`
- **T1** `> Verdict : **non — et la mesure a d'abord menti.** Le premier essai donnait **×0,81** (une`
- **T1** `> amélioration de 19 % !) en imposant à A le routage de B à la dernière couche. Les contrôles l'ont`
- **T1** `> démonté : **tout** routage différent y fait varier la perplexité de ±20 à 50 %, **le signe dépend`
- **T1** `> du texte** (A : ×0,81 · A2 : ×1,46 · B en sens inverse : ×1,26), et l'ordre « le routage réel fait`
- **T1** `> ×0,94 contre réel ×1,26). Il n'y a **pas** de gain latéral.`
- **T1** `(0,006 %) — parce que la trace **trie** les experts (« l'ordre de `select_nth` est arbitraire ») et`
- **T1** `(±20 %) aurait baigné dans un artefact de 0,006 % — petit, mais du même genre que ce qu'on cherche.`
- **T1** `| A avec **son** routage (référence) | **37,2013** | ×1,00 |`
- **T1** `| A + le routage de **B** (autre texte) | **3 445,03** | **×92,6** |`
- **T1** `| A + routage **aléatoire** | 13 958,96 | ×375 |`
- **T1** `| A + routage de B **décalé d'une couche** | 37 825,73 | ×1 017 |`
- **T1** `| **0** | 133,4957 | **×3,59** |`
- **T1** `| 8 | 41,3360 | ×1,11 |`
- **T1** `| 16 | 38,1149 | ×1,02 |`
- **T1** `| 24 | 37,1813 | ×1,00 |`
- **T1** `| 32 | 42,0470 | ×1,13 |`
- **T1** `| 40 | 38,4055 | ×1,03 |`
- **T1** `| **47** | **30,1705** | **×0,81** |`
- **T1** `**dernière** donne… une amélioration de 19 %. **C'est là que la mesure a menti**, et c'est le § 3`
- **T1** `| rien (son propre routage) | 37,2013 (×1,00) | 92,4832 (×1,00) | 84,6539 (×1,00) |`
- **T1** `| **le routage de l'autre instance** | **30,1705 (×0,81)** | **135,0935 (×1,46)** | **107,0258 (×1,26)** |`
- **T1** `| routage **aléatoire** | 35,4832 (×0,95) | 143,1992 (×1,55) | **79,4284 (×0,94)** |`
- **T1** `| routage de l'autre **décalé** d'une couche | 37,9628 (×1,02) | — | — |`
- **T1** `| un **troisième** texte (B2) | 34,6692 (×0,93) | — | — |`
- **T1** `* **le signe dépend du texte** : ×0,81 sur A, ×1,46 sur A2, ×1,26 sur B — un « gain » qui devient`
- **T1** `une perte de 46 % sur un autre texte n'est pas un gain ;`
- **T1** `* **tout** routage différent à la dernière couche fait bouger la perplexité de ±20 à 50 %, y`
- **T1** `* le contrôle **décalé** (×1,02) montre qu'un routage cohérent mais mal apparié est inerte — c'est`
- **T1** `routage du modèle n'est pas optimal (tout routage différent y change la perplexité de ±20-50 %).`
- **T1** `**Réponse courte : non.** ×1,09 prédit, pour un plafond absolu de ×1,41 — contre`
- **T1** `un plafond de ×3,1 pour le chantier du dense, qui est déjà nommé.`
- **T1** `# S'il est faux, les effets mesurés (±20 %) baignent dans un artefact — et c'est arrivé : la`
- **T1** `echo "     (la porte existe pour ça : l'invariant a déjà été faux de 0,006 % le 13/10)"`
- **T1** `# A8.3a — le régime 1 % a ses propres références et ses propres plafonds : la`
- **T1** `(`DRAVE_TRACE_EXPERTS`, 48 couches × 194 jetons) et compte les matrices lues —`
- **T1** `| argmax identique | 191/191 = **100 %** |`
- **T1** `routés (29,8 %) et 60,958 pour le partagé + l'attention + la tête (70,2 %). Le`
- **T1** `regroupement par experts ne peut donc adresser **que 30 %** du trafic d'un`
- **T1** `jeton — moins que sur Qwen3, où les experts sont 56 % des octets.`
- **T1** `* **ventilation** : nombre de clusters nécessaires pour couvrir 90 % des experts`
- **T1** `| 4 | **0,799** | **1,94** | 0,440 | 3,59 | ×1,8 |`
- **T1** `| 8 | **0,607** | **3,08** | 0,319 | 5,32 | ×1,9 |`
- **T1** `| 16 | **0,442** | **4,46** | 0,250 | 6,55 | ×1,8 |`
- **T1** `cluster, 625 ms au lieu de 3,9 s, 1 587 tenseurs vérifiés — le format est décrit`
- **T1** `/// fois au lieu de `t` fois (mesuré au noyau : ×2,4 à 16 jetons sur une`
- **T1** `/// matrice 4864 × 896).`
- **T1** `116:    // (une couche MoE = 1 366 ms/jeton, et 93 couches en f32 demanderaient`
- **T1** `1416:                    // pas la déquantification (mesuré : ×1,07 en vectorisant la`
- **T1** `1596:/// experts distincts, 50 % des lectures dans 394 experts, 31,9 % de réutilisation`
- **T1** `3876:/// contrôle : jusqu'à ~15 To demandés au noyau. 256 Mo couvrent largement un lot`
- **T1** `> taille ne change rien à quatre décimales. Le signe du mélange 1 % bascule avec ce chemin.`
- **T1** `| lot | f32 | mélange 1 % |`
- **T1** `- En f32, lotter **améliore** (61,9920 → 60,8135, −1,9 %) ; sous la règle 1 %, lotter`
- **T1** `**dégrade** (58,3200 → 62,7357, +7,6 %). Le signe **bascule avec le chemin**, pas avec la taille.`
- **T1** `"question": "le signe du mélange 1 % vient-il de la taille de lot ou d'un chemin lot binaire ?",`
- **T1** `// les relisait `rep` fois — mesuré ×2,2 sur ce poste.`
- **T1** `// cette ligne, « paires experts » tombait à ~1 % de sa valeur`
- **T1** `// génération, et un chiffre qui chute de 97 % sans raison`
- **T1** `3648:    /// les quantifier » : c'est peut-être là que se joue son +0,8 % de`
- **T1** `drave-core/src/model.rs:4709:        // premières couches, +0,03 % sur les dernières (A5.3) — le budget `DRAVE_PERTE_MAX``
- **T1** `#      de 108,87 à 118,53 de perplexité — soit 9 % d'écart — parce que l'erreur de`
- **T1** `#      d'un pont de 448 fibres va de +0,52 % (coupe 18/6) à +17,09 % (coupe 15/9).`
- **T1** `# mesurer +4,92 % là où le pont symétrique coûte +2,81 % (attrapé en comparant avec`
- **T1** `sys.exit(f"  ❌ avec un lien encodé, le point de coupe devrait compter : écart {ecart:.2%}")`
- **T1** `#      de la qualité — 3 664 octets et +7,8 % de perplexité à 448 fibres. C'est`
- **T1** `print(f"  ✅ PPL de référence épinglées ({'1 %' if perte else 'f32'}) : dense {ref} · blocs {refb}")`
- **T1** `// précision par couche quand rien n'est forcé : l'int8 coûte +2,28 % sur les`
- **T1** `// premières couches, +0,03 % sur les dernières (A5.3) — le budget `DRAVE_PERTE_MAX``
- **T1** `// décale les chiffres des portes (mesuré le 24/10 : porte-coupe passe de +0,5-17 % à`
- **T1** `// 5,9-11,6 % et échoue) — on ne change pas un défaut sans épingler les portes d'abord.`
- **T1** `(l'int8 coûte +2,28 % sur les premières, +0,03 % sur les dernières)");`
- **T1** `// une récurrence qui fuit ne retient pas (R² 0,104), un tampon retient exactement.`
- **T1** `23 tokens notés — perplexité cumulée 48.580  (23.9 tok/s)`
- **T1** `=== perplexité 48.5799 sur 23 tokens (0 événements, 1.0 s) ===`
- **T1** `[config] KV par la règle place+perte : budget 1.0 % → 12 couche(s) en int8 (l'int8 coûte +2,28 % sur les premières, +0,03 % sur les dernières)`
- **T1** `23 tokens notés — perplexité cumulée 48.594  (22.5 tok/s)`
- **T1** `=== perplexité 48.5937 sur 23 tokens (0 événements, 1.0 s) ===`
- **T1** `23 tokens notés — perplexité cumulée 48.567  (28.5 tok/s)`
- **T1** `=== perplexité 48.5666 sur 23 tokens (0 événements, 0.8 s) ===`
- **T1** `23 tokens notés — perplexité cumulée 48.670  (28.2 tok/s)`
- **T1** `=== perplexité 48.6700 sur 23 tokens (0 événements, 0.8 s) ===`
- **T1** `=== perplexité 33.1059 sur 23 tokens (0 événements, 1.0 s) ===`
- **T1** `=== perplexité 33.2277 sur 23 tokens (0 événements, 0.8 s) ===`
- **T1** `=== perplexité 70.1813 sur 23 tokens (172995 événements, 1.0 s) ===`
- **T1** `=== perplexité 66.2076 sur 23 tokens (0 événements, 0.8 s) ===`
- **T1** `# mesure plus la taille du lot (constaté : ×17 sur un lot 2 mesuré pendant`
- **T1** `* **ventilation** (fan-out) : nombre de clusters nécessaires pour couvrir 90 % des`
- **T1** `20:| **réutilisation immédiate** (t−1 → t) | 46,9 % | **47,9 %** | **48,8 %** |`
- … (tronqué)

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : /home/stephane/Data13TB/stephane/GitHub/Qtrinet total 208 drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 . drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 .. -rw-r--r--. 1 stephane stephane  99
- **T1** : thread 'main' (972473) panicked at src/main.rs:689:35: ouverture du GGUF: Os { code: 2, kind: NotFound, message: "No such file or directory" } note: run with `RUST_BACKTRACE=1` environment variable to
- **T1** : référence locale  : perplexité 61.9920  (1.0 s)   deux nœuds        : perplexité 61.9920  (1.0 s)   référence locale  : perplexité 60.8135  (0.9 s)   deux nœuds        : perplexité 60.8135  (0.9 s) [s

