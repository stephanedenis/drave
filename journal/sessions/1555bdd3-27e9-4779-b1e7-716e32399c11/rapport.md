# Session 1555bdd3 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `1555bdd3-27e9-4779-b1e7-716e32399c11` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 09:31 |
| Durée | 1.4 h |
| Tours | 1 |
| Messages | 126 |
| Appels d'outils | 151 |
| Fichiers touchés | 2 |
| Commandes | 122 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, dépôt Drave). Mission : écrire la **documentation d'usage du premier produit** — ce qu'un utilisateur peut faire aujourd'hui, en autonomie, avec le système.  Contexte : lis d'abord `README.md` (la vitrine), `docs/pilotage/en-cours.md` (l'état), `reports/rapport-pensee-v12.md` + `reports/pensee-v12.json` (l'a … [2155 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, dépôt Drave). Mission : écrir … [2435 caractères tronqués]

*151 appels d'outils.* Actions notables :

- bash — List repo root, docs and tools
- read
- bash — Check product dir, reports and tools
- bash — Inspect bloc_linguistique size and v12 JSON
- bash — Read module docstring of bloc_linguistique
- bash — List public functions and constants
- bash — Read autotest, CLI and summary functions
- bash — Find cascade_pos red gate and 0.6s claim
- bash — Inspect tolerated red gates references
- bash — List implantation docs
- bash — Inspect evaluer_gold API and CLI
- bash — Search performance claim 0.6s for 612 corpus
- bash — Find evaluer_gold module
- bash — Read attachment audit header and timing
- … et 124 autres

**Synthèse produite :**

⏵ Contrôle final des sorties de la notice après les changements du hub.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 3 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md` | 2 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repo root, docs and tools
- **T1** Check product dir, reports and tools
- **T1** Inspect bloc_linguistique size and v12 JSON
- **T1** Read module docstring of bloc_linguistique
- **T1** List public functions and constants
- **T1** Read autotest, CLI and summary functions
- **T1** Find cascade_pos red gate and 0.6s claim
- **T1** Inspect tolerated red gates references
- **T1** List implantation docs
- **T1** Inspect evaluer_gold API and CLI
- **T1** Search performance claim 0.6s for 612 corpus
- **T1** Find evaluer_gold module
- **T1** Read attachment audit header and timing
- **T1** Inspect evaluer_gold structure
- **T1** Read bloc-linguistique contract sections
- **T1** Read Annotation.json schema
- **T1** Run heuristic analysis on French sentence
- **T1** Run analyses and save JSON outputs
- **T1** Summarize all analysis outputs
- **T1** Find known failure phrases in gold
- **T1** Analyze known failure sentences
- **T1** Time gold 612 evaluation and check determinism
- **T1** List unattached gold spans
- **T1** Check network usage and refusal cases
- **T1** Test refusal and unknown language outputs
- **T1** Read documentation review rules
- **T1** Read review main checks including links/orphans
- **T1** Check git state and version sources
- **T1** Check JSON keys and timing provenance
- **T1** Inspect the first-product commit
- **T1** Read today's journal for product plan
- **T1** Check byte-identical replay and duration field
- **T1** Run the gold evaluation CLI
- **T1** Inspect gold evaluation tail/verdicts
- **T1** Get concise eval metrics and cascade verdict
- **T1** Analyze failure sentence r035
- **T1** Search for drave.py references and product gate
- **T1** Inspect state change and parent plan
- **T1** Read parent session plan
- **T1** Read existing usage document
- … et 82 autres

## 4. Mesures et résultats marquants

- **T1** `/controle_negatif/permutation = '1,997/220 (0,908 %) p=0'`
- **T1** `/controle_negatif/candidat_aleatoire = '42,14 % top-1'`
- **T1** `f"({a.fraction_semantique:.1%} du texte)")`
- **T1** `[still running after 60000ms; moved to background job bash-2679]`
- **T1** `| `porte-c4-retard.sh` | 29 s | PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne |`
- **T1** `| `porte-coupe.sh` | 131 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit pour  |`
- **T1** `| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.77 s → 9.67 s (+2.9 s ≈ 50 ms × 64 pas) |`
- **T1** `reports/rapport-cache-chunker.md:239:- **Cache complet (C2)** : ×1,026 sur le corpus, ×1,26-3,65 sur les longues ; **×2,06 à 160**,`
- **T1** `reports/rapport-e6-poids-lognormaux.md:62:   7,2241 · 41,6677) — mais l'avantage sur le témoin dense reste **modeste** : ×1,006 sans élagage,`
- **T1** `reports/rapport-e9-homeostasie.md:227:* **ce que la porte ne vérifie pas** : que ×0,6 soit l'optimum **universel** ✗ — le balayage a été`
- **T1** `la cascade (mock de contrat) préserve ces chiffres et couvre **67,1 %** en unités sémantiques.`
- **T1** `(les réels passent de 40 % à 80 % en tête avec les deux lectures). Le **vrai** modèle neuronal est **refusé**`
- **T1** `- **L'attachement par tête couvre 100 %** ; le gold annote 29 cibles ambiguës en double lecture,`
- **T1** `[still running after 60000ms; moved to background job bash-2755]`
- **T1** `CPU + neuronal de contrat, parallèle/cascade, activation 51–76 %) ; **398 langues à 0,9687**,`
- **T1** `**tête 0,560**, pragmatique **1,0/1,0/0,994/0,889** ; cascade (mock) **67,1 %** ;`
- **T1** `0,71 % ✓) — mais ce n'est **pas encore** une vision multimodale utilisable ✗ (§ 2).`
- **T1** `| `lora_recopie.py` ✓ | apprend au modèle à **recopier** (LoRA, 100,0 % avec contrôle à 0,0 % ✓) | `python3 tools/lora_recopie.py --hf <snapshot> --ids <corpus>` |`
- **T1** `| **`lecteur_non_lineaire.py`** ✓ | le lecteur **MLP** (et sa leçon : mal réglé, il **sur-apprend** ✗ — 119,9 % contre 85,2 % pour le ridge ✓) | `... --modeles A,B --ids <corpus>` |`
- **T1** `un ridge **sous-déterminé** (moins de positions que de coefficients ✓) **interpole** et rend 0,0 % ✓✗ ;`
- **T1** `une cible qui contient **sa propre source** (même position ✓) rend aussi 0,0 % ✓✗ ; un plan de textes qui`
- **T1** `unités sémantiques : 2 (61.5% du texte)`
- **T1** `langue=fr script=Latn source=heuristique · 19 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `langue=en script=Latn source=heuristique · 37 étiquettes · unités sémantiques=3 (45.7% du texte)`
- **T1** `POS         exactitude 75.81 %  (fermé 90.04 %, ouvert 62.34 %)`
- **T1** `SYNTAGMES   F1 58.49 %  (P 62.92 % / R 54.64 %)`
- **T1** `tête      F1 73.36 %  (P 81.00 % / R 67.04 %)`
- **T1** `ATTACHEMENT exact 92.89 % · couverture 92.89 % · exact sur span 100.00 % · top-k 92.47 %`
- **T1** `tête      couverture 100.00 % · top-k 99.55 %`
- **T1** `PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %`
- **T1** `FRACTION SÉMANTIQUE 55.37 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)`
- **T1** `POS         exactitude 76.03 %  (fermé 90.07 %, ouvert 62.69 %)`
- **T1** `SYNTAGMES   F1 58.93 %  (P 63.19 % / R 55.22 %)`
- **T1** `tête      F1 73.92 %  (P 81.36 % / R 67.72 %)`
- **T1** `PRAGMATIQUE acte 99.67 % · négation 97.67 % · modalité 98.84 % · double sens 94.35 %`
- **T1** `FRACTION SÉMANTIQUE 55.54 %`
- **T1** `langue=fr script=Latn source=heuristique · 59 étiquettes · unités sémantiques=5 (49.1% du texte)`
- **T1** `langue=en script=Latn source=heuristique · 45 étiquettes · unités sémantiques=4 (43.9% du texte)`
- **T1** `langue=fr script=Latn source=heuristique · 30 étiquettes · unités sémantiques=3 (55.2% du texte)`
- **T1** `[still running after 60000ms; moved to background job bash-2983]`
- **T1** `langue=und script=Latn source=heuristique · 13 étiquettes · unités sémantiques=2 (85.7% du texte)`
- **T1** `**Lecture.** Le banc mesure **20 combinaisons** (4 lectures × 5 sources) et écrit un JSON de`
- **T1** `unités     2 (61,5 %)`
- **T1** `docs/pilotage/roadmap.md:38:**État au 06/11 10 h 45.** B13 est à **183/183** ; **attachement 222/222 (1,0000)** (fr 136/136, en 86/86), **couverture 0,9289**, F1 0,5849 ; dev 153/153, test 69/69 ; **l`
- **T1** `| `porte-homeostasie.sh` | 495 s | ✅ porte tenue (×0 exact · activité monotone · dominance reproduite) |`
- **T1** `produit aucun événement. 15 % de zéros MXFP4 = 0,30 octet/poids économisé,`
- **T1** `(35 M pour 6 400). Le dense, lui, calcule `784 × n_exc × 700` produits : **219 M** pour 400, **3,5 G** pour`
- **T1** `(8,5 tok/s) parce que sa boucle de produit scalaire était limitée par une chaîne`
- **T1** `Conséquence : les identifiants produits diffèrent dans **5,2 % des cas** (38 sur 737).`
- **T1** `Trace produite : 17,4 Mo par couche.`
- **T1** `0,5 à 1,2 % selon le jeu et le contexte, et le gain se reproduit sur des tokens`
- **T1** `# Rapport — Le produit matrice-vecteur f32 de V4.1 : ×9,34 sur l'attention, sans changer un bit`
- **T1** `- Le poste dominant est `proj+mlp` (le produit des experts) : **3 270,65 ms/token**`
- **T1** `AVX2+FMA du produit scalaire (`DRAVE_SIMD_DOT=1`, ×2,06 sur la passe) — un gain`
- **T1** `20 Go/s), mais par le **calcul de déquantification + produit scalaire**.`
- **T1** `| **P9** — noyaux natifs | `matvec_f32` parallèle par lignes : **×9,34** sur l'attention de V4.1, **bit à bit identique** (2 544 vides comparés, 0 écart) ; déqu`
- **T1** `grand pour compenser un routage qui perdait 10 % : le modèle produit est`
- **T1** `> (1) **la chaîne hors-ligne reproduit le moteur** — 0,013 % (24 couches) et 0,006 % (16 couches) :`
- **T1** `> Verdict : **personne.** Le produit théorique monte bien (17,0 % des paires au mieux à la sortie`
- **T1** `* **la tendance du produit se retourne, et son maximum est à 8** : 16,96 % des paires au mieux —`
- **T1** `38,1 %** (m20 ✓) — **la direction du résultat publié est reproduite** ✓, et c'est la **première`
- **T1** `cher**. Le gain de A7.5 venait du flux **synthétique à 20 % de zéros** ; il **ne se reproduit pas**`
- **T1** `| **restitution** (modèle spécialisé, 1 langue) | reproduit-il exactement le texte lu ? | **85,1 %** de fragments de 32 octets exacts (français), **99,4 %** d'o`
- **T1** `> est **verte** (504 s, ×0 exact, activité monotone, dominance reproduite). Les références sont stables :`
- **T1** `> activité monotone, dominance reproduite : m32 ×0,6 **−8,33 %** contre ×1,0 **−6,51 %**, m20 **−15,10 %**`
- **T1** `> la dominance de ×0,6 est reproduite) entre dans la passe, et `porte-vision` y vérifie ses`
- **T1** `calcul**, pas à la mémoire (151 936 lignes × 896 produits par jeton, en`
- **T1** `- **Trace de calcul** : `--drvm-ppl --trace-flux` produit **6 144 listes** (16 Mo) ; rejouée sur le GGUF source et sur le DRVM, elle rend **0 liste manquante**.`
- **T1** `- **Pas de nouvelle mesure du natif** : le **69,3 %** est repris de B11.7 ; il n'est pas reproduit ici.`
- **T1** `- **Pas de champ natif** : le 69,3 % n’est pas reproduit ici.`
- **T1** `- **Pas de champ natif** : le 69,3 % n’est pas reproduit.`
- **T1** `La chaîne anglaise **reproduit la chaîne française** : −10,9 % en domaine (le français : −11,7 %),`
- **T1** `| [rapport-matvec-f32-parallele.md](rapport-matvec-f32-parallele.md) | Rapport — Le produit matrice-vecteur f32 de V4.1 : ×9,34 sur l'attention, sans changer un`
- **T1** `| `drave.py evaluer` | POS 75,81 %, F1 syntagmes 58,49 %, tête 73,36 % | attachement exact 92,89 %, couverture 92,89 % |`
- **T1** `- **La mémoire** : ~50 Mo pour le module.`
- **T1** `134:le gold gelé 602 (F1 58,93 %, POS 76,03 %). La commande sort **0** : elle ne teste pas la cascade`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] ls: cannot access 'tools/evaluer_gold.py': No such file or directory [exit code: 2]

