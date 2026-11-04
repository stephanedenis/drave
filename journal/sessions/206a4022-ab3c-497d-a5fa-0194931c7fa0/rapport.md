# Session 206a4022 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-04/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `206a4022-ab3c-497d-a5fa-0194931c7fa0` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-04 15:56 |
| Durée | 0.0 h |
| Tours | 1 |
| Messages | 13 |
| Appels d'outils | 15 |
| Fichiers touchés | 0 |
| Commandes | 15 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt Drave, racine /home/stephane/Data13TB/stephane/GitHub/Qtrinet (lis AGENTS.md pour le contexte général, mais ton périmètre est strictement celui ci-dessous).  CONTEXTE. La session `aeafe951` a clos la limite de D : les 8 scans `.PDF` du fonds CEGEP (58 p) ont été OCRisés (rapport `reports/rapport-ocr-pdf-restants.md`, manifeste `reports/ocr-pdf-restants.json`, texte brut … [4629 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt Drave, racine /home/stephane/Data13TB/stephane/GitHub/Qtrinet (lis AGENTS.md pour le context … [4909 caractères tronqués]

*15 appels d'outils.* Actions notables :

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
- … et 1 autres

**Synthèse produite :**

⏵ Recherche des traces de l'append et lancement de la contamination réelle

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

