# Session session- — API JSON candidats et rôles normalisés

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-a03a9d9e-ca57-4212-9a3d-b2ae8c71c43f` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 21:50 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 157 |
| Appels d'outils | 184 |
| Fichiers touchés | 2 |
| Commandes | 181 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche T2 (exploitable, 2/5) : **l'API du JSON** — (1) les `candidats` de l'attachement deviennent des **objets** `{span, cible, source}` au lieu des chaînes d'affichage (le schéma v2 gagne un champ, v1 toujours lue ; la sortie lisible garde les chaînes) ; (2) les `role` sont **normalisés** (un vocabulaire fermé : predicat, agent, objet, lieu, temps, qualite, possesseur, destinataire — sans accents … [285 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche T2 (exploitable, 2/5) : **l'API du JSON** — (1) les `candidats` de l'attachement deviennent des **objets** `{span, … [565 caractères tronqués]

*184 appels d'outils.* Actions notables :

- bash — Inspect repository root and recent history
- bash — Find attachment-related Python files
- bash — Locate T2 in the work plan
- bash — Find schema v2 / candidates references
- bash — Search contract JSON and T2 mentions
- bash — Read attachment report head
- bash — Search for exploitable task plan
- bash — Find candidates implementation
- bash — Find attachment code
- bash — Find role handling in code
- bash — Read restitution v2 beginning
- bash — Find v2 schema docs
- bash — Read bloc_linguistique header
- bash — Find schema names
- … et 170 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/roles_vocabulaire.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_contrat_json.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Inspect repository root and recent history
- **T1** Find attachment-related Python files
- **T1** Locate T2 in the work plan
- **T1** Find schema v2 / candidates references
- **T1** Search contract JSON and T2 mentions
- **T1** Read attachment report head
- **T1** Search for exploitable task plan
- **T1** Find candidates implementation
- **T1** Find attachment code
- **T1** Find role handling in code
- **T1** Read restitution v2 beginning
- **T1** Find v2 schema docs
- **T1** Read bloc_linguistique header
- **T1** Find schema names
- **T1** Read product schemas
- **T1** Read schema verifier
- **T1** Find attachment blocks and candidates
- **T1** Read syntagm generation and attachment
- **T1** Read verb candidates and vue
- **T1** Inventory role assignments
- **T1** Inspect role module
- **T1** Read roles_gp module
- **T1** Read role production context
- **T1** Search task batch
- **T1** Find T1-T5 plan
- **T1** Read T1 exploitability report
- **T1** List product doc headings
- **T1** Find product doc role/candidate sections
- **T1** Read product doc §3.1-3.3bis
- **T1** Read product doc §4 and §7 manques
- **T1** Read product tests
- **T1** Find rendering in CLI
- **T1** Read restitution forms
- **T1** Find candidates in examples
- **T1** Read examples head
- **T1** Read example candidates JSON
- **T1** Find candidate assertions in tests
- **T1** Find role normalization usage
- **T1** Inspect generator roles
- **T1** Inspect restitution gold roles
- … et 141 autres

## 4. Mesures et résultats marquants

- **T1** `journal/sessions/d300542e-6e9d-47ac-875b-b44a192eec35/rapport.md:130:- **T1** `T2 si base nom -> rang0                n=145 exact=139/145 (base 137) top1=140/145 (base 140) fix=2 reg=0 net=+2``
- **T1** `- **La couverture est la première limite** : 145 cibles sur 239 sont annotées (60,7 %) — les`
- **T1** `docs/theorie/glossaire/06-repartition-materiel-et-energie.md:187:cartes graphiques (2 × 16 Go, 30,2 Go exploitables) ; *RSS* (resident set size) :`
- **T1** `docs/theorie/glossaire/entrees/ram-vram-rss.md:4:> **Fiche glossaire — RAM · VRAM · RSS.** *RAM* : mémoire de l'hôte (125 Go ici) ; *VRAM* : mémoire des cartes graphiques (2 × 16 Go, 30,2 Go exploitab`
- **T1** `sprints/25-le-disque-dur-deguise-en-defaut-moteur.md:71:fait exploitable (×1,81 par le placement du fichier). Aucune lecture de code`
- **T1** `reports/rapport-optimisations.md:16:**0,484 ms → 0,011 ms** (×44). C'est ce qui rend le débit *variable* exploitable :`
- **T1** `docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 lan`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `71:| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |`
- **T1** `83:1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat`
- **T1** `90:attachement 99,46 %). Les chiffres de la fiche v12 (0,6511/0,6482, 235/236) sont **datés** : ils`
- **T1** `151:  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture`
- **T1** `186:POS (94,51 % contre 81,59 %) et en syntagmes (F1 86,56 % contre 74,75 %) ; l'attachement est`
- **T1** `386:**88,91 %**, F1 **79,06 %**, attachement **99,46 %**. Sans lui, `evaluer` publie la ligne`
- **T1** `477:(**+8,57 pts**), syntagmes et attachement **inchangés**. Sur le **gold 612** : **86,25 % →`
- **T1** `802:**1,67 %** ; l'audit v10 ajoute un **candidat aléatoire** dans les listes (**42,14 %** de top-1)`
- **T1** `**Lecture.** Le porteur `REL [22:42]` est le **rang 2** d'un groupe de **3** segments ; ses deux`
- **T1** `alternatives sont au rang 1 (la REL longue `[22:54]`, qui le **contient** : `inclus`) et au rang 3`
- **T1** `chevauchement (v2) ; `rang: 1` est la vue préférée, pas une suppression.`
- **T1** `tools/tests/linguistique/classement_cible.py:580:        juste_rang0 = int(s["candidats"][0]["texte"] == s["cible"])`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/r`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.`
- **T1** `docs/pilotage/roadmap.md:288:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"`
- **T1** `**1,67 %** ; l'audit v10 ajoute un **candidat aléatoire** dans les listes (**42,14 %** de top-1)`
- **T1** `et une **permutation des cibles** (**0,908 %**). La mesure est **in-sample** : les règles ont`
- **T1** `base réelle 452, **183/184 (99,46 %)**. Détail : [`rapport-g017.md`](../../reports/rapport-g017.md).`
- **T1** `| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |`
- **T1** `1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat`
- **T1** `aléatoire** dans les listes donne **42,14 %** de top-1 — et la **permutation des cibles**`
- **T1** `**1,997/220 = 0,908 %** ; les deux donnent p = 0. Un chiffre sans sa contre-épreuve n'est pas un`
- **T1** `attachement 99,46 %). Les chiffres de la fiche v12 (0,6511/0,6482, 235/236) sont **datés** : ils`
- **T1** `| **1 bis** | A5 contrat S, A6 coût/cache | interface S, O(n²) | ✅ intégrée (cache ×139) |`
- **T1** `| 1 (P0) | frontières, partition, POS R4 | 32/40 → 0 frontières fausses ; `meta.alternative` ; **POS 85,00 %** |`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `| 4 | **Que change `--tagger` ?** | POS seul : **95,75 %** contre **86,25 %** (612) ; **95,00 %** contre **88,91 %** (réel 452) ; ponctuation **25/25** | `q4_tagger` |`
- **T1** `| 6 | **L'attachement ?** | **238/239** cibles (**0,9958**) ; **1,0000** sur les spans prédits ; top-k **0,9874** ; hasard **1,67 %** ; audit **42,14 %** / **0,908 %** | `q6_attachement` |`
- **T1** `[still running after 60000ms; moved to background job bash-181]`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 53, in <module> AssertionError [exit code: 1]
- **T1** : OK overview OK row_att MISS 3.2 [exit code: 1]

## 6. Commits

- T1-T2 — LE PRODUIT EXPLOITABLE : L'EMPAQUETAGE (8 TESTS) ET L'API DU JSON (2 139 CANDIDATS OBJETS, 0 SPAN FAUX ; 21 RÔLES → 8, 0 HORS TABLE ; 711 PRÉDICATS, 0 A

