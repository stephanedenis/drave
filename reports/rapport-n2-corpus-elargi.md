# N2.i — Le corpus élargi : 4,84 Mo uniques au lieu de 3,24

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : élargir le corpus au dépôt
> courant (**+49 %** de texte unique, autres registres) ne fait pas baisser la PPL en domaine
> (**3,1278** sur son propre jeu ; **3,6996** sur l'ancien, contre **3,0904**) mais
> **améliore nettement la généralité** : littérature **12,93** contre **16,70**, anglais
> **33,83** contre **57,58**.

## La question

N2.h a laissé une question chiffrée : le corpus propre fait **3,24 Mo** d'entraînement, alors que
le dépôt courant en contient bien plus (recensement du 01/11 : 27,7 Mo avec les transcripts, mais
ceux-ci sont du méta-texte). La question testable sans changer de recette : **le corpus de prose
du dépôt, dédupliqué, est-il plus grand que celui du snapshot ?** Oui — 6,39 Mo bruts pour
docs+journal+rapports, 5,36 Mo uniques. Est-ce que cela fait baisser la PPL honnête ?

## Le dispositif

- **corpus** : `docs/` + `journal/` (hors `sessions/`) + `reports/`, 1 308 documents, 6,39 Mo
  bruts ; dédupliqué par les mêmes shingles de 96 octets (−16,2 %, 2 008 runs), split par chunks
  de 8 Ko → **4 836 314** octets d'entraînement, 262 144 de validation, 262 144 de test ;
  **0 / 3 000** fenêtres de validation dans l'entraînement (vérifié) ;
- **recette identique** à [`n2-propre`](rapport-n2-propre.md) : professeur 23,57 M, base 11,47 M
  (20 000 pas supervisés), distillation 20 000 pas × 16 × 128, lr 1e-4 puis 3e-5, **3 graines** ;
- **évaluation identique** : validation/test du corpus, littérature, anglais, wikitext2, courbe
  129→512, décomposition.

C'est **1,49×** le texte unique de N2.h (3,24 Mo), à genre constant.

## Ce qui est mesuré

| bras | val (corpus) | val (ancien) | test | littérature | anglais | wikitext2 | 256 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **N2.h — 3,24 Mo** | 3,0904 | 3,0904 | 3,1960 | 16,70 | 57,58 | 56,88 | 14,11 |
| **N2.i — 4,84 Mo** | 3,1278 | 3,6996 | 3,2714 | 12,93 | 33,83 | 35,53 | 14,28 |

## Lecture

En domaine, **3,1278** sur son propre jeu et **3,6996** sur l'ancien, contre **3,0904** : l'élargissement ne fait pas mieux sur la prose du snapshot, et le corpus courant contient d'autres registres (rapports, tableaux) qui diluent la prose. Mais sur des textes **identiques** pour les deux modèles : littérature **12,93** contre **16,70** (−22 %), anglais **33,83** contre **57,58** (−40 %), wikitext2 **35,53** contre **56,88** (−38 %), et 256 octets **14,28** contre 14,11.

## Ce que ça change pour N2

Le levier « plus de texte du dépôt » n'est pas un levier de domaine : il **dilue la prose** (3,70 sur l'ancienne validation contre 3,09) parce qu'il ajoute des registres — et il **généralise** (littérature −22 %, anglais −40 %). Pour la porte < 2,5, il faut un corpus **d'un autre ordre** : du français réel en volume, pas les rapports du dépôt. Pour R, en revanche, c'est un gain net : le modèle lit mieux ce qu'il n'a pas écrit.

**La comparaison honnête est hors domaine.** Les deux modèles ne sont pas évalués sur le même
texte — N2.h sur la prose du snapshot, N2.i sur le corpus courant —, donc la colonne « domaine »
du tableau ne se compare pas. Les colonnes **littérature**, **anglais** et **wikitext2** portent le
même texte pour les deux : c'est là que l'élargissement se juge, et c'est là qu'il gagne.

## Ce qui pourrait le rendre faux

- **Le corpus a changé de contenu, pas seulement de taille** : les documents du dépôt courant sont
  des versions réécrites de ceux du snapshot ; une partie de l'écart peut venir du **genre** et de
  la fraîcheur, pas du volume.
- **+49 % de texte unique, pas 10×** : le recensement à 27,7 Mo comptait les transcripts de
  sessions (méta-texte, code, JSON) ; la prose du dépôt ne fait que 5,36 Mo uniques.
- **Le budget est le même** (20 000 pas) : le modèle voit moins de répétitions par octet unique.
- **Trois graines**, une architecture.

## Fichiers

- Code : [`tools/corpus_propre.py`](../tools/corpus_propre.py) ·
  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py).
- Corpus : `data/corpus_repo_propre/`, manifeste [`corpus-repo-propre.json`](corpus-repo-propre.json).
- Points de contrôle : `work/n2i/I-g{1,2,3}.pt`.
