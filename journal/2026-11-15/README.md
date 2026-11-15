# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**9 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 2 | [distribue.md](distribue.md) |
| docs | 2 | [docs.md](docs.md) |
| mesures | 4 | [mesures.md](mesures.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 347.4 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |
| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |
| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |
| 02:00 | `5891ef8a` | ÉTAT — T0 TENU : LA LIGNE FAIT RACCOURCIE |
| 02:13 | `292c70b5` | C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09 |
| 02:27 | `f926b5bc` | C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PROFONDEUR, 41 VERDICTS À RE-JUGER ; PORT 8765 PRIS, PARE-FEU ACTIF ; LES 11 VERDICTS COMMITTÉS (389b99f) |
| 03:04 | `c37fed06` | B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE |
| 03:48 | `011b8b8e` | B2 — LES ATOMES NE PRÉDISENT PAS POS, SYNTAGMES NI ATTACHEMENT : SUR 28 ŒUVRES PROPRES, R² −0,092 / −0,160 / −0,092 (p 0,56 / 0,85 / 0,67) ; LE STYLE EST PRÉDIT (GRAPHÈMES +0,811, MOTS +0,657, NÉGATION +0,440, VERBES +0,429) MAIS ABSORBÉ PAR LA DATE (p_resid 0,76–1,0) |
| 03:51 | `01b6db6e` | JOURNAL — 2026-11-15 : B2, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX (NÉGATIF CONTRÔLÉ ; LE STYLE EST ABSORBÉ PAR LA DATE) |

## Le récit de la journée (écrit à la main)

<!-- notes -->
### B2 — les atomes ne prédisent pas les niveaux

La table J2.1 promettait un **porteur** pour chacun des 14 atomes ; B2 devait la mesurer. Le résultat est
un **négatif contrôlé**. Sur les **44 signatures** de Panini, **36 œuvres** ont assez de prose pour être
mesurées, **28** ont une fenêtre de signature propre et ≥ 1 000 jetons. Sur ces 28, les 14 atomes ne
prédisent pas **POS** (R²_CV **−0,092**, p=0,56), les **syntagmes** (**−0,160**, p=0,85) ni
l'**attachement** (**−0,092**, p=0,67). Le seul ρ nominal (POS **+0,176**, p=0,029) tombe à **Holm 0,088**
et ne survit pas à la date (**p_resid=1,0**).

Le dispositif n'est pas muet : il prédit l'**entropie des graphèmes** (**+0,811**), la **longueur des
mots** (**+0,657**), la **négation** (**+0,440**) et la **part de verbes** (**+0,429**). Mais la date
explique **0,16–0,54** de ces métriques et **aucune** ne survit au contrôle de date (**p_resid=0,76–1,0**).
Les atomes sont une signature **d'époque et de genre**, pas une entrée syntaxique.

Le signal brut des **36 mesurables** (POS **+0,102**, syntagmes **+0,060**) tombe à **+0,010 / +0,014**
sur 34, puis **−0,080 / −0,204** sur 26 : il est porté par les **sources courtes** et **deux signatures
non-propres**. Le protocole, les 2 000 permutations de colonnes et les 1 000 permutations de date sont dans
[`reports/rapport-atomes-prediction.md`](../../reports/rapport-atomes-prediction.md) et
[`reports/atomes-prediction.json`](../../reports/atomes-prediction.json). La suite : un gold anglais de
niveaux et une signature recalculée sur le texte nettoyé.

### B3 — le corpus CIC tient, mais le vérificateur voit plus loin

J12.2 avait le **42/42** ; B3 devait fermer les trous de contrôle. Trois ajouts, une seule fixture
inchangée. **Le type d'abord** : les 42 types de de Bruijn sont **clos** (aucun indice hors portée)
et **bien formés** (`[] ⊢ type : sort n`, 38 en `sort 0`, 4 en `sort 1`), les 42 preuves sont closes.
Un type ouvert ou mal typé est refusé avant de servir de contrat. **L'empreinte ensuite** : `sha256`
est réécrit depuis **FIPS 180-4**, sans `hashlib` ; il retrouve le sha256 du fichier, les **42**
couples `preuve || type` et les **24** termes de l'environnement, **0 écart** avec `hashlib`. **Les
contrôles négatifs** : les **36/36** preuves altérées sont rejetées, les **42/42** types altérés
aussi (**36** deviennent invalides, **6** restent bien formés mais la preuve ne passe plus), les
**1 020/1 020** mutations de `eq(2,2)` sont rejetées, et un corpus corrompu (preuve ou type) sort en
**1**. La porte `tools/porte-cic.sh` et **21 + 17 = 38** tests rejouent le tout :
[`reports/rapport-cic-v2.md`](../../reports/rapport-cic-v2.md) et
[`reports/cic-verificateur-v2.json`](../../reports/cic-verificateur-v2.json).
<!-- /notes -->
