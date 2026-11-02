# Plan de session — D/R/A : les données, le lecteur, le moteur

> **Mandat ouvert** le 2026-11-01 16 h 25 HNE depuis
> [`docs/pilotage/plan-travail.md`](../../../docs/pilotage/plan-travail.md) (§ 2, § 3) — la session
> reprend la session `fe3c05f0` (R4.4 close) pour le rôle **D/R/A**. Le heartbeat est celui de
> l'état.

- **Session** : `fe3c05f0-834b-44f2-8739-501865d652c1`
- **Rôle** : **D/R/A — les données, le lecteur, le moteur** : le texte intégral, l'extraction
  PDF/OCR, la préparation de R1.1/R1.2, A2.6/A8.3.
- **Périmètre** : D (texte intégral, PDF/OCR, licences, stubs), R1.1/R1.2 (préparation), A2.6/A8.3
- **Fichiers réservés** : `data/wikipedia/` (lecture), `data/corpus_wiki_*`,
  `tools/corpus_wikipedia*.py`, `tools/verifie_contamination.py`, `tools/catalogue_corpus.py`,
  `reports/corpus-wiki-*`, `reports/corpus-wikipedia-*`, `reports/inventaire-*`,
  `reports/rapport-corpus-*`, `reports/r11-*`, `reports/r12-*`, `reports/a26-*`, `reports/a83-*`,
  `journal/sessions/fe3c05f0-…/`
- **Heartbeat** : 2026-11-01 19:40
- **État** : en cours
- **Prochaine action** : les **neuf langues** en texte intégral (les neuf lancées), puis la contamination, les fiches,
  le catalogue et l'extraction PDF/OCR.

## Objectif final

**Les dix corpus en texte intégral, mesurés et ficés** — le français réel en volume pour N2 :

1. le **texte intégral** des dix langues (le dump, un débaliseur mesuré, la déduplication exacte,
   les splits par article, les contrôles de contamination) ;
2. l'**extraction PDF native et OCR** des documents locaux (les 104 livres, les 2 711 PDF du
   CEGEP, les collections) avec leurs licences ;
3. la **préparation de R1.1/R1.2** (le contexte natif) et les mesures A2.6/A8.3 ;
4. pour chaque livraison : le chiffre, la fiche, le JSON, le commit et la ligne d'état.

## Ambition

Que **D** cesse d'être un inventaire et devienne le **carburant mesuré** de N2, L et S : des
corpus dont on connaît la taille, la qualité, les fuites et les limites — et dont le passage à
l'échelle (10 langues, texte intégral, documents) est reproduit par un outil, pas à la main.

## Stratégie

1. **Le pilote avant le run** : 100 000 articles pour mesurer le débaliseur (temps, résidus,
   volume), puis le run complet en arrière-plan.
2. **La même chaîne que les résumés** : dédup exacte, split par article, SHA-256, manifeste,
   contamination — pour que les deux corpus se comparent.
3. **Les limites écrites** : débaliseur regex (infobox, formules, tableaux perdus), licence
   CC-BY-SA, dédup exacte seulement.
4. **Ne pas toucher aux GPU** : la session est CPU/IO ; N2 garde les siens.

## Reprise

**R4.4** est close (fiche `rapport-r44-scans`), ses trois limites nommées ; la session reprend
pour le rôle D/R/A, sans rouvrir R4.4.
