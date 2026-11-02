# Session abb58991 — Reprise session L/B13 et mise à jour plan

> **Journaux :** [le jour](../../2026-11-02/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `abb58991-fe0a-4d6e-b039-6552b09f8454` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-02 16:15 |
| Durée | 0.7 h |
| Tours | 1 |
| Messages | 104 |
| Appels d'outils | 151 |
| Fichiers touchés | 10 |
| Commandes | 114 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu reprends la session L/B13 `e181ce02-cd50-488a-a6be-e84b79d40dcc`. Lis son plan, AGENTS.md  et docs/pilotage/en-cours.md. Remets `- **État** : actif` et `- **Heartbeat** : <maintenant>`  dans son plan, puis vérifie `python3 tools/sessions.py --check --strict`. Le cycle 140/140  (gold 432, 116 liens) est committé. Prochaine action : gold neuronal (qualifier un modèle  local) ; DRVM/native est blo … [114 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu reprends la session L/B13 `e181ce02-cd50-488a-a6be-e84b79d40dcc`. Lis son plan, AGENTS.md  et docs/pilotage/en-cours. … [394 caractères tronqués]

*151 appels d'outils.* Actions notables :

- bash — Show repo state and recent commits
- bash — List root and sessions tool help
- bash — List session dirs and locate the session id
- bash — Show session status
- read
- bash — Count lines of target docs
- bash — Get current local and Montreal time
- bash — Inspect heartbeat parsing and strict checks
- bash — Get fresh timestamp for heartbeat
- bash — Timestamp for the heartbeat
- edit `/home/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md`
- edit `/home/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md`
- bash — Run strict session plan check
- bash — Inspect the unlisted active plan
- … et 122 autres

**Synthèse produite :**

⏵ Écriture de la fiche `reports/rapport-pensee-gold-neuronal.md`

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md` | 0 | 2 |
| `/tmp/qualif_proto.py` | 1 | 0 |
| `/tmp/qualif_proto_srv.py` | 1 | 0 |
| `/tmp/qualif_proto_srv2.py` | 1 | 0 |
| `/tmp/qualif_7b.py` | 1 | 0 |
| `/tmp/qualif_7b_180.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py` | 0 | 3 |
| `/home/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py` | 0 | 1 |
| `/home/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_neuronal.py` | 1 | 6 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-pensee-gold-neuronal.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Show repo state and recent commits
- **T1** List root and sessions tool help
- **T1** List session dirs and locate the session id
- **T1** Show session status
- **T1** Count lines of target docs
- **T1** Get current local and Montreal time
- **T1** Inspect heartbeat parsing and strict checks
- **T1** Get fresh timestamp for heartbeat
- **T1** Timestamp for the heartbeat
- **T1** Run strict session plan check
- **T1** Inspect the unlisted active plan
- **T1** Status and references of the extra session
- **T1** Check git status and file mtimes
- **T1** Inspect newly created session dirs
- **T1** Inspect uncommitted changes
- **T1** List active DSH/gate processes
- **T1** Search hub digest for N2 integration
- **T1** List pensee tools and gold reports
- **T1** Look for local models and taggers
- **T1** Re-run strict check after concurrent integration
- **T1** Find neuronal refusal details in gold report
- **T1** Inspect linguistic test scripts
- **T1** Read neuronal refusal section
- **T1** Read NeuronalLLM adapter code
- **T1** Smoke-test llama-cli with local Qwen model
- **T1** Check llama-cli version and options
- **T1** Check GPU and CPU resources
- **T1** Test llama-cli single-turn generation
- **T1** List ollama and heavy model manifest
- **T1** Check grammar/JSON options in llama-cli
- **T1** Find local GGUF models
- **T1** Re-check strict status and git state
- **T1** Inspect gold JSON structure
- **T1** Test exact prompt with JSON constraint
- **T1** Test exact prompt single-turn without grammar
- **T1** Smoke-test Qwen3-0.6B local model
- **T1** Check installed NLP libraries
- **T1** Look for installed spaCy/stanza models
- **T1** Inspect eval entry points
- **T1** Find B13/R0.7 backlog cards
- … et 74 autres

## 4. Mesures et résultats marquants

- **T1** `3510:- Vérifie `nvidia-smi` avant N2 : les deux cartes sont saines (1 Mio, 0 %), mais l'incident est récent.`
- **T1** `> **1,0/1,0/0,994/0,889**, cascade **67,1 %**, **attachement par tête couverture 1,0 / top-1 0,957 / top-k 1,0** (span 0,323/0,338), hasard 0,015 ; **36 cibles ambiguës annotées en double lecture**. ⚠`
- **T1** `couvre **67,1 %** du texte en unités sémantiques.`
- **T1** `- **L'attachement par tête couvre 100 %**, mais le gold ne donne **qu'une** lecture des`
- **T1** `ambiguïtés (le GP au verbe) ; le 40 % des réels est un **désaccord de lecture**, pas seulement`
- **T1** `Quadro RTX 5000, 1 MiB, 0 %`
- **T1** `[still running after 60000ms; moved to background job bash-38]`
- **T1** `/dev/mapper/system-root   11T  9,0T  2,0T  83% /home/stephane/Data13TB`
- **T1** `| [rapport-speculatif-reflexe.md](rapport-speculatif-reflexe.md) | Le réflexe propose, le cerveau vérifie — acceptation 2 à 30 % (le cerveau non entraîné : 0 %) |`
- **T1** `| [rapport-vitesse-v41.md](rapport-vitesse-v41.md) | Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé |`
- **T1** `| 00:12 | `713c0bbc` | B13 — LA DÉRIVE CONTINUE : 5 % → 50 %, v FINAL 0,5, 20/20, 8,6 PAS ; 56/56 |`
- **T1** `| 00:17 | `19da83fb` | B13 — LA RUPTURE : 90 % D'ERREUR, v FINAL 0,12, 20/20, 8,0 PAS ; 57/57 |`
- **T1** `246:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `| **B5** | la sémantique des jeux : contrat [RSN-jeu](../theorie/glossaire/entrees/rsn-jeu.md), cinq niveaux, bruit | ✅ | aucune — 112 items, **100 %** au niveau 4 |`
- **T1** `| **B6** | la logique dans la pensée : règles, recherche, cartes, invariance | ✅ | aucune — perft, **3/3** mats, dames **20/20**, cartes **79,7 %** |`
- **T1** `| **B8** | les maîtres : 17 principes, 9 sources, livre, parties | ✅ | aucune — livre **10/10**, go 9×9 **10/10** contre 3/10, cartes **44,7 %** |`
- **T1** `| **B11** | la base d'universaux typés : schéma, [parseur](../theorie/glossaire/entrees/parseur.md), codec, contexte | ✅ | **B11.10 close** (cartes, ambiguïtés refusées) ; le codec lit **100 %** |`
- **T1** `| **C3.2** | les modules par famille de langues | ✅ | aucune — **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤ 0,5 %** |`
- **T1** `**Ce qui compte pour R** : le **codec classique** lit **100 %** des surfaces ; c'est la preuve qu'un bloc`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-pensee-bord-fin.md`](rapport-pensee-bord-fin.md) | **B13** — le bord fin : 73 % à 0,38, 100 % à 0,41, **87/87** |`
- **T1** `| [`rapport-pensee-courbe20.md`](rapport-pensee-courbe20.md) | **B13** — la courbe sur 20 graines : 20 % à 0,35, 100 % à 0,41, **86/86** |`
- **T1** `| [`rapport-pensee-seuil.md`](rapport-pensee-seuil.md) | **B13** — le seuil d'oubli : ×0,5 réussit, ×0,2 échoue, seuil dans (0,2 ; 0,5], **74/74** |`
- **T1** `| [`rapport-pensee-oubli.md`](rapport-pensee-oubli.md) | **B13** — la mémoire courte : Q × 0,9/10, 20/20, 10,0 pas, **71/71** |`
- **T1** `| [`rapport-pensee-ultra-rare.md`](rapport-pensee-ultra-rare.md) | **B13** — l'information ultra-rare : utile 0,1 %, 4 looks, v final 0,44, 20/20, **68/68** |`
- **T1** `| [`rapport-pensee-tres-rare.md`](rapport-pensee-tres-rare.md) | **B13** — l'information très rare : utile 1 %, v final 0,54, 20/20, 8,0 pas, **67/67** |`
- **T1** `| [`rapport-pensee-rare.md`](rapport-pensee-rare.md) | **B13** — l'information rare : utile 10 %, v final 0,8, 20/20, 8,0 pas, **66/66** |`
- **T1** `| [`rapport-pensee-rupture.md`](rapport-pensee-rupture.md) | **B13** — la rupture : 90 % d'erreur, v final 0,12, 20/20, 8,0 pas, **57/57** |`
- **T1** `- **Les dix corpus Wikipédia en texte intégral** : 20,53 M articles, 67,73 G caractères, 81,2 Go, 8 Ko 0 partout ; l'anglais clos à 99,2 % (l'écriture bloquée à 125/125 Go, le manifeste reconstruit de`
- **T1** `- **Le corpus PDF** : 2 785 PDF, 1 927 documents, 322 Mo, 8 Ko 0, licences nommées.`
- **T1** `- **Le corpus Documents** : 7 459 PDF, 3 384 documents, 872 M caractères, 8 Ko 2,07 % (les 372 tronçons dupliqués).`
- **T1** `- **Le corpus OCR** : 20 livres, 7 381 pages, 15,36 M caractères, 8 Ko 0 (val 115 fenêtres, éval 0/40) ; le pilote `--max-doc 20` est clos (le 20e, *Life Histories of Etnos Theory*, 450 p).`
- **T1** `- **Le corpus OCR du CEGEP** : 10 notes scannées, 1 596 pages, 2 519 507 caractères, 8 Ko 0 (val 11 fenêtres) — le pilote `--racine CEGEP` ferme la boucle « livres, CEGEP, collections » (4 *Algorithms`
- **T1** `- **Les genres** : l'encyclopédie 103–147 car/ligne, les livres et documents 32–37, les lignes dupliquées 8,7–24 % (l'OCR 4,8 %).`
- **T1** `- **A2.6/A8.3** : le lot ne divise pas les lectures denses (+27 % de calcul, PPL −0,006 %).`
- **T1** `- **15 h 06 — reboot.** Les deux GPU étaient bloqués (`GPU requires reset`, `nvidia_drm refcnt -1`) ; le reset logiciel a échoué et le reboot a rendu les cartes (1 Mio, 0 %). Les deux sessions de trav`
- **T1** `- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 intérieur, ×62,7 tout ; [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../reports/rapport-typogly`
- **T1** `-- **S — le banc de structures** : outil web (`tools/structures`), générateur, pragmatique (niveaux 0–4), export ; analyseur **7/7** séquences, **93,9 %** de couverture, **19 tests** ; [`analyseur`](.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `-| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | 🔬 **v0** : 7 phrases + **générateur** + **pragmatique** (statuts, double sens conservé, **niveaux 0–4**, n`
- **T1** `+| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v2** : rôles **contextuels** et subordonnées typées, gold **39** phrases ; analyseur **38/39** types (`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : Error: could not connect to ollama server, run 'ollama serve' to start it --- total 1656188 drwxr-xr-x. 1 stephane stephane       138 15 oct 09:02 . drwxr-xr-x. 1 stephane stephane       100 15 oct 09
- **T1** : > Tu es un étiqueteur linguistique. Réponds UNIQUEMENT par un objet JSON valide, sans texte autour. Schéma : {"langue":"fr","script":"Latn","etiquettes":[{"niveau":"phrase|pragmatique|syntagme|pos","t
- **T1** : Error: Failed to initialize samplers: std::exception  [ Prompt: 0,0 t/s | Generation: 0,0 t/s ]   Exiting... EXIT=0

