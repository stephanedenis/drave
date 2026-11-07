# Session 538288b3 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `538288b3-117b-4daf-8d16-0cd8d6b0090d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 21:13 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 19 |
| Appels d'outils | 31 |
| Fichiers touchés | 0 |
| Commandes | 13 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier A** (le moteur) — lecture seule, aucun code.  Contexte : `docs/pilotage/roadmap.md` (A : A2.6 experts/tête, A6.2, A8.3a, A17, A23, A24…), `docs/pilotage/en-cours.md`, `docs/pilotage/backlog/index.md` + `dependances.md`, les fiches `reports/rapport-a*.md`. A23 a noté : « A2.6 n'est pas li … [1370 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier A** (le  … [1650 caractères tronqués]

*31 appels d'outils.* Actions notables :

- bash — Show repo root, branch, recent commits
- glob
- bash — Count lines of key documents
- grep
- read
- bash — List report files matching A-numbered variants
- bash — Check for existing target files and git status
- bash — Read prior sibling session digest
- bash — Inspect prior sibling session outcome
- bash — Check if target files ever existed in git
- bash — Check artifacts for A17/A23/A24
- bash — Extract A2.6 mentions with context from A23 report
- bash — List verification tools and placement tests
- bash — Run backlog verification read-only
- … et 2 autres

**Synthèse produite :**

⏵ Lecture des fiches A2.6 et A8.3a
Je lis maintenant les fiches et artefacts de A2.6, A8.3a et A6.2.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Show repo root, branch, recent commits
- **T1** Count lines of key documents
- **T1** List report files matching A-numbered variants
- **T1** Check for existing target files and git status
- **T1** Read prior sibling session digest
- **T1** Inspect prior sibling session outcome
- **T1** Check if target files ever existed in git
- **T1** Check artifacts for A17/A23/A24
- **T1** Extract A2.6 mentions with context from A23 report
- **T1** List verification tools and placement tests
- **T1** Run backlog verification read-only
- **T1** Inspect placement tests
- **T1** Read A2.6 and A8.3a JSON artifacts

## 4. Mesures et résultats marquants

- **T1** `182-        // Un KV de 1 M de jetons sur un 0,5 B : ~100 Mo lus par jeton.`
- **T1** `202-        // Un petit KV (100 Mo) va en VRAM.`
- **T1** `210-        // Le KV tardif : l'int8 (+0,03 %) passe un budget de 1 % ; l'int4 (+2,7 %) non.`
- **T1** `226-        // +10 % de PPL : elle « tient », mais la place n'est pas la qualité.`
- **T1** `229-        // Et l'int4 global (+364 %) ne passe aucun budget raisonnable.`
- **T1** `236-        // 24 couches : l'int8 passe sur les 12-23 (+0,03 %), pas sur les 0-11 (+2,28 %).`
- **T1** `241-        // Un budget de 3 % laisse passer les deux.`
- **T1** `"preuve": "rapport-placement-kv-8k.md, ×1,93 / ×5,8"`
- **T1** `"preuve": "TETE_4BIT +10 % PPL ; choisir_avec_perte la refuse à 5 %"`
- **T1** `"controle": "choisir_avec_perte refuse la tête 4 bits à 5 % (test) ; sans MoE local, les experts ne sont pas mesurables",`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : a26-bilan.json a26-lot-disque.json a83a-coupe.json a83a-flux.json a83a-pont.json a83b-decision.json a83b-lot.json a83b-regimes.json a83c-ctx.json a83c-lot.json a83-defaut.json a83d-lot-threads.json ra

