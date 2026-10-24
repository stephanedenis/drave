# 6. Comment savoir qu'on a raison — la méthode, et ses pièges

> **Périmètre** : ce chapitre relève du programme **méthode** ; la vision est dans [`docs/vision.md`](../vision.md), la roadmap dans [`docs/roadmap.md`](../roadmap.md).

## Le problème

Un dépôt de recherche produit beaucoup de chiffres. Le danger n'est pas de se tromper : c'est de **croire**
un chiffre qui ne mesure rien. Cette nuit, **cinq fois**, une mesure s'est déguisée en résultat.

## Les cinq pièges, et le signe qui les trahit

| le piège | ce qui se passe | le signe |
|---|---|---|
| **la position avec elle-même** | on aligne l'état sur l'entrée de sa propre position | écart **0,0 %** — trop beau |
| **le ridge sous-déterminé** | moins de positions que de coefficients | écart **0,0 %** encore, et la contre-épreuve aussi |
| **le plan de textes hors corpus** | les fenêtres sortent du fichier | « n = 149 » sur 24 textes demandés |
| **les couches ignorées** | la boucle du modèle est bornée par sa config | trois mesures **identiques au chiffre près** |
| **le λ fixé** | les chiffres dépendent des réglages | 104,3 à longueur 64, **87,0** à 128 |

**La règle qui sauve les cinq** : *écrire à côté du chiffre ce qui pourrait le rendre faux.* Pas après —
**à côté**, dans la même fiche, avant de conclure.

## Les instruments qui en sont nés

* **`tools/banc_lecteur.py`** : un λ de ridge par **validation croisée**, et une **batterie de longueurs**.
  Il transforme un chiffre en **mesure** — le classement des modèles devient stable, et l'écart entre deux
  modèles tombe de 14 points (artefact) à 1-2 (réel).
* **`tools/toutes-les-portes.sh`** : la passe complète écrit un **registre** avec les codes de sortie.
* **la porte de fraîcheur** : `docs/en-cours.md` doit dater du dernier commit — un cycle qui commite sans
  mettre la page à jour **échoue**.

## Ce que la méthode a produit cette nuit

Sur **douze** mesures, **trois** ont été corrigées après coup, **deux** étaient des artefacts de réglages,
et **sept** tiennent. C'est un **bon** bilan — pas parce que sept sur douze, mais parce que les cinq autres
ont été **trouvées** avant d'être publiées.

## Les leçons des 168 mesures

Huit leçons ont émergé, chacune payée par une erreur trouvée à temps :

| leçon | l'erreur qui l'a payée | la règle |
|---|---|---|
| **le juge doit être post-cutoff** | l'UDHR récitée (mesure 61) | un texte neuf, jamais vu à l'entraînement |
| **le plancher est obligatoire** | des « marges » sans plancher | la marge = traduction − source, jamais le chrF seul |
| **une référence minée gonfle** | WikiMatrix +41 / +46 contre +33-36 humain | vérifier que la référence est une **traduction**, pas un parallèle miné |
| **le domaine avant le volume** | XNLI : 13 394 paires hors domaine = 1 992 du dev (mesure 164) | mesurer le domaine, pas la taille du train |
| **les contrôles négatifs** | le pont qui « marchait » sans contrôle | paires mélangées, étiquettes mélangées, à chaque fois |
| **les petits tests mentent** | 88 items, h2/h3 « dans le bruit » | IC, et ≥ 200-300 items pour un effet de 0,05-0,10 |
| **la carte des lignes** | l'erratum 6 : 40 mesures sur une fausse carte | assertir l'invariant à la source |
| **le point de mesure** | la « décroissance » du 3 B — la couche 18, puis la profondeur 50 % — **deux fois le même jour** | comparer les modèles **à leur pic** (ou donner les deux bornes) : chaque modèle a sa couche, et elle est **tardive** |

*Ce qui vaut n'est pas le chiffre : c'est la chaîne qui le rend falsifiable.*

*Une nuit de recherche ne vaut pas par ce qu'elle affirme : elle vaut par ce qu'elle refuse d'affirmer.*
