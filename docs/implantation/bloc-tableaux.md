# Le bloc tableaux — une grille, des colonnes, des opérations exactes

> **Ce que ce document est.** La spécification de **R4.1** : ce qu'un tableau devient quand
> on le lit, ce que ses cellules déclarent, quelles opérations sont permises et quels refus
> sont nommés. Le code est `tools/bloc_tableaux.py` ; la porte est
> [`porte-bloc-tableaux.sh`](../../tools/porte-bloc-tableaux.sh) ; les chiffres vivent dans
> [`rapport-r41-bloc-tableaux.md`](../../reports/rapport-r41-bloc-tableaux.md).
>
> **Chargement** : lire § 2 et § 5 pour coder contre le bloc ; § 7 pour les limites.
>
> **Ce que ce bloc n'est pas** : un lecteur de tableaux PDF non balisés. R0.1 les laisse en
> texte, et R4.1 ne les invente pas — c'est R4.4 (vision) qui les prendra.

## 1. Le besoin

R0.1 range un tableau en **région** et en garde le texte **aplati** : chaque rangée devient
une chaîne tabulée. C'est assez pour retrouver une ligne, pas pour la lire. Un tableau n'est
pas du texte plat : sans les colonnes, on ne peut ni comparer, ni filtrer, ni agréger, ni
joindre. Et le banc R0.3 ne le voit pas : sur les 59 questions de son type « tableau », 27
ont une rangée aplatie pour gold et **20 de ces 27** attendent le numéro de l'étiquette
(`B11` → « 11 »). Le premier nombre de la rangée est le nom du chantier, pas une donnée.

Un tableau doit donc devenir une **grille** — et la grille doit **prouver** qu'elle est
fidèle : chaque cellule pointe la tranche de source dont elle vient.

## 2. Le contrat

| élément | contenu |
|---|---|
| **entrée** | un fichier Markdown, HTML ou CSV (ou une grille construite à la main) |
| **sortie** | une `Grille` : en-têtes (ou `None`), lignes de `Cellule`, fusions, légende, provenance |
| **coût** | linéaire en cellules — **×3,8** de temps pour ×4 de cellules |
| **trace** | chaque cellule porte `ligne`, `debut`, `fin`, `octet` (Markdown) ou `bloc` (HTML/CSV) |
| **rejeu** | aucun horodatage, aucun aléa : l'empreinte SHA-256 de la grille est stable |

Une `Cellule` porte **deux textes** : `brut` (la tranche exacte de la source) et `texte`
(le visible, après `inline` — le gras, les liens et le code disparaissent comme dans le
graphe R0.1). Une case couverte par une fusion a `texte = ""`, `fusion = True` et
`origine = (ligne, colonne)` ; `Grille.resolue()` rend la cellule d'origine. **La valeur
d'une fusion n'est comptée qu'une fois.**

## 3. Les formats et les en-têtes

| format | en-tête | provenance | refus nommés |
|---|---|---|---|
| **Markdown** | la rangée suivie du séparateur (tirets et deux-points) ; sans séparateur → `sans_entete` | ligne, indice de caractère, offset octet | une colonne, en-tête vide, séparateur incohérent, rangée irrégulière |
| **HTML** | `thead`/`th` ; plusieurs rangées → jointes par « / » | `sourceline` + rangée + bloc | en-tête fusionné, largeur incohérente, tableau imbriqué, fidélité |
| **CSV** | première ligne, **déclarée** (`entetes=True`), pas devinée | numéro de ligne et de colonne | rangée irrégulière, aller-retour `writer`/`reader` |

**On ne devine pas une en-tête.** Une première rangée en `<td>` n'est pas une en-tête
(`entites.html` le montre) : la grille est marquée `sans_entete=True` et l'opération qui
exige un nom de colonne lève `SansEntete`. Une en-tête **fusionnée** (`rowspan`/`colspan`)
est refusée : la jointure par colonne inventerait une hiérarchie que le document ne dit pas.

**Le Markdown sait aussi** lire un tableau dans une citation (`> | … |`) et un tableau
indenté dans une liste ; les indices de caractère restent ceux de la ligne d'origine.

## 4. Le typage

`type_de(texte)` rend `vide`, `entier`, `reel` ou `texte`. Les nombres sont lus en français :
`1 234` = 1234, `12,5` = 12.5, `−3` = −3, `12 %` = 12. Deux séparateurs décimaux (`1.234,5`)
sont **ambigus** → texte. `12–13` est du texte.

**Une colonne non numérique n'est pas sommée** : `agregat` lève `NonNumerique` avec la ligne
fautive. Sauter les cellules qui dérangent est la façon la plus sûre de rendre un agrégat
faux sans le dire.

## 5. Les opérations

| opération | signature | résultat |
|---|---|---|
| **filtre** | `filtre(grille, colonne, valeur)` | les rangées dont la cellule vaut `valeur` (égalité numérique si les deux sont des nombres) |
| **agrégat** | `agregat(grille, colonne, operation)` | `somme`, `moyenne`, `min`, `max`, `compte` sur une colonne numérique |
| **jointure** | `jointure(gauche, col_g, droite, col_d)` | jointure **interne** sur l'égalité des clés ; les colonnes sont préfixées `g.` et `d.` |

Elles sont classiques par construction : aucun modèle, aucun entraînement, aucune
approximation. Le résultat est exact, ou il est refusé.

## 6. La porte

```
bash tools/porte-bloc-tableaux.sh
```

Elle exige, ensemble : **≥ 100 cellules** sur le corpus et **100 %** de provenance exacte ;
au moins 5 tableaux avec en-tête ; les opérations justes sur fixtures ; le **texte plat qui
échoue 3/3** ; les refus nommés (irrégulier, en-tête fusionnée, tableau imbriqué, sans
en-tête, colonne de texte) ; le coût linéaire ; le rejeu identique. Une seule condition
manquante rend la porte rouge.

## 6 bis. La restitution (miroir)

La grille se **rend** en Markdown ou en CSV, puis se **relit** : 34/34 tableaux gardent
en-têtes, dimensions et textes de cellules. Les fusions ne sont pas représentables dans ces
formats et sont comptées à part — le miroir ne prétend pas les restituer. Le contrôle
négatif est le **texte plat** : rendu tel quel, il ne redonne aucun tableau.

Porte : [`porte-miroir-blocs.sh`](../../tools/porte-miroir-blocs.sh).

## 7. Ce que le bloc ne fait pas

- **pas de PDF non balisé** : un tableau PDF reste du texte (R0.1) ; le bloc ne l'invente pas
  (R4.4) ;
- **pas d'en-tête fusionnée** : `colspan`/`rowspan` dans l'en-tête → refus nommé, pas de
  hiérarchie devinée ;
- **pas de position à l'écran** : la grille dit la ligne et la colonne, pas le `x`/`y` ;
- **pas de sémantique** : un en-tête est un texte, pas un type métier ;
- **pas de correction** : une cellule fausse dans la source reste fausse dans la grille.

## 8. Voir aussi

- [R4.1 — le bloc tableaux](../pilotage/backlog/R41-bloc-tableaux.md) — la fiche de fonctionnalité.
- [Le graphe de document](document-graph.md) — les régions et leur provenance (R0.1).
- [Le banc de lecture rapide](banc-lecture.md) — ce que le banc mesure, et son type « tableau ».
- [La lecture rapide](../theorie/lecture-rapide.md) — pourquoi la structure est le premier levier.
