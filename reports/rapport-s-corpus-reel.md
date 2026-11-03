# S — L'analyseur lit le français propre (65,5 % de GN+GV), pas le CEGEP OCR (8,5 %, plancher du mélange)

> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur **50 000 lignes** et
> **20 799 phrases** du corpus **CEGEP OCR** (D/R/A, 4,41 M car.) et **50 000** lignes/phrases de
> **littérature propre** (17 M car.), l'analyseur trouve un **GN et un GV** dans **65,5 %** des
> phrases propres contre **9,1 %** quand les mots sont mélangés — le signal est la **langue**. Sur
> le CEGEP OCR, il est au **plancher du mélange** : **8,5 %** contre **9,1 %**. Le corpus CEGEP
> est **multilingue et technique** (les scans anglais de réseaux et d'algorithmique) et
> l'analyseur est **français** : ce n'est pas une mesure du français OCR, c'est une mesure de ce
> que le corpus n'est pas. L'unité compte : la ligne coupe les phrases (3,6 % contre 51,0 %).

## Le dispositif

- **CEGEP** : `data/corpus_ocr_cegep/train.txt` (D/R/A, 4,41 M car., OCR) ; **propre** :
  `data/corpus_fr_litterature.txt` (17 M car., texte natif).
- **Filtre** : lignes de 20–300 caractères (phrases 20–400), au moins 4 mots alphabétiques, au
  moins 80 % de lettres/espace/ponctuation ; échantillon **régulier** (pas de hasard) de
  **50 000** unités par corpus, phrases reconstruites par lignes jointes et coupées sur `. ! ?`
  (le CEGEP a **20 799** phrases plausibles, toutes prises).
- **Mesure** : `generateur.structure()` sur chaque unité ; **GN+GV** (au moins un GN et un GV),
  **sans GV**, **couverture** des octets par les segments, **homographes nominaux** (GN dont le
  dernier mot est dans le lexique de verbes — `ferme`, `fait`, `lit`…).
- **Contrôle négatif** : le **mélange des mots** de chaque unité (graine 0), mêmes statistiques.
- **Baseline** : un segment par unité couvre 100 % des octets et donne **0 %** de GN+GV — la
  couverture seule ne prouve rien.

## Les chiffres

| unité | corpus | GN+GV | sans GV | couverture | homographes | unités homographes |
|---|---|---:|---:|---:|---:|---:|
| ligne | CEGEP | 3,6 % | 0,5 % | 0,94 | 21 | 18 |
| ligne | propre | **51,0 %** | 10,3 % | 0,88 | 596 | 592 |
| ligne | mélange | 3,8 % | 0,5 % | 0,94 | 20 | 20 |
| phrase | CEGEP | 8,5 % | 0,8 % | 0,94 | 28 | 28 |
| phrase | propre | **65,5 %** | 8,0 % | 0,88 | 1 184 | 1 150 |
| phrase | mélange | 9,1 % | 0,4 % | 0,93 | 23 | 23 |

## Les contrôles

- **Mélange des mots** : 3,8 % (lignes) et 9,1 % (phrases) — le plancher structurel de
  l'heuristique. Le CEGEP (3,6 % / 8,5 %) est **à ce plancher** ; la littérature propre
  (51,0 % / 65,5 %) est **très au-dessus**.
- **Un segment par unité** : couverture 1,0, GN+GV 0 % — la couverture n'est pas la structure.
- **Unité** : la ligne (fragment) divise le taux par deux environ ; la phrase reconstruite est
  l'unité de la banque.
- **Propre vs CEGEP** : le contraste est la **langue et le genre**, pas l'OCR seul : le CEGEP
  contient des livres anglais et techniques ; l'analyseur n'a pas de lexique anglais.

## Le négatif nommé

**Le CEGEP OCR n'est pas un corpus français de prose.** Le taux de GN+GV y est au plancher du
mélange (8,5 % contre 9,1 % sur les phrases) : l'analyseur n'y « lit » pas plus de structure que
dans un sac de mots. Deux causes se superposent : le corpus est **multilingue et technique**, et
la **ligne OCR** est un fragment de phrase. La conséquence est une règle de travail : **filtrer
la langue et le genre, segmenter en phrases** avant d'analyser ; le CEGEP brut ne peut pas
alimenter la banque tel quel.

## Ce qui pourrait le rendre faux

- **Pas de gold sur le corpus** : GN+GV est un **taux de structure**, pas une exactitude ; un
  segment faux peut produire un GN et un GV. C'est le gold de 47 phrases qui mesure la justesse ;
  ceci mesure la **robustesse**.
- **Le filtre** sélectionne les lignes plausibles (20–300 car., ≥ 4 mots, ≥ 80 % de lettres) : les
  titres, les tableaux et les formules sont exclus — le taux ne vaut pas pour eux.
- **Le corpus propre est de la littérature** (genre unique) ; le CEGEP est un mélange
  anglais/technique/français. Le contraste mesure surtout la **langue**, pas la qualité OCR.
- **Les homographes** dépendent du lexique de verbes : 28 sur 20 799 phrases CEGEP, 1 184 sur
  50 000 propres ; le chiffre propre est plus haut parce qu'il y a plus de GN nominaux. C'est un
  décompte de **suspects** (GN finissant sur un mot du lexique), pas une erreur : la règle de
  contexte v4 en résout une partie par le mot suivant.
- **Le mélange** garde les mots et la ponctuation : il teste l'ordre, pas le vocabulaire ; un
  analyseur qui ne lit que les déterminants aurait le même plancher.

## Le miroir entrée/sortie

- **entrée** : surface → structure, mesurée par GN+GV, la couverture et les rôles ;
- **sortie** : le **corpus de référence** de 55 structures (`data/structures/banque.jsonl`,
  SHA `76accf9d…`) et son `verifier_corpus.py` — l'analyseur lit, le corpus se restitue.

Le corpus réel **n'est pas exporté** : la prochaine étape est une **banque de candidats** filtrée
par langue et segmentée en phrases, à valider par un humain. La fluidité (un GN+GV) n'est pas la
fidélité (le rôle juste).

## Fichiers

- Sous-module : commits **`140feb6`** (mesure), **`97641d5`** (banque), **`00d2a01`** (v4) et
  **`230d03a`** (v6), `mesure_corpus.py`, `candidats_corpus.py`, `donnees/mesure-corpus.json`,
  `donnees/phrases_generees.json`, **55 tests**.
- Mesure : `python3 mesure_corpus.py --max 50000` (60 s CPU) ;
  `donnees/mesure-corpus.json` (50 000 lignes, 20 799 phrases CEGEP, 50 000 propres).
- Fiche : celle-ci ; état et roadmap S mis à jour.

## La suite (ligne S)

1. **Filtrer langue et genre** (français détecté, prose), **segmenter en phrases** avant
   l'analyse ;
2. ~~banque de candidats~~ (**200 phrases, 355 candidats**) → validation humaine ;
3. ~~homographes/lexique~~ (v4) et ~~h050/h053~~ (v6) ; reste le nom après un adjectif hors lexique ;
4. le corpus de référence (55 structures) reste le test de structure pour N2/R1.
