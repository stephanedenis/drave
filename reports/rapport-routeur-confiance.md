# B24 — le round-trip M1 améliore la typo, mais coûte les espaces

> **Objet.** B23 routait par appartenance au lexique et laissait la typo à **56,2 %** contre
> **68,3 %** pour M2. B24 ajoute un **score de confiance M1** : le code lu doit se **rendre** puis
> se **relire** à l'identique. Sinon, on bascule sur M2.

## Résultats (146 items `de`, 3 graines)

| mode | M1 | M2 | **B23** | **B24** | oracle |
|---|---:|---:|---:|---:|---:|
| original | **100 %** | 93,15 % | 100 % | **100 %** | 100 % |
| casse | **99,32 %** | 93,15 % | 99,32 % | **99,32 %** | 100 % |
| espaces | 11,64 % | 34,25 % | **41,78 %** | **34,25 %** | 39,04 % |
| typo | 44,52 % | **69,18 %** | 56,16 % | **63,70 %** | 79,45 % |
| phrase | **92,47 %** | 0 % | 92,47 % | **92,47 %** | 92,47 % |

## Lecture

- **B24 gagne +7,5 pts sur la typo** par rapport à B23 (56,2 → 63,7), mais reste **sous M2**
  (69,2) et **perd 7,5 pts sur les espaces** (41,8 → 34,2).
- Le round-trip M1 **détecte 31 %** des typos (part M2) ; les 69 % restants sont des typos qui
  **reviennent à un code cohérent** — le codec se relit lui-même, même faux.
- L'**oracle** M1/M2 plafonne à **79,45 %** sur la typo : même un routeur parfait ne récupère pas
  tout, car M2 plafonne à 69,2.
- **Aucun score ne domine** : B24 est meilleur sur la typo, B23 sur les espaces.

## Verdict

**B24 est un gain partiel** : +7,5 pts sur la typo, −7,5 sur les espaces. Le **round-trip** est un
signal utile mais insuffisant ; il faudrait une **marge de code** ou un **modèle de confiance**
entraîné, pas une simple cohérence du codec.

## Limites

- **Une graine**, 146 items, pas d'intervalle de confiance.
- Le round-trip dépend du **contexte** ; une surface valide peut se relire faux.
- Le routeur reste un **outil de secours** ; M2 n'est pas un étage (B14).
- B24 ne teste pas les **phrases** avec un autre codec.

## Fichiers

- Code : [`tools/cerveau/routeur_confiance.py`](../tools/cerveau/routeur_confiance.py).
- Test : [`tools/cerveau/tests/test_routeur_confiance.py`](../tools/cerveau/tests/test_routeur_confiance.py).
- JSON : [`routeur-confiance.json`](routeur-confiance.json).
