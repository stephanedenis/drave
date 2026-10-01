# Session ff364db0 — Relecture ADVERSARIALE de clôture, dans

| | |
|---|---|
| Identifiant | `ff364db0-d28f-47eb-973e-f13bdafd35a2` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-01 05:50 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 63 |
| Appels d'outils | 75 |
| Fichiers touchés | 0 |
| Commandes | 69 |
| Sous-agents | 1 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Relecture ADVERSARIALE de clôture, dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. Tu vérifies les artefacts de la nuit (30/09 19h49 → 01/10 07h39) qui n'ont PAS encore été audités par une relecture. Budget : 20 minutes. Ne modifie AUCUN fichier du dépôt.  Ce qui a déjà été audité (ne refais pas) : les rapports `rapport-gpu-topk-selection.md` (sprints 1-2), `rapport-logits-gpu-vs-cp … [2471 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Relecture ADVERSARIALE de clôture, dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. Tu vérifies les artefa … [2751 caractères tronqués]

*75 appels d'outils.* Actions notables :

- bash — Show recent commits and repo status
- bash — List repo root and tmp files
- bash — Show commit dates and file sizes
- bash — Locate sprint 7 section in REPRISE.md
- read
- bash — List reports and sprints directories
- bash — Locate Prochaines étapes in README
- bash — Read sprint 6 and 7 notes
- bash — Grep key table numbers across markdown
- bash — Search error magnitudes in topk report
- bash — Read topk report grid section
- bash — Read sprint 2 note
- bash — Search sinks and error values in report
- bash — Search 8.38e-7 and 7.19e-7 everywhere
- … et 59 autres

**Synthèse produite :**

⏵ Review complete, result sent to the parent agent

Relecture terminée (lecture seule ; aucun fichier du dépôt modifié — seuls `/tmp`, `target/` et le binaire release existant ont servi aux essais). Résultat transmis à l'agent parent.

---

\# Relecture adversariale de clôture — artefacts non encore audités (30/09 19h49 → 01/10 07h39)

\## 1. Écarts classés par gravité

\### A — CRITIQUE : « Vérifié : la même invite rend la main en 312 s » est un SIGABRT
- **(a)** `REPRISE.md` §« Sprint 7 » (l.518‑521), `reports/rapport-aiguille-topk.md` (l.264‑266), message du commit `32951e9`.
- **(b)** « la capacité est plafonnée au contexte déclaré, et `Model::generate` tronque l'invite en le disant […] Vérifié : la même invite rend la main en 312 s au lieu de ne jamais finir. »
- **(c)** FAUX quant à l'issue. `generate` (model.rs:3930‑3934) tronque à **exactement** `ctx` sans réserver `n_new` ; la décodage fait `let pos = ids.len() + step; self.forward(next, pos)` (model.rs:3976‑3977) et `forward` assert `pos < self.ctx` (model.rs:3025). **Reproduit 3×** sur le binaire release du dépôt (Qwen2.5‑0.5B, ctx 256) : invite 300 > ctx → message de troncature puis `panicked at src/model.rs:3025: contexte dépassé (256 ≥ 256)`, **exit 134** (`panic = "abort"`). Idem avec invite == ctx. Le mode session, lui, réserve la place (main.rs:851‑856). Le script de vérification du journal ne lisait ni `returncode` ni « panicked » : l'abort est passé pour une réussite ; « code trouvé : False » vient de l'abort, pas de la troncature (l'aiguille était à mi‑profondeur, donc conservée).
- **(d)** Le correctif échange un livelock contre un core dump sur le chemin même qu'il prétend réparer.
- **(e)** Tronquer à `ctx - n_new` (comme la session) ou arrêter proprement la génération quand `pos ≥ ctx`, puis re‑vérifier en testant le code de sortie.

