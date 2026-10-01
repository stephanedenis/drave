# Session 8288d350 — You are doing an ADVERSARIAL

| | |
|---|---|
| Identifiant | `8288d350-b68e-4245-b903-5ef6d71910b4` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-01 05:52 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 33 |
| Appels d'outils | 51 |
| Fichiers touchés | 0 |
| Commandes | 34 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — You are doing an ADVERSARIAL code review in the Rust repository /home/stephane/Data13TB/stephane/GitHub/Qtrinet. DO NOT MODIFY ANY FILE. Read-only analysis. Report findings in French, concisely but precisely, with file:line references and exact code quotes.  Context: a "livelock" bug was found and fixed in `drave-core/src/model.rs`: `KvCache::assurer` had `while cap < besoin { cap = (cap * 2).min( … [2916 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — You are doing an ADVERSARIAL code review in the Rust repository /home/stephane/Data13TB/stephane/GitHub/Qtrinet. DO NOT  … [3196 caractères tronqués]

*51 appels d'outils.* Actions notables :

- bash — Show recent git log and status
- bash — List repo layout and count tests
- bash — Show commit 32951e9 diff
- bash — Show commit c7fd7ea diff
- bash — Grep all assurer call sites
- bash — Count tests per file
- read
- bash — Locate generate/forward/forward_lot definitions
- bash — Find KV write sites
- bash — Find the observed run output in digest
- bash — Read digest around observed run
- bash — Find call sites in main.rs
- bash — Look for panic evidence in session trace
- bash — Check Cargo profile and ids option
- … et 23 autres

**Synthèse produite :**

⏵ Rapport final : verdict, chemins non bornés, test, comptage

Rapport transmis à l'agent parent. Analyse strictement en lecture (aucun fichier du dépôt modifié ; seuls `target/`, `/tmp` et le binaire existant ont servi aux vérifications).

\# (a) Verdict sur le correctif — INCOMPLET

**La boucle est bien terminée et `cap ≤ ctx` toujours** (y compris `ctx == 0`) :
- `drave-core/src/model.rs:1118` `if besoin <= self.cap { return; }`
- `drave-core/src/model.rs:1126` `let besoin = besoin.min(self.ctx);`
- `drave-core/src/model.rs:1129` `while cap < besoin { cap = (cap * 2).min(self.ctx); }`

**Mais l'invariant annoncé est faux et le scénario revendiqué ne fonctionne pas.**
1. `drave-core/src/model.rs:1124-1125` affirme « l'appelant voit la troncature par le message ci-dessous » : **faux**. Le message n'existe que dans `generate`. `ecrire` ne teste que `pos + 1 > self.cap` (`model.rs:1210`) puis indexe `let d = (kvh * self.cap + pos) * self.hd;` (`model.rs:1211`) : au-delà de `ctx`, `assurer` ne grandit plus, l'écriture part dans le **bloc de la tête KV suivante** (corruption silencieuse) puis panique sur la dernière tête. Le plafond convertit le livelock en OOB.
2. `generate` tronque à `ctx` **sans réserver `n_new`** (`model.rs:3930-3934` → `ids.len() == ctx`), puis la décodage fait `model.rs:3976-3977` `let pos = ids.len() + step; last = self.forward(next, pos);` — et le seul garde est `model.rs:3025` `assert!(pos < self.ctx, "contexte dépassé ({pos} ≥ {})", self.ctx);`. **Dès le 1er jeton généré : panique** (release `panic = "abort"` → SIGABRT, exit 134). Le mode session, lui, fait le bon calcul (`main.rs:851-856`, `ids.len() + n_new + 8 > ctx` → `garde = ctx - (n_new + 8)`), pas `generate`.

**Preuves (binaire release du dépôt, Qwen2.5‑0.5B)**
| essai | résultat |
|---|---|
| `--ids 1..12 --n 2 --ctx 8 --lot 4` | message de troncature puis `panicked at src/model.rs:3025:9: contexte dépassé (8 ≥ 8)`, exit **134** |
| invite 6 ≤ ctx 8, `--n 4` (la génération dépasse) | même panique, exit **134** |
| réplique exacte des drapeaux du digest (`--infer --chat --flux --prompt … --n 8 --ctx 8 --threads 16 --temp 0 --lot 4`) | message puis même panique, exit **134** |
| `--ppl-reparti … --ids <40> --ctx 8 --limit 4 --lot 4` | `panicked at src/model.rs:1213:20: range end index 1088 out of range for slice of length 1024`, exit **134** |

**Le « vérifié : rend la main en 312 s » est un abort.** La commande exacte, extraite de `journal/.../session.jsonl.zstd`, est `--inf
… [5943 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Show recent git log and status
- **T1** List repo layout and count tests
- **T1** Show commit 32951e9 diff
- **T1** Show commit c7fd7ea diff
- **T1** Grep all assurer call sites
- **T1** Count tests per file
- **T1** Locate generate/forward/forward_lot definitions
- **T1** Find KV write sites
- **T1** Find the observed run output in digest
- **T1** Read digest around observed run
- **T1** Find call sites in main.rs
- **T1** Look for panic evidence in session trace
- **T1** Check Cargo profile and ids option
- **T1** Read digest context around panics
- **T1** Check zstd availability
- **T1** Find ctx-overflow asserts in source
- **T1** Stream raw trace for panic evidence
- **T1** Extract full command of the 312s run
- **T1** List available models and binary
- **T1** Run over-long prompt with lot=4, ctx=8
- **T1** Read gpu kv_assurer guard
- **T1** Test generation crossing ctx with lot=1
- **T1** Test ppl-reparti ids beyond ctx
- **T1** Enumerate KV writes and forward calls
- **T1** Read the new test and test module
- **T1** Run cargo test release in background
- **T1** Check chat branch condition and harmony windows
- **T1** Inspect GPU attn_kv bounds
- **T1** Read fenetres_harmony
- **T1** Find session flag source
- **T1** Locate cache allocation and harmony lines
- **T1** Check model ctx vs kv ctx wiring
- **T1** Count tests before and after the fix
- **T1** Replicate digest command shape with tiny ctx

## 4. Mesures et résultats marquants

- **T1** `783f1f9 Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384`
- **T1** `0d50e75 À 8 192 clés, k=1024 (12,5 %) suffit : le k nécessaire croît plus lentement que le contexte (deux points)`
- **T1** `était resté, et une invite de 4 788 jetons avec `--ctx 4608` tournait à ~1 700 % de`
- **T1** `+        // `--ctx 4608` tournait à ~1 700 % de CPU pendant plus de 22 minutes sans`
- **T1** `| `7d0d2578` | 2026-09-30 11:53 | 0.6 Mo | 68 Ko | 1 | 41 | 53 | 0 | 0 |`
- **T1** `| `8e04c99a` | 2026-09-30 18:17 | 0.7 Mo | 118 Ko | 1 | 59 | 85 | 0 | 0 |`
- **T1** `| `aa5f9fc5` | 2026-09-30 15:17 | 0.8 Mo | 129 Ko | 1 | 78 | 100 | 0 | 0 |`
- **T1** `-| `bbd6969f` | 2026-10-01 05:39 | 19.0 Mo | 2313 Ko | 48 | 2535 | 2401 | 11 | 6 |`
- **T1** `+| `bbd6969f` | 2026-10-01 05:46 | 19.0 Mo | 2321 Ko | 48 | 2545 | 2411 | 11 | 6 |`
- **T1** `| `bcfe0b97` | 2026-09-30 12:39 | 1.0 Mo | 145 Ko | 1 | 102 | 110 | 0 | 0 |`
- **T1** `| `c25f97d1` | 2026-09-30 11:59 | 0.8 Mo | 126 Ko | 1 | 73 | 104 | 0 | 0 |`
- **T1** `| `c776b71f` | 2026-09-30 18:43 | 0.7 Mo | 82 Ko | 1 | 35 | 54 | 0 | 0 |`
- **T1** `| `da69b1fa` | 2026-09-30 15:13 | 0.5 Mo | 56 Ko | 1 | 37 | 45 | 0 | 0 |`
- **T1** `| `e7dfe34f` | 2026-09-28 14:59 | 0.2 Mo | 28 Ko | 1 | 20 | 21 | 0 | 0 |`
- **T1** `-Total : 47.7 Mo de traces brutes.`
- **T1** `+Total : 47.8 Mo de traces brutes.`
- **T1** `+        // `n_blocs × 4` octets + un Vec<f32> (mesuré : 16 Gio sur une trame de`
- **T1** `- **T1** : 511 tokens notés — perplexité cumulée 247.031  (4.9 tok/s) === perplexité 247.0308 sur 511 tokens (0 événements, 104.5 s) ===  ### B3 harmony assistant 511 --- ref --- 0.0 0.0 0:00 ls: cann`
- **T1** `entre 12,5 % et 25 % du contexte sur ce cas.`
- **T1** `KV, lui, ne pèse que 0,25 %.`
- **T1** `+| 1 | **Noyau fusionné du top-k** : descente radix + collecte + somme en UN noyau par ligne | 8 lancements → 2 · tampon `nh × n × 4` supprimé · écart 7,2e-7 (avec puits) et 8,4e-7 (sans) |`
- **T1** `+| 2 | **Le déport du top-k gagne** | attention plate 4,5–5,0 ms/jeton de 255 à 4 095 clés · croisement ~300 clés · ×7,8 à 4 095 clés |`
- **T1** `+| 3 | **Le préremplissage déporté** | prompt de 3 961 jetons : **286,6 → 63,8 s** (×4,5) · perplexité 9,4335 / 9,4337 (écart relatif 2,1e-5) |`
- **T1** `+| 5 | **Le noyau fusionné gagne au décodage, jusqu'à 16 k clés** | GPU plat, CPU 4,26 → 38,84 ms/jeton · k = 1 024 suffit à 8 192 clés (12,5 %) |`
- **T1** `+| 6 | **L'attention creuse à 6 % échoue sur 1 fenêtre sur 3** (4 096 clés, milieu) | dense 3/3 · k = 256 **1/3** · k = 1 024 3/3 · par fenêtre, 8/9 en dense sur neuf fenêtres contiguës |`
- **T1** `-| `bbd6969f` | 2026-10-01 05:46 | 19.0 Mo | 2321 Ko | 48 | 2545 | 2411 | 11 | 6 |`
- **T1** `+| `bbd6969f` | 2026-10-01 05:46 | 19.0 Mo | 2321 Ko | 48 | 2546 | 2412 | 11 | 6 |`
- **T1** `// `n_blocs × 4` octets + un Vec<f32> (mesuré : 16 Gio sur une trame de`
- **T1** `transport         : listes à échelle par bloc (2 octets/actif, écarts) · 1868 octets par flux (aller) · 159 au retour · 95.4 % d'activité (854 neurones par flux) · 2 flux`
- **T1** `temps             : 14.4 ms par jeton en local · 0.4 ms à attendre le pair (son calcul + l'aller-retour) · soit 0.03× le calcul local seul`
- **T1** `'78.6 % d\'activité (704 neurones par flux) · 256 flux\\n  temps             : 16.8 ms par jeton en local · 17.1 ms à attendre le pair (son calcul + l\'aller-retour) · soit 1.01× le calcul local seul\`
- **T1** `"r flux (aller) · 2971 au retour · 78.6 % d'activité (704 neurones par flux) · 256 flux\\n  temps             : 16.8 ms par jeton en local · 17.1 ms à attendre le pair (son calcul + l'aller-retour) · `
- **T1** `'ons\\n  référence locale  : perplexité 36.0178  (4.8 s)\\n[flux] le nœud moteur a fermé la connexion (failed to fill whole buffer).\\n       Cause la plus probable : il a REFUSÉ le lot (son contexte `
- **T1** `"afonne à `ctx`). Le même défaut avait été corrigé côté GPU au sprint 2\\\\n(`kv_assurer`) ; le chemin CPU était resté.\\\\n\\\\nCorrectif : la capacité est plafonnée au contexte déclaré, et `Model::g`

## 5. Erreurs rencontrées

6 sorties en erreur ou divergentes. Les premières :

- **T1** : écart             : 5.39e0   transport         : listes à échelle par bloc (2 octets/actif, écarts) · 1868 octets par flux (aller) · 159 au retour · 95.4 % d'activité (854 neurones par flux) · 2 flux 
- **T1** : locage muet\\n\\nLe lot 128 faisait tomber le programme sur :\\n\\n```\\nthread '<unnamed>' panicked at src/engine.rs:473:77:\\nindex out of bounds: the len is 90 but the index is 90\\n```\\n\\n`90` =
- **T1** : EXIT=134 [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué. [config] cache KV : 32 bits, 
- **T1** : === A: invite 6 < ctx 8, n=4 (la génération dépasse) === EXIT=134 Qwen2 · 24 couches · hidden 896 · 14 têtes / 2 KV · FFN 4864 · vocab 151936  thread 'main' (2720544) panicked at src/model.rs:3025:9: 
- **T1** : === B: ppl-reparti --ids 40 > ctx 8, lot 4 === EXIT=134 [config] rotation : RoPE simple (le modèle ne déclare pas YaRN) [flux] quantification : 127 niveaux, seuil 0, top-k 0, renorm false [flux] pilot
- **T1** : EXIT=134 9:[contexte] invite de 29 jetons > ctx 8 : les 21 premiers sont ABANDONNÉS (troncature, pas de fenêtrage) 11:thread 'main' (2721397) panicked at src/model.rs:3025:9: [stderr] bash: line 1: 27

