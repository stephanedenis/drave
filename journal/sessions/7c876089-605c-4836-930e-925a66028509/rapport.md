# Session 7c876089 — Tu es relecteur ADVERSARIAL dans

| | |
|---|---|
| Identifiant | `7c876089-605c-4836-930e-925a66028509` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 13:10 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 45 |
| Appels d'outils | 62 |
| Fichiers touchés | 2 |
| Commandes | 48 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français. Ton rôle est de TROUVER DES DÉFAUTS dans des correctifs récents, pas de les valider.  CONTEXTE : une session a corrigé, entre 13h et 13h10, une série de défauts trouvés par une relecture … [3429 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'i … [3709 caractères tronqués]

*62 appels d'outils.* Actions notables :

- bash — List recent commits and repo root
- bash — Show stats for target commits
- bash — Show main.rs diff of 901f28d part 1
- bash — Dump diffs a9fff24 and 86ddf12
- bash — Show rest of 901f28d main.rs diff
- bash — Show R4 cap diff
- bash — Grep flux modes and caps
- bash — Grep trace key logic
- read
- bash — Grep call sites in main.rs
- bash — Show options-actives diff
- bash — Show unknown flag diff and parser
- bash — Read banc MLA and replay diagnostics
- bash — Check build artifacts and models
- … et 39 autres

**Synthèse produite :**

⏵ Rapport transmis à l'agent parent

Le rapport complet (8 défauts prouvés, vérifications positives, limites) a été rendu ci-dessus et transmis à l'agent parent `bbd6969f`. Aucun fichier du dépôt n'a été touché, aucun processus de la campagne n'a été arrêté, et tous mes serveurs de test ont été tués.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/r4_probe.py` | 1 | 0 |
| `/tmp/r4_probe2.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List recent commits and repo root
- **T1** Show stats for target commits
- **T1** Show main.rs diff of 901f28d part 1
- **T1** Dump diffs a9fff24 and 86ddf12
- **T1** Show rest of 901f28d main.rs diff
- **T1** Show R4 cap diff
- **T1** Grep flux modes and caps
- **T1** Grep trace key logic
- **T1** Grep call sites in main.rs
- **T1** Show options-actives diff
- **T1** Show unknown flag diff and parser
- **T1** Read banc MLA and replay diagnostics
- **T1** Check build artifacts and models
- **T1** Read a9fff24 diff head
- **T1** Check working tree and build freshness
- **T1** Test whether binary reports unknown flag
- **T1** Read main function
- **T1** Check which commits touched src
- **T1** Run ppl with dashboard and many flags
- **T1** Run inference with dashboard
- **T1** Run ppl with dashboard, absolute paths
- **T1** Run inference with dashboard, absolute paths
- **T1** Test limit 1 NaN output
- **T1** Test act-topk honored in lot mode
- **T1** List trace write/read sites in model.rs
- **T1** Read FluxRelecteur
- **T1** Check memory and overcommit
- **T1** Look at tools and pair_factice
- **T1** Prove n_blocs allocation bypass on real server
- **T1** Run three R4 bypass scenarios with real PID
- **T1** Prove with_capacity(n) allocation hole
- **T1** Re-run probe with correct units
- **T1** Run the 11 tests in release
- **T1** Read flux_codec.py
- **T1** Read pair_factice lot handling
- **T1** Read D5 message placement
- **T1** Read codec decoder and TraceFlux
- **T1** Write traces at ctx 64 and 512
- **T1** Compare trace keys across window layouts
- **T1** Inspect MLA synthetic tool
- … et 8 autres

## 4. Mesures et résultats marquants

- **T1** `d89e340 Cache KV : int4/int4 mesuré (+364 %), la courbe a ses six premiers points`
- **T1** `da6415b Colab : le mode lot chiffré dans la recette (2,6 s contre 47,6 s à 20 ms par message)`
- **T1** `1bc0470 Règle R4 : plafond des allocations pilotées par le réseau (256 Mo)`
- **T1** `Règle R4 : plafond des allocations pilotées par le réseau (256 Mo)`
- **T1** `par `verifier_taille`, qui refuse au-delà de 256 Mo en NOMMANT la règle.`
- **T1** `- **D4** : `tools/pair_factice.py` ne lisait pas le mode lot (`n × 4` au lieu de`
- **T1** ``n × dimension × 4`) — il bloquait le client et mourait. C'est pour cela que le`
- **T1** `+/// annonce `n = 4 milliards` fait allouer `n × dimension × 4` octets AVANT tout`
- **T1** `+/// contrôle : jusqu'à ~15 To demandés au noyau. 256 Mo couvrent largement un lot`
- **T1** `+/// de 8 192 jetons × 8 192 canaux (268 Mo... soit un lot par fenêtre maximale).`
- **T1** `/// n'est plus bornée par la RAM (20 Go/s) mais par la VRAM (≈ 450 Go/s).`
- **T1** `/// en version 2 lirait `n × 4` octets d'un corps qui en fait `n × hidden × 4`,`
- **T1** `+| 45 | `README.md:34` | « Croisement push/pull à **10 %** de densité ✅ mesuré » | `reports/rapport-croisement-push-pull.md:43` : « **~22 %** … pas à 10 » ; le README lui-même le dit ligne 389 | CONTR`
- **T1** `+| 46 | `docs/vision.md:46,133,198` et `docs/histoire.md:12` | croisement « mesuré » à **10 %** | 22 % (rapport de référence + REPRISE §5.1 + `docs/convertisseur.md:225`) | CONTRADICTOIRE |`
- **T1** `+| 51 | `docs/contexte-long.md:103` | KV int4 « mesuré : **+384 %*`
- **T1** `+| 44 | `reports/rapport-compacite-trace.md:13-14` | « restent à faire : valeurs i8 (−60,9 %), échelles f16 (−63,5 %), zstd (−79 %) » | la v3 non commitée implémente déjà i8 + échelles f16 par bloc (``
- **T1** `d89e340 2026-09-30 13:06:14 -0400 Cache KV : int4/int4 mesuré (+364 %), la courbe a ses six premiers points`
- **T1** `da6415b 2026-09-30 13:00:18 -0400 Colab : le mode lot chiffré dans la recette (2,6 s contre 47,6 s à 20 ms par message)`
- **T1** `1bc0470 2026-09-30 12:57:35 -0400 Règle R4 : plafond des allocations pilotées par le réseau (256 Mo)`
- **T1** `ae85043 2026-09-30 12:30:38 -0400 DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité`
- **T1** `6b3b53f 2026-09-30 12:17:39 -0400 DRVF v2 sur le disque : −49,87 % de trace, rejeu identique`
- **T1** `// barrière ne tolère aucune sursouscription (mesuré : ×1,3 de perte à 40+1`
- **T1** `ae85043 DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité`
- **T1** `parcimonie imposée : seuil 10.0 % du max, k-WTA k=5`
- **T1** `5 tokens notés — perplexité cumulée 328866.777  (48.0 tok/s)`
- **T1** `[trace] 288 listes · 1296 neurones actifs · 0 Mo`
- **T1** `=== perplexité 328866.7766 sur 5 tokens (10136822 événements, 0.1 s) ===`
- **T1** `48.0 tok/s effectifs (avant + tête)`
- **T1** `part de l'attention dans le flux d'événements : 0.1 %`
- **T1** `gain FFN : couche 0 × 2`
- **T1** `parcimonie imposée : k-WTA garde 0.0 %, seuil 10.0 %`
- **T1** `prompt  : 3 tokens en 0.156 s  (19.3 tok/s, TTFT 51.8 ms)`
- **T1** `0 tokens notés — perplexité cumulée NaN  (0.0 tok/s)`
- **T1** `=== perplexité 410.7398 sur 5 tokens (0 événements, 0.5 s) ===`
- **T1** `=== perplexité 54171.2701 sur 5 tokens (0 événements, 0.5 s) ===`
- **T1** `=== perplexité 41524.7214 sur 5 tokens (0 événements, 0.5 s) ===`
- **T1** `=== perplexité 410.9033 sur 5 tokens (0 événements, 0.4 s) ===`
- **T1** `[sonde] après envoi (400 Mo d'échelles) : {'VmPeak': '5844 kB', 'VmSize': '5844 kB', 'VmRSS': '2440 kB'}`
- **T1** `[sonde] après envoi (400 Mo d'échelles) : {'VmPeak': '1576796 kB', 'VmSize': '1576796 kB', 'VmRSS': '1011704 kB'}`
- **T1** `réelle de 512 jetons : 132 396 736 octets en v1, **66 370 408** en v2 (−49,87 %),`
- **T1** `# LOT : `n` est le nombre d'ÉTATS, le corps fait n × dimension × 4.`
- **T1** `# Lire n × 4 (comme avant) laissait le client BLOQUÉ dans read_exact`
- **T1** `// f16 par bloc de 32 canaux (l'étude de compacité annonce −22 % de plus,`
- **T1** `// début et personne ne s'en apercevait (2 octets sur 132 Mo).`
- **T1** `[trace] 6240 listes · 5587213 neurones actifs · 17 Mo`
- **T1** `=== perplexité 345.5146 sur 127 tokens (0 événements, 61.0 s) ===`
- **T1** `[trace] 6240 listes · 5588199 neurones actifs · 17 Mo`
- **T1** `=== perplexité 168.6228 sur 129 tokens (0 événements, 56.6 s) ===`
- **T1** `LATENT (une seule tête de 128 + 32 valeurs par jeton au lieu de n_head × 192),`
- **T1** `[modele] 2 couches chargées en 8.820276ms — listes 0.00 Go , 20 threads`
- **T1** `référence locale  : perplexité 261.1724  (1.3 s)`
- **T1** `deux nœuds        : perplexité 151936.0000  (0.5 s)`
- **T1** `référence locale  : perplexité 994.2334  (2.1 s)`

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué. [options] 1 drapeau(x) INCONNU(S), don
- **T1** : [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.  thread 'main' (545252) panicked at sr
- **T1** : [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.  thread 'main' (545293) panicked at sr
- **T1** : [dos] réponse reçue : 0 octets (pas de panique) [dos] code de sortie : -6 0 Go , 2 threads [config] 24 couches, hidden 896 ·  [config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0 [
- **T1** : référence locale  : perplexité 994.2334  (2.1 s)  thread 'main' (569094) panicked at src/main.rs:2001:26: envoi du flux: Os { code: 32, kind: BrokenPipe, message: "Broken pipe" } note: run with `RUST_

