# R44 — Encodeur visuel / OCR (scans, figures, layout)

> **Statut** : bloquée · **Priorité** : P3 · **Programme** : R · **Dépend de** : R41, R42, R43 · **Bloqué par** : aucun OCR installé (ni tesseract ni pytesseract)
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

- WER de l'OCR
- exactitude du layout (colonnes, tableaux, figures)
- parité de réponse avec le texte natif

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

1. choisir l'OCR et le modèle de layout
2. brancher sur R01 (régions et offsets)
3. mesurer WER, layout et parité ; écrire la fiche

## Documents à écrire

- `encodeur-visuel.md` (OCR, layout, parité, porte, dans `docs/implantation/`)
- mettre à jour R4.4

## Voir aussi

- [Programme R](../roadmap.md#r4--les-blocs-structurels)
- [Analyse, § 6](../../theorie/lecture-rapide.md#6-par-type-de-document)