\### B — ÉLEVÉ : le garde est au mauvais endroit, `ecrire` n'a aucun contrôle `pos < ctx`
- **(a)** `model.rs:1209‑1213`, commentaire faux `model.rs:1124‑1125`, `forward_lot` sans garde (`model.rs:2545`).
- **(c)** Au‑delà de `ctx`, `assurer` ne grandit plus : `d = (kvh*cap + pos)*hd` écrit dans le bloc de la **tête KV suivante** (corruption silencieuse) puis panique sur la dernière. Reproduit : `--ppl-reparti 127.0.0.1:9 --ids <300> --ctx 256 --lot 8` → `panicked at src/model.rs:1213: range end index 32832 out of range for slice of length 32768`, avant même la connexion au pair (cause : `limite` calculé puis ignoré quand `--ids` est fourni, main.rs:2114 vs
… [3142 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Sous-agents lancés

- tour 1 — Audit livelock fix in model.rs

### Commandes exécutées (échantillon)

- **T1** Show recent commits and repo status
- **T1** List repo root and tmp files
- **T1** Show commit dates and file sizes
- **T1** Locate sprint 7 section in REPRISE.md
- **T1** List reports and sprints directories
- **T1** Locate Prochaines étapes in README
- **T1** Read sprint 6 and 7 notes
- **T1** Grep key table numbers across markdown
- **T1** Search error magnitudes in topk report
- **T1** Read topk report grid section
- **T1** Read sprint 2 note
- **T1** Search sinks and error values in report
- **T1** Search 8.38e-7 and 7.19e-7 everywhere
- **T1** Read bench section of topk report
- **T1** Find topk bench logs in tmp
- **T1** Inspect topk bench logs
- **T1** List tmp logs from sprint 2 window
- **T1** Search logs for sinks mentions
- **T1** Trace 8.38e-7 origin
- **T1** Read raw bench output in journal
- **T1** Read aiguille topk k-table
- **T1** Grep all k recovery fractions
- **T1** Read sprint 5 grid section in report
- **T1** Verify 8/9 claim and sprint6 logs
- **T1** Verify prefill perplexity source
- **T1** Find sprint 6 raw logs
- **T1** Read sprint 6 raw aiguille logs
- **T1** Read full s6 log
- **T1** Find sources for artifacts 3 and 5
- **T1** Check 312s, 4788 tokens, and old line 1117
- **T1** Read report sprint 7 section
- **T1** Find truncation verification log
- **T1** Trace 312s verification source
- **T1** Find truncation message in journal
- **T1** Read journal around truncation verification
- **T1** Trace sixth artifact and 16384 claim
- **T1** Show last five commit messages and stats
- **T1** Check commit 783f1f9 and sixth artifact source
- **T1** Check sprint 1 note and kv_assurer references
- **T1** Check line counter and dirty working tree
- … et 29 autres

## 4. Mesures et résultats marquants

- **T1** `783f1f9 Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384`
- **T1** `783f1f9 2026-10-01 03:38:47 -0400 Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384`
- **T1** `- `783f1f9` Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384`
- **T1** `Neuf sondes × 246 s ne tiennent pas dans un box — la grille complète du taux demande`
- **T1** `./reports/rapport-inference.md:251:| **Perplexité WikiText-2** | **24,90** | **27,83** | **+12 %** |`
- **T1** `./reports/rapport-gpu-topk-selection.md:62:| 262 144 | 14/14 | 14/14 | 14/14 | **0** | 0,44 ms (224×) | 97,88 ms | 0,45 ms (896×) | 399,21 ms |`
- **T1** `./reports/rapport-gpu-topk-selection.md:280:GPU en prend 36 %, à 4 095 clés il est **7,8× plus rapide** (4,97 contre`
- **T1** `./reports/rapport-aiguille-topk.md:90:| **k = 256** (6,25 %) | NON (244,7 s) | NON (237,8 s) | NON (237,0 s) | **0/3** |`
- **T1** `./reports/rapport-aiguille-topk.md:92:| **k = 512** (12,5 %) | NON (240,5 s) | NON (238,1 s) | NON (237,8 s) | **0/3** |`
- **T1** `./journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:12537:⏵ Q4 : perplexité **27,83 contre 24,90** pour le Q8 — 12 % de qualité perdue pour 11 % de mémoire gagnée. Je fige les mesures`
- **T1** `./.git/logs/HEAD:289:9e22ed894d07c1a78c88d312a8fd4b39f7ea2793 2ae761cbdb8ed7cfba3ec36562aa1465301698e1 Stéphane <stephane@localhost> 1790826727 -0400	commit: Préremplissage déporté : ×4,5 sur un promp`
- **T1** `./.git/logs/refs/heads/master:288:9e22ed894d07c1a78c88d312a8fd4b39f7ea2793 2ae761cbdb8ed7cfba3ec36562aa1465301698e1 Stéphane <stephane@localhost> 1790826727 -0400	commit: Préremplissage déporté : ×4,5`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:38498:2ae761c Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:38712:- Préremplissage, mêmes commandes que le digest (`--infer --prompt "$(cat /tmp/prompt4096.txt)" --n 4 --ctx 4608 --lot 256 --thr`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:38727:- Valeurs dérivées du préremplissage : 286,638/63,793 = 4,49 → « ×4,5 » ; 3961/286,638 = 13,8 tok/s ; 3961/63,793 = 62,1 tok/s ;`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:38807:| préremplissage CPU | 286,638 s (13,8 tok/s) · attention 52,6 · matvec+mlp 18,4 | **371,959 s** (10,6 tok/s) · **71,0** · **21,`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:2738:- Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5" && git log --oneline -1; cat `
- **T1** `./journal/sessions/13446299-79d8-497c-ba83-673c176a4637/digest.md:18:2. `docs/contexte-long.md`, section « Le PRÉREMPLISSAGE aussi : 286,6 s → 63,8 s sur un prompt de 3 961 jetons » — sources : la sor`
- **T1** `./journal/sessions/13446299-79d8-497c-ba83-673c176a4637/digest.md:26:- **Le chiffre du préremplissage** (286,6 s → 63,8 s, ×4,5 ; attention 52,6 → 2,2 ms/jeton) : re-mesurable en ~6 min au total ; si `
- **T1** `./journal/sessions/4d7a793b-74d1-4c46-bb53-21953fe91d87/digest.md:92:5: **0,038 nat** en moyenne — même top-1 partout, mais 1,2 % de perplexité à 511`
- **T1** `./reports/rapport-minimal.md:65:| modèle minimal — multi 4 bits (bitmap+signe) | 0.0 Mo | 0.000 | 3497465.6 | 78 | 2340 |`
- **T1** `./reports/rapport-minimal.md:66:| modèle minimal — int8 | 0.0 Mo | 0.000 | 3497465.6 | 78 | 2340 |`
- **T1** `./reports/rapport-encodage.md:42:| 2.00 | 4971.00 % | 5.5 | dense ternaire (référence CDC) |`
- **T1** `./reports/rapport-drapeaux-ignores.md:170:  === perplexité 4949.4977 sur 3 tokens … ===                       ← 1929,3 → 4949,5 : appliqué`
- **T1** `./reports/rapport-gpu-topk-selection.md:6:tailles testées) et coûte **0,89 ms** là où le tri CPU en coûte **497 ms** à`
- **T1** `./reports/rapport-parcimonie-imposee.md:34:| 0,5 % | 312,3 M (−11,5 %) | 20,1511 | 1,05× |`
- **T1** `./sprints/02-fusionner-la-cha-ne-du-top-k-d-port-desc.md:31:| 4 | **le gain dans le moteur** | attention 4,53 → 4,86 ms/jeton **de 255 à 4 095 clés** (plate) contre 4,26 → 38,84 pour le CPU · **croise`
- **T1** `./reports/rapport-gpu-topk-selection.md:281:38,84 ms/jeton).`
- **T1** `./reports/rapport-encodage.md:69:2. **Le gain dépend entièrement de la densité** : ~×1,3 à 12,5 %, ×2,2 à 5 %,`
- **T1** `./reports/rapport-inference.md:248:| Événements par token | 352,7 M | 312,5 M | −12 % |`
- **T1** `./reports/bilan-multi-materiel.md:66:3. **Pas de multiplieur requis.** Le PE atteint 112,5 MHz avec 176 ALMs **et zéro`
- **T1** `./reports/rapport-attention-creuse.md:39:matrice **creuse à ~12,5 %**. Et cette densité **décroît avec le contexte** :`
- **T1** `./reports/rapport-attention-creuse.md:43:| 256 | 12,5 % |`
- **T1** `./reports/rapport-attention-creuse.md:60:À contexte 256, k = 32 est optimal (12,5 % des clés) ; à contexte 512, c'est`
- **T1** `./reports/rapport-attention-creuse.md:61:k = 64 (12,5 % également). L'optimum est donc une **fraction** du contexte, ce`
- **T1** `./reports/rapport-attention-creuse.md:110:| Poids creux, donc listables | ✅ 12,5 % de densité à 256, 0,8 % à 4 096 |`
- **T1** `./reports/rapport-optimisations.md:53:| 100 % | 4 303 745 | **4,51 G év/s** (0,95 ms) | **5,44 G év/s** (0,79 ms) |`
- **T1** `./reports/rapport-parcimonie-imposee.md:69:| `down` seul à 50 % | 302,9 M (−14,5 %) | +0,86 % | — |`
- **T1** `./reports/rapport-croisement-push-pull.md:98:| 50 | 5 % | 0 év — 9,1 s | 4,5 G év — **6,2 s** |`
- **T1** `./reports/rapport-mur-memoire-4bits.md:92:**4,5 bits/poids effectifs** (4 + 16/32), contre 8 pour l'int8 : ×1,78 moins`
- **T1** `./reports/rapport-mur-memoire-4bits.md:112:| 4 bits **attention** | 18,3503 | +5,4 % | 24,5 | 27,0 |`
- **T1** `./src/roofline.py:11:  M20K                    2 014 blocs × 20 Kbit = 5,03 Mo   (Quartus)`
- **T1** `./reports/rapport-parcimonie-imposee.md:37:| 5,0 % | 145,0 M (−58,9 %) | **2264,84** | **117×** |`
- **T1** `./reports/rapport-coherence-docs.md:226:| OK | **17** | formats des modes 2 et 3 · `flux_brut` · `hôte:port` · trace dense 66 370 408 o (fichier réellement relu) · 66 370 406 hors sentinelle · 24 576 `
- **T1** `142:| 100 | 3 | 0,03 ms | 0,02 ms | **1,04e-7** |`
- **T1** `143:| 4 096 | 256 | 0,07 ms | 0,64 ms | **4,79e-7** |`
- **T1** `144:| 65 536 | 256 | 0,07 ms | 1,07 ms | **3,10e-7** |`
- **T1** `145:| 262 144 | 256 | 0,07 ms | 0,98 ms | **2,70e-7** |`
- **T1** `211:~74 000 lancements pour ces 511 jetons, à comparer aux ~0,1 ms de calcul utile par`
- **T1** `253:| 4 096 | **0,13 ms** | 0,22 ms | 7,19e-7 |`
- **T1** `254:| 16 384 | **0,18 ms** | 0,43 ms | 9,15e-7 |`
- **T1** `255:| 65 536 | **0,43 ms** | 0,57 ms | 5,68e-7 |`
- **T1** `256:| 131 072 | **0,85 ms** | 0,89 ms | 6,36e-7 |`
- **T1** `257:| 262 144 | 1,58 ms | **1,35 ms** | 7,01e-7 |`
- **T1** `342:| 3 | `attn_topk_somme` : softmax sur les k retenus + puits, puis Σ pondérée des V | ✅ 1,0–4,8e-7 · temps GPU constant (0,07 ms) |`
- **T1** `| 4 096 | **0,13 ms** | 0,22 ms | 7,19e-7 |`
- **T1** `| 16 384 | **0,18 ms** | 0,43 ms | 9,15e-7 |`
- **T1** `| 65 536 | **0,43 ms** | 0,57 ms | 5,68e-7 |`
- **T1** `| 131 072 | **0,85 ms** | 0,89 ms | 6,36e-7 |`
- **T1** `| 262 144 | 1,58 ms | **1,35 ms** | 7,01e-7 |`
- **T1** `⚠️ **Le noyau fusionné perd au-delà de 131 072 clés** (1,58 contre 1,35 ms) : ses`
- **T1** `**Le croisement est à ~300 clés** : à 255 clés le CPU garde 6 % d'avance, à 512 le`
- **T1** `GPU en prend 36 %, à 4 095 clés il est **7,8× plus rapide** (4,97 contre`
- **T1** `38,84 ms/jeton).`
- **T1** `linéairement (+0,0043 ms par clé et par jeton). La perplexité est identique à 2e-5`
- **T1** `# Sprint 2 — Fusionner la chaîne du top-k déporté : descente radix, collecte et somme dans UN noyau par ligne (8 lancements → 2, plus de tampon nh×n×4), et gagner dès ~1 000 clés`
- **T1** `- **Objectif** : Fusionner la chaîne du top-k déporté : descente radix, collecte et somme dans UN noyau par ligne (8 lancements → 2, plus de tampon nh×n×4), et gagner dès ~1 000 clés`
- **T1** `nh×n×4), et gagner dès ~1 000 clés ». **Livré, mesuré, et le gain est plus grand`
- **T1** `| 1 | `attn_topk_tout` : descente radix + collecte + somme en **un** noyau par ligne (256 compteurs, k indices et k poids en partagé ; aucun indice ne quitte la VRAM) | 2 lancements au lieu de 8 · tam`
- **T1** `| 2 | seuil de bascule **mesuré** avec la chaîne (noyau 4 plus rapide jusqu'à 131 072 clés, la chaîne au-delà) | 0,13 contre 0,22 ms à 4 k · 0,85 contre 0,89 à 131 k · 1,58 contre 1,35 à 262 k |`
- **T1** `| 4 | **le gain dans le moteur** | attention 4,53 → 4,86 ms/jeton **de 255 à 4 095 clés** (plate) contre 4,26 → 38,84 pour le CPU · **croisement à ~300 clés** |`
- **T1** `| 511 | 255 | **4,26** | 4,53 | CPU +6 % |`
- **T1** `| 1 023 | 512 | 7,17 | **4,62** | GPU −36 % |`
- **T1** `| 2 047 | 1 024 | 12,08 | **4,82** | GPU −60 % |`
- **T1** `| 4 095 | 2 047 | 19,77 | **4,86** | GPU −75 % |`
- **T1** `Le CPU croît de **0,0090 ms par clé** ; le GPU est plat.`
- **T1** `| CPU top-k 256 | 19,0740 | **+2,66 %** |`
- **T1** `| GPU dense (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % vs CPU |`
- **T1** `| GPU top-k 256 (`DRAVE_GPU_TOPK`) | 18,8391 | **+2,90 %** |`
- **T1** `| GPU sans miroir KV | 18,3538 | −1,22 % vs CPU |`
- **T1** `Le coût du pruning est le MÊME des deux côtés (+2,7 % / +2,9 %) : le chemin`
- **T1** `n'est pas le miroir KV (−0,25 %) mais le déport des projections (−1,22 %).`
- **T1** `**F4/F5/F6** : `k > n` accepté (refusé maintenant) · `shCle` mort (4 ko de partagé`
- **T1** `la perplexité de 1,22 % alors qu'il ne la change que de 0,06 % à ctx 256 (mêmes`
- **T1** `511 jetons). Ce n'est pas le miroir KV (−0,25 %). Une erreur d'ordre de sommation`
- **T1** `256 seaux × 4 passes, balayage de 1024 cases, somme du filet) pendant que 1023`
- **T1** `./reports/rapport-gpu-topk-selection.md:253:| 4 096 | **0,13 ms** | 0,22 ms | 7,19e-7 |`
- **T1** `pour la collecte et ≈900× pour le seuil (0,0004 ms au lieu de 0,45 ms, 0,0003 au`
- **T1** `lieu de 0,27 ms). Un affichage mal étiqueté est un affichage qui ment — et il a`
- **T1** `| 100 | 3 | 0,03 ms | 0,02 ms | **1,04e-7** |`
- **T1** `| 4 096 | 256 | 0,07 ms | 0,64 ms | **4,79e-7** |`
- **T1** `| 65 536 | 256 | 0,07 ms | 1,07 ms | **3,10e-7** |`
- **T1** `| 262 144 | 256 | 0,07 ms | 0,98 ms | **2,70e-7** |`
- **T1** `Le temps GPU est **constant** (0,07 ms de 4 k à 262 k clés) : le noyau ne lit que`
- **T1** `dénominateur ×45,7 et sortie 55× trop petite à k = 1 ; écart relatif 2,05e-1. Une`
- **T1** `banc top-k : 1000000 clés · 2 têtes KV × 64 dim · 7 têtes de requête par tête KV · KV 8 bits`
- **T1** `CPU  20 fils :   951.78 ms`
- **T1** `GPU  scores  :    19.49 ms  (48.8× plus rapide)`
- **T1** `CPU  tri + comptage :   401.05 ms`
- **T1** `GPU  4 passes d'histogramme :     0.98 ms  (409.0× plus rapide)`
- **T1** `collecte GPU     0.95 ms · CPU tri complet  1653.52 ms (1744.4× plus rapide)`
- **T1** `noyau 3 (softmax sur k + Σ w·V) : GPU 0.07 ms · CPU 0.96 ms · écart max 7.451e-8 sur 1.249e-1 (relatif 5.97e-7)`
- **T1** `étape 5 — 14 lignes × 1000000 clés :`
- **T1** `chaîne top-k GPU sans relecture des scores :     3.90 ms`
- **T1** `attention COMPLÈTE sur CPU (14 fils)   :   539.89 ms  (×138.3)`
- **T1** `coût de la relecture des scores (banc seul) :    15.59 ms`
- **T1** `second passage k = 512, mêmes tampons : 14/14 lignes · 0.78 ms (0.95 ms de seuil) · cases non écrites 0`
- **T1** `Qwen Q8_0 ctx 256 : perplexité 19.3885 sur 510 tokens`
- **T1** `gpt-oss MXFP4 ctx 256 : perplexité 15.1757 sur 510 tokens`
- **T1** `=== perplexité 12.2265 sur 4095 tokens (0 événements, 142.9 s) ===`
- **T1** `=== perplexité 15.1757 sur 510 tokens (0 événements, 99.3 s) ===`
- **T1** `=== perplexité 15.1666 sur 510 tokens (0 événements, 107.7 s) ===`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:37058:[DRAVE_BANC_SANS_PUITS=1]  noyau 4 (UN lancement) : 0.13 ms · écart max 1.043e-7 sur 1.245e-1 (relatif 8.38e-7)`
- **T1** `[timed out after 60000ms]`
- **T1** `noyau 3 (softmax sur k + Σ w·V) : GPU 0.06 ms · CPU 0.73 ms · écart max 5.960e-8 sur 1.244e-1 (relatif 4.79e-7)`
- **T1** `noyau 4 (UN lancement) : 0.13 ms · écart max 1.268e-4 sur 1.244e-1 (relatif 1.02e-3)`
- **T1** `[]  noyau 4 (UN lancement) : 0.14 ms · écart max 8.941e-8 sur 1.244e-1 (relatif 7.19e-7)`
- **T1** `[DRAVE_BANC_SANS_PUITS=1]  noyau 4 (UN lancement) : 0.13 ms · écart max 1.043e-7 sur 1.245e-1 (relatif 8.38e-7)`
- **T1** `| **k = 256** (6,25 %) | NON (244,7 s) | NON (237,8 s) | NON (237,0 s) | **0/3** |`
- **T1** `| **k = 1 024** (25 %) | oui (239,6 s) | oui (253,2 s) | oui (244,1 s) | **3/3** |`
- … (tronqué)

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : 57:        (opt.ppl, "--ppl"), (opt.infer, "--infer"), 528:            "--infer" => { o.infer = true; 1 } 549:            "--ids" => { o.ids = suivant(i).split(',') 552:            "--prompt" => { o.p
- **T1** : ok [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué. [config] cache KV : 32 bits, 0.01 G
- **T1** : === TEST ids == ctx ===  thread 'main' (2721392) panicked at src/model.rs:3025:9: contexte dépassé (256 ≥ 256) note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace timeout: th
- **T1** : [config] rotation : RoPE simple (le modèle ne déclare pas YaRN) [flux] quantification : 127 niveaux, seuil 0, top-k 0, renorm false [flux] pilote : 12 couches en local, 12 chez le pair, 300 jetons  th

