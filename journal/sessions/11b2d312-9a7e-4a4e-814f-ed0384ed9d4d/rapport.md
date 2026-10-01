# Session 11b2d312 — Tu es relecteur ADVERSARIAL autonome

| | |
|---|---|
| Identifiant | `11b2d312-9a7e-4a4e-814f-ed0384ed9d4d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-01 02:50 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 42 |
| Appels d'outils | 60 |
| Fichiers touchés | 0 |
| Commandes | 56 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSARIAL autonome dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave »). Mission : auditer les artefacts du sprint 5 (01h37 → 03h37) — aucun chiffre sans source, aucune affirmation qui dépasse la mesure, aucun outil qui fait ce qu'il annonce sans le faire.  Contexte : la nuit compte déjà quatre « artefact-trust errors » (un garde-fou j … [3412 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSARIAL autonome dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence R … [3692 caractères tronqués]

*60 appels d'outils.* Actions notables :

- bash — Inspect repo root and recent commits
- bash — Check existence of cited source files
- bash — Locate sprint 5 sections in report
- bash — Dump all aiguille logs
- read
- bash — Search 8192 and growth claims in report
- bash — Read report head
- bash — Check working tree and commit contents
- bash — Show full commit messages of last three
- bash — Show stats of the two other commits
- bash — List sprint journal files
- bash — List changed paths and journal dirs
- bash — Grep for the growth section title
- bash — Read session rapport and digest
- … et 45 autres

**Synthèse produite :**

⏵ Rédigeant le rapport d'audit final.

Audit terminé. Aucun fichier du dépôt modifié (`git status` inchangé : seul `journal/README.md`, déjà modifié avant mon passage), aucune sonde coûteuse lancée — j'ai vérifié par lecture, calcul, relance du comparateur et tokenisation (gratuite) via `--tokenize`.

\## Écart 1 — [GRAVE] La mesure à 8 192 n'existe dans aucun artefact, et le rapport dit le contraire

**(a) Sections citées** : sujet du commit `0d50e75` ; `reports/rapport-aiguille-topk.md` l.172-181 (« Ce que ce rapport ne dit pas ») et l.196-211 (« Reproduire »).

**(b) Ce qui est écrit** : le sujet du commit affirme « À 8 192 clés, k=1024 (12,5 %) suffit : le k nécessaire croît plus lentement que le contexte (deux points) ». La section nommée par la mission, « Le k nécessaire semble croître PLUS LENTEMENT que le contexte », **n'existe nulle part** : `grep -rni "lentement"` sur tout le dépôt ne rend qu'une ligne, dans la liste des commandes du journal de session.

**(c) Ce que dit la source** : `git show --stat 0d50e75` = 4 fichiers (`journal/README.md`, `MANIFEST.md`, `digest.md`, `rapport.md`), **uniquement des compteurs de session** ; aucun rapport, aucun fichier de sprint. Le rapport, lui, écrit encore l.177 : « 8 192 et 16 384 (grille creuse) : **non mesurés dans ce box** » et l.179-181 : « **seule** la sonde “8 192 / 0,5 / complète” a été lancée ». La source réelle est `/tmp/aiguille_s5.log` §B : **exactement 2 sondes** (k=1024 → oui 764,7 s ; k=2048 → oui 755,7 s), **une seule fenêtre chacune** (prompt 7 963 = offset 0 ; reproduit au token près : 7 955 bruts + 8 du gabarit de chat), et les deux portent « `--attn-topk` … est IGNORÉ en mode lot ». Le rapport ne cite jamais `aiguille_s5.log` (0 occurrence), et sa section « Reproduire » s'arrête au sprint 4.

**(d) Verdict** : **non sourcé + contradiction interne**. « k = 1 024 suffit » n'est soutenu que par 1 fenêtre ; « croît plus lentement » n'est qu'une borne supérieure (aucun k en échec à 8 192 : le seuil n'est pas localisé) ; et le rapport n'applique pas sa propre règle (« trois fenêtres restent un petit échantillon »). Au passage, « 12,5 % » = 1 024/8 192 demandés ; sur les 7 963 clés réellement vues, c'est 12,9 %.

**(e) Correction minimale** : écrire la section dans le rapport (2 sondes, 1 fenêtre, avertissement « IGNORÉ en mode lot », absence de point d'échec, source `/tmp/aiguille_s5.log`) et corriger la puce 177-181 — ou assumer une correction par commit, l'historique ne se réécrivant pas.

\#
… [6400 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Inspect repo root and recent commits
- **T1** Check existence of cited source files
- **T1** Locate sprint 5 sections in report
- **T1** Dump all aiguille logs
- **T1** Search 8192 and growth claims in report
- **T1** Read report head
- **T1** Check working tree and commit contents
- **T1** Show full commit messages of last three
- **T1** Show stats of the two other commits
- **T1** List sprint journal files
- **T1** List changed paths and journal dirs
- **T1** Grep for the growth section title
- **T1** Read session rapport and digest
- **T1** Grep for growth claims across markdown
- **T1** Show 0d50e75 diff on session rapport
- **T1** Show journal README diffs
- **T1** Show 508d3d8 report diff
- **T1** Compute corpus length and offset sequence
- **T1** Rerun the logits comparison
- **T1** Find the grep pattern in scripts
- **T1** Dump sprint 5 shell runners
- **T1** Read compare_logits tool
- **T1** Locate attn-topk lot-mode guard in source
- **T1** Read rest of compare_logits
- **T1** Read lot-mode guard and topk decode path
- **T1** Find forward function boundaries
- **T1** Search digest for sprint5 8192 narration
- **T1** Compare the three window slices
- **T1** Search 1024-k claims across docs
- **T1** Find lot1/lot256 bin creation in digest
- **T1** Inspect bin headers and tool history
- **T1** Read digest lines around bin generation
- **T1** Find dense 8192 command and sprint files
- **T1** Compute Clopper-Pearson interval for 1/3
- **T1** Correct Clopper-Pearson bounds
- **T1** Read sprint 5 file
- **T1** Global search for the growth wording
- **T1** Cross-check table against log
- **T1** Simulate offset behaviour on edge cases
- **T1** Confirm sprint4 prompts and tokenizer availability
- … et 16 autres

## 4. Mesures et résultats marquants

- **T1** `0d50e75 À 8 192 clés, k=1024 (12,5 %) suffit : le k nécessaire croît plus lentement que le contexte (deux points)`
- **T1** `2ae761c Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5`
- **T1** `92:| **k = 512** (12,5 %) | NON (240,5 s) | NON (238,1 s) | NON (237,8 s) | **0/3** |`
- **T1** `101:structurelle du top-k : **0 à k = 256 (6,25 %), 0 à k = 512 (12,5 %), 3/3 à`
- **T1** `104:déjà non à 512 et oui à 1 024. Le seuil est donc **entre 512 et 1 024 clés** (12,5 % et`
- **T1** `190:  entre 12,5 % et 25 % du contexte sur ce cas.`
- **T1** `**En une ligne** : à 4 096 clés, l'attention à **256 clés (6,25 %)** des 24 jetons`
- **T1** `générés (0,58 % des passes), ce qui est bien le moment où le modèle doit regarder`
- **T1** `lots est donc actif en inférence, et le chiffre « ~175 ms par jeton de prompt »`
- **T1** `était faux lui aussi (4114 jetons à 175 ms feraient 720 s, alors que la sonde`
- **T1** `À 8 192 clés, k=1024 (12,5 %) suffit : le k nécessaire croît plus lentement que le contexte (deux points)`
- **T1** `| k = 256 (6,25 %) | NON | oui | oui | **1/3** |`
- **T1** `| k = 1 024 (25 %) | oui | oui | oui | **3/3** |`
- **T1** `trois essais va de 1 % à 90 %) : le sprint 6 en fera neuf.`
- **T1** `La relecture adversariale du mode 4 (fraîchement écrit) a trouvé **10 défauts, dont 2 graves** — et le plus embarrassant était **un de mes correctifs de l'après-midi** : le refus de `n == 0` que j'ava`
- **T1** `| court/moyen, CPU | **clés f16 + valeurs int8** (39 % du f32, +0,018 %) | le meilleur compromis taille/qualité |`
- **T1** `| long, **avec** miroir VRAM | **int8/int8** homogène | toute variante d'attribution **désactive** le miroir, qui divise l'attention par 40 (1,7 ms contre 70-174 ms par passe) |`
- **T1** `| long, sans GPU | int8/int8 | les clés f16 coûtent **2,3× le temps CPU** (162 contre 70 ms à 262 144 clés) |`
- **T1** `Le mode creux ne peut pas utiliser le miroir VRAM (le chemin GPU est conditionné à `attn_topk == 0`) : à 1 M de clés il coûte **968 ms par couche** contre 13,2 ms. Trois noyaux, une sélection radix, s`
- **T1** `| 3 | collecte des k indices | **même ensemble que le CPU** (diff. symétrique **0**), **0,95 ms** contre 1 653 ms de tri à 1 M |`
- **T1** `| 4 | `attn_topk_somme` | écart **1,0–4,8e-7** · temps GPU **constant (0,07 ms)** |`
- **T1** `| 5 | `DRAVE_GPU_TOPK=1` dans `forward` | PPL identique (12,2265 vs 12,2267) · **à 2 047 clés vues : attention 19,58 → 7,59 ms/jeton (−61 %), balayage −24 %** |`
- **T1** `| 6 | à 1 M clés | chaîne complète **3,90 ms** contre 539,9 ms CPU (×138), **0,3×** le complet en VRAM |`
- **T1** `Fusionner la sélection en un noyau par ligne (8 lancements → 2), supprimer le tampon `nh × n × 4` par couche, refuser bruyamment `-`
- **T1** `- **T1** `// scalaire dense (pull). Le croisement mesuré est à 10 %.``
- **T1** `- **T1** `part de l'attention dans le flux d'événements : 100.0 %``
- **T1** `- **T1** `255 tokens notés — perplexité cumulée 17.431  (31.9 tok/s)``
- **T1** `- **T1** `510 tokens notés — perplexité cumulée 19.388  (31.8 tok/s)``
- **T1** `- **T1** `=== perplexité 19.3885 sur 510 tokens (0 événements, 16.1 s) ===``
- **T1** `- **T1** `0  1.00000000e+00  1.00000000e+00    0.000 %``
- **T1** `- **T1** `1  6.89044306e-01  6.89044306e-01    0.000 %``
- **T1** `- **T1** `2  4.74782055e-01  4.74782055e-01    0.000 %``
- **T1** `- **T1** `3  3.27145872e-01  3.27145872e-01    0.000 %``
- **T1** `- **T1** `4  2.25418000e-01  2.25418000e-01    0.000 %``
- **T1** `- **T1** `5  1.55322989e-01  1.55322989e-01    0.000 %``
- **T1** `- **T1** `6  1.07024421e-01  1.07024421e-01    0.000 %``
- **T1** `- **T1** `7  7.37445682e-02  7.37445682e-02    0.000 %``
- **T1** `- **T1** `8  5.08132748e-02  5.08132748e-02    0.000 %``
- **T1** `- **T1** `9  3.17056962e-02  3.16207523e-02    0.268 %``
- **T1** `- **T1** `10  1.93350011e-02  1.94509675e-02    0.600 %``
- **T1** `- **T1** `11  1.15920493e-02  1.17921911e-02    1.727 %``
- **T1** `- **T1** `12  6.79495949e-03  7.01571391e-03    3.249 %``
- **T1** `- **T1** `13  3.86035932e-03  4.06955471e-03    5.419 %``
- **T1** `- **T1** `14  2.09379238e-03  2.27727194e-03    8.763 %``
- **T1** `- **T1** `15  1.05260210e-03  1.20613097e-03   14.586 %``
- **T1** `- **T1** `16  4.56483919e-04  5.80947502e-04   27.266 %``
- **T1** `- **T1** `17  1.29318701e-04  2.27947796e-04   76.268 %``
- **T1** `- **T1** `18  3.83088124e-05  3.83088124e-05    0.000 %``
- **T1** `- **T1** `19  2.63964690e-05  2.63964690e-05    0.000 %``
- **T1** `- **T1** `20  1.81883367e-05  1.81883367e-05    0.000 %``
- **T1** `- **T1** `21  1.25325698e-05  1.25325698e-05    0.000 %``
- **T1** `- **T1** `22  8.63549588e-06  8.63549588e-06    0.000 %``
- **T1** `- **T1** `23  5.95023926e-06  5.95023926e-06    0.000 %``
- **T1** `- **T1** `24  4.09997848e-06  4.09997848e-06    0.000 %``
- **T1** `- **T1** `25  2.82506683e-06  2.82506683e-06    0.000 %``
- **T1** `- **T1** `26  1.94659621e-06  1.94659621e-06    0.000 %``
- **T1** `- **T1** `27  1.34129104e-06  1.34129104e-06    0.000 %``
- **T1** `- **T1** `28  9.24208950e-07  9.24208950e-07    0.000 %``
- **T1** `- **T1** `29  6.36820915e-07  6.36820915e-07    0.000 %``
- **T1** `- **T1** `30  4.38797825e-07  4.38797825e-07    0.000 %``
- **T1** `- **T1** `31  3.02351143e-07  3.02351143e-07    0.000 %``
- **T1** `- **T1** `63 tokens notés — perplexité cumulée 20.836  (5.2 tok/s)``
- **T1** `- **T1** `=== perplexité 20.8361 sur 63 tokens (0 événements, 12.2 s) ===``
- **T1** `- **T1** `63 tokens notés — perplexité cumulée 41.114  (5.0 tok/s)``
- **T1** `- **T1** `=== perplexité 41.1140 sur 63 tokens (0 événements, 12.5 s) ===``
- **T1** `- **T1** `[timed out after 600000ms]``
- **T1** `- **T1** `238 tokens notés — perplexité cumulée 144.168  (4.9 tok/s)``
- **T1** `- **T1** `357 tokens notés — perplexité cumulée 320.482  (4.9 tok/s)``
- **T1** `- **T1** `511 tokens notés — perplexité cumulée 247.031  (4.9 tok/s)``
- **T1** `- **T1** `=== perplexité 247.0308 sur 511 tokens (0 événements, 104.5 s) ===``
- **T1** `- **T1** `255 tokens notés — perplexité cumulée 13.715  (5.0 tok/s)``
- **T1** `- **T1** `509 tokens notés — perplexité cumulée 15.076  (5.0 tok/s)``
- **T1** `- **T1** `=== perplexité 15.0763 sur 509 tokens (0 événements, 102.5 s) ===``
- **T1** `- **T1** `119 tokens notés — perplexité cumulée 940.867  (4.9 tok/s)``
- **T1** `- **T1** `(**5,62 tok/s**), premier jeton en 166 ms.``
- **T1** `- **T1** `/// deux architectures se croisent à 10 % de densité ; on bascule un peu``
- **T1** `- **T1** `226 tokens notés — perplexité cumulée 3940.363  (4.6 tok/s)  [fenêtre 1 : 226 notés, PPL 3940.363]``
- **T1** `- **T1** `452 tokens notés — perplexité cumulée 3476.367  (4.6 tok/s)  [fenêtre 2 : 226 notés, PPL 3067.009]``
- **T1** `- **T1** `511 tokens notés — perplexité cumulée 3431.623  (4.5 tok/s)  [fenêtre 3 : 59 notés, PPL 3107.404]``
- **T1** `- **T1** `=== perplexité 3431.6228 sur 511 tokens (0 événements, 113.9 s) ===``
- **T1** `- **T1** `230 tokens notés — perplexité cumulée 5559.111  (4.7 tok/s)  [fenêtre 1 : 230 notés, PPL 5559.111]``
- **T1** `- **T1** `460 tokens notés — perplexité cumulée 10738.682  (4.6 tok/s)  [fenêtre 2 : 230 notés, PPL 20744.198]``
- **T1** `- **T1** `511 tokens notés — perplexité cumulée 8462.826  (4.6 tok/s)  [fenêtre 3 : 51 notés, PPL 987.567]``
- **T1** `- **T1** `=== perplexité 8462.8255 sur 511 tokens (0 événements, 111.7 s) ===``
- **T1** `- **T1** `230 tokens notés — perplexité cumulée 643.509  (4.8 tok/s)  [fenêtre 1 : 230 notés, PPL 643.509]``
- **T1** `- **T1** `460 tokens notés — perplexité cumulée 549.601  (4.9 tok/s)  [fenêtre 2 : 230 notés, PPL 469.398]``
- **T1** `- **T1** `511 tokens notés — perplexité cumulée 442.825  (4.8 tok/s)  [fenêtre 3 : 51 notés, PPL 63.104]``
- **T1** `- **T1** `=== perplexité 442.8254 sur 511 tokens (0 événements, 106.0 s) ===``
- **T1** `- **T1** `255 tokens notés — perplexité cumulée 14.483  (5.1 tok/s)  [fenêtre 1 : 255 notés, PPL 14.483]``
- **T1** `- **T1** `509 tokens notés — perplexité cumulée 17.141  (5.2 tok/s)  [fenêtre 2 : 254 notés, PPL 20.301]``
- **T1** `- **T1** `=== perplexité 17.1414 sur 509 tokens (0 événements, 98.5 s) ===``
- **T1** `- **T1** `255 tokens notés — perplexité cumulée 24.579  (5.2 tok/s)  [fenêtre 1 : 255 notés, PPL 24.579]``
- **T1** `- **T1** `509 tokens notés — perplexité cumulée 26.154  (5.2 tok/s)  [fenêtre 2 : 254 notés, PPL 27.837]``
- **T1** `- **T1** `=== perplexité 26.1538 sur 509 tokens (0 événements, 98.8 s) ===``
- **T1** `- **T1** `prompt  : 5 tokens en 0.815 s  (6.1 tok/s, TTFT 163.0 ms)``
- **T1** `- **T1** `généré  : 16 tokens en 2.989 s  (5.35 tok/s)``
- **T1** `- **T1** `prompt  : 5 tokens en 0.842 s  (5.9 tok/s, TTFT 168.4 ms)``
- **T1** `- **T1** `généré  : 16 tokens en 3.073 s  (5.21 tok/s)``
- **T1** `- **T1** `1 tokens notés — perplexité cumulée 14469095357.465  (0.2 tok/s)``
- **T1** `- **T1** `=== perplexité 14469095357.4649 sur 1 tokens (0 événements, 4.2 s) ===``
- **T1** `- **T1** `89 tokens notés — perplexité cumulée 25.009  (4.2 tok/s)``
- **T1** `- **T1** `=== perplexité 25.0091 sur 89 tokens (0 événements, 21.3 s) ===``
- **T1** `- **T1** `229 tokens notés — perplexité cumulée 13.657  (5.2 tok/s)``
- **T1** `- **T1** `=== perplexité 13.6567 sur 229 tokens (0 événements, 44.1 s) ===``
- **T1** `- **T1** `254 tokens notés — perplexité cumulée 203.115  (5.2 tok/s)``
- **T1** `- **T1** `=== perplexité 203.1151 sur 254 tokens (0 événements, 49.2 s) ===``
- **T1** `- **T1** `13 tokens notés — perplexité cumulée 14.626  (2.0 tok/s)``
- **T1** `- **T1** `=== perplexité 14.6260 sur 13 tokens (0 événements, 6.5 s) ===``
- **T1** `- **T1** `19 tokens notés — perplexité cumulée 5.721  (4.9 tok/s)``
- **T1** `- **T1** `=== perplexité 5.7209 sur 19 tokens (0 événements, 3.8 s) ===``
- **T1** `- **T1** `89 tokens notés — perplexité cumulée 677321.831  (2.0 tok/s)``
- **T1** `- **T1** `=== perplexité 677321.8310 sur 89 tokens (0 événements, 44.5 s) ===``
- **T1** `- **T1** `316 tokens notés — perplexité cumulée 258.640  (5.2 tok/s)``
- **T1** `- **T1** `=== perplexité 258.6401 sur 316 tokens (0 événements, 61.3 s) ===``
- **T1** `- **T1** `=== perplexité 258.6401 sur 316 tokens (0 événements, 61.6 s) ===``
- **T1** `- **T1** `=== perplexité 1880.7184 sur 301 tokens (0 événements, 57.6 s) ===``
- **T1** `- **T1** `89 tokens notés — perplexité cumulée 677321.831  (1.9 tok/s)``
- **T1** `- **T1** `=== perplexité 677321.8310 sur 89 tokens (0 événements, 46.7 s) ===``
- **T1** `- **T1** `255 tokens notés — perplexité cumulée 17.431  (31.8 tok/s)  [fenêtre 1 : 255 notés, PPL 17.431]``
- **T1** `- **T1** `510 tokens notés — perplexité cumulée 19.388  (31.8 tok/s)  [fenêtre 2 : 255 notés, PPL 21.565]``
- … (tronqué)

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : te :**  ⏵ Créneau 15h07 → 18h00 terminé : machine rendue, dépôt vert, objectif clos.  \## Créneau 15h07 → 17h35 — ce qui a été fait  \### 1. Le mode 4 « lot en listes » : écrit, mesuré, relu, corrigé 

