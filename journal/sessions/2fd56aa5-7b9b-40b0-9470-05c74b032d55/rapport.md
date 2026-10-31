# Session 2fd56aa5 — Dépôt /home/stephane/GitHub/Qtrinet, f

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `2fd56aa5-7b9b-40b0-9470-05c74b032d55` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 18:48 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 30 |
| Appels d'outils | 37 |
| Fichiers touchés | 0 |
| Commandes | 32 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, fenêtre jusqu'à 2026-10-28 08:00 HAE. Sous-agent A19 : améliorer le routeur M1→M2 (B23) par un **score de confiance**, sans modifier les modules existants.  Contexte : - B23 `tools/cerveau/routeur_m1_m2.py` : original 100 %, casse 99,3 %, phrase 92,5 %, espaces 41,8 %, typo **56,2 %** < M2 **68,3 %** (collision de lexique). - M1 `hub.py`, M2 `voies.py`/`m2_typo … [1347 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, fenêtre jusqu'à 2026-10-28 08:00 HAE. Sous-agent A19 : améliorer le routeur M1→M2 ( … [1627 caractères tronqués]

*37 appels d'outils.* Actions notables :

- bash — List repo root and cerveau tools
- bash — Check git status and recent log
- read
- bash — List tests and read hub head
- bash — Read voies head
- bash — Find B23 references
- bash — Check tmp checkpoints and GPU
- bash — Find router JSON and roadmap B23
- bash — Inspect B23 seeds JSON
- bash — Inspect B23 report JSON
- bash — Inspect base checkpoint config
- bash — Inspect real items and normalization
- bash — Locate Python environment with torch
- bash — Look for environment hints
- … et 19 autres

**Synthèse produite :**

⏵ Conception finalisée du score et du protocole
Je vérifie le bus (mémoire) puis j'écris le module.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo root and cerveau tools
- **T1** Check git status and recent log
- **T1** List tests and read hub head
- **T1** Read voies head
- **T1** Find B23 references
- **T1** Check tmp checkpoints and GPU
- **T1** Find router JSON and roadmap B23
- **T1** Inspect B23 seeds JSON
- **T1** Inspect B23 report JSON
- **T1** Inspect base checkpoint config
- **T1** Inspect real items and normalization
- **T1** Locate Python environment with torch
- **T1** Look for environment hints
- **T1** Search for torch and site-packages
- **T1** Inspect system python packages
- **T1** Check drave venv torch
- **T1** Inspect corpus items with venv
- **T1** Read normalization module
- **T1** Read evaluer_champs implementation
- **T1** Read training/eval functions
- **T1** Analyze typo collisions by game
- **T1** Debug B23 typo decisions
- **T1** Inspect 146 items and M1 round-trip
- **T1** Read ItemType and chess codec API
- **T1** Read chess render signature and context handling
- **T1** Compute M1 features and accuracy by bucket
- **T1** Rerun feature analysis with correct codes
- **T1** Inspect B23 M1 typo subset accuracy
- **T1** Benchmark one seed and verify B23 numbers
- **T1** Check context type handling
- **T1** Read Bus implementation
- **T1** Test torch-free imports under system python

## 4. Mesures et résultats marquants

- **T1** `d6fd9c85 A7.5 — GRAPPE SUR RÉSEAU : 4,44× MOINS D'OCTETS, FIDÉLITÉ 1 792/1 792, 0,125 MS LOOPBACK`
- **T1** `361-| B12.8 | **M8 sommeil** | ❌ **marginal** | 96,48 % de champs mais exact **65,1 %**, baseline par jeu **96,10 %** ; leave-one-code-out exact **0 % par construction**, non nuls 63,5 % ; coordonnées`
- **T1** `362-| B12.9 | **M9 lésion** | ✅ **table** | contexte **29,2 %** ; M2 ventrale **24,7 %** ; M2 dorsale **2,1 %** ; M7 **13,7 %** ; M3 **0** ; M4 **0** ; M5 **1,1 %** ; M6 **30 %** ; M8 **0** |`
- **T1** `363-| B12.10 | **Pipeline M1 → M4 → M8** | ⚠️ **intégration** | **528/528**, 7 prototypes, 96,33 % de complétion — tautologique : M4 ne généralise pas, M8 est la marginale |`
- **T1** `364:| B23.1 | **Routeur M1→M2** | ⚠️ **partiel** | original **100 %**, casse **99,3 %**, phrase **92,5 %** = M1 ; espaces **41,8 %** vs M1 **11,6 %** ; typo **56,2 %** < M2 **68,3 %** (collision de le`
- **T1** `365-| B22.1 | **M2 et les typos** | ⚠️ **niche robuste** | M1 suppression **32,8 %**, substitution **27,1 %**, insertion **44,5 %**, transposition **24,1 %** ; M2 `de` **72,6 / 62,3 / 66,4 / 70,5 %**,`
- **T1** `366-| B21.1 | **M9 par dose** | ✅ **dose** | M3 span **0/4/8/12/12** (linéaire, tautologique) ; M5 ordre 0/1/2 **13,81/15,70/18,06 %** (+4,25 pts, surprise +0,012 nat) ; sham **nul** ; double lésion *`
- **T1** `367-| B19.1 | **M2 secours hors codec** | ⚠️ **typos seulement** | M1 original **100 %**, casse **98,7 %**, phrase **86,6 %** ; M1 espaces **34,8 %**, typo **36,6 %** ; M2 typo **71,2 / 76,7**, espace`
- **T1** `402-celle du module unique. Le `sino-tibetan` partait de **40,5 %** avant l'entraînement (le modèle connaissait déjà une`
- **T1** `406-> à 56,2 % ; **B22** : typos réelles et secours conditionnel ; **B21** : reproduire la dose M5 sur une`
- **T1** `Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 947.50it/s]`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/m2_typo.py", line 14, in <module>     from .voie
- **T1** : n 146 Counter({'echecs': 146}) Counter({'ml-echecs-nf3': 61, 'ml-echecs-e4': 61, 'echecs-e4': 7, 'echecs-nf3': 6, None: 4, 'echecs-petit-roque': 2, 'echecs-grand-roque': 2, 'echecs-promotion': 2, 'ech
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/a19_features.py", line 42, in <module>     code_ok=int(p==it.code)                    ^^^^^^^ AttributeError: 'Item' object has no attribute 'c

