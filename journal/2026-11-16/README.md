# 2026-11-16

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-16/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**18 commits** · **1 session(s)** · **7 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 1 | [distribue.md](distribue.md) |
| docs | 4 | [docs.md](docs.md) |
| memoire | 2 | [memoire.md](memoire.md) |
| mesures | 4 | [mesures.md](mesures.md) |
| modele | 5 | [modele.md](modele.md) |
| moteur | 1 | [moteur.md](moteur.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 378.4 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO |
| 00:24 | `75a56c05` | U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE) |
| 00:28 | `04894aea` | U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4) |
| 00:45 | `c77ed4b6` | U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE |
| 00:48 | `1d4eb49e` | JOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4 |
| 02:10 | `2e617034` | EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF) |
| 02:47 | `ae3c24f2` | V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE |
| 03:12 | `3c10e3ee` | V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON |
| 04:08 | `19992f2f` | Z1 — L'INTÉGRATION CONTINUE : MATRICE 3.10/3.13, 10/10 ÉTAPES VERTES (ARCHIVE SANS SOUS-MODULE, COPIE DE SECOURS S) ; PORTE 183/183 ; TEST CASSÉ → 1, JOB ARRÊTÉ ; act ABSENT, YAML PARSÉ |
| 06:24 | `25a727be` | PASSE 1611 — 84 PORTES, 81 VERTES, 3 ROUGES NOMMÉES (INDICE, MELANGE, SESSIONS DU HUB) ; TABLEAUX TRANSIENT (VERTE EN ISOLATION) |
| 06:38 | `d0364c0a` | EXPLOITABLE — Z3 : LE BILAN FINAL (LES 3 VOIES D'INSTALLATION, LE DÉMARRAGE EN 3 COMMANDES, LE JSON V2, LA PERFORMANCE, LES NÉGATIFS NOMMÉS) |
| 06:42 | `615f84be` | ÉTAT — T0 VERT APRÈS LA CLÔTURE (LA LIGNE N2 RACCOURCIE) |
| 07:57 | `6f5e0f0c` | SOUS-MODULES — LE DOCWATCH REPINÉ SUR 95e94c4 (LE PIN d256888 N'EXISTE PAS SUR LE REMOTE) ; LE CLONE --recurse-submodules PASSE |
| 08:02 | `d1715692` | DOCS — LE CLONE RÉPARÉ ET DOCUMENTÉ : --recurse-submodules, protocol.file.allow=always, LES SOUS-MODULES LOCAUX ; LE PIN DOCWATCH REPINÉ, LE COMMIT 648adce DE structures POUSSÉ |
| 10:44 | `cf3f9bc7` | NATIF — LE BANC DE GÉNÉRATION (20 PROMPTS, 3 RÉGLAGES, LE CONTRÔLE ALÉATOIRE) : LE MODÈLE A APPRIS LES MOTS (0,87 CONTRE 0,34) PAS LA PHRASE (RÉPÉTITION 15 EN GREEDY) |
| 10:47 | `78cdb7f0` | DOCS — LE README DES FICHES DANS LE BUDGET (T1) ; ÉTAT HORODATÉ |
| 10:53 | `b2dfc1cc` | NATIF — LE BANC DE GRAMMATICALITÉ : NOTRE ANALYSEUR JUGE LE MODÈLE (GV 6,9 CONTRE 2,3 AU HASARD, MAIS LE CIMENT EST BAS : DES MOTS SANS LA GLU) |
| 11:00 | `90fb737a` | NATIF — LA SYNTHÈSE HONNÊTE : L'ÉCHELLE, LA DONNÉE, L'ALIGNEMENT, LE RUNTIME (LE TOKENIZER MESURÉ N'EST PAS LE LEVIER) ; LES 4 PALIERS CHIFFRÉS |

## Le récit de la journée (écrit à la main)

<!-- notes -->
### U2 — la roue autonome, et la roue sans gold qui refuse de mesurer

`python3 -m pip wheel . --no-deps --no-build-isolation -w dist` a rendu
**`drave-0.1.0-py3-none-any.whl`** (1 727 201 o, 422 entrées, sha256 `d980c470…a99dbce`).
Installée dans un venv propre **depuis le fichier**, elle rend depuis `/tmp` `drave 0.1.0`,
`drave analyser "Le chat dort."` (`rôle=agent`) et `drave evaluer --json` (gold 612, POS 0,8625,
F1 0,7902, exact 0,9958). Les JSON sont **identiques au bit près** à ceux du dépôt.

La décision : les cinq **gold** sont des `package-data`, avec `tools.tests.linguistique`,
`tools.structures` et `tools.llm`. Une roue **amputée** des gold installe et analyse encore,
mais `drave evaluer` sort en **4**, `stdout` vide, et nomme les fichiers manquants ; `--gold`
sélectionne le gelé et ne remplace pas un gold absent. C'est le contrôle négatif qui manquait
à T1, où le wheel échouait avant même d'analyser. Le point S (sans `generateur`, `rôle=objet`
au lieu d'`agent`) a été trouvé et corrigé par l'embarquement de `tools.structures`.

[Fiche](../../reports/rapport-roue.md) · [JSON](../../reports/roue.json) · doc § 8.10.

### V2 — les exemples de la doc rejoués, et le contrôle qui les tient

Les **cinq blocs** de [`exemples.md`](../../docs/produit/exemples.md) ont été rejoués avec le
code courant : **3 corrigés**, tous par la **normalisation des rôles** (`qualité` → `qualite`,
`prédicat` → `predicat`, `groupe nominal` → `objet`), **2 identiques** hors enrichissement. Les
**candidats objets** sont publiés et vérifiés — **18 objets, 0 span faux** — et la **durée**
(`--duree`, `cout.duree_s`) est documentée sans être confondue avec une performance.

Le contrôle n'est plus une relecture : `tools/verifie_exemples.py` lit les deux documents,
exécute chaque commande et compare le **JSON parsé**, le texte exact, le code du refus et les
syntagmes du tagger à l'heuristique. **27/27 cas conformes, 0 écart** ; une mutation
`qualite` → `qualité` est détectée. Les **3 commandes** du démarrage sont **3/3** dans une copie
sans `tools/structures` (JSON **5 899 octets**).

[Fiche](../../reports/rapport-exemples-v2.md) · [JSON](../../reports/rapport-exemples-v2.json).

### V3 — la clôture de la nuit exploitable, et le tag sur le dernier commit vert

Les **neuf tâches** du lot exploitable (**T1–T6**, **U1–U3**) et les deux vérifications
(**V1–V2**) sont liées dans un second bilan : [rapport-bilan-exploitable-2.md](../../reports/rapport-bilan-exploitable-2.md)
+ [JSON](../../reports/rapport-bilan-exploitable-2.json). Le chiffre de la nuit : le produit
s'installe, **10 000 mots** passent en **0,82 s** (α **1,076**, sorties identiques), la roue est
autonome (**1 727 201 o**, sans gold → **4**), les profils font **20/20** (ambigu **`und`**),
`--strict` fait **0,8625 / 0,8891** et les exemples **27/27**.

La passe `work/portes/roue-1116/` est **lue, pas relancée** : **86 portes, 82 vertes, 4 rouges**
— `indice` et `melange` structurelles, `produit` (V1 n'avait pas fini) et `sessions` (heartbeat
périmé) de circonstance. La vérification ciblée `work/portes/verif-cloture-1116/` rend
`sessions` **0** et `produit` **0** (`evaluer --strict` 5 tests, exemples **27/27**, autotest
**183/183**) : **84 vertes, 2 rouges structurelles**. Le tag annoté
**`exploitable-2026-11-16`** est posé sur **`ae3c24f2`** (V2), le dernier commit vert ; le
commit de clôture suit. **La prochaine mesure est J4 — l'or de rôles**.

### Z1 — l'intégration continue, la matrice et le test qui casse

Le workflow `.github/workflows/ci.yml` rejoue le produit sur **Python 3.10 et 3.13** :
`pip install -e .`, `test_produit.py`, `test_tagger_api.py`, `porte-produit.sh`,
`test_schema_produit.py`. Comme `act` n'est pas installé, `tools/verifier_ci.py` charge le YAML
avec PyYAML, exécute les cinq commandes en **fail-fast** et **casse** un test : la copie de
`test_produit.py` avec un `self.fail` sort en **1** et l'étape témoin n'est pas lancée.

Les deux jambes locales sont vertes : **10/10** étapes, porte **183/183**, **482,3 s** au total.
La mesure part d'une archive **sans sous-module** : le sous-module `tools/structures` a une URL
locale, donc le workflow restaure une **copie de secours** de `generateur.py` et du gold de
l'analyseur depuis `.github/ci/structures/` ; `tools/verifie_structures_secours.py` vérifie
qu'elle est identique au sous-module. Le CI a trouvé avant de tourner un vrai défaut : deux
doubles de `test_tagger_api.py` ne prenaient pas le mot-clé `gele` ajouté à `evaluer` ; le
correctif est dans le test, pas dans le produit. [Fiche](../../reports/rapport-ci.md) ·
[JSON](../../reports/rapport-ci.json) · [doc](../../docs/produit/ci.md).
<!-- /notes -->
