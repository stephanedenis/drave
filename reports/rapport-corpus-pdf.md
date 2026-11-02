# Le corpus PDF local — les livres et les cours

> **Verdict.** `tools/extrait_pdf.py` a extrait le **texte natif** des documents locaux :
> **2 785 PDF**, **222 570 pages**, **1 927 documents gardés**, **314,4 M caractères**,
> **322,5 Mo**, **39 506 tronçons** — **8 Ko à zéro** entre les splits, **0 / 40** sur les trois
> jeux d'évaluation locaux. **159 documents sont scannés** (comptés, pas océrisés) et **616
> doublons** ont été retirés. Les **licences sont nommées** : livres et notes de cours, droits
> réservés, usage local, non diffusé.
>
> **Date** : 2026-11-01. **Ligne** : Données (D/R/A). **Machine** : CPU seul.

## 1. Les sources et leurs licences

| racine | PDF | licence |
|---|---:|---|
| `Biblio_large` | **104** | livres — droits réservés, usage local, non diffusé |
| `archives/CEGEP` | **2 681** | notes de cours — droits réservés, usage local, non diffusé |

Ce sont des **documents**, pas de la prose encyclopédique : des livres entiers, des notes de
cours, des rapports. Le corpus reste **local** ; il n'est ni publié ni redistribué. La licence
est écrite dans le manifeste (`reports/corpus-pdf.json`) et ici.

## 2. La méthode

`tools/extrait_pdf.py` :

1. parcourt les racines, lit le nombre de pages (`pdfinfo`) et le texte (`pdftotext -enc UTF-8`) ;
2. **détecte les scannés** : moins de 50 caractères par page → compté, écarté (le texte d'un scan
   n'existe pas sans OCR) ;
3. **déduplique** les documents (BLAKE2b) et les tronçons de l'entraînement ;
4. **sépare** par document (hash salé du chemin, 5 % val, 5 % test) ;
5. écrit `train/val/test.txt` (tronçons de 8 192 caractères), le **SHA-256** et le manifeste.

## 3. Le résultat

| grandeur | valeur |
|---|---:|
| PDF parcourus | **2 785** |
| pages | **222 570** |
| documents gardés | **1 927** |
| documents scannés (écartés) | 159 |
| documents trop courts (< 300 car.) | 83 |
| doublons de documents | 616 |
| caractères gardés | **314 351 704** |
| mots estimés (car. / 6,2) | 50 701 887 |
| tronçons (8 192 car.) | 39 506 (15 doublons) |
| train / val / test | 295,8 Mo / 15,0 Mo / 11,7 Mo |
| documents train / val / test | 1 736 / 101 / 90 |

**Contrôles** : **0 / 40** fenêtres sur chacun des trois jeux d'évaluation locaux ; au niveau du
**tronçon de 8 Ko**, **0** fuite entre les splits. Le contrôle ligne signale 4,0 % / 2,6 % de
lignes dupliquées : ce sont les **en-têtes et pieds de page** répétés à chaque page d'un même
document, pas de la prose dupliquée.

## 4. Ce qui pourrait être faux

- **Texte natif seulement** : les **159 scannés** ne sont pas dans le corpus (l'OCR viendra du
  pipeline R4.4) ; les PDF sans couche texte sont invisibles ici.
- **La mise en page est perdue** : en-têtes, pieds de page, numéros conservés ; formules,
  tableaux et figures perdus (`pdftotext`).
- **Les gros PDF** : le délai de 120 s par document écarte les cas extrêmes (documentation
  Valgrind) ; ils sont comptés comme courts.
- **Les droits** : livres et cours sous droits réservés, corpus local non diffusé ; toute
  réutilisation hors du dépôt est une question de licence, pas de technique.
- **La déduplication est exacte** : les quasi-doublons (versions d'un même cours) restent.

## 5. La suite

L'**OCR des 159 scannés** (le pipeline R4.4 : prétraitement, tesseract, parité) ; les
**collections et Documents** (7 496 PDF, le personnel) ; le **catalogue des corpus** (Wikipédia
texte intégral + PDF) ; et la comparaison des genres (encyclopédie, livre, cours).

## Fichiers

- `tools/extrait_pdf.py` — l'extracteur (PDF → texte natif).
- `reports/corpus-pdf.json` — le manifeste (racines, licences, pages, SHA-256).
- `reports/corpus-pdf-contamination.json` — le contrôle (8 Ko + jeux locaux).
- `data/corpus_pdf/` — le corpus (322,5 Mo, gitignoré).
