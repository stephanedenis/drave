# Session 206a4022 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-04/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `206a4022-ab3c-497d-a5fa-0194931c7fa0` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-04 15:56 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 36 |
| Appels d'outils | 44 |
| Fichiers touchés | 0 |
| Commandes | 40 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt Drave, racine /home/stephane/Data13TB/stephane/GitHub/Qtrinet (lis AGENTS.md pour le contexte général, mais ton périmètre est strictement celui ci-dessous).  CONTEXTE. La session `aeafe951` a clos la limite de D : les 8 scans `.PDF` du fonds CEGEP (58 p) ont été OCRisés (rapport `reports/rapport-ocr-pdf-restants.md`, manifeste `reports/ocr-pdf-restants.json`, texte brut … [4629 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt Drave, racine /home/stephane/Data13TB/stephane/GitHub/Qtrinet (lis AGENTS.md pour le context … [4909 caractères tronqués]

*44 appels d'outils.* Actions notables :

- bash — Inspecte la racine et les répertoires cibles
- bash — Date courante et liste des outils
- bash — Tailles, dates et SHA-256 des fichiers du corpus
- bash — Comparaison queue et vérification jonction
- bash — cmp de la queue extraite et sommes arithmétiques
- bash — Lit le rapport et manifeste OCR des PDF restants
- bash — Lit le manifeste historique du corpus CEGEP
- bash — Compte octets, caractères, lignes, mots par split
- bash — Cherche le calcul des stats dans ocr_pdf.py
- bash — Inventaire des artefacts OCR
- bash — Lit la logique de tronçons, split et écriture
- bash — Aide du script de contamination
- bash — Lecture du script de contamination
- bash — Traces récentes et état git
- … et 28 autres

**Synthèse produite :**

⏵ Correction du script de mesure 500 o

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Inspecte la racine et les répertoires cibles
- **T1** Date courante et liste des outils
- **T1** Tailles, dates et SHA-256 des fichiers du corpus
- **T1** Comparaison queue et vérification jonction
- **T1** cmp de la queue extraite et sommes arithmétiques
- **T1** Lit le rapport et manifeste OCR des PDF restants
- **T1** Lit le manifeste historique du corpus CEGEP
- **T1** Compte octets, caractères, lignes, mots par split
- **T1** Cherche le calcul des stats dans ocr_pdf.py
- **T1** Inventaire des artefacts OCR
- **T1** Lit la logique de tronçons, split et écriture
- **T1** Aide du script de contamination
- **T1** Lecture du script de contamination
- **T1** Traces récentes et état git
- **T1** Contrôle de contamination 8 Ko sur le corpus réel
- **T1** Mesure indépendante du recouvrement append/ancien train
- **T1** Restaure les 4 430 959 premiers octets et vérifie le hash
- **T1** Contrôle de l'état réel du train après alerte
- **T1** Processus et fichiers récemment modifiés
- **T1** Que contiennent les nouveaux val et test
- **T1** Lecture des constantes et fonctions OCR, liste des PDF
- **T1** Vérifie les trois préfixes et les tailles
- **T1** OCR des 8 PDF un par un sur cpu1
- **T1** Copie des splits 15:57 pour le contrôle négatif
- **T1** Injection alignée d'une fenêtre de val dans une copie du train
- **T1** Contrôle négatif : fenêtre de val injectée dans le train
- **T1** Fenêtres 8 Ko des suffixes dans les préfixes et autres suffixes
- **T1** Identifie la fenêtre 8 Ko du suffixe présente dans le préfixe
- **T1** Compare les empreintes OCR aux manifestes
- **T1** Teste les variantes de hash et le contenu OCR
- **T1** Fenêtres 500 o par texte dans préfixes et suffixes
- **T1** Exemples et offsets de la duplication DOC1/DOC2
- **T1** Contamination 8 Ko finale avec contrôle de stabilité
- **T1** Vérifie l'absence des livrables et inspecte les suffixes
- **T1** Longueurs et offsets des textes OCR dans les suffixes
- **T1** Construit train/val/test propres et vérifie les jonctions
- **T1** Contamination 8 Ko sur le corpus propre
- **T1** Contrôle négatif du corpus propre
- **T1** Baseline 500 o et contrôle du corpus propre
- **T1** Mesure baseline et propre en 500 o

## 4. Mesures et résultats marquants

- **T1** `> 9 tronçons de 8 Ko) : **6 fichiers uniques**, **5 textes distincts**, **3 copies** et **1`
- **T1** `| tronçons de 8 Ko | **9** |`
- **T1** `| `DOC.PDF` ×2 | 1 | 210 | `7ceb214210b97112` | **écarté** (< 300 car.) |`
- **T1** `| `Choquette c. Chagnon.PDF` ×2 | 6 | 7 575 | `8568cf8d6899ec09` | 1 retenu |`
- **T1** `| `Assurance pour stagiaires[-B2344-11403].PDF` ×2 | 1 | 2 021 | `3bf071e129bf357d` | 1 retenu |`
- **T1** `contamination à 8 Ko (`verifie_contamination.py --taille-troncon 8192`).`
- **T1** `"split": "hash salé du chemin : 5% val, 5% test",`
- **T1** `"split": f"hash salé du chemin : {args.val:.0%} val, {args.test:.0%} test",`
- **T1** `fichiers (tronçon de 8 Ko écrit par `corpus_wikipedia.py`) est hachée ; un`
- **T1** `(`corpus_wikipedia_texte.py`), l'unité est la **fenêtre** de 8 Ko coupée au`
- **T1** `0 = lignes ; 8192 = fenêtres de 8 Ko (texte intégral)`
- **T1** `1. **les doublons de tronçons entre splits** : chaque ligne des fichiers (tronçon de 8 Ko écrit`
- **T1** `(`corpus_wikipedia_texte.py`), l'unité est la **fenêtre** de 8 Ko coupée au mot`
- **T1** `ce dernier, l'unité de comparaison est la **fenêtre** de 8 Ko coupée au mot, pas la ligne —`
- **T1** `sinon les titres de sections répétés (« Biographie », etc.) font un faux taux de 5 %.`
- **T1** `help="0 = lignes ; 8192 = fenêtres de 8 Ko (texte intégral)")`
- **T1** `--- suffixe train: 5 fenetres 8 Ko, tailles [8176, 8187, 8188, 8185, 1248]`
- **T1** `--- suffixe val: 3 fenetres 8 Ko, tailles [8184, 8189, 3308]`
- **T1** `--- suffixe test: 1 fenetres 8 Ko, tailles [2184]`
- **T1** `=== resultat 8 Ko`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr]   File "<stdin>", line 22     t=sum(1 for p in pos if split_find:= ((propre/f'{s}.txt').read_bytes().find(b[p:p+500]) if p+500<=len(b) else -1))!=-1                                       ^^ S

