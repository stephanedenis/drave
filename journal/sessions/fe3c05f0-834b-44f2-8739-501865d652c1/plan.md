# Plan de session — R4.4, les scans (mandat libre de 10 h)

> **Mandat ouvert** le 2026-10-31 22 h 50 HAE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) — le heartbeat est celui de
> l'état ; la session le met à jour à chaque cycle. **Échéance : 2026-11-01 07 h 14** (10 h
> humain, pas une estimation de durée de travail).

- **Session** : `fe3c05f0-834b-44f2-8739-501865d652c1`
- **Rôle** : **R4.4 — les scans** — CPU seulement ; les deux GPU restent à N2.h.
- **Périmètre** : R4.4 — les scans (OCR, prétraitement, exposants, colonnes, second moteur)
- **Fichiers réservés** : `work/r44/`, `work/ocr/`, `tools/simuler_scan.py`, `tools/nettoyer_scan.py`,
  `tools/mesurer_scans.py`, `tools/graphe_document_ocr.py`, `tools/mesurer_ocr.py`, `tools/porte-ocr.sh`,
  `reports/r44-*`, `docs/implantation/encodeur-visuel.md`, `journal/sessions/fe3c05f0-…/`
- **Heartbeat** : 2026-11-01 00:35
- **État** : en cours
- **Prochaine action** : la **parité** sur photocopie (6,6 % de WER mais 48 % de parité), puis
  exposants et colonnes.

## Objectif final

**R4.4 mesurée, pas partielle.** Un lecteur qui lit des **scans** — photocopie, photo de
téléphone, fax, papier — avec la **même réponse** que le texte natif :

1. **WER ≤ 5 %** et **parité ≥ 90 %** sur les pages de **test** (jamais vues) ;
2. la **porte** `porte-ocr` resserrée sur ce corpus, avec ses contrôles négatifs ;
3. la **fiche**, la **spécification**, la **roadmap** et le **journal** qui portent le résultat ;
4. et une limite écrite : les scans sont **simulés** — le jour où un scanner existe, le même
   banc tourne sur des scans réels sans changer une ligne.

## Ambition

Faire de l'OCR un **bloc classique robuste** du lecteur, pas un pilote qui marche sur des
rendus vectoriels. Trois idées portent le programme :

- **la parité juge, pas le WER** : un WER de 6 % qui casse la réponse à une question n'est pas
  une lecture ; c'est la réponse du **même lecteur** (R0.2) sur le natif et sur le scan qui
  décide ;
- **le prétraitement est mesurable** : chaque étape porte un nom, et une étape qui ne paie pas
  est retirée — agrandir une photocopie a **doublé** son WER, c'est une mesure, pas une opinion ;
- **le corpus d'abord** : un levier mesuré sur un banc faux ne vaut rien. Cinq familles de
  dégradation, un split dev/test, une vérité terrain qui ne bouge pas.

## Stratégie

1. **Mesurer le brut** famille par famille, dev et test, sans rien toucher — c'est la ligne de
   base, et elle est déjà parlante : photo **55,9 %** (dev), fax **27,1 %**, papier **13,0 %**,
   photocopie **6,6 %**, propre **4,5 %**.
2. **N'ajouter que ce qui paie** : le prétraitement est un pipeline d'étapes nommées ; on
   mesure le delta de chaque étape, famille par famille, sur **dev**.
3. **Trancher sur test** : le réglage ne voit jamais les pages de test ; si le gain ne transfère
   pas, il n'existe pas.
4. **Contrôles négatifs partout** : page **noire** (aucun mot), page **propre** (plafond),
   **rejeu** (les mêmes chiffres), et le **sans-OCR** du pilote.
5. **Un commit par résultat** : chiffre, dispositif, contrôle, fiche, ligne d'état.

## Plan par phases (avec l'état au fil de l'eau)

| # | phase | livrable | état |
|---|---|---|---|
| 1 | **corpus** de scans simulés (5 familles, dev/test, manifeste) | `tools/simuler_scan.py`, 100 scans | ✅ fait |
| 2 | **baseline** brute, WER + parité + contrôles | `work/r44/mesure-brut.json` | ✅ fait |
| 3 | **prétraitement** (recadrage, éclairage, redressement, échelle, lissage) | `tools/nettoyer_scan.py`, deltas mesurés | ✅ photo **55,9 → 7,0 %**, papier test **53,2 → 6,2 %** |
| 4 | **parité** : préservation, pas « les deux échouent » | métrique corrigée + diagnostic | ✅ préservation **86,7 %** (plafond propre **90 %**) |
| 5 | **exposants** : passe ciblée chiffres sur les petits mots du TSV | récupération des appels de note | ✅ plafond propre **83,3 → 90 %** |
| 6 | **colonnes** : gouttière verticale, ordre de lecture | pages 2 colonnes synthétiques | ✅ **89,4 → 0,5 %** de WER |
| 7 | **tables** : mots → lignes/colonnes → cellules | exactitude de cellules | ✅ **92,6 %** (propre), **69,1 %** (photocopie) |
| 8 | **second moteur** : RapidOCR (ONNX, CPU) comparé | un tableau, un verdict | ✅ contrôle : 3 à 10× pire sur le français |
| 9 | **scan réel** : Internet Archive + couche OCR | un accord entre moteurs, dit comme tel | ✅ **7,10 %** sur 10 pages |
| 10 | **consolidation** : porte `porte-ocr-scans`, fiche, spec, roadmap, journal | commit | ✅ fait |

## Ce que les autres sessions peuvent réutiliser

- [`tools/simuler_scan.py`](../../../tools/simuler_scan.py) — 100 scans déterministes, cinq
  familles, un manifeste avec les paramètres de chaque image ;
- [`tools/mesurer_scans.py`](../../../tools/mesurer_scans.py) — WER + parité par famille et par
  split, cache d'OCR par empreinte des pixels ;
- [`tools/nettoyer_scan.py`](../../../tools/nettoyer_scan.py) — prétraitement à étapes nommées,
  diagnostic d'image ;
- `work/r44/scans/` (images + manifeste), `work/r44/ocr/` (cache), `work/r44/journal.md`
  (journal de bord).

Les sessions **R3/R31** (restitution, lecture d'images) peuvent réutiliser le corpus et le banc
tels quels. **N2.h** garde les GPU ; cette session ne prend que du CPU.

## Contraintes et fichiers réservés

- **CPU seulement** ; pas de `toutes-les-portes.sh` (la passe complète lancerait les portes GPU) ;
- fichiers réservés : `work/r44/`, `work/ocr/`, `tools/simuler_scan.py`,
  `tools/nettoyer_scan.py`, `tools/mesurer_scans.py`, `tools/graphe_document_ocr.py`,
  `tools/mesurer_ocr.py`, `tools/porte-ocr.sh`, `reports/r44-*`,
  `docs/implantation/encodeur-visuel.md`, `journal/sessions/fe3c05f0-…/` ;
- l'état est **partagé** : une session écrit `en-cours` à la fois ; les faits
  (`reports/`, roadmap, backlog) se committent **avec** leur ligne.

## Critères de réussite (pré-enregistrés)

- **dev** : WER ≤ 5 %, parité de passage **≥ 90 %**, parité de valeur rapportée ;
- **test** : WER ≤ 8 % (le transfert), parité non mesurable (pas de questions) ;
- **contrôles** : page noire → 0 mot ; page propre → plafond ; rejeu → identique ;
- **porte** : les seuils ci-dessus, écrits dans `mesurer_scans.py`, et la porte échoue si on
  lui donne une page noire ou une image sans OCR.
