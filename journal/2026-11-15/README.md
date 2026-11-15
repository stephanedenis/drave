# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**35 commits** · **1 session(s)** · **7 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 5 | [distribue.md](distribue.md) |
| docs | 9 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 14 | [mesures.md](mesures.md) |
| modele | 3 | [modele.md](modele.md) |
| outils | 1 | [outils.md](outils.md) |
| portes | 2 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 356.4 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

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
| 04:03 | `2067a6f0` | B3 — LE CORPUS D'OR CIC V2 : 42/42 TYPES DE BRUJIN BIEN FORMÉS, 42/42 SHA256 PAR DEUX IMPLÉMENTATIONS, 36/36 PREUVES ET 42/42 TYPES ALTÉRÉS REJETÉS |
| 04:26 | `f1c6b506` | PHASE 3 (C PUIS B) — N2 (--rope --canal-dir), S (page / et 11 VERDICTS), R (GOLD RÉEL 452), PANINI (PROTOCOLE À DATE CONTRÔLÉE, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX, CIC 42/42) ; 6 FICHES, SEPT. 9 DU PLAN |
| 04:30 | `c24253ee` | DOC PRODUIT — LA PASSE D'HONNÊTETÉ : LES TROIS BASES (612, 602, RÉEL 452), L'ATTACHEMENT 238/239, LE TAGGER 95,75, LES CHIFFRES DATÉS ANNOTÉS |
| 04:33 | `ee04ea91` | BILAN DE LA NUIT — LE TAGGER (95,75), LA BASE HONNÊTE (452), LA PHASE C/B (N2, S, R, PANINI) ET LES NÉGATIFS DITS |
| 04:46 | `d23780d7` | D1 — LES EXEMPLES DU TAGGER ET DE LA BASE RÉELLE : 3 BLOCS --tagger (441 TOKENS, 3,7 S), 2 BLOCS --reel (452 PHRASES, POS 88,91, F1 79,06), 5/5 REJOUÉS, MUTATION 4/5 |
| 04:48 | `e42bac4f` | JOURNAL — 2026-11-15 : D1, LES EXEMPLES --tagger (441 TOKENS, 3,7 S) ET --reel (452 PHRASES) SONT DANS LA DOC ; 5/5 REJOUÉS, MUTATION 4/5 |
| 06:08 | `5b2d07fc` | D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270) |
| 06:20 | `4d6cffc4` | PHASE 4 — D1-D3 (LES EXEMPLES DU TAGGER, LA RESTITUTION v2, LA FAQ 10/10) ; L'INDEX, LA FICHE C3 ORPHELINE (GOLD RÉEL 50) ET LE PLAN COMMITTÉS |
| 06:23 | `503da67e` | BILAN DE LA SEMAINE — LE PRODUIT (F1 0,7902, 238/239, TAGGER 95,75), PANINI BORNÉ (DEUX NÉGATIFS), LA COORDINATION, LE HARNAIS (38 LANCEMENTS) ; LES 5 DÉCISIONS EXÉCUTÉES |
| 06:31 | `7d4e3bc5` | E1 — LA FAQ AU SOMMAIRE ET SES LIENS : 9/9 ANCRES, 5/5 LIENS, 0 MORT ; LA LIGNE FAQ DANS docs/README, LES RÉPONSES INCHANGÉES |
| 07:04 | `840e613e` | TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES |
| 07:10 | `7ee92dd9` | JOURNAL — 2026-11-15 : E2, LES CAS D'ERREUR DU TAGGER (REFUS D'AUTHENTIFICATION → CODE 4, RÉSEAU ET RÉPONSE NON CONFORME → REPLI 0 ; 18/18) |
| 07:27 | `cd4d1060` | FINITION — E1-E2 (LA FAQ AU SOMMAIRE, LES CAS D'ERREUR DU TAGGER) ; LE PLAN ET LE JOURNAL À JOUR |
| 07:30 | `cf2d1fb1` | ÉTAT — T0 DANS LE BUDGET |
| 07:32 | `2b7e520b` | ÉTAT — T0 VERT |
| 07:35 | `49011807` | ÉTAT — T0 VERT (LA LIGNE FAIT NETTOYÉE, COQUILLE CORRIGÉE) |
| 07:47 | `8cb0a926` | PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE CONTRÔLÉE, RESTITUTION V3, TAGGER PAR DÉFAUT ? |
| 08:08 | `6b2208ee` | PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE, RESTITUTION v3, LE TAGGER PAR DÉFAUT ? ; LA FILE DU CHANTIER À 41 TÂCHES |
| 09:18 | `4dbeff45` | SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S |
| 09:24 | `1683c2b4` | W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3 |
| 09:41 | `3439cb0c` | ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte |
| 10:47 | `be3f41ad` | SEMAINE 2 — W3 : LA MATRICE DU TAGGER (DÉFAUT HORS LIGNE CODE 0, CLÉ INVALIDE 4, RÉSEAU COUPÉ 0 APRÈS 3 ESSAIS, 1 000 PHRASES = 143 870 TOKENS) ; 4 TESTS DE PLUS |
| 10:59 | `93e046f7` | SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE |
| 12:08 | `9960b37f` | SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE GOLD v2 NE GAGNE QU'UN CADRE (20/46, F1 0,5406, LIEU 0,60) ; --roles-v3 OPT-IN |
| 12:20 | `049343d3` | SEMAINE 2 — W6 : LA CLÔTURE (5 VAGUES, 3 POSITIVES, 1 BLOQUÉE, 1 MIXTE) ; 85 PORTES LUES (81/4), CIBLAGE 9/9 ; TAG ANNOTÉ semaine-2-2026-11-20 SUR 73edb3dd |
| 12:35 | `2b5bd1cd` | JOURNAL — RÉGÉNÉRÉ APRÈS LA CLÔTURE DE LA SEMAINE 2 (W1-W6) ; LE TAG semaine-2-2026-11-20 REPOSÉ SUR LE COMMIT W5 |

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

### W2 — le tagger sur 402/H50 : il gagne sur les deux, le fermé du 402 paie

Le split de W1 (**402 / H50**) reçoit sa mesure : le tagger POS de l'API gagne **+4,45 pts** sur les
**402** (0,9198 → 0,9643) et **+17,65** sur **H50** (0,6842 → 0,8607) ; le F1 et l'attachement du
402 sont **inchangés**. La passe **API** paie **447 requêtes** et **65 029 tokens réseau** pour 452
phrases (**0,982 s/phrase**) ; le **cache chaud après API** rejoue **0 réseau / 0 token** et redonne
exactement les mêmes scores. La règle « une règle qui ne gagne que sur H50 est rejetée » **ne rejette
pas** le tagger : il gagne sur le 402, pas seulement sur H50. La **réserve** est nommée : sur 402, le
fermé perd **−1,55 pt** (PREP −8,43, CONJ −10,15) et le gain vient de l'ouvert (VERB +19,14, ADJ
+19,40) ; H50, lui, gagne **aussi** le fermé. La suite (W3) doit décider du défaut et, si possible,
tester l'hybride fermé/ouvert.
[`fiche`](../../reports/rapport-tagger-h50.md) · [`JSON`](../../reports/rapport-tagger-h50.json).

