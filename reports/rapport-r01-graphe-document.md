# R0.1 — le graphe de document : 51 pages, partitions exactes, fidélité 1,000

> **Ligne de roadmap** : R0.1 · **Date** : 2026-10-29 · **Verdict** : ✅ la découpe est
> mesurée — partition exacte, provenance exacte, rejeu identique, et les trois contrôles
> négatifs se comportent comme prévu.
>
> **Dispositif** : 30 documents, **51 pages**, 5 formats ; `tools/graphe_document.py` ;
> porte `tools/porte-document.sh` ; JSON brut
> [`r01-graphe-document.json`](r01-graphe-document.json) ; spécification
> [`document-graph.md`](../docs/implantation/document-graph.md).

## La question

Un document peut-il être découpé en **régions typées** (titre, section, paragraphe, tableau,
code, note, figure…), avec des **offsets exacts**, de façon **vérifiable** et **rejouable** —
sans modèle ? C'est la condition de R0.2 : un contrôleur de lecture qui ne sait pas où est un
tableau ne peut pas décider de le lire.

## Le dispositif

| ce qui est mesuré | comment |
|---|---|
| partition | les spans des régions sont contigus, couvrent tout le flux, et chaque SHA-256 se recalcule depuis `flux[start:end]` (offsets en **octets** UTF-8) |
| provenance | l'offset source (Markdown), la page (PDF) ou l'indice de bloc (HTML/DOCX/EPUB) pointent le **début** du bloc |
| fidélité | le flux contre une extraction **indépendante** : la source pour le Markdown, `lxml` pour le HTML, `pypdf` pour le PDF, `pandoc -t plain` pour le DOCX/EPUB |
| rejeu | deux découpes du même fichier donnent la même empreinte (aucun horodatage dans le manifeste) |
| structure | le corpus doit produire au moins 6 types, un tableau, une note, du code |

**Corpus** (51 pages) : 16 résolutions ONU (37 pages réelles, 5 langues : en, es, fr, ru, zh) ;
8 documents Markdown du dépôt (roadmap, état, vision, analyse, méthode, format, glossaire,
synthèse — une « page » = un document de moins de 8 ko) ; 3 fixtures HTML ; 3 conversions
DOCX/EPUB fabriquées par pandoc. Mélange délibéré : chaque format a son extracteur et son
contrôle.

## Ce qui est mesuré

| mesure | valeur |
|---|---|
| pages découpées | **51** |
| régions | **2 816** au total, dont **1 423** hors blancs |
| types | 11 : `blanc` 1 393, `paragraphe` 805, `section` 226, `liste` 203, `note` 120, `titre` 32, `tableau` 30, `code` 3, `figure` 3, `legende` 1 |
| fidélité | **1,0000** sur les **30/30** documents (minimum = 1,0000) |
| partition, provenance, rejeu | **30/30** conformes |
| durée de la porte | **5,4 s** |

**Second contrôle, plus large** : les **451 documents Markdown** du dépôt (`docs/**/*.md`),
soit **13 279 régions**, passent la partition, la provenance et la fidélité (minimum
**0,9996**) en **1,7 s**, sans un seul échec. C'est le corpus le plus exigeant : la source est
la référence, donc chaque mot doit s'y retrouver.

## Les contrôles négatifs

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **texte plat** | échouer : une seule région, la structure perdue | ✅ types = 1, la porte le voit |
| **PDF deux colonnes** | lire toute la gauche avant toute la droite | ✅ `GGGGGGDDDDDD`, **0 retour** |
| **notes hors corps** | ne pas recopier une note dans un paragraphe | ✅ 120 notes, **0 fuite** |
| **requête par type** | « où est le tableau X ? » sans modèle | ✅ 30 tableaux, dont l'offset pointe une ligne de tableau |

## Ce qui pourrait le rendre faux

- **La fidélité PDF est un recouvrement de caractères**, pas d'ordre : elle prouve que rien
  n'est perdu ni inventé, **pas** que l'ordre est juste. L'ordre n'est testé que par la
  fixture deux-colonnes — **synthétique**, avec une gouttière franche. Un PDF académique réel
  (deux colonnes, notes en marge, figures) n'est pas dans le corpus : c'est la première chose
  à ajouter.
- **Les notes sont une heuristique** (corps plus petit que la médiane) : un en-tête courant est
  typé `note`. C'est défendable pour la lecture (ce n'est pas du corps), pas pour la sémantique.
- **Le corpus a peu de tableaux PDF** : les 30 tableaux viennent du Markdown et du HTML. Un
  tableau PDF non balisé reste du texte, et c'est assumé — mais la porte ne le mesure pas.
- **`pypdf` n'est pas une vérité** : sur le CJK, son extraction est elle-même fragile. C'est
  pourquoi la comparaison est un recouvrement de caractères dans les **deux sens**.
- **Petit N par type** : 3 HTML, 3 conversions, 8 Markdown. Les taux par format ne sont pas
  des taux par type de document.
- **Pas de scan, pas d'OCR, pas de figures** : le graphe ne couvre que le texte extractible.

## Ce que ça change

R0.1 est **mesuré** : le lecteur a un champ de lecture. La prochaine action est **R0.2** (le
contrôleur), qui lira ce graphe ; puis R0.3 (le banc), dont la courbe est la mesure jointe du
contrôleur.

Les quatre signaux d'alarme ci-dessus sont la matière de R4.1 (tableaux) et de R4.4 (OCR), et
le PDF académique réel est une dette de corpus à payer avant de conclure sur les colonnes.

## Fichiers

- `tools/graphe_document.py` — le cœur : manifeste, partition, provenance, fidélité, porte.
- `tools/graphe_document_html.py`, `tools/graphe_document_pdf.py` — les deux parseurs.
- `tools/porte-document.sh` — la porte.
- `docs/implantation/document-graph.md` — la spécification du manifeste.
- `reports/r01-graphe-document.json` — les mesures brutes (30 documents).
- `tools/tests/documents/{html,pdf}/` — les fixtures et le générateur du PDF deux colonnes.
