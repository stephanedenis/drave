# Session bcfe0b97 — Tu es relecteur ADVERSARIAL dans

| | |
|---|---|
| Identifiant | `bcfe0b97-1795-4610-8e8b-b598ca1ba6cb` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 12:20 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 101 |
| Appels d'outils | 110 |
| Fichiers touchés | 0 |
| Commandes | 86 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, paquet `drave-core`, binaire `drave`). Documentation et rapports en FRANÇAIS : écris en français. Ton rôle est de TROUVER DES DÉFAUTS, pas de valider.  CONTEXTE : une session de travail vient d'ajouter, en une douzaine de commits, (a) un mode « l … [3823 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'i … [4103 caractères tronqués]

*110 appels d'outils.* Actions notables :

- bash — List recent commits and status
- bash — List repo structure and source sizes
- todo_write
- bash — Show stats of key commits
- bash — Show diff of lot mode commit
- bash — Find protocol constants lines
- bash — Find model functions lines
- bash — Show topk transport commit diff
- read
- bash — Re-grep model.rs functions with checksum
- bash — Check working tree state and time
- bash — Inspect concurrent uncommitted edits
- bash — Extract HEAD and cda3162 sources to /tmp
- bash — Check models, data and existing binary/traces
- … et 76 autres

**Synthèse produite :**

⏵ Rédaction du rapport final et envoi au parent

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List recent commits and status
- **T1** List repo structure and source sizes
- **T1** Show stats of key commits
- **T1** Show diff of lot mode commit
- **T1** Find protocol constants lines
- **T1** Find model functions lines
- **T1** Show topk transport commit diff
- **T1** Re-grep model.rs functions with checksum
- **T1** Check working tree state and time
- **T1** Inspect concurrent uncommitted edits
- **T1** Extract HEAD and cda3162 sources to /tmp
- **T1** Check models, data and existing binary/traces
- **T1** Check docs and fake peer for version 4
- **T1** Locate DRVF code in HEAD model.rs
- **T1** Identify DRVF trace versions in /tmp
- **T1** Locate flux-forcer code at HEAD
- **T1** Look for existing tests
- **T1** Read flux-forcer reporting and lot option
- **T1** Read start of pair_factice.py
- **T1** Check commit times and last main.rs change
- **T1** Show drave help
- **T1** Find gate commands and available GGUF models
- **T1** Find gate command and other models
- **T1** Read REPRISE gate commands
- **T1** Check token id files and gpt-oss model
- **T1** Show plumbing commit diff
- **T1** Find option defaults at HEAD
- **T1** Check CPU count, id files, run_ppl threads
- **T1** Inspect threading of matvec
- **T1** Read Pool implementation
- **T1** Find Pool definition
- **T1** Read Pool in engine.rs
- **T1** Run Qwen non-regression gate
- **T1** Find flux_lot and trace counter
- **T1** Read flux_lot callers and token counter
- **T1** Find forward_lot usages in main
- **T1** Read run_ppl lot branch
- **T1** Read single-token trace key scheme
- **T1** Check claims in prefill report
- **T1** Run fake peer with dense client
- … et 46 autres

## 4. Mesures et résultats marquants

