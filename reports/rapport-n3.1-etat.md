# N3.1 — l’état des opérations natives : une porte composée serait prématurée

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ⛔ **pas de porte composée
> aujourd’hui** — deux briques n’ont ni service ni porte (`k-WTA/routes`, profondeur routée), et
> une méta-porte qui lance les portes existantes ne testerait **pas** leur composition.
>
> **Dispositif** : inventaire statique des gates et des chemins de service ; aucun nouveau run ;
> données [`n3.1-etat.json`](n3.1-etat.json).

## L’inventaire

| brique | porte | service |
|---|---|---|
| sortie précoce | `porte-reflexe.sh` | **non** — bench `--reflexe-essai` |
| rejeu | `porte-trace.sh` | oui |
| placement | `porte-topologie.sh` | oui |
| pont | `porte-pont.sh` | oui |
| coupe | `porte-coupe.sh` | oui |
| profondeur routée | **aucune** | rapport design-H, pas de porte |
| k-WTA / routes | **aucune** | **aucun chemin** |

## Ce que ça décide

N3 reste **partielle**. Une porte composée honnête demanderait que chaque brique **s’exécute dans
le moteur** puis que la composition soit mesurée (temps, perte, rejeu) ; lancer cinq portes
séparées n’est pas une composition, c’est `toutes-les-portes`.

Les prochains pas, nommés :

1. **N3.2** — porter la sortie précoce dans le chemin de service (pas seulement le bench) ;
2. **N3.3** — donner une porte à `k-WTA / routes` (ou nommer le chemin absent) ;
3. **N3.4** — une porte pour la profondeur routée (design-H) ;
4. alors seulement, une **porte de composition** N3.

## Ce qui pourrait le rendre faux

- **Inventaire statique** : un chemin de service peut exister sans être nommé dans une porte.
- **Pas de run N3** : la variabilité ±10 % n’est pas mesurée ici.
- **La composition n’est pas testée** : c’est précisément la décision.

## Fichiers

- `reports/n3.1-etat.json` — l’inventaire.
- `reports/rapport-n3.1-etat.md` — cette fiche.
