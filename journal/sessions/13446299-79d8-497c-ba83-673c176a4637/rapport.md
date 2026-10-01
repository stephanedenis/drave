# Session 13446299 — Tu es relecteur ADVERSARIAL autonome

| | |
|---|---|
| Identifiant | `13446299-79d8-497c-ba83-673c176a4637` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-01 00:54 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 50 |
| Appels d'outils | 68 |
| Fichiers touchés | 0 |
| Commandes | 56 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSARIAL autonome dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave »). Mission : vérifier les artefacts du sprint 4 (23h44 → 01h44) — aucun chiffre sans source, aucune affirmation non mesurée, aucun raisonnement qui va plus loin que la mesure. Le dépôt a une règle : « chaque chiffre publié doit avoir une source ». Trois erreurs de ce … [3391 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSARIAL autonome dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence R … [3671 caractères tronqués]

*68 appels d'outils.* Actions notables :

- bash — Check existence of cited source files
- bash — Show recent git log and status
- read
- bash — Show aig5 script and sprint3 topk log
- bash — Find sprint 4 section in report
- bash — Find prefill section in docs
- bash — Inspect aiguille.py for offset handling
- bash — Show commit messages and stats
- bash — Find the top-k lot warning in source
- bash — Compute normalized corpus length
- bash — Check corpus file history and attn_topk usage
- bash — Simulate aiguille offset logic for 3 probes
- bash — Search journal for prefill measurement commands
- bash — Find prompt4096 usage and scripts
- … et 44 autres

**Synthèse produite :**

⏵ Rédaction du verdict final

\## Verdict de la revue adverse — sprint 4

Aucun fichier du dépôt modifié. Deux re-mesures lancées (préremplissage, perplexité) ; toutes deux sous **charge** (load 8,7 → 35,4 ; un ppl gpt-oss-120b 16 fils + une sonde aiguille d'un autre agent tournaient en parallèle sur 40 cœurs). Logs neufs : `/tmp/audit_prefill.log`, `/tmp/audit_ppl.log`.

---

\### ÉCARTS

**1. GRAVE — « trois fenêtres de corpus différentes » est faux**
- **(a)** `reports/rapport-aiguille-topk.md:76-79` + en-têtes « fenêtre 1/2/3 » (:81-86) ; commit `09adea5` (« trois fenêtres de corpus »).
- **(b)** « trois **fenêtres de corpus différentes** (l'outil avance son offset de 200 000 caractères à chaque profondeur listée) ».
- **(c)** `tools/aiguille.py:161-163` : après **chaque** sonde, `offset += 200_000` puis `if offset > len(corpus) - 400_000 { offset = 0 }`. Or `aiguille.charger_corpus()` rend **353 778** caractères (`data/wikitext2_test.txt`, inchangé depuis le 25/09) → le seuil vaut **−46 222** → la remise à zéro se déclenche **toujours**. Offsets réellement utilisés : **[0, 0, 0]**. Preuve par le vrai module : les 3 invites reconstruites ont le **même md5** (`6a94ff027ad0` ×3). Même sans le garde-fou, l'offset 400 000 est hors corpus (400 000 + 17 603 > 353 778) : au mieux **2** fenêtres distinctes étaient possibles. Les 12 lignes du log disent d'ailleurs toutes « prompt 4114 jetons ».
- **(d)** **FAUX.** Les « 3/3 » et « 0/3 » sont trois répétitions de la **même invite**. La justification annoncée (« avec une seule sonde, impossible de distinguer *l'attention creuse échoue* de *cette exécution a déraillé* ») n'est pas servie : trois fois la même invite ne dit rien de la généralité inter-fenêtres.
- **(e)** Écrire « trois **répétitions** de la même invite (offset remis à 0 par le garde-fou ; corpus de 353 778 car. < 400 000 supposés) », remplacer « fenêtre 1/2/3 » par « répétition 1/2/3 », borner la conclusion à cette fenêtre — ou corriger l'outil et refaire la grille. Le commentaire de `/tmp/aig5.sh` porte la même erreur.

**2. GRAVE (feuille de route) — la grille n'est pas celle de l'objectif du sprint**
- **(a)** section « Suite (sprint 4) » ; `sprints/04-…md`.
- **(b)** « l'échec au milieu n'est PAS une impossibilité structurelle du top-k — c'est un **réglage** ».
- **(c)** L'objectif du sprint exige « Grille en **--lot 1** (tout le passage creux) et k = 256/512/1024 ». `aig5.sh` et `aiguille_k.log` tournent en **--lot 256**, où `--attn-topk` est **I
… [7799 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check existence of cited source files
- **T1** Show recent git log and status
- **T1** Show aig5 script and sprint3 topk log
- **T1** Find sprint 4 section in report
- **T1** Find prefill section in docs
- **T1** Inspect aiguille.py for offset handling
- **T1** Show commit messages and stats
- **T1** Find the top-k lot warning in source
- **T1** Compute normalized corpus length
- **T1** Check corpus file history and attn_topk usage
- **T1** Simulate aiguille offset logic for 3 probes
- **T1** Search journal for prefill measurement commands
- **T1** Find prompt4096 usage and scripts
- **T1** Read digest around prefill measurement
- **T1** Check load, binary, model, prompt file
- **T1** Find perplexity measurement command in digest
- **T1** Run CPU+GPU prefill re-measurement in background
- **T1** Read perplexity command context in digest
- **T1** Inspect running processes and CPU count
- **T1** Count verdicts per series in aiguille_rep.log
- **T1** Show 09adea5 journal report diff
- **T1** Show 2ae761c journal diff
- **T1** Check re-measurement log progress
- **T1** Check source citations in artifacts
- **T1** Find aig5 launch in digest
- **T1** Compare summed durations vs mtime window
- **T1** Read repetition grid timeline in digest
- **T1** Prove identical windows using real loader
- **T1** Precise mtimes and re-measurement progress
- **T1** Inspect ppl ids file and commands
- **T1** Poll re-measurement progress
- **T1** Hash-compare prompts of the three probes
- **T1** Poll CPU measurement after a minute
- **T1** Check how other reports cite log sources
- **T1** Read current re-measurement output
- **T1** Find all 3961 occurrences in docs
- **T1** Read sprint 3 prefill profiling note
- **T1** Get commit and sprint timestamps
- **T1** Poll re-measurement
- **T1** Search /tmp for preserved prefill output
- … et 16 autres

## 4. Mesures et résultats marquants

- **T1** `2ae761c Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5`
- **T1** `306:| CPU | **286,6 s** (13,8 tok/s) | attention **52,6** · matvec+mlp 18,4 |`
- **T1** `307:| `DRAVE_GPU=1 DRAVE_GPU_KV=1` | **63,8 s** (62,1 tok/s) | attention **2,2** · matvec+mlp 12,8 |`
- **T1** `309:L'attention du préremplissage est **le** poste dominant sur CPU (73 % du temps :`
- **T1** `346:**×2,8 sur le préremplissage**, perplexité identique au chiffre près. C'est le`
- **T1** `| k = 256 (6,25 %) | **0/3** |`
- **T1** `| k = 512 (12,5 %) | **0/3** |`
- **T1** `| k = 1 024 (25 %) | **3/3** |`
- **T1** `Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:32509:| la même, **KV en VRAM** (`DRAVE_GPU_KV=1`, noyaux `attn_kv_*`) | **13,2 ms** (×73) |`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:35249:./reports/rapport-placement-bits-kv.md:137:| contexte long **avec** `DRAVE_GPU_KV=1` | **int8/int8** (28 %, +3,04 %) ou f32/f32 | `
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:35250:./docs/contexte-long.md:104:| E4 | **KV déporté sur les 2 GPU** (pagination, préchargement) | **fait** : noyau `attn_kv_*` (tuiles`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:35329:163:| 8 | suite du plan 1 M | **fait pour E4/E5** | **E4 KV déporté en VRAM** : noyaux `attn_kv_*` (tuiles de 32 clés, softmax en `
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:35330:185:| KV déporté dans le moteur (`DRAVE_GPU_KV=1`, ctx 4 096) | attention **22,16 → 3,29 ms/jeton** (÷6,7) · balayage 219,4 → **13`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:35840:Qwen Q8_0 DRAVE_GPU=1 DRAVE_GPU_KV=1 (attendu ~19,3885) : perplexité 19.3885 sur 510 tokens`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:38199:prompt  : 3961 tokens en 286.638 s  (13.8 tok/s, TTFT 72.4 ms)`
- **T1** `prompt  : 3961 tokens en 286.638 s  (13.8 tok/s, TTFT 72.4 ms)`
- **T1** `généré  : 4 tokens en 0.358 s  (11.19 tok/s)`
- **T1** `prompt  : 3961 tokens en 63.793 s  (62.1 tok/s, TTFT 16.1 ms)`
- **T1** `généré  : 4 tokens en 0.125 s  (31.93 tok/s)`
- **T1** `1. GRAVE — rapport-logits-gpu-vs-cpu.md:5-6 et :77 : « même top-1 partout » puis « sans changer les jetons choisis en top-1 » → FAUX : 497/511 (14 positions divergentes), la mesure du rapport lui-même`
- **T1** `2. GRAVE — rapport-aiguille-topk.md:3-12 et toute la grille : avec `--lot 256` (défaut d'aiguille.py, réglage de la grille), le moteur IGNORE `--attn-topk` au préremplissage. Seuls les 24 jetons génér`
- **T1** `3. MOYEN — rapport-aiguille-topk.md:63-67 : trois défauts. (i) « avec le préremplissage jeton par jeton » contredit la correction :22-32. (ii) « les trois sondes de 8 192 ont été LANCÉES puis arrêtées`
- **T1** `4. MOYEN — tools/compare_logits.py:64-84 : le dénominateur affiché n'est pas le nombre de positions comparées. Démontré : sans ids → « accord du top-1 : 0/255 » et « perplexité 1.0000 » ; avec un fich`
- **T1** `36049:lot 8 : perplexité 9.4335 sur 1023 tokens`
- **T1** `36050:lot 1 : perplexité 9.4167 sur 1023 tokens`
- **T1** `36695:cpu ctx2048 : perplexité 9.4167 sur 1023 tokens`
- **T1** `36696:gpu ctx2048 : perplexité 9.4162 sur 1023 tokens`
- **T1** `36703:=== perplexité 9.4167 sur 1023 tokens (0 événements, 38.0 s) ===`
- **T1** `36706:=== perplexité 9.4162 sur 1023 tokens (0 événements, 35.8 s) ===`
- **T1** `36961:10. Perf (à titre indicatif, non bloquant) : le fil 0 fait en série la descente (jusqu'à 256 itérations partagées × 4 passes), le balayage exclusif de 1024 cases (1049-1057) et la somme du poiso`
- **T1** `38480:CPU      (lot 256, ctx 4096, 1023 jetons) : perplexité 9.4335 sur 1023 tokens`
- **T1** `38481:GPU KV   (lot 256, ctx 4096, 1023 jetons) : perplexité 9.4337 sur 1023 tokens`
- **T1** `CPU      (lot 256, ctx 4096, 1023 jetons) : perplexité 9.4335 sur 1023 tokens`
- **T1** `GPU KV   (lot 256, ctx 4096, 1023 jetons) : perplexité 9.4337 sur 1023 tokens`
- **T1** `docs/contexte-long.md:104:| E4 | **KV déporté sur les 2 GPU** (pagination, préchargement) | **fait** : noyau `attn_kv_*` (tuiles de 32 clés en mémoire partagée, une passe par (tête KV, tranche), recom`
- **T1** `+- Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5" && git log --oneline -1; cat /tmp/aiguille_k.log | tail -3`
- **T1** `[timed out after 600000ms]`
- **T1** `- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\np='reports/rapport-aiguille-topk.md'; s=open(p).read()\nvieux = \"\"\"| k = 512 (12,5 %) | (en cours) |`
- **T1** `[timed out after 60000ms]`
- **T1** `rien : refusé), p90, chemins de reproduction, « 6 % » → 6,25 %, et trois`
- **T1** `| CPU | 286,6 s (13,8 tok/s) | attention **52,6** · matvec+mlp 18,4 | le terme quadratique domine (73 %) |`
- **T1** `| `DRAVE_GPU=1 DRAVE_GPU_KV=1` | **63,8 s (62,1 tok/s)** | attention **2,2** · matvec+mlp 12,8 | **×4,5 sur le prompt** |`
- **T1** `2ae761c 2026-09-30 23:52:07 -0400 Préremplissage déporté : ×4,5 sur un prompt de 3 961 jet`
- **T1** `prompt  : 3961 tokens en 371.959 s  (10.6 tok/s, TTFT 93.9 ms)`
- **T1** `généré  : 4 tokens en 0.416 s  (9.62 tok/s)`
- **T1** `prompt  : 3961 tokens en 95.941 s  (41.3 tok/s, TTFT 24.2 ms)`
- **T1** `généré  : 4 tokens en 0.171 s  (23.34 tok/s)`
- **T1** `12:générés (0,58 % des passes), ce qui est bien le moment où le modèle doit regarder`
- **T1** `CPU      (lot 256, ctx 4096, 1023 jetons) :     1023 tokens notés — perplexité cumulée 9.433  (20.0 tok/s)`
- **T1** `=== perplexité 9.4335 sur 1023 tokens (0 événements, 51.2 s) ===`
- **T1** `GPU KV   (lot 256, ctx 4096, 1023 jetons) :     1023 tokens notés — perplexité cumulée 9.434  (29.9 tok/s)`
- **T1** `=== perplexité 9.4337 sur 1023 tokens (0 événements, 34.2 s) ===`

