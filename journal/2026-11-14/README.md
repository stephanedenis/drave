# 2026-11-14

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**13 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 3 | [docs.md](docs.md) |
| memoire | 2 | [memoire.md](memoire.md) |
| mesures | 6 | [mesures.md](mesures.md) |
| portes | 2 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 324.3 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:52 | `64d9dd23` | J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CONVENTION DU GOLD À TRANCHER |
| 01:06 | `b6e474dc` | J6.2 — s065 : LA REL SUIVIE D'UN GV PREND LE SUJET DU GV (238/238 LABELS, 238/239 CIBLES, F1 0,7902 INCHANGÉ, 0 SPAN, 0 POS) |
| 01:08 | `6ecc9763` | JOURNAL — 2026-11-14 : J6.2 AU RÉCIT (2 COMMITS, LE THÈME MESURES), s065 238/238 |
| 01:16 | `2d6f5bff` | PORTES — LA PASSE DU 14/11 : 84 PORTES, 81 VERTES, 3 ROUGES (INDICE, MELANGE, SESSIONS DU HUB) ; MANDAT E181CE02 RAFRAÎCHI |
| 01:19 | `e4288023` | J6.2 — PORTE PRODUIT VERTE (183/183) : FIXTURES D'ATTACHEMENT À 238/238, FICHE ET JSON À JOUR |
| 01:41 | `d31e8788` | J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE |
| 03:23 | `229098ec` | J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS) |
| 03:32 | `ecef7250` | J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT |
| 03:40 | `81fc9ecf` | JOURNAL — 2026-11-14 : J9.1 AU RÉCIT (19 FICHES « INSTANTANÉ HISTORIQUE ») |
| 03:53 | `03ecee41` | J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ |
| 04:16 | `a6808c5e` | CHANTIER — LE PLAN EST RELU À CHAQUE TOUR (LA BOUCLE VOYAIT UNE FILE VIDE APRÈS UN AJOUT DE TÂCHES) ; ÉTAT HORODATÉ |
| 04:28 | `84e393bb` | J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238 |
| 04:40 | `09e54143` | J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ |

## Le récit de la journée (écrit à la main)

