# Session 8c024745 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `8c024745-95cb-4885-9d0b-865142606b6d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 08:58 |
| Durée | 0.5 h |
| Tours | 1 |
| Messages | 74 |
| Appels d'outils | 90 |
| Fichiers touchés | 1 |
| Commandes | 61 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français). La machine est dédiée : 2 GPU Quadro RTX 5000 libres, 40 threads.  TÂCHE : mesurer la GRAMMATICALITÉ du modèle natif de 100 M (work/n2ac/mix1024-100m.pt) avec le banc existant, et comparer au 34 M déjà mesuré.  Étapes : 1. Lis reports/rapport-grammaticalite*.md (ou le rapport qui porte le banc  … [1875 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français). La machine est  … [2155 caractères tronqués]

*90 appels d'outils.* Actions notables :

- bash — Liste les fichiers de grammaticalité
- glob
- read
- bash — Cherche les rapports de grammaticalité
- bash — Lit les JSON de grammaticalité et le rapport 100M
- bash — Vérifie banc_generation et JSON de génération
- bash — Vérifie GPU, torch et fichiers modèles
- bash — Inspecte structure des JSON de génération
- bash — Compte les paramètres des deux modèles
- bash — Cherche le contexte du 100M et l'état git
- bash — Vérifie la fenêtre et l'analyseur
- bash — Vérifie le protocole 128 octets du 34M
- bash — Génère 100M, 20 prompts, 128 octets, cuda:0
- bash — Lit le récit du 16 novembre sur le modèle
- … et 65 autres

**Synthèse produite :**

⏵ Récapitulatif final

\## Livrables

- `reports/banc-grammaticalite-100m.json` — clés `n128`, `n64`, `controle_100m_n128`
- `reports/rapport-grammaticalite-100m.md` — fiche complète (protocole, tableaux, contrôles, limites, protocole r1)
- Aucun code modifié : `banc_grammaticalite.py` ne charge pas de modèle et `banc_generation.py` avait déjà `--device`. Aucun commit, aucun fichier interdit touché.

\## Chiffres clés

**n=128 (protocole exact du 34 M, 20 prompts, 3 réglages, même analyseur) :**

| modèle | réglage | GV | ciment | GV/100 mots |
|---|---|---:|---:|---:|
| 34 M | greedy | **6,90** | **0,335** | 15,4 |
| 34 M | top-40/0,8 | 6,35 | 0,377 | 18,0 |
| 34 M | top-20/0,5 | 5,85 | 0,310 | 15,2 |
| **100 M** | greedy | **1,45** | **0,661** | 4,1 |
| **100 M** | top-40/0,8 | 4,00 | 0,375 | 14,4 |
| **100 M** | top-20/0,5 | 2,65 | 0,461 | 8,3 |

En greedy, 8/20 textes du 100 M n'ont aucun GV (3/20 pour le 34 M).

**n=64 (contrôle de longueur) :** 34 M greedy **3,35 GV / 0,427** ; 100 M greedy **1,10 / 0,693** ; contrôle 34 M aléatoire n=64 **1,50 / 0,790**. Le contrôle 100 M aléatoire n=128 donne **4,75 GV / 0,763**.

**Ratios GV/100 au hasard :** 34 M **3,4–4,7×** (stable à 64 et 128 octets) ; 100 M greedy **0,8×** (n=128, son propre hasard) et **1,8×** (n=64) — au plancher ; top-40/top-20 **1,9–3,4×**.

\## Deux réserves majeures

1. **Le « 100 M » fait 73 366 568 paramètres** (×2,14, pas ×3) et **3 000 pas** contre 30 000 pour le 34 M (PPL val **4,014** contre **2,404**) : la comparaison confond échelle et entraînement. Ne pas conclure « l'échelle n'achète pas la grammaire ».
2. **GV et ciment mesurent surtout la classe du token de boucle** : 42 % des GV du 34 M sont le seul « a » (58/138) ; 46 % des mots du 100 M sont « de » (304/661). Le 100 M est plus répétitif (46 % vs 18 % de mot dominant) et moins divers (74 vs 149 types), mais le banc ne prouve pas qu'il est « moins grammatical ».

\## Commandes

```bash
\# génération 100 M, n=128, GPU
/home/stephane/gpu-env/bin/python tools/banc_generation.py \
  --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 \
  --sortie /tmp/banc-generation-100m-128o.json

\# grammaticalité n=128, contrôle 34 M aléatoire n=128
/home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py \
  --entree /tmp/banc-generation-100m-128o.json \
  --controle reports/banc-generation-aleatoire.json \
  --sortie /tmp/banc-grammaticalite-100m-128o-controle34.json

\# grammaticalité n=64, contrôle 34 M aléatoire n=64
/home/stepha
… [510 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grammaticalite-100m.md` | 1 | 12 |

### Commandes exécutées (échantillon)

- **T1** Liste les fichiers de grammaticalité
- **T1** Cherche les rapports de grammaticalité
- **T1** Lit les JSON de grammaticalité et le rapport 100M
- **T1** Vérifie banc_generation et JSON de génération
- **T1** Vérifie GPU, torch et fichiers modèles
- **T1** Inspecte structure des JSON de génération
- **T1** Compte les paramètres des deux modèles
- **T1** Cherche le contexte du 100M et l'état git
- **T1** Vérifie la fenêtre et l'analyseur
- **T1** Vérifie le protocole 128 octets du 34M
- **T1** Génère 100M, 20 prompts, 128 octets, cuda:0
- **T1** Lit le récit du 16 novembre sur le modèle
- **T1** Affiche les échantillons 100M à 64 octets
- **T1** Lit la ligne N de l'état courant
- **T1** Vérifie l'activité GPU et CPU du job
- **T1** Vérifie l'état détaillé du processus
- **T1** Compare l'heure et l'âge du processus
- **T1** Contrôle l'avancement du job
- **T1** Teste le banc de grammaticalité sur les données 64 octets
- **T1** Attend et vérifie le job de génération
- **T1** Attend la fin de la génération
- **T1** Affiche les résultats de génération 100M 128 octets
- **T1** Produit le JSON de grammaticalité 100M
- **T1** Reproduit la référence 34M et compare
- **T1** Génère le contrôle aléatoire 100M, 128 octets
- **T1** Analyse la composition lexicale des générations
- **T1** Lit les métadonnées du 34M et le log du 100M
- **T1** Calcule les écarts et GV normalisés
- **T1** Vérifie l'avancement du contrôle aléatoire
- **T1** Lit la configuration par défaut du modèle natif
- **T1** Mesure la part de « de » dans les classes fermées
- **T1** Inspecte la classe Etiquette
- **T1** Calcule la concentration de « de » dans les classes fermées
- **T1** Attend le contrôle aléatoire 100M
- **T1** Compare les préfixes greedy 64 et 128 octets
- **T1** Vérifie la fin du contrôle aléatoire
- **T1** Calcule la grammaticalité du contrôle 100M
- **T1** Compare le greedy 34M CPU/GPU et inspecte le hasard
- **T1** Affiche les deux générations greedy 34M
- **T1** Refait la comparaison de préfixes dans le bon sens
- … et 21 autres

## 4. Mesures et résultats marquants

- **T1** `1. **Le vocabulaire est saturé dès 34 M** : 0,884 contre 0,882 en greedy — l'échelle ×3 n'achète`
- **T1** `0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `| 15:52 | `14ef014d` | ÉTUDE — LES 2 GPU NVLink VS CPU : L'ENTRAÎNEMENT ×12-39 (×77 EN TANDEM), LE PRÉFILL ×12, LE NVLink 23 Go/s, MAIS LE 34 M EST SOUS-UTILISÉ ET LA GÉNÉRATION EST BLOQUÉE PAR LE CAC`
- **T1** ``×12` · `×77` · `×20` · `23 Go` · `0,137` · `0,278` · `0,335` · `0,247` · `0,494` · `0,870``
- **T1** `0, 1 MiB, 0 %`
- **T1** `1, 1 MiB, 0 %`
- **T1** `0, 502 MiB, 57 %`
- **T1** `1, 4 MiB, 0 %`
- **T1** `0, 4 MiB, 0 %`
- **T1** `1, 124 MiB, 0 %`
- **T1** `top40_0.8 mots 101 top5 [('�', 2), ("�f&����7�+��*\x1b?]c�e����l�(zsu'i�\x00z:\x02ư�v߰��$l\x00wvw܋��g���ռ�f\x0el'#�g", 1), ('�\x11>h�˫/r�', 1), ('n*�ji*�', 1), ('l��3��\x12���(�y+ca\x05,c~ga"pdk�\x04%`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : {  "modele": "drave-n0-rope",  "parametres": 34301224,  "corpus": "data/wiki_mix/propre/train.txt",  "octets": 1017487092,  "pas": 30000,  "seq": 1024,  "lot": 8,  "lr": 0.0003,  "graine": 1,  "window
- **T1** : greedy textes sans verbe (brut): top40_0.8 textes sans verbe (brut): top20_0.5 textes sans verbe (brut): == 34M [stderr] Traceback (most recent call last):   File "<stdin>", line 23, in <module>   Fil