### W5 — la restitution v3 : les cinq rôles se séparent, le cadre ne suit pas

`_role_gp` passe au contexte et sépare **lieu / temps / destinataire / possession / complément**
(**24/24** cas). Le **gold S** monte à **144/144** (cinq rôles **18/18**) ; le **gold v2** ne gagne
qu'un cadre (**20/46**, F1 **0,5406**, `lieu` F1 **0,60**). Le découpage sépare **+4 rôles** et
**+1 appariement**. Le contrôle négatif permute les rôles : cinq rôles **0/18**, tous les rôles
**0,4028**, rôle constant **0,0208**. `--roles-v3` est opt-in ; `--roles` reste la v2.
[`fiche`](../../reports/rapport-restitution-v3.md) · [`JSON`](../../reports/pensee-restitution-v3.json).

### W6 — la clôture : cinq vagues, le tag `semaine-2-2026-11-20`, 85 portes lues

La semaine 2 est close : **W1** gold 452, **W2** tagger 402/H50, **W3** défaut hors ligne,
**W4** Panini bloqué (27/60, calibration 42/44, aucune p-value), **W5** restitution v3
(séparation 18/18, produit 20/46). Le rapport [semaine 2](../../reports/rapport-semaine-2.md) +
[JSON](../../reports/rapport-semaine-2.json) relient les cinq fiches ; le tag annoté
`semaine-2-2026-11-20` est posé sur le dernier commit de code vert `73edb3dd` (W5).
**Aucune passe complète relancée** : le relevé lit `work/portes-1115-09h53` (**85** portes,
**81** vertes, **4** rouges nommées : `indice`, `melange`, `sessions` réparée, `prechargement`
environnementale) et un ciblage **9/9** après heartbeat.
<!-- /notes -->
