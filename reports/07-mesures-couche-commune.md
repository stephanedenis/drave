> **Fiche de résultats** — ce document est le journal des mesures de la couche commune entrée-sortie
> (168 mesures, 6 erratums, les pièges d'instrument). La **théorie** et l'**état** sont dans
> [`docs/synthese/07-modeles-alternatifs-entree-sortie.md`](../docs/synthese/07-modeles-alternatifs-entree-sortie.md).

# 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune

> **Vocabulaire** : « couche commune » est le **nom historique** de l'**étage entrée-sortie** (voir le
> [glossaire](../docs/glossaire.md)) ; « couche 1 » désigne, lui, une **couche de neurones**. Les deux ne se
> confondent pas.

> **La question.** Peut-on arriver **plus vite** à une couche d'entrée-sortie **commune**, qui fasse
> **abstraction de la langue** — la langue, le dialecte, le style n'étant plus que des **paramètres** ?
> Cette note examine les familles de solutions, avec pour chacune : ce qu'elle gagne, ce qu'elle coûte, et
> **comment on le mesure**.

![Une couche commune, et la langue comme paramètre](../docs/synthese/schemas/couche-commune.svg)


## Les parties — les mesures, de la première à la dernière

Le chapitre fait **5 972 lignes** et **179 sections** : il est découpé en **10 parties**, chacune
atteignable directement. Les 26 documents qui pointent vers ce fichier continuent de fonctionner :
ils arrivent ici, et d'ici on atteint la partie voulue.

| partie | de | à | sections | lignes |
|---|---|---|---:|---:|
| [**1**](07/p1.md) | « ERRATUM MAJEUR (18/10, 0 h 30) : le « noyau neutre » était un **arte… » | « Dixième mesure (17/10, 20 h 30) : un noyau **bilingue** bat un noyau… » | 17 | 607 |
| [**2**](07/p2.md) | « Onzième mesure (17/10, 21 h) : la pensée itérée est **SANS LANGUE** … » | « Trentième mesure (17/10, 19 h 40) : le contenu se réplique aussi — l… » | 18 | 605 |
| [**3**](07/p3.md) | « Trente-et-unième mesure (17/10, 20 h 15) : l'hypothèse « récit contr… » | « Mesure 49 — l'alignement suit la GÉNÉALOGIE des langues… » | 23 | 586 |
| [**4**](07/p4.md) | « Mesure 49b — la généalogie tient **à écriture contrôlée** (et le tes… » | « Mesure 66 — LE 14 B PROLONGE LA COURBE : +3,8 en eng→fra, mais seule… » | 18 | 608 |
| [**5**](07/p5.md) | « Mesure 67 — LA QUALITÉ SE RÉPLIQUE SUR UN SECOND DOCUMENT : +1,1 à +… » | « Mesure 78 — ÉTAGE 2 : LA TAILLE NE CHANGE PRESQUE RIEN À L'ALIGNEMEN… » | 12 | 608 |
| [**6**](07/p6.md) | « Mesure 79 — ÉTAGE 2 : LA COMPOSITION N'EST PAS DÉMONTRÉE — seuls les… » | « Mesure 94 — LA VALIDATION CROISÉE **DÉMENT** LE GAIN : sur les 5 con… » | 16 | 582 |
| [**7**](07/p7.md) | « Mesure 95 — LES 2 832 PAIRES TRANSLATEWIKI AMÉLIORENT L'ÉCRITURE : m… » | « ERRATUM 6 — LA CARTE DES LIGNES DES ÉTATS VERNE : les mesures 82-85,… » | 19 | 580 |
| [**8**](07/p8.md) | « Mesure 113 — LE PAS DE PENSÉE LINÉAIRE **N'EXISTE PAS** : sur la car… » | « Mesure 130 — LE PONT N'EST PAS UNE COUCHE : il marche à **12, 18 et … » | 18 | 603 |
| [**9**](07/p9.md) | « Mesure 131 — LE PONT EST **LANGUE-GÉNÉRAL** (4 LANGUES) : FR/DE donn… » | « Mesure 149 — LE CONTRÔLE DU CONTRASTE : avec des paires **mélangées*… » | 19 | 602 |
| [**10**](07/p10.md) | « Mesure 150 — L'ALIGNEMENT VIENT DU **BILINGUISME**, PAS DU CONTRASTE… » | « Mesure 168 — LE PLAN MULTI-TÂCHES NE L'ALIGNE PAS NON PLUS : EN→FR *… » | 19 | 574 |

## Lire par sujet (le sujet → la partie)

- **La couche commune, les adaptateurs, la neutralité** → les parties [1](07/p1.md), [2](07/p2.md) ;
- **Le corpus, le crible, les fichiers mal étiquetés** → les parties [2](07/p2.md) ;
- **Le cross-lingue, l'alignement, la variation** → les parties [2](07/p2.md), [3](07/p3.md) ;
- **Les audits (numérotation, journal, portes)** → les parties [3](07/p3.md) ;
- **La carte des langues (448 langues, la généalogie, la restitution)** → les parties [3](07/p3.md) ;
- **La qualité, le plancher, les six registres** → les parties [4](07/p4.md), [5](07/p5.md) ;
- **L'étage 2 : la composition et le pas de pensée** → les parties [5](07/p5.md), [6](07/p6.md) ;
- **Le pidgin nigérian** → les parties [6](07/p6.md), [7](07/p7.md) ;
- **Le plan et la carte du raisonnement (mesures 108-173)** → les parties [7](07/p7.md), [8](07/p8.md), [9](07/p9.md), [10](07/p10.md) ;
