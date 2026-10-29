# R4.1 — le bloc tableaux : 996 cellules, 802 exactes à leur place, le texte plat rate 3/3

> **Ligne de roadmap** : R4.1 · **Date** : 2026-10-29 · **Verdict** : ✅ **la grille est
> mesurée** — 35 tableaux, **996 cellules**, **802 cellules Markdown** (en-têtes compris)
> rendues **exactement** à la tranche de source qu'elles déclarent ; **8/8** opérations
> justes ; **3/3** contrôles « texte plat » qui **échouent**, et **4 refus nommés**
> (irrégulier, en-tête fusionnée, tableau imbriqué, colonne de texte non sommable).
> ⚠️ **ce n'est pas un gain sur le banc** : R0.3 sélectionne déjà la bonne rangée ; ce que
> R4.1 ajoute est la **colonne**, donc les opérations — que le banc ne demande jamais.
>
> **Dispositif** : CPU seul, aucun modèle chargé ; 9 fichiers, 3 formats (Markdown, HTML,
> CSV) ; fixtures à réponse connue ; JSON brut
> [`r41-bloc-tableaux.json`](r41-bloc-tableaux.json) ; spec
> [`bloc-tableaux.md`](../docs/implantation/bloc-tableaux.md) ; porte
> [`porte-bloc-tableaux.sh`](../tools/porte-bloc-tableaux.sh).

## La question

R0.1 range les tableaux en régions et en garde le **texte aplati** : chaque rangée devient
une chaîne tabulée. R0.2 et R0.3 lisent donc des rangées, pas des colonnes. Peut-on lire un
tableau **comme une grille** — en-têtes, cellules, fusions — et répondre à des questions de
structure sans modèle ?

## Le corpus et le dispositif

| format | fichiers | tableaux | cellules du corps | en-têtes détectés |
|---|---:|---:|---:|---:|
| Markdown | 7 | 32 | 686 (+116 en-têtes) | **32/32** |
| HTML | 2 | 2 | 10 | 1/2 |
| CSV (Glottolog) | 1 | 1 | 300 (20 lignes × 15) | 1/1 |
| **total** | **9** | **35** | **996** | **34/35** |

Les tableaux Markdown viennent du dépôt, dont deux cas que le graphe ne couvrait pas : un
tableau **dans une citation** (`plan-deepseek41-complet.md`) et un tableau **indenté dans une
liste** (`colab-reparti.md`). Le seul tableau sans en-tête est `entites.html` : sa première
rangée est en `<td>`, on la **signale** au lieu de la deviner.

**La provenance** est le contrôle central : chaque cellule Markdown déclare sa ligne, son
indice de caractère, sa longueur et l'offset octet de la ligne ; la porte **recalcule la
tranche** dans le fichier. **802/802** cellules tombent exactement, et le texte visible est
bien `inline(tranche)`. Aucune cellule inventée, aucune perdue.

## Les opérations

Trois opérations classiques, à réponse connue (`tests/tableaux/`) :

| opération | attendu | rendu |
|---|---:|---:|
| somme d'une colonne | 120 | **120** |
| moyenne d'une colonne | 3,0 | **3,0** |
| min / max | 10 / 50 | **10 / 50** |
| filtre texte (`état = rouge`) | 2 | **2** |
| filtre numérique (`coût = 40`) | 1 | **1** |
| jointure `notes × élèves` | 3 | **3** |
| en-tête à deux niveaux | `Région / Zone · Mois / Janvier · Mois / Février` | **identique** |

**Le typage refuse au lieu de sauter** : une cellule `rouge` ou `—` dans une colonne
sommée lève `NonNumerique` avec la ligne fautive. Sauter les cellules qui dérangent est la
façon la plus sûre de rendre un agrégat faux sans le dire.

## Les contrôles négatifs

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **texte plat** (rangées tabulées) | donner une réponse fausse | ✅ **3/3 faux** |
| **tableau irrégulier** (rangée courte) | être refusé, pas complété | ✅ `Refus` nommé |
| **en-tête fusionnée** (`colspan`) | ne pas inventer la hiérarchie | ✅ `Refus` nommé |
| **tableau imbriqué** | ne pas aplatir en silence | ✅ `Refus` nommé |
| **sans en-tête** | être signalé, et l'opération refusée | ✅ `sans_entete=True`, `SansEntete` |
| **colonne de texte** dans un agrégat | être refusée | ✅ `NonNumerique` |