- **T1** `6b3b53f DRVF v2 sur le disque : −49,87 % de trace, rejeu identique`
- **T1** `af18f29 Transport en listes à 1 024 jetons : ÷2,3 pour 1,3 % d'écart`
- **T1** `disque coûte 6,04 octets par neurone actif (66 % d'indices u32) : indices par`
- **T1** `écarts = −49,7 % sans perte, avec blocs i8 = −60,9 %, + zstd = −79 %.`
- **T1** `DRVF v2 sur le disque : −49,87 % de trace, rejeu identique`
- **T1** `L'étude de compacité déléguée disait où était le gras : **66 % du fichier est fait`
- **T1** `précédent tient sur un octet dans 99,9997 % des cas (22 échappements sur 8,79 M`
- **T1** `| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |`
- **T1** `132 Mo, mais la comptabilité mentait depuis le premier jour).`
- **T1** `+/// en version 2 lirait `n × 4` octets d'un corps qui en fait `n × hidden × 4`,`
- **T1** `+/// payait 256 allers-retours. Le corps fait `n × hidden × 4` octets ; la`
- **T1** `/// en version 2 lirait `n × 4` octets d'un corps qui en fait `n × hidden × 4`,`
- **T1** `+    /// canaux, ~22 % plus petit, avec perte).`
- **T1** `+        // f16 par bloc de 32 canaux (l'étude de compacité annonce −22 % de plus,`
- **T1** `// début et personne ne s'en apercevait (2 octets sur 132 Mo).`
- **T1** `// neurone précédent tient sur UN octet dans 99,9997 % des cas mesurés`
- **T1** `| la taille suit l'activité | densité ÷2,3 → trace ÷2,5 (132 Mo → 53 Mo) |`
- **T1** `| un lot ne change pas le résultat non plus | 256 jetons en 4 lots de 64 : écart **0,00e0** (18,0851 = 18,0851) ; en 1 lot de 256 : **0,00e0** (918 ko sur le fil) |`
- **T1** `40:99,9997 % des cas (22 échappements sur 8 790 000 mesurés). Trois octets par`
- **T1** `45:| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |`
- **T1** `6b3b53f 2026-09-30 12:17:39 -0400 DRVF v2 sur le disque : −49,87 % de trace, rejeu identique`
- **T1** `reports/rapport-compacite-trace.md:6:> **identique** (perplexité 19,3885 dans les deux cas), et la relecture par`
- **T1** `reports/rapport-transport-liste.md:47:(19,3885), mais ici 16 bits coûtent 2,6 % : la différence n'est pas la précision,`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:23746:=== perplexité 19.3885 sur 510 tokens (0 événements, 16.4 s) ===`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:23775:=== perplexité 19.3885 sur 510 tokens (0 événements, 16.5 s) ===`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:23777:=== perplexité 19.3885 sur 510 tokens (0 événements, 16.8 s) ===`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:23916:| Qwen2.5-0.5B | Q8_0 | 19,3885 | 32 tok/s | **0,81 s** | **0,57 Go** |`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:24901:=== perplexité 19.3885 sur 510 tokens (0 événements, 14.6 s) ===`
- **T1** `[timed out after 60000ms]`
- **T1** `#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le`
- **T1** `// Défauts du mode PERPLEXITÉ : 256 jetons, trois quarts des cœurs, 16 bits`
- **T1** `/// survivent au-delà (bug trouvé par le banc : divergence au rang 895).`
- **T1** `// sur 128, soit 6 % du FFN — et c'est le régime où l'architecture`
- **T1** `60:ligne relisait *tout* le lot d'activations (64 × 896 × 4 = 229 Ko) — 4 864`
- **T1** `131:1. **La tête en lot ne gagne rien** (5,47 contre ~5,63 ms/jeton). L'argument de`
- **T1** `194:| gpt-oss-120b MXFP4, MoE groupé, 16 fils | 256 | ≈ 50 s | 34,4 s (lot 256) | **−31 %** |`
- **T1** `référence locale  : perplexité 994.2334  (1.3 s)`
- **T1** `deux nœuds        : perplexité 151936.0000  (0.1 s)`
- **T1** `transport         : dense f32 · 3663 octets par flux (aller) · 3663 au retour · 100.0 % d'activité (896 neurones par flux) · 3 flux`
- **T1** `temps             : 46.2 ms par jeton en local · 0.4 ms à attendre le pair (son calcul + l'aller-retour) · soit 0.01× le calcul local seul`
- **T1** `référence locale  : perplexité 995.8546  (0.5 s)`
- **T1** `[modele] 24 couches chargées en 902.774515ms — listes 0.00 Go , 4 threads`
- **T1** `référence locale  : perplexité 148.1267  (3.0 s)`
- **T1** `deux nœuds        : perplexité 148.1267  (2.9 s)`
- **T1** `transport         : LOTS de 8 jetons · 28751 octets par lot (aller) · 3.5 ko par jeton · 5 lots (au lieu de 39 flux)`
- **T1** `temps             : 237.9 ms par LOT en local · 247.9 ms à attendre le pair · soit 1.04× le calcul local seul`
- **T1** `7 tokens notés — perplexité cumulée 795.033  (10.8 tok/s)`
- **T1** `[trace] 384 listes · 343492 neurones actifs · 1 Mo`
- **T1** `=== perplexité 795.0325 sur 7 tokens (0 événements, 0.7 s) ===`
- **T1** `7 tokens notés — perplexité cumulée 795.210  (12.2 tok/s)`
- **T1** `[trace] 384 listes · 343497 neurones actifs · 1 Mo`
- **T1** `=== perplexité 795.2102 sur 7 tokens (0 événements, 0.6 s) ===`
- **T1** `[modele] 24 couches chargées en 819.150997ms — listes 0.00 Go , 4 threads`
- **T1** `7 tokens notés — perplexité cumulée 6215.557  (11.7 tok/s)`
- **T1** `=== perplexité 6215.5568 sur 7 tokens (0 événements, 0.6 s) ===`
- **T1** `11.7 tok/s effectifs (avant + tête)`
- **T1** `part de l'attention dans le flux d'événements : 100.0 %`
- **T1** `[modele] 24 couches chargées en 847.749472ms — listes 0.00 Go , 4 threads`
- **T1** `7 tokens notés — perplexité cumulée 795.210  (10.4 tok/s)`
- **T1** `=== perplexité 795.2102 sur 7 tokens (0 événements, 0.7 s) ===`
- **T1** `10.4 tok/s effectifs (avant + tête)`
- **T1** `7 tokens notés — perplexité cumulée 795.210  (11.3 tok/s)`
- **T1** `7 tokens notés — perplexité cumulée 795.210  (11.2 tok/s)`
- **T1** `7 tokens notés — perplexité cumulée 795.210  (11.4 tok/s)`
- **T1** `ae85043 DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité`
- **T1** `DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité`
- **T1** `| erreur par valeur | — | nulle | RMS 0,085 % du max |`
- **T1** `Soit −65,9 % depuis la v1 pour +0,074 % de perplexité. La v3 est AVEC PERTE, donc`
- **T1** `| trace dense, 512 jetons | 66 370 408 o | **45 079 930 o (−32,1 %)** |`
- **T1** `| rejeu `--flux-forcer` | 19,3885 | **19,4029 (+0,074 %)** |`
- **T1** `| neurones actifs | 22 008 776 | 21 630 645 (−1,7 % : les valeurs qui s'arrondissent à zéro ne sont pas écrites) |`
- **T1** `| erreur par valeur | nulle | RMS **0,085 %** du max de la liste (max 0,394 %) |`
- **T1** `26521:perplexité 1958.7210 sur 510 tokens`
- **T1** `26600:=== perplexité 1958.7210 sur 510 tokens (0 événements, 23.2 s) ===`
- **T1** `trace] 24576 listes · 22008776 neurones actifs · 66 Mo`
- **T1** `perplexité 19.3885 sur 510 tokens`
- **T1** `perplexité 1958.7210 sur 510 tokens`
- **T1** `Le rejeu v2 est bon (19,3885, −49,87 % de taille) mais l'ancienne trace v1 ne se relit plus : je vérifie l'hypothèse d'un en-tête historique de 16 octets.`
- **T1** `=== perplexité 19.3885 sur 510 tokens (0 événements, 21.9 s) ===`
- **T1** `=== perplexité 1958.7210 sur 510 tokens (0 événements, 23.2 s) ===`
- **T1** `référence locale  : perplexité 102.6664  (4.5 s)`
- **T1** `référence locale  : perplexité 160.5998  (3.2 s)`
- **T1** `deux nœuds        : perplexité 160.5998  (3.3 s)`
- **T1** `transport         : LOTS de 8 jetons · 26362 octets par lot (aller) · 3.2 ko par jeton · 6 lots (au lieu de 43 flux)`

## 5. Erreurs rencontrées

6 sorties en erreur ou divergentes. Les premières :

- **T1** : [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.  thread 'main' (391048) panicked at sr
- **T1** : (no output) [exit code: 1]
- **T1** : |         ^^^^^^^^^^^^ help: use shorthand field pattern: `mut ids`     |     = note: `#[warn(non_shorthand_field_patterns)]` on by default  [exit code: 2]
- **T1** : ########## 1. SERVEUR ANCIEN (cda3162, en-tête 39 o) + CLIENT NOUVEAU (HEAD, 79 o)   client nouveau exit=134   --- serveur ancien : [flux] arrêt : magie de flux absente [flux] 1 flux servis   --- clie
- **T1** : === panic client nouveau (x1) === thread 'main' (487435) panicked at src/main.rs:1879:60: réception du flux: Os { code: 104, kind: ConnectionReset, message: "Connection reset by peer" } note: run with
- **T1** : [stderr] bash: -c: line 1: syntax error near unexpected token `(' bash: -c: line 1: `cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo "== working tree (état 12:40) =="; grep -n "listes_blocs

