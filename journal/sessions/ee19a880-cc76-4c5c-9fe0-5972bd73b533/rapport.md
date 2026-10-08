# Session ee19a880 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `ee19a880-cc76-4c5c-9fe0-5972bd73b533` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:18 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 30 |
| Appels d'outils | 43 |
| Fichiers touchés | 0 |
| Commandes | 32 |
| Sous-agents | 2 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave : moteur d'inférence Rust dans drave-core/, outils Python dans tools/, rapports dans reports/). MISSION STRICTEMENT EN LECTURE : n'écris, ne modifie et ne lance AUCUN fichier ni entraînement. Uniquement read/grep/glob et commandes bash de lecture (ls, wc, du, file, head) — jamais rien qui écrive ou télécharge … [2818 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave : moteur d'inférence Rust dans … [3098 caractères tronqués]

*43 appels d'outils.* Actions notables :

- bash — List repo root and tools directory
- bash — Find weight/checkpoint files in repo
- bash — Inspect models, data, colab, src dirs
- bash — Look at neighboring plausible locations
- bash — List weight files inside repo
- bash — Inventory neighbor weight files
- grep
- bash — Find references to pont_semantique.npz
- read
- sous-agent — Analyser scripts directions/discriminants
- sous-agent — Chercher entraînements hors tools
- bash — Map methods and fit calls in pont_generatif
- bash — Read pont_generatif lines 160-340
- bash — Find all save calls and read options
- … et 24 autres

**Synthèse produite :**

⏵ Résultat livré au parent ; synthèse finale

**MISSION LECTURE SEULE respectée** : aucun fichier écrit, aucune commande d'écriture/téléchargement, aucun script exécuté. Tout est *mesuré* (code lu, `ls`/`unzip`/`md5`), sauf mention « supposé ».

\## A. Le seul poids entraîné et persisté du projet
| Chemin absolu | Taille / date | Ce que c'est |
|---|---|---|
| `/home/stephane/Data13TB/stephane/pont_semantique.npz` | 1 382 064 o · 05/10 10:45 · md5 `325a5583…` | Écrit par `tools/pont_recurrent.py` L191-193 (env `DRAVE_PONT_SORTIE`). Contenu vérifié : `P` f4 (896,128), `moy` f4 (896), `W0` f8 (896,128), `couche`, `rang`, `langues_train/test`. Lu par `tools/applique_pont.py` L58 et `tools/sonde_pont.py` L85. |
| `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz` | 1 382 064 o · 05/10 10:47 | Copie **byte-identique** (même md5). |
| `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz` | 16 560 o · 05/10 11:02 | Rang 1 : `P` (896,1), `W0` (896,1) f8, `moy` (896). « `--rang 1` » = supposé (défaut du script : 64). |

Aucun `.pt/.pth/.safetensors/.pkl/.ckpt/.bin` de poids dans le dépôt (`find` = 0). `models/` = 2 GGUF téléchargés (Qwen2.5-0.5B Q4_0 353 Mo, Q8_0 531 Mo) → inférence seule.

\## B. Pont (point 3) — ajustement de la lecture en forme fermée, sans rétropropagation
Base : entrée = plongée couche 0 (T,896) ; cible = couche 10 du professeur (896).
- `tools/pont_recurrent.py` — 2 régressions crête : récurrence `s_t=A·s_{t−1}+B·e_t` dans un sous-espace de rang r (SVD de Y, défaut 64) + témoin `W0`. Loss `‖XW−Y‖²+λ‖W‖²`, λ=1e-2·n, `np.linalg.solve`, **0 itération** ; rayon spectral de A ramené à 0,95. **ÉCRIT `pont_semantique.npz`**.
- `tools/pont_generatif.py` (moteur, 1041 l.) — réseau récurrent qui **croît puis subit une attrition**. Neurone : `s=(1−a)s+a·tanh(W_par·x_{c−1}+W_self·s+B·e_t)`, a=0,2 (ou 120 constantes log-étalées [0,02;0,8]), B/W_self **aléatoires gelés** (graine 5) ; seule W s'ajuste (`solve`, ride=0,3) ; lecture quadratique `[X,X²]` optionnelle (240 col.). Objectif `‖XW−Y‖² + μ_lang·P_lang − μ_cont·P_cont`. Défauts : 3 cycles × 3 couches, naissance 1,1,2,4… puis +n/4, plafond 256 neurones, patience 12, seuil d'attrition 0,02 (retrait de 25 % par redondance `1−1/((G⁻¹)_jj·G_jj)` ou contribution), retour au meilleur passage, `renforce()` local η=0,6. **N'écrit aucun poids.**
- `pont_reservoir.py` — réservoir N=256 gelé (rayon 0,9), fuite a=0,2, W seule (ride 3e-1). `pont_fidele.py` — linéaire rangs 1→128 et ELM
… [4201 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Sous-agents lancés

- tour 1 — Analyser scripts directions/discriminants
- tour 1 — Chercher entraînements hors tools

### Commandes exécutées (échantillon)

- **T1** List repo root and tools directory
- **T1** Find weight/checkpoint files in repo
- **T1** Inspect models, data, colab, src dirs
- **T1** Look at neighboring plausible locations
- **T1** List weight files inside repo
- **T1** Inventory neighbor weight files
- **T1** Find references to pont_semantique.npz
- **T1** Map methods and fit calls in pont_generatif
- **T1** Read pont_generatif lines 160-340
- **T1** Find all save calls and read options
- **T1** Read pont_generatif main loop and end
- **T1** Read 5 pont helper scripts
- **T1** Read headers of remaining pont scripts
- **T1** Inspect npz artifacts headers
- **T1** Read artifact writer and git history
- **T1** Trace origins of tmp bin files
- **T1** Search distillation and teacher mentions
- **T1** Check bin dump origin and pont report
- **T1** Read pont-semantique report conclusion
- **T1** Enumerate closed-form fit scripts
- **T1** List npz entries and read REPRISE excerpt
- **T1** Read npz array headers via unzip -p
- **T1** Extract fit parameters from remaining scripts
- **T1** Check torch-based scripts for training
- **T1** Check clustering scripts for unsupervised fitting
- **T1** Check root run_*.py scripts
- **T1** Verify k-means and tiny_model training
- **T1** Read renforcement.py
- **T1** Read renforcement_directions.py
- **T1** Extract docstrings and fit lines of 11 scripts
- **T1** Find cache npz files and citations
- **T1** Size caches and synthetic GGUF

## 4. Mesures et résultats marquants

- **T1** `649:    # Critère PRINCIPE, là où « 50 % de l'énergie » était un seuil arbitraire : on`
- **T1** `f"{part_langues:.0%} des langues d'apprentissage "`
- **T1** `f"({len(garde)/H:.0%} des canaux)")`
- **T1** `# du vivier coûtait ~35 s par naissance, soit 95 % du temps de la`
- **T1** `6df6de4 §10 : le palier NVMe donne −8,8 %, la prédiction était de −16,3 %`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:11544:- Le pont rang-1 est l'artefact, et la sonde est un échec de protocole — dit tel quel  Artefact : pont_semantique_r1.npz (W0 89`
- **T1** `./REPRISE.md:184:> **L'artefact rang-1** : `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz``
- **T1** `31:| rang 32 | 0,5822 | 0,0447 |`
- **T1** `32:| rang 64 | 0,5380 | 0,0016 |`
- **T1** `33:| rang 128 | 0,4912 | 0,0579 |`
- **T1** `34:| rang 256 | 0,5654 | 0,1266 |`
- **T1** `57:## Résultat 3 — LE PONT : une matrice 896×896 qui rend la langue invisible`
- **T1** `154:  W0 : 896 × 1        P : 896 × 1        moy : 896`
- **T1** `223:seule la lecture `W` (H × 896) s'ajuste, par blocs indépendants.`
- **T1** `260:`B` (64×896) sont **aléatoires et gelés**, donc identiques sur tous les nœuds sans`
- **T1** `261:aucune coordination ; seule la lecture `W` (64×896) s'ajuste, et ses blocs sont`
- **T1** `W0 : 896 × 1        P : 896 × 1        moy : 896`
- **T1** `> **L'artefact rang-1** : `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz``
- **T1** `> (`P` 896×128, `W0` 896×128, `moy` 896), appliqué par`
- **T1** `LATENT (une seule tête de 128 + 32 valeurs par jeton au lieu de n_head × 192),`
- **T1** `et elle échoue : +1,7 % du chemin nécessaire, plateau dès la deuxième passe. La raison`
- **T1** `"""discriminant_transfert.py — les directions apprises sur un panel servent-elles sur un autre ?  LA QUESTION, ET ELLE EST NEUVE. Le §80 a mesuré qu'un discriminant linéaire appris portait le rapport `
- **T1** `"""stabilite_directions.py — les directions du discriminant viennent-elles des DONNÉES ou du TIRAGE ?  LA QUESTION. Le §92 montre qu'un discriminant de rang 2 appris sur nos sorties sépare le contenu `
- **T1** `"""energie_du_contenu.py — peut-on retrouver l'ÉNERGIE de contenu, pas seulement son rapport ?  CE QUI MÈNE ICI. Le §87 a mesuré, hors vivier sur un panel de 6 langues, que notre pont atteint **136 % `
- **T1** `"""calibre_modes.py — le mode DENSE trace-t-il la même chose que le mode ÉVÉNEMENTIEL ?  POURQUOI LA QUESTION SE POSE. Le mode par défaut du moteur construit ses listes d'événements **au chargement** `