Le détail des trois questions plates — c'est là que le contrôle est honnête :

| question | grille | texte plat |
|---|---:|---|
| somme de la colonne `coût` | **120** | **146** = 132 (tous les nombres) + 14 (les étiquettes `A2`, `B4`, `C1`, `D7` : 2+4+1+7) |
| cellule (ligne 2, `durée`) | **3** | la rangée entière (`B4 40 3 rouge —`) |
| lignes où `état = rouge` | **2** | **3** (la colonne `note` porte aussi « rouge ») |

**Ce que ce contrôle prouve, et ce qu'il ne prouve pas** : il prouve que la **colonne** porte
l'information, pas que tout lecteur plat échoue. Un lecteur plat plus malin (position, regex)
récupérerait une partie — mais ce serait déjà de la structure.

## Ce qui pourrait le rendre faux

- **Les fixtures sont les miennes.** Les trois contrôles sont construits pour que le plat
  échoue ; c'est une démonstration, pas un taux sur corpus aléatoire.
- **Le corpus est facile.** Les tableaux Markdown du dépôt sont réguliers, sans fusions
  (impossible en Markdown), et il n'y a **aucun tableau PDF non balisé** : R0.1 les laisse en
  texte, R4.1 ne les invente pas. Les 996 cellules ne sont pas un échantillon aléatoire.
- **L'en-tête fusionné est refusé à 100 %** : les tableaux multi-niveaux à `colspan` sont
  fréquents dans les rapports ; le taux d'échec sur ce format n'est mesuré que sur **une**
  fixture. C'est un refus assumé, pas une couverture.
- **Les nombres sont lus en français** : `1 234` = 1234, `12,5` = 12.5, `12 %` = 12 ;
  `1.234` est lu **1,234** (ambigu : milliers ou décimales), et `12–13` est du **texte**.
- **La provenance HTML est à la ligne**, pas au caractère ; le CSV n'a pas d'offset de
  caractère (son contrôle est l'aller-retour `writer`/`reader`, 20/20 lignes).
- **Le coût** est celui du **parsing** (25,0 ms pour 1 000 cellules, entrées-sorties
  comprises ; ×3,8–4,1 selon la passe — ×3,80 dans le JSON — donc linéaire) ; le coût des opérations n'est pas
  mesuré séparément.

## Ce que ça change pour R0.3 — et ce que ça ne change pas

Le banc R0.3 a un type **« tableau »** (59 questions sur 249). Sur ces 59, **27** ont une
région `tableau` pour gold, et **20 de ces 27** attendent comme réponse le **numéro de
l'étiquette de ligne** : `B11` → « 11 », `R0.4` → « 0.4 », `R2.1` → « 2.1 ». Le gabarit
prend le premier nombre de la rangée aplatie ; l'étiquette de chantier est ce nombre.

Conséquence : le **0,932** du type tableau dit « la bonne rangée a été sélectionnée », pas
« un tableau a été lu ». R4.1 **ne relève pas** ce chiffre — il n'y a rien à relever, la
sélection est déjà à 1,000. Ce que R4.1 ajoute est une **autre mesure** : la cellule exacte,
l'en-tête, l'opération. C'est cette mesure qui manquait au dépôt, et c'est elle que R4.2
(code) et R4.3 (maths) pourront reprendre.

## Reproduire

```bash
bash tools/porte-bloc-tableaux.sh
python3 tools/bloc_tableaux.py --mesure reports/r41-bloc-tableaux.json
python3 tools/bloc_tableaux.py --json docs/pilotage/roadmap.md
```

## Ce qui vient

**R4.2 — le bloc code** : AST, portée, exécution exacte, contrôle « lecture du texte seul ».
**R4.3 — le bloc maths** : LaTeX, CAS, contrôle « surface ». **R4.4 — vision/OCR** seulement
après R4.1–R4.3. **R0.4 — les trois têtes** reste la suite de la ligne lecteur.
