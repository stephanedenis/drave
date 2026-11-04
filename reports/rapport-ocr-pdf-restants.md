# D — les 8 `.PDF` restants : 4 documents, 49 pages, 3 doublons — la limite est mesurée

> **Ligne de roadmap** : D · **Date** : 2026-11-04 · **Verdict** : ✅ **la limite nommée de D
> est close** — les **8 scans `.PDF`** (58 p) que `rglob("*.pdf")` manquait sont **OCRisés** en
> **90,1 s** ; ils ne donnent que **4 documents retenus** (49 p, **54 167 car.**, 8 736 mots,
> 9 tronçons de 8 Ko) : **6 fichiers uniques**, **5 textes distincts**, **3 copies** et **1
> formulaire de 210 car.** écartés. ⛔ **l'intégration au corpus CEGEP reste au hub** :
> `data/` est réservé par N2 et le split à 4 documents est vide en val/test.
>
> **Dispositif** : fonds `/home/stephane/Data13TB/stephane/archives/CEGEP`, 30 `.PDF`
> majuscules ; qualification au **texte natif intégral** (`pdftotext`, seuil 50 car/page) ;
> OCR `tools/ocr_pdf.py --liste` (tesseract 5.5.3 sans root, 300 dpi, fra+eng, 8 ouvriers)
> sur **cpu1** (claim `aeafe951/ocr-pdf-restants`) ; manifeste
> [`ocr-pdf-restants.json`](ocr-pdf-restants.json) ; texte brut dans `work/ocr/restants/`.

## 1. La qualification : 8 scans sur 30, et 22 `.PDF` natifs exclus

Les 30 `.PDF` (majuscules) du fonds, texte natif par page :

| classe | fichiers | car./page | ce qu'on en fait |
|---|---:|---|---|
| **scans** | **8** | **0** | OCR (liste explicite, 58 p) |
| natifs | 22 | **307,5 – 3 688,8** | exclus (déjà lus par `extrait_pdf.py`) |

L'écart est **net** : aucun fichier entre 0 et 307 car/page. Le seuil de 50 car/page (la règle
du dépôt) n'a donc aucune zone d'ambiguïté sur ce fonds. Le rapport CEGEP annonçait « 8 scans,
58 p (6 uniques) » : les pages et le nombre de scans sont exacts ; le « 6 uniques » compte des
**fichiers**, pas des **textes** (voir § 3).

## 2. L'OCR : 8 fichiers, 58 pages, 90,1 s

| mesure | valeur |
|---|---:|
| fichiers OCRisés | **8** (58 p) |
| documents retenus | **4** (49 p) |
| caractères retenus | **54 167** |
| mots estimés | **8 736** |
| tronçons de 8 Ko | **9** |
| octets du corpus (train) | **55 857** |
| temps | **90,1 s** (8 ouvriers, cpu1) |
| val / test | **0 / 0** (4 documents, tirage salé) |

## 3. Le contrôle qui compte : les doublons au texte, pas au nom

Chaque fichier a été OCRisé séparément et son texte empreinté (SHA-256) :

| fichier(s) | pages | car. OCR | empreinte (16) | sort |
|---|---:|---:|---|---|
| `DOC.PDF` ×2 | 1 | 210 | `7ceb214210b97112` | **écarté** (< 300 car.) |
| `Choquette c. Chagnon.PDF` ×2 | 6 | 7 575 | `8568cf8d6899ec09` | 1 retenu |
| `DOC1.PDF` | 22 | 25 470 | `0448a973889f56c9` | retenu |
| `DOC2.PDF` | 20 | 19 101 | `ce3278ad842d24e0` | retenu |
| `Assurance pour stagiaires[-B2344-11403].PDF` ×2 | 1 | 2 021 | `3bf071e129bf357d` | 1 retenu |
| **total** | **58** | **54 377** (5 textes) | | **4 retenus / 49 p** |

- **Les paires sont identiques au bit près** (3/3 : DOC, Choquette, Assurance) : la
  déduplication n'est pas une supposition sur les noms.
- **Les cinq textes sont tous distincts** : ce n'est pas un « tout se ressemble ».
- **Le formulaire d'une page** (`DOC.PDF`, 210 car.) est **nommé**, pas perdu : il tombe sous
  `--min-chars 300`, le seuil du corpus. Le suivant (2 021 car.) passe — le seuil sépare un
  formulaire d'un contenu, il ne les confond pas.
- **6 fichiers uniques, 5 textes, 4 retenus** : le « 6 uniques » du rapport CEGEP était un
  compte de fichiers ; l'OCR tranche à **4 documents**.

## 4. Ce qui n'est pas fait — et qui ne peut pas l'être ici

- **L'intégration au corpus CEGEP** (`data/corpus_ocr`) : `data/` est réservé par N2. Surtout,
  relancer `ocr_pdf.py --sortie data/corpus_ocr` **écraserait** les splits existants (le script
  ouvre `train/val/test.txt` en `w`) : la fusion doit être un **ajout explicite**, pas un run.
- **Le split tenu à l'écart** : à 4 documents, le tirage salé met **tout en train** (0 val,
  0 test). Le corpus CEGEP actuel a 2/2/56 ; y ajouter 4 documents et **re-tirer** le split
  pourrait déplacer des documents entre splits — décision du hub, avec un contrôle de
  contamination à 8 Ko (`verifie_contamination.py --taille-troncon 8192`).
- **La WER** : pas de vérité terrain sur ces scans réels ; l'OCR est **brut**, sans le
  prétraitement R4.4 (rotation, contraste, colonnes).
- **La licence** : notes de cours, droits réservés, usage local non diffusé (le manifeste le
  porte).

## 5. Ce que ça change

La dernière limite nommée de D n'est plus « 8 scans non parcourus » : elle est **mesurée** —
4 documents, 49 pages, 54 167 caractères, 3 doublons et 1 formulaire nommés. La ligne de D peut
passer de « clos avec une limite » à **close**, et le hub peut décider l'ajout au corpus
(60 → 64 documents, 1 982 → 2 031 pages, 4,41 → 4,46 M car.) avec un re-split contrôlé.

Ligne d'état proposée au hub :

> **D — clos** : les 8 `.PDF` restants sont OCRisés (4 documents, 49 p, 54 167 car., 90 s ;
> 3 doublons et 1 formulaire de 210 car. nommés ; 22 `.PDF` natifs exclus) ;
> [fiche](./rapport-ocr-pdf-restants.md) · [manifeste](./ocr-pdf-restants.json).

## 6. Fichiers

- `reports/ocr-pdf-restants.json` — le manifeste (agrégats, SHA-256 du corpus).
- `reports/rapport-ocr-pdf-restants.md` — cette fiche.
- `work/ocr/restants/train.txt` — le texte OCR brut (non versionné).
- `work/ocr/restants-pdf.liste` — la liste des 8 scans qualifiés (non versionnée).
