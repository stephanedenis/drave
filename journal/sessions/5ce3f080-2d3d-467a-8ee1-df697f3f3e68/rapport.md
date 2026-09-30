# Session 5ce3f080 — Tu es relecteur ADVERSARIAL dans

| | |
|---|---|
| Identifiant | `5ce3f080-2d3d-467a-8ee1-df697f3f3e68` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 15:32 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 70 |
| Appels d'outils | 77 |
| Fichiers touchés | 9 |
| Commandes | 47 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français. Ton rôle est de TROUVER DES DÉFAUTS, pas de valider.  CONTEXTE : le protocole de flux réseau vient de passer en **version 5** avec un cinquième mode, le **mode 4 « lot en listes »** (com … [3649 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'i … [3929 caractères tronqués]

*77 appels d'outils.* Actions notables :

- bash — Show recent log and commit stat
- bash — Count lines of relevant docs
- bash — Show main.rs diff for commit
- read
- bash — Locate key functions and constants
- bash — Read flux_en_liste_blocs implementation
- bash — Read plat/forward_lot and list models
- bash — Check worktree state and history
- bash — Show uncommitted changes to main.rs
- bash — Find CLI flags for mode 4
- bash — Check CPUs, running drave, cargo config
- bash — Run release test suite with 2 threads
- bash — Read forward_lot
- bash — Read quant_scratch
- … et 45 autres

**Synthèse produite :**

⏵ Rapport final.

\# Relecture adversariale — mode 4 « lot en listes », protocole v5

**Méthode.** `git show 8e132aa`, lecture du code en place (l'arbre de travail contient 3 tests non commités en plus de HEAD), `cargo test --release` (17/17 ✓), un **pair Python v5 indépendant** (`/tmp/m4_peer.py`) qui décode ce qu'émet le vrai client, un **client Python hostile** (`/tmp/m4_attack.py`) qui forge des trames contre le vrai serveur, et des mesures réelles. Aucun fichier du dépôt modifié ; les scripts sont dans `/tmp`. Serveurs : un par trame, `timeout ≤ 110 s`, `--threads 2`, tous tués ; le processus de campagne (691410) est intact.

---

\## 1. Défauts prouvés

\### D1 — GRAVE : le garde **cumulatif** de R4 promis par le plan n'existe pas

Le plan l'exige trois fois : §1.3 R4 (« le cumul du corps aussi »), §4.5 (« `cumul += 12 + 4·n_blocs_j + longueur_j` puis `verifier_taille(cumul, "corps du lot en listes (cumul)")`. Sans lui, un pair peut annoncer `t × 256 Mo` de corps licites un par un : la mémoire resterait bornée (on décode état par état) mais le temps, non ») et §8 étape 2 (`lire_etat_blocs(s, j, hidden, dst, cumul)`).

Le code accumule exactement ce cumul… et ne le vérifie jamais :

```rust
// main.rs:1808  -> seul le cumul d'UN état est contrôlé
verifier_taille(12usize.saturating_add(nb.saturating_mul(4)).saturating_add(lg), ...)?;
...
// main.rs:1840  -> la variable EST le cumul ; aucun verifier_taille(lus, ...) nulle part
lus += 12 + nb * 4 + lg;
```

**Preuve exécutable** (trame K) : état 0 légal au bord du plafond (`a=67 108 833`, `nb=28`, `lg=268 435 330` → `12+4·28+lg = 268 435 454 ≤ 268 435 456`), 268 Mo réellement envoyés, puis le préfixe de l'état 1 annonçant autant — cumul annoncé **536 870 908 > 268 435 456** :

```
etat 0 (268 Mo) envoye + prefixe de l'etat 1 (268 Mo de plus)
cumul annonce = 536 870 908 octets > plafond 268 435 456
AUCUN refus : le serveur lit encore l'etat 1 (pas de garde cumulatif)
srv: [flux] arrêt : failed to fill whole buffer     <- seulement quand MOI je ferme
```

Avec `n = 74 898` (maximum accepté pour hidden = 896), le corps annoncé atteint ≈ 19 Po.

\### D2 — GRAVE : le refus `n == 0` (commit voisin `64a86ca`) est **faux** pour les modes 1/2 et tue une session légitime

`main.rs:1776-1779` refuse tout flux `n == 0`, **tous modes, avant le dispatch** — donc « oui, il couvre tous les modes », et c'est précisément le défaut. Or `n = 0` est **représentable** :

* `flux_en_liste_blocs` (`model.rs:3638-3662`) : `seuil = a
… [12034 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/m4_peer.py` | 1 | 0 |
| `/tmp/m4_attack.py` | 1 | 0 |
| `/tmp/run_e2e.sh` | 1 | 0 |
| `/tmp/run_matrix.sh` | 1 | 0 |
| `/tmp/run_attack.sh` | 1 | 0 |
| `/tmp/run_suite2.sh` | 1 | 0 |
| `/tmp/m4_badreply.py` | 1 | 0 |
| `/tmp/run_suite3.sh` | 1 | 0 |
| `/tmp/run_suite4.sh` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Show recent log and commit stat
- **T1** Count lines of relevant docs
- **T1** Show main.rs diff for commit
- **T1** Locate key functions and constants
- **T1** Read flux_en_liste_blocs implementation
- **T1** Read plat/forward_lot and list models
- **T1** Check worktree state and history
- **T1** Show uncommitted changes to main.rs
- **T1** Find CLI flags for mode 4
- **T1** Check CPUs, running drave, cargo config
- **T1** Run release test suite with 2 threads
- **T1** Read forward_lot
- **T1** Read quant_scratch
- **T1** Inspect forward_lot return shape
- **T1** Find forward_lot end
- **T1** List methods after forward_lot
- **T1** Read end of forward_lot
- **T1** Scan plan doc for guards
- **T1** Read plan measurement command and CLI flags
- **T1** Find documented command and system state
- **T1** Read REPRISE server command
- **T1** Check server option handling
- **T1** Run real client against v5 fake peer
- **T1** Run end-to-end mode 4 tests
- **T1** Inspect the n==0 commit
- **T1** Find stale doc claims
- **T1** Run error matrix for mode 4
- **T1** Read plan section 5
- **T1** Read plan sections 7-8
- **T1** Check actifs() usage and debug_assert
- **T1** Check if actifs() was ever used
- **T1** Run forged-frame attack campaign
- **T1** Fix case names in attack script
- **T1** Run second test suite
- **T1** Fix case K byte accounting
- **T1** Run cumulative-guard and bad-reply tests
- **T1** Read stale doc lines and reports
- **T1** Check missing mode-4 report and stale mentions
- **T1** Check which stale lines were touched
- **T1** Make bad peer wait after replying
- … et 7 autres

## 4. Mesures et résultats marquants

- **T1** `Le lot dense (mode 3) coûtait 3,5 ko par jeton ; le mode 4 enchaîne N états`
- **T1** `| **mode 4, lot en listes de 16** | **1,5 ko** | **3,03e-2** |`
- **T1** `/// en version 2 lirait `n × 4` octets d'un corps qui en fait `n × hidden × 4`,`
- **T1** `/// payait 256 allers-retours. Le corps fait `n × hidden × 4` octets ; la`
- **T1** `+    // inconnu se refusait après avoir lu `n × 4` octets et s'être désynchronisé,`
- **T1** `3614-        // découpage passait de quelques pour mille à ×2. Le seuil, lui, reste`
- **T1** `3631-    /// en relatif sur les petits canaux (2,6 % de perplexité à 16 bits pleins,`
- **T1** `3689-        // int8 — et non par le pool. Le pool coûtait 4 ms de plus par jeton pour`
- **T1** `3690-        // 72 Mo lus au lieu de 136 : ses seize tampons de sortie (9,7 Mo) sont`
- **T1** `+        assert!((x[40] - 1.5).abs() < 1e-6, "canal 40 = 3 × 0,5 = 1,5, vu {}", x[40]);`
- **T1** `- Les pourcentages du cache KV : « 75 % / 50 % » était une ERREUR de ma part (j'avais`
- **T1** `compté 1,5/2 sans les échelles de bloc). Les valeurs justes sont **64 %** (clés f32`
- **T1** `+ valeurs int8) et **28 %** (int8/int8) ; le rapport de placement est à jour dans`
- **T1** `ses trois documents, bandeau compris (+0,018 % et non +0,06 %).`
- **T1** `// inconnu se refusait après avoir lu `n × 4` octets et s'être désynchronisé,`
- **T1** `docs/format-flux.md:128:f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.`
- **T1** `écritures ; mesuré 97,6 ms contre 15,6 ms de calcul).`
- **T1** `contre 66 370 408, au prix de +0,074 % de perplexité au rejeu). Le protocole`
- **T1** `(`git bundle`, 4,5 Mo — il n'y a pas de dépôt distant) et vérifie l'empreinte du`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:27455:docs/format-flux.md:111:f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.`
- **T1** `./journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:202:- **T1** `+f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.``
- **T1** `./journal/sessions/aa5f9fc5-9450-4118-b65f-e8b99a28519d/digest.md:2256:docs/format-flux.md:117:f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.`
- **T1** `+| `DRAVE_KV_K_F32=1` | garde les CLÉS en f32 (valeurs quantifiées) | mesuré : à 8 192, **64 %** de la taille f32 (5,125 octets par élément, échelles comprises) pour +0,023 %, contre +3,04 % pour l'in`
- **T1** `référence locale  : perplexité 841.7671  (2.4 s)`
- **T1** `cli:   référence locale  : perplexité 841.7671  (2.7 s)`
- **T1** `[modele] 24 couches chargées en 853.626969ms — listes 0.00 Go , 2 threads`
- **T1** `référence locale  : perplexité 841.7671  (2.7 s)`
- **T1** `cli:   référence locale  : perplexité 520.0365  (0.9 s)`
- **T1** `référence locale  : perplexité 239.5010  (6.9 s)`
- **T1** `deux nœuds        : perplexité 230.6490  (7.9 s)`
- **T1** `transport         : listes à échelle par bloc (2 octets/actif, écarts) · 1655 octets par flux (aller) · 1783 au retour · 81.3 % d'activité (728 neurones par flux) · 63 flux`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : cli exit=1 (134 = SIGABRT) [flux] pilote : 12 couches en local, 12 chez le pair, 16 jetons   référence locale  : perplexité 841.7671  (2.4 s) [flux] le nœud moteur a fermé la connexion (failed to fill
- **T1** : cli exit=0 [pair] ecoute 127.0.0.1:46601 · hidden=896 · 79 octets d'en-tete [pair] client ('127.0.0.1', 63674) [pair] flux 1 : couches 12..24 pos 0 · version 5 · mode LOT EN LISTES · t=16 · corps=2042

