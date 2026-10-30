# A8.0 — audit final : 19/33, les 14 restantes classées

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-30 · **Verdict** : ✅ **audit clos** — **19
> portes PPL épinglées**, **14 restantes classées** : 3 comparatifs intra-run non épinglés,
> 2 rouges qualifiées, 1 verte sans PPL, 8 sans PPL. Aucune porte mesurable n’est laissée dans
> un flou non nommé.
>
> **Dispositif** : inventaire statique des 33 portes, recoupé avec les 19 fiches de pin ; données
> [`a80-audit-final.json`](a80-audit-final.json).

## Les 19 épinglées

`adaptateur-sortie`, `budget`, `bus-socket`, `bus`, `c4-retard`, `consolidation`, `coupe`,
`cycle-c2`, `delais`, `flux`, `fusion`, `gain`, `pannes`, `pont`, `profondeur-routee`, `reflexe`,
`reparti-moteur`, `topologie`, `trace`.

## Les 14 restantes

| catégorie | portes | raison |
|---|---|---|
| comparatif intra-run, non épinglé | `horloge`, `poids-creux`, `registre` | compare deux bras, pas une valeur externe |
| verte sans PPL | `homeostasie` | mesure des normes, pas une perplexité |
| rouge qualifiée | `indice`, `melange` | calibration/indice extérieur, refus explicite |
| sans PPL | `diff-couche`, `echange-experts`, `harnais-invariants`, `jumeaux`, `mistral`, `occupation-moteur`, `prechargement`, `push-paresseux` | aucune PPL à épingler |

## Le contrôle négatif

- **Les 3 comparatifs** ne prouvent pas une valeur absolue : une régression commune aux deux bras
  passerait ; c’est pourquoi ils ne sont pas comptés comme pins.
- **Les 2 rouges** échouent explicitement (calibration, indice extérieur) ; elles ne sont pas
  converties en vert.
- **Les 8 sans PPL** ne peuvent pas être épinglées sans changer ce qu’elles mesurent.
- **Le compte** 19 + 3 + 1 + 2 + 8 = 33.

## Ce qui pourrait le rendre faux

- **Audit statique** : une porte peut avoir une référence cachée hors motif.
- **Les 3 comparatifs** pourraient recevoir une référence externe plus tard ; ce serait un
  nouveau pin, pas un oubli.
- **Les rouges** peuvent être corrigées, pas épinglées.
- **La PPL n’est pas la qualité** : 19 pins protègent une valeur, pas un jugement.

## Ce que ça change

A8.0 est **close dans son périmètre mesurable** : 19 pins, 3 comparatifs nommés, 2 rouges
qualifiées, 8 sans PPL. A8.3 reste opt-in ; la condition duale pour les 19 pins n’est pas remplie.

## Fichiers

- `reports/a80-audit-final.json` — l’inventaire.
- `reports/rapport-a80-audit-final.md` — cette fiche.
