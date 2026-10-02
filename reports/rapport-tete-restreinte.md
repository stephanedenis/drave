# Rapport — restreindre la tête de sortie : ce qui marche, ce qui ne marche pas

Session du 01/10 au 02/10. Question posée : peut-on calculer moins de logits que
tout le vocabulaire **sans jamais changer la sortie** — « charger dynamiquement
les logits manquants ou faire du JIT », à défaut d'y être explicitement
contraint ?

**Réponse : non, pas avec une garantie exacte.** Trois voies ont été explorées,
implémentées et mesurées. Une seule survit, et elle change la sortie — ce qui la
qualifie comme *génération contrainte*, pas comme optimisation.

## Ce qui est mesuré d'abord : le vocabulaire utile

| jetons lus (français) | identifiants distincts | % du vocabulaire |
|---|---|---|
| 10 000 | 1 462 | 0,96 % |
| 100 000 | 4 659 | 3,07 % |
| 1 000 000 | 15 768 | 10,38 % |
| 3 050 991 | **19 793** | **13,03 %** |

Exposant de Heaps ≈ **0,21** : atteindre 50 % du vocabulaire demanderait des
milliards de jetons. **13 % est un plafond de fait.**

Et le rang du vrai token, seule mesure comparable entre deux vocabulaires :

| | |
|---|---|
| médian | **3** |
| p90 | 250 |
| maximum | 4 319 |

Un vocabulaire de 16 384 tokens contient donc **100 %** des vrais jetons d'un
corpus français.

## Voie 1 — restriction simple : elle marche, mais elle change la sortie

`--tete-restreinte <liste>` : ne calculer que les lignes de la liste.

| liste | couverture | sans | avec | gain |
|---|---|---|---|---|
| français | 13,0 % | 9,384 s | 8,400 s | **+10,5 %** |
| anglais | 5,8 % | 1,155 s | 0,982 s | **+15 %** |

Trois tours alternés chaque fois, stable. Et l'équivalence du refactor est
**parfaite** : avec la liste complète, la sortie est identique au token près.

**Mais la sortie change dès que la liste est partielle** — y compris avec la
« bonne » langue :

| liste | sortie |
|---|---|
| complète | `[6224, 1076, 330, 438, …]` — identique à sans ✅ |
| française | `[1129, 269, 330, 304, …]` puis **boucle** |
| anglaise | `[77455, 330, 315, 279, …]` — différent |

Les tokens hors liste sont à zéro, donc le modèle ne peut plus les choisir — et
il en aurait eu besoin. **Ce n'est pas une optimisation transparente.**

## Voie 2 — borne de Cauchy-Schwarz : exacte, et inutilisable

L'idée : `logit_o = W_o · h ≤ ‖W_o‖ · ‖h‖`. Si le maximum trouvé sur la liste
dépasse cette borne pour tout le reste, l'argmax global **est** dans la liste.
C'est une preuve, pas une heuristique.

Implémentée sur les deux chemins de calcul (tête 4 bits et `q8_view`), avec :

- précalcul de `‖W_o‖` pour chaque ligne (608 Ko pour 151 936 tokens) ;
- le reste trié par norme décroissante : il suffit de tester sa **tête** ;
- sortie **identique au token près** à une tête complète — vérifié.

**Elle ne conclut jamais.** La borne vaut `logit / cos(W_o, h)` : en haute
dimension, le cosinus typique est de 0,05 à 0,2, donc la borne est **5 à 20 fois**
le logit réel. La boucle descendait tout le vocabulaire **ligne par ligne** — bien
plus lentement que la passe parallèle complète. Mesuré : la génération ne
terminait pas là où la tête entière prend 6,9 ms.

*(Découverte au passage : `--infer` passe par `logits`, pas `logits_lot`. Le
premier patch visait la mauvaise fonction et mesurait « aucun gain » — c'est en
cherchant pourquoi que je l'ai trouvé. Et la branche bornée manquait entièrement
dans le chemin `q8_view`, celui des modèles sans tête 4 bits : `--tete-bornee` y
était **silencieusement ignoré**.)*

## Voie 3 — sparsité de l'entrée : exacte, et destructrice

Dernière voie exacte : si l'entrée de la tête est creuse, un stockage **par
colonnes** ne lirait que les colonnes vivantes. Aucune approximation, aucun
calcul de logits manquants.

Densité mesurée, et le prix en perplexité :

| seuil d'activation | densité de l'entrée | perplexité | écart |
|---|---|---|---|
| 0 | 85,4 % | **19,3885** | référence |
| 0,01 | 61,5 % | 22,3563 | +15 % |
| 0,02 | 30,3 % | 28,7635 | +48 % |
| 0,05 | **5,1 %** | **2 073,80** | **×107** |

**La sparsité n'existe qu'au prix d'un seuil qui détruit le modèle.** Lire 5 % de
la matrice multiplie la perplexité par 107 ; lire 30 % la majore de moitié. Le
compromis est mauvais dans toute la plage.

## Conclusion

| voie | exactitude | gain | verdict |
|---|---|---|---|
| restriction simple | **change la sortie** | +10 à +15 % | génération contrainte assumée |
| borne de Cauchy-Schwarz | exacte | **négatif** (plus lent) | retirée |
| sparsité par seuil | exacte pour l'entrée quantifiée | ×107 de perplexité | inutilisable |

**On ne peut pas garantir l'argmax en lisant moins que tout**, sur cette
architecture. Le seul usage légitime de `--tete-restreinte` est celui où l'on
**veut** contraindre la sortie : sortie dans une langue imposée, énumération
fermée, décodage contraint.

`--tete-bornee` a été **retirée du code** après mesure : elle ralentit sans rien
garantir de plus. La leçon reste, écrite dans `model.rs` à l'endroit où elle
vivait.

## Ce que ça laisse ouvert

Le seul moyen de rendre la restriction transparente serait de **prédire** quels
tokens hors liste pourraient gagner — donc une borne apprise, statistique, pas une
preuve. Les mesures de rang disent que c'est possible en pratique (le vrai token
est presque toujours dans les 4 000 premiers), mais ce serait une garantie
probabiliste, et il faudrait la mesurer comme telle.
