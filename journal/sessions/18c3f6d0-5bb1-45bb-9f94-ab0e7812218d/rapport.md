# Session 18c3f6d0 — Relecture ADVERSARIALE ciblée (10 minut

| | |
|---|---|
| Identifiant | `18c3f6d0-5bb1-45bb-9f94-ab0e7812218d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-01 05:20 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 23 |
| Appels d'outils | 35 |
| Fichiers touchés | 0 |
| Commandes | 23 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Relecture ADVERSARIALE ciblée (10 minutes maximum) dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. Tu vérifies TROIS affirmations du sprint 6 (03h38 → 05h38), et rien d'autre. Ne modifie aucun fichier. Sois bref : une ligne par écart, avec le verdict.  Affirmation 1 : « L'attention complète retrouve l'information sur 8 des 9 fenêtres contiguës à 4 096 clés, profondeur 0,5 ; la fenêt … [2288 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Relecture ADVERSARIALE ciblée (10 minutes maximum) dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. Tu vér … [2568 caractères tronqués]

*35 appels d'outils.* Actions notables :

- bash — Check logs exist and sizes
- bash — Inspect repo git log and status
- read
- bash — Show the two runner scripts
- bash — List tools and count lines
- bash — Find engine warning source and topk logic
- bash — Verify corpus length and window offsets
- bash — Trace forward_lot and attn_topk usage
- bash — Search /tmp for 4608 evidence
- bash — Search report and journal for the timeout claim
- bash — Run window 3 prompt at ctx 4608 bounded to 240s
- bash — Check tool margin change in git history
- bash — Find sprint 6 evidence lines in digest
- bash — List logs modified during sprint 6 window
- … et 11 autres

**Synthèse produite :**

⏵ Reading the logs and the aiguille tool to verify the three claims

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check logs exist and sizes
- **T1** Inspect repo git log and status
- **T1** Show the two runner scripts
- **T1** List tools and count lines
- **T1** Find engine warning source and topk logic
- **T1** Verify corpus length and window offsets
- **T1** Trace forward_lot and attn_topk usage
- **T1** Search /tmp for 4608 evidence
- **T1** Search report and journal for the timeout claim
- **T1** Run window 3 prompt at ctx 4608 bounded to 240s
- **T1** Check tool margin change in git history
- **T1** Find sprint 6 evidence lines in digest
- **T1** List logs modified during sprint 6 window
- **T1** Find killed-process timing evidence in digest
- **T1** Read digest around probe monitoring
- **T1** Read digest diagnosis section
- **T1** Read digest from relaunch to verification
- **T1** Read early sprint-6 digest lines and kill markers
- **T1** Read digest around second hang inspection
- **T1** Locate the hung prompt text in corpus
- **T1** Check engine for prompt-over-context warning
- **T1** Check machine state after confirmation run
- **T1** Look for context clamping in engine

## 4. Mesures et résultats marquants

- **T1** `783f1f9 Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384`
- **T1** `0d50e75 À 8 192 clés, k=1024 (12,5 %) suffit : le k nécessaire croît plus lentement que le contexte (deux points)`
- **T1** `2ae761c Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5`
- **T1** `/tmp/bascule_yarn.log:8:[config] rotation : YaRN ×32 (contexte demandé 4608 > 4096 initial)`
- **T1** `/tmp/profil_experts.log:19:    experts jamais choisis : 1461/4608 (32 %) ;                                   taux moyen 0.031 par jeton`
- **T1** `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:6184:[config] rotation : YaRN ×32 (contexte demandé 4608 > 4096 initial)`
- **T1** `39409:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -m \"Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384\" &`
- **T1** `0, 20 %, 1605 MiB`
- **T1** `1, 14 %, 602 MiB`
- **T1** `[timed out after 600000ms]`
- **T1** `Qwen : perplexité 19.3885 sur 510 tokens`
- **T1** `gpt-oss : perplexité 15.1757 sur 510 tokens`
- **T1** `- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -m \"Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384\" && git `

