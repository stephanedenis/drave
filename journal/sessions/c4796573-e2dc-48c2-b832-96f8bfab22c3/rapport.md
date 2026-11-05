# Session c4796573 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `c4796573-e2dc-48c2-b832-96f8bfab22c3` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 13:16 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 105 |
| Appels d'outils | 129 |
| Fichiers touchés | 6 |
| Commandes | 83 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : écrire le **contrat d'interface** entre le bloc linguistique (`tools/bloc_linguistique.py`, territoire L) et le générateur de structures S (`tools/structures/generateur.py`, territoire S), en particulier pour les **subordonnées REL/SUB**, et mesurer l'écart actuel.  Contexte mesuré le 2026 … [2024 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : écrire le  … [2304 caractères tronqués]

*129 appels d'outils.* Actions notables :

- bash — Vérifier branche et état du dépôt
- bash — Compter lignes et lister reports
- read
- grep
- bash — Chercher le dispositif de mesure
- bash — Lister fichiers parlant d'attachement
- bash — Chercher fichier gold
- bash — Lire fiche échecs attachement
- bash — Chercher la qualification 48 REL/33 SUB
- bash — Lister fiches attachement/cible
- bash — Lire fiche spans
- bash — Chercher chiffres dans mesures du jour
- bash — Lister tests linguistiques
- bash — Repérer le gold dans evaluateur
- … et 106 autres

**Synthèse produite :**

⏵ Envoi du résultat au parent

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/mesure_contrat_s.py` | 1 | 0 |
| `/tmp/mesure_detail.py` | 1 | 0 |
| `/tmp/mesure_detail2.py` | 1 | 0 |
| `/tmp/mesure_detail3.py` | 1 | 0 |
| `/tmp/synthese_contrat.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md` | 1 | 29 |

### Commandes exécutées (échantillon)

- **T1** Vérifier branche et état du dépôt
- **T1** Compter lignes et lister reports
- **T1** Chercher le dispositif de mesure
- **T1** Lister fichiers parlant d'attachement
- **T1** Chercher fichier gold
- **T1** Lire fiche échecs attachement
- **T1** Chercher la qualification 48 REL/33 SUB
- **T1** Lister fiches attachement/cible
- **T1** Lire fiche spans
- **T1** Chercher chiffres dans mesures du jour
- **T1** Lister tests linguistiques
- **T1** Repérer le gold dans evaluateur
- **T1** Compter cibles par type dans le gold
- **T1** Historique des fichiers S et bloc
- **T1** Vérifier commit courant
- **T1** Exécuter la mesure sur le gold
- **T1** Mesurer convention gold et cibles S par tête
- **T1** Exécuter mesure détaillée 2
- **T1** Corriger puis relancer la mesure 2
- **T1** Lire exemples REL plus large et SUB
- **T1** Exécuter mesure détaillée 3
- **T1** Chercher le cas antécédent dans un GP
- **T1** Position de la cible gold vs segment
- **T1** Chercher antécédents dans un GP
- **T1** Calculer le contrôle négatif aléatoire
- **T1** Inspecter la sortie réelle de S
- **T1** Inspecter tous les champs Segment
- **T1** Répartition langue et canaux cibles
- **T1** Chercher docs sur le générateur S
- **T1** Trouver tous les consommateurs des cibles S
- **T1** Lire le contrat du bloc sur S
- **T1** Lire le doc moteur sur les cibles
- **T1** Lire le format des JSON existants
- **T1** Baselines, permutations, invariants, rôles
- **T1** Relancer baselines et permutation
- **T1** Invariants de partition et accord des rôles
- **T1** Répartition par source et cas français absents
- **T1** Position de la cible pour les SUB au span exact
- **T1** Lancer l'évaluateur gold du dépôt
- **T1** Lire la convention documentée
- … et 43 autres

## 4. Mesures et résultats marquants

- **T1** `| **span faux** (aucun segment prédit au même span) | **94** | 74,0 % |`
- **T1** `| **cible hors des candidats** (span bon) | **33** → **32** après le correctif | 26,0 % |`
- **T1** `| **tout** | **127** → **126** après | 100 % |`
- **T1** `255-| **T83** | où est le seuil sur 20 graines ? | 20 % à 0,35, 100 % à 0,41 | le seuil est ~0,41, gradué |`
- **T1** `256-| **T84** | où est le bord fin ? | 73 % à 0,38, 100 % à 0,41 (400 essais) | le seuil robuste est 0,41 |`
- **T1** `326:| **T154** | combien de cibles sont annotées ? | **239/1863** (12,8 %) | l'attachement est à peine annoté |`
- **T1** `333:| **T161** | la cible par proximité paie-t-elle ? | exact **0,0042 → 0,0544** (×13), top1 0,3975 | 226/239 restent faux |`
- **T1** `362-| **4 ter** | `tools/pensee/` (`taquin.py`, `banc.py`) | taquin 3×3, AUC/regret, aléatoire | T7 |`
- **T1** `367-**Le corpus v0** : un jeu de petits graphes (morpion, taquin 3×3, un CSP jouet) et un jeu de`
- **T1** `# B13 — la cible par proximité : l'exact passe de 0,0042 à 0,0544 (×13)`
- **T1** `> **exact 1 (0,0042)** à **13 (0,0544)** — **×13**. La tête fait **94/145 (0,6483)** contre 81`
- **T1** `| **exact** | **1 (0,0042)** | **13 (0,0544)** | **+12 (×13)** |`
- **T1** `- **La proximité est un signal réel** : +13 top1 et **×13 en exact** — le verbe le plus proche est`
- **T1** `15:> REL/SUB (43,4 %). L'attachement REL/SUB passe de **54/62** (état initial) à **60/62** (état`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : invariant texte S 0 / 1101 invariant texte gold 0 / 1863 [stderr] Traceback (most recent call last):   File "<stdin>", line 43, in <module>   File "<stdin>", line 43, in <lambda> TypeError: 'Segment' 
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 23, in <module>   File "<stdin>", line 9, in cat TypeError: 'Etiquette' object is not subscriptable [exit code: 1]
- **T1** : [stderr] bash: -c: line 1: unexpected EOF while looking for matching ``' [exit code: 2]

