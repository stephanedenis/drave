# R44 — Encodeur visuel / OCR (scans, figures, layout)

> **Statut** : partiel · **Priorité** : P3 · **Programme** : R · **Dépend de** : R41, R42, R43 · **Bloqué par** : — (l'OCR est installé ; restent les scans réels, le layout et les exposants)
> **Ligne de roadmap** : R4.4 · **Fiche de résultat attendue** : rapport-r44-encodeur-visuel.md (à créer dans `reports/`)
> **Résumé** : Lire les pages scannées, les figures et le layout, et retrouver la réponse du texte natif.
> **Glossaire** : [OCR](../../theorie/glossaire/entrees/ocr.md) · [layout](../../theorie/glossaire/entrees/layout.md) · [WER](../../theorie/glossaire/entrees/wer.md).

## Le besoin

Une partie des documents n'existe qu'en image. Sans OCR et layout, Drave ne lit que le texte déjà extrait. C'est le dernier bloc de R4, après les blocs structurels classiques.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | une image ou une page PDF et une question |
| **sortie** | des régions, du texte et un layout ; la même réponse que le texte natif |
| **coût** | coût par page ; l'OCR est un bloc externe ou neuronal |
| **trace** | les régions OCR et les scores sont tracés |

## Ce qui est mesuré

**Pilote du 2026-10-31** — 10 pages rendues à 300 dpi, 6 PDF, 3 langues (détail :
[`reports/rapport-r44-ocr-pilote.md`](../../../reports/rapport-r44-ocr-pilote.md)) :

- **WER 4,48 %** mot à mot, rappel 97,37 %, confiance 93,2 ;
- **parité de passage 27/30 (90,0 %)** sur les questions du banc R0.3 ; valeur stricte 25/30 ;
- contrôles : **sans OCR 0/30** ; page « photo » simulée **WER 17,08 %, parité 26,7 %**.

Reste à mesurer : les **scans réels**, le **layout** (colonnes, tableaux, rotations) et les
**exposants** — les trois causes des écarts du pilote sont nommées dans la fiche.

## Portes

1. 10 pages scannées donnent la même réponse que le texte natif
2. le contrôle sans OCR échoue
3. les scores d'OCR sont tracés

## Contrôles négatifs

- texte natif ; sans OCR ; layout mélangé
- page propre contre page bruitée

## Ce qui pourrait le rendre faux

- les scans sont propres et les mêmes que le texte d'entraînement
- l'OCR est un modèle externe non mesuré
- la langue ou la police n'est pas couverte

## Étapes

1. ~~choisir l'OCR~~ — **fait** : tesseract 5.5.3, sans root (`tools/installer_ocr.sh`) ; le
   modèle de layout reste à choisir
2. ~~brancher sur R01 (régions et offsets)~~ — **fait** : `tools/graphe_document_ocr.py` rend des
   blocs au manifeste commun
3. mesurer WER, layout et parité ; écrire la fiche — **pilote fait** (ci-dessus) ; **la porte
   de R4.4 reste ouverte** : pages **scannées** réelles, colonnes, exposants

## Documents à écrire

- ~~`encodeur-visuel.md`~~ — **écrit** : [`docs/implantation/encodeur-visuel.md`](../../implantation/encodeur-visuel.md)
- mettre à jour R4.4 — fait dans la roadmap

## Voir aussi

- [La fiche du pilote](../../../reports/rapport-r44-ocr-pilote.md) · [l'installeur](../../../tools/installer_ocr.sh) · [la porte](../../../tools/porte-ocr.sh)
- [La spécification du bloc](../../implantation/encodeur-visuel.md)
- [Programme R](../roadmap.md#r4--les-blocs-structurels)
- [Analyse, § 6](../../theorie/lecture-rapide.md#6-par-type-de-document)
