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

**Pilote du 2026-10-31** — 10 pages rendues à 300 dpi, 6 PDF, 3 langues
([`pilote`](../../../reports/rapport-r44-ocr-pilote.md)) : **WER 4,48 %**, parité de passage
**90 %**, sans OCR 0/30.

**Programme de la nuit du 31/10 au 1/11** — 100 scans **simulés** (5 familles, dev/test),
colonnes, tableaux et un **vrai scan** ([`scans`](../../../reports/rapport-r44-scans.md)) :

- WER (dev → test) : **propre 4,1 → 3,0 %**, **photocopie 6,3 → 4,7 %**, **photo 6,7 → 5,7 %**,
  **papier 6,9 → 6,4 %**, **fax 21,9 → 15,5 %** ; la photo partait de **55,9 %** brute ;
- **préservation** des réponses du lecteur (dev, 30 questions) : **90,0 / 86,7 / 86,7 / 73,3 /
  53,3 %** ; **exposants** : le plafond du texte propre monte de 83,3 à **90 %** ;
- **colonnes** : deux colonnes **89,4 % → 0,5 %** de WER (mono inchangée) ;
- **tableaux** : **92,6 %** de cellules exactes (propre), **69,1 %** (photocopie), **53,7 %**
  (photo) ; sans redressement **0 %** ; texte à plat **0 cellule localisée** ;
- **scan réel** (Internet Archive) : **7,10 %** d'accord avec la couche OCR du PDF ; un second
  livre à lexiques **prouve l'ordre des colonnes** (**15,3 / 7,1 / 12,8 %** contre **98 %** en ordre
  inverse), et la validation réelle a corrigé le lecteur : un en-tête centré traversait la
  gouttière (ligne cherchée sur les mots + couverture verticale).

Reste : les **scans réels de bout en bout** (un seul livre, référence = un autre OCR), le **fax**
1 bit (limite d'information), l'**exposant fusionné**, et les tableaux **sans traits**.

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

1. ~~choisir l'OCR~~ — **fait** : tesseract 5.5.3, sans root (`tools/installer_ocr.sh`).
2. ~~brancher sur R01 (régions et offsets)~~ — **fait** : `tools/graphe_document_ocr.py` rend des
   blocs au manifeste commun ; le prétraitement, les exposants, les colonnes et les tableaux sont
   mesurés.
3. mesurer WER, layout et parité ; écrire la fiche — **fait sur scans simulés + un vrai scan**
   (ci-dessus). **La porte de R4.4 reste ouverte** : 10 pages **scannées** réelles, de bout en
   bout, avec une vérité humaine. Les limites (fax, exposant fusionné, tableaux sans traits) sont
   nommées dans la fiche.

## Documents à écrire

- ~~`encodeur-visuel.md`~~ — **écrit** : [`docs/implantation/encodeur-visuel.md`](../../implantation/encodeur-visuel.md)
- mettre à jour R4.4 — fait dans la roadmap

## Voir aussi

- [La fiche des scans](../../../reports/rapport-r44-scans.md) · [le pilote](../../../reports/rapport-r44-ocr-pilote.md) · [l'installeur](../../../tools/installer_ocr.sh) · [la porte](../../../tools/porte-ocr.sh) · [la porte des scans](../../../tools/porte-ocr-scans.sh)
- [La spécification du bloc](../../implantation/encodeur-visuel.md)
- [Programme R](../roadmap.md#r4--les-blocs-structurels)
- [Analyse, § 6](../../theorie/lecture-rapide.md#6-par-type-de-document)
