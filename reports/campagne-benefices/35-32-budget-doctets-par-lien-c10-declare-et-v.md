> Campagne : **campagne-benefices** · expérience **32**
> Titre : 32. Budget d'octets par lien (C10) : déclaré, et vérifié sur ce qui PASSE
> Date réelle : **2026-10-10 05:48 HAE** (source : commit `203872a`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 32. Budget d'octets par lien (C10) : déclaré, et vérifié sur ce qui PASSE

Le plan demande des **budgets par lien** (`{paires/s, octets/s, ms}`) vérifiés au
démarrage. La mesure a imposé une correction au plan : **la taille d'un flux n'est pas une
propriété du mode**, elle dépend de l'ACTIVITÉ réelle — 1 951 octets par pas en listes par
blocs à 97,7 % d'activité, **1 096 à 50 %** (§31). Un contrôle au démarrage ne pourrait
donc comparer qu'à une valeur nominale inventée.

Le budget est donc déclaré dans la topologie (`"budget_octets": N` sur un lien) et
**comparé à ce qui passe**, au pas où il passe :

| cas | mesure |
|---|---|
| aucun budget (défaut) | perplexité **111,9225**, 1 951 octets par pas, code 0 |
| budget **généreux** (2 451) | perplexité **111,9225** — identique, code 0 |
| budget **insuffisant** (975) | le premier flux fait **1 860 octets** ⇒ arrêt **au pas 0**, message nommant le lien, les octets, le budget et le pas, **code 6**, et **aucune perplexité rendue** |

**Ce que la porte verrouille** (`tools/porte-budget.sh`, 3 cas) : un budget généreux ne
change rien ; un budget insuffisant arrête l'exécution **en le disant** ; et surtout
**aucun résultat partiel n'est rendu** — une perplexité calculée sur un transport qui n'est
pas celui qui a été déclaré aurait l'air d'un résultat. C'est la même règle que C4 (borne
de pas atteinte) et que le pont (C9) : *s'arrêter et le dire*, jamais rendre un chiffre qui
mentirait sur ses conditions.

**Suite — le budget de LATENCE, troisième volet du plan** (`{paires/s, octets/s, ms}`).
Déclaré par `"budget_ms": N` sur un lien, il se compare à l'**allé-retour mesuré** de chaque
pas. Mesuré (mêmes conditions que ci-dessus) :

| cas | mesure |
|---|---|
| latence **généreuse** (100 000 ms) | perplexité **111,9225** — identique, code 0 |
| latence **insuffisante** (1 ms) | `LATENCE DÉPASSÉE … : **20,1 ms pour un budget de 1 ms, au pas 0**` · **code 8** · aucune perplexité |

Quatre codes d'arrêt distincts désormais : **5** = borne de pas (C4) · **6** = budget
d'octets (C10) · **7** = panne de lien (C11) · **8** = budget de latence (C10). Un script
peut donc nommer la cause sans lire les messages.

**Un défaut de porte attrapé au passage** : la porte écrasait la variable `D` (le chemin du
binaire) avec la sortie du pilote, et le cas suivant échouait sur un code **127**
(« command not found ») — l'échec ne disait rien de ce qu'on mesurait.

**Détail mesuré au passage** : le PREMIER flux est plus gros que la moyenne (1 860 contre
1 951 en moyenne par pas sur 47 pas, mais le premier contient l'état le plus dense) — un
budget déclaré juste sous la moyenne arrête donc dès le premier pas, ce qui est le
comportement voulu et le plus sûr.