<!-- notes -->
**J6.1 — g017 : la règle de l'adverbe final hors de la SUB est rejetée.** Le bloc inclut
`yesterday` dans la SUB de `g017` (span 9:38 au lieu de 9:28). La règle demandée corrige
`g017` et retire un faux positif de `g005`, mais casse `r264` (« qu'il vient demain ») et
`r288` (« that he comes tomorrow ») : F1 **0,7902 → 0,7901**, dev **+0,0011**, test
**−0,0028**, attachement **237/238 → 236/237**. Les deux cas favorables sont en **dev**, les
deux défavorables en **test**. Rejet ; la convention du gold (inclure ou exclure l'adverbe
final) doit être tranchée avant toute règle. Fiche [`reports/rapport-g017.md`](../../reports/rapport-g017.md),
JSON [`reports/pensee-g017.json`](../../reports/pensee-g017.json).

**J6.2 — s065 : la REL « qui commence » prend le sujet du GV qui la suit.** Le gold attend
`elle`, le bloc prédisait `nage` (le GV le plus proche). La règle **REL suivie d'un GV → le
sujet de ce GV** corrige la seule cible fausse : **F1 0,7902 inchangé**, **POS 0,8625
inchangée**, **attachement 237/238 → 238/238 labels** (238/239 cibles, **0,9958**),
**exactitude sur les spans 0,9958 → 1,0**. Le gain est en **dev** (161/162 → 162/162) ; le
test reste à 76/76 car il n'a aucun cas déclencheur. Une seule annotation change, `s065` :
REL 5:17, `nage` → `elle`. Règle intégrée avec un test ; porte du bloc verte, porte produit
verte (**183/183**, fixtures d'attachement mises à jour). Fiche
[`reports/rapport-s065.md`](../../reports/rapport-s065.md), JSON
[`reports/pensee-s065.json`](../../reports/pensee-s065.json).
**J7.1 — le retrieval par famille : l'écriture d'abord, la sœur ensuite.** Sur les **532 textes
UDHR** de Panini (même source XML, article 1, 1948 ; **445 langues distinctes** après déduplication,
**521/532** étiquetées Glottolog), le top-1 de voisinage est de la même famille **66,1 %** (hasard
10,3 %) et de la même branche **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout est au hasard**
(famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %) ; dans la même écriture, la famille monte à
**69,8 %** et la sœur à **27,8 %**. Le retrieval parallèle 30 articles le chiffre : sur les **25
langues LANG_TREE** disponibles, les **sœurs** valent **0,619** (60 paires), les mêmes familles d'une
autre branche **0,170** (216), les familles différentes **0,0445** (324) — **13,9×**, coefficient de
sœur **+0,448** (p = 0,002) contre +0,213 pour l'écriture, **11/11** langues positives. Sur
l'**échantillon 20**, le contraste est **nul** (sœurs 0,058 vs 0,039, p = 0,078) : l'échantillon ne
contient que 12 paires de sœurs, dont 8 hors écriture. **J3.1 est reproduit à l'identique** (écart 0) ;
son coefficient de famille (+0,0556) était un **minorant** dilué. L'époque est **mono-époque** (1948) ;
le placebo de dates est nul (−0,0013 [−0,065 ; +0,041]) et le seul bras daté de J3.1 (Bible) donne
−0,034/siècle (p = 0,19) contre +0,609 pour l'écriture. L'écriture est la **porte** ; **dans la même
écriture, sur LANG_TREE**, l'ordre est **sœur (+0,448) > famille-autre (+0,092) > époque (nulle)** — le coefficient de
sœur dépasse même celui de l'écriture (+0,213) une fois la famille séparée. Fiche
[`reports/rapport-retrieval-familles.md`](../../reports/rapport-retrieval-familles.md), JSON
[`reports/retrieval-familles.json`](../../reports/retrieval-familles.json), outil
[`tools/retrieval_familles.py`](../../tools/retrieval_familles.py).
**J8.1 — la restitution v1 : le miroir strict ne monte pas, la forme canonique vaut 1,0000.**
La v0 restitue la surface **46/46** mais le miroir strict tombe à **5/46 = 0,1087** parce que
`rendre_mots`/`rendre_pos` séparent la ponctuation (`dort .`). La v1 construit une **forme
canonique** depuis les **segments + rôles + cibles** : **46/46 formes exactes** contre une
source canonisée (casse repliée, ponctuation retirée), mais **1/46 = 0,0217** contre la source
brute — et le **miroir strict reste 0,1087**. C'est la réponse : le strict ne doit pas monter,
il mesure la surface ; la forme canonique mesure autre chose. La structure tient : **395
segments**, **395 rôles**, **315 cibles**, **315/315 résolues**, **313/315** portées par un
autre segment ; couverture **65,84 % des jetons**, **75,19 % des caractères**. La limite est la
**stabilité structurelle** : **18/46** seulement après re-analyse de la surface canonique (le
lexique, lui, est stable 46/46). Contrôles : mélange/troncature canoniques **0/46**, détection
**46/46** ; rôles/cibles retirés, clé changée **43/43** textes éligibles. Fiche
[`reports/rapport-restitution-v1.md`](../../reports/rapport-restitution-v1.md), JSON
[`reports/pensee-restitution-v1.json`](../../reports/pensee-restitution-v1.json), outil
[`tools/mesurer_restitution_v1.py`](../../tools/mesurer_restitution_v1.py).
**J11.3 — les 50 textes libres : le contrat tient, la vue linéaire ne chevauche pas.** Les
**50 phrases de l'audit A26** sont rejouées avec le code du 14/11 (F1 **0,7902**, schéma
**v2**, restitution **v1**) : **0 plantage**, **50/50 JSON valide**, **50/50 portent les 8
champs** du schéma v2 et passent la validation ; les **4 refus** sont désormais des réponses
JSON en **code 3**, là où l'audit avait un stdout vide en code 1. En vue **`alternative`**,
**395 segments** et **115 chevauchements** dans **21/46** textes ; en vue **`filtrer`**,
**313 segments** et **0 chevauchement**. La restitution est **46/46 canonique**, le strict
**5/46 = 0,1087**. Comparaison A26 : **107 → 115 paires** — le compteur est le même, le code
a bougé (`f50` 50 → 63, `f26`/`f29` 1+2 → 0) ; les 8 champs passent de **0/46** à **50/50**.
Temps CLI médian **159,2 ms**, API **2,7 ms**. Fiche
[`reports/rapport-robustesse-semaine.md`](../../reports/rapport-robustesse-semaine.md), JSON
[`reports/pensee-robustesse-semaine.json`](../../reports/pensee-robustesse-semaine.json), outil
[`tools/mesurer_robustesse_semaine.py`](../../tools/mesurer_robustesse_semaine.py).
<!-- /notes -->
