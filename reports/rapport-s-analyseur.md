# S — L'analyseur contre les structures écrites à la main : 7/7 séquences, 93,9 % de couverture

> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur les **7 phrases** du banc,
> l'analyseur heuristique retrouve la **séquence de types 7/7** et couvre **93,9 %** des octets des
> structures écrites à la main (94–97 % par phrase, sauf une à 42 % avant correction). Le reste
> est l'**espace de tête** des segments (convention du banc) et trois cas corrigés en chemin.

## Le dispositif

- Structures de référence : les **7 phrases** du banc (`donnees/phrases.json`), une structure
  écrite à la main chacune (la première lecture).
- Analyseur : [`tools/structures/generateur.py`](../tools/structures/generateur.py) — lexique de
  mots grammaticaux, frontières de proposition, rôles par préposition.
- Mesure : la **séquence de types** (GN, GV, GP, REL, SUB) et la **couverture** des octets de la
  référence par les segments générés **du même type**.

## Ce qui est mesuré

| phrase | types | couverture | segments (réf / gén) |
|---|---|---:|---|
| p001 — « Le chat de la voisine qui dort… » | **OK** | 94 % | 4 / 4 |
| p002 — « J'ai vu l'homme avec le télescope. » | **OK** | 94 % | 3 / 3 |
| p003 — « La femme a vu l'homme dans le parc. » | **OK** | 91 % | 4 / 4 |
| p004 — « Il a couru pour attraper le bus. » | **OK** | 97 % | 2 / 2 |
| p005 — « Il a parlé à Marie de son projet. » | **OK** | 94 % | 3 / 3 |
| p006 — « Elle a dit qu'elle viendrait hier. » | **OK** | 94 % | 3 / 3 |
| p007 — « Le canard est prêt à manger. » | **OK** | 93 % | 3 / 3 |
| **global** | **7/7** | **93,9 %** | — |

## Les trois corrections de la nuit

1. **L'adverbe de temps** : la relative s'arrête avant « hier » (« qu'elle viendrait » / « hier ») —
   p006 passe de 30 % à 42 %, puis à 94 % avec la correction suivante.
2. **Le « que » élidé** : « qu'elle » est reconnu comme complément après un verbe (SUB) et non
   comme relative — la séquence de types de p006 devient juste.
3. **La coordination** : « et », « ou », « mais » ouvrent une nouvelle proposition au lieu d'une
   subordonnée — « Il court et il rit. » donne deux GV.

## Ce que ça dit

L'analyseur est **bon sur la segmentation** (7/7 séquences, 94 % de couverture) et **faible sur les
frontières exactes** (l'espace de tête, les limites de mots) : pour le banc, c'est la structure qui
compte, pas l'octet exact. Les corrections sont des **règles** (adverbe, élision, coordination),
pas des apprentissages — et elles se mesurent.

## Ce qui pourrait le rendre faux

- **Sept phrases** seulement, avec une seule structure de référence chacune : la mesure dit la
  cohérence interne, pas la généralité.
- **La couverture** est calculée par type : un segment généré du bon type mais décalé compte à
  moitié — c'est volontaire (la frontière compte).
- **Le corpus de test** est le banc lui-même (écrit à la main après l'analyseur) : il y a un risque
  d'ajustement au banc.

## Fichiers

- Sous-projet : commit **`3b68143`** (fusion pragmatique + export + analyseur), **19 tests**.
- Mesure : `work/n2w/analyse.py` ; banc : `tools/structures/donnees/phrases.json`.
