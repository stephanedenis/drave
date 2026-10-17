# 6. Comment savoir qu'on a raison — la méthode, et ses pièges

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

*Une nuit de recherche ne vaut pas par ce qu'elle affirme : elle vaut par ce qu'elle refuse d'affirmer.*
