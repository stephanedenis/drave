# 2026-11-16

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-16/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**7 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 2 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 3 | [mesures.md](mesures.md) |
| moteur | 1 | [moteur.md](moteur.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 370.1 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO |
| 00:24 | `75a56c05` | U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE) |
| 00:28 | `04894aea` | U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4) |
| 00:45 | `c77ed4b6` | U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE |
| 00:48 | `1d4eb49e` | JOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4 |
| 02:10 | `2e617034` | EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF) |
| 02:47 | `1a5a6548` | V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE |

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
<!-- /notes -->
