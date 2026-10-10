> Campagne : **campagne-benefices** · expérience **36**
> Titre : 36. Balayage des portes : le piège de fenêtre était LATENT dans une deuxième porte
> Date réelle : **2026-10-10 07:27 HAE** (source : commit `dee9e58`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 36. Balayage des portes : le piège de fenêtre était LATENT dans une deuxième porte

Le §34 avait montré qu'une porte rouge accusait le modèle alors que c'était la porte :
`--limit` ne veut pas dire la même chose dans les deux chemins (`--ppl` note les `limit`
**premiers** jetons, `--ppl-reparti` **tronque aux `limit` derniers**). La question qui suit
est mécanique : **combien d'autres portes portent le même piège ?**

Balayage des 20 portes (celles qui invoquent `--ppl-reparti`) :

| porte | `--ppl` entier | comparaison à un entier ? | verdict |
|---|---|---|---|
| **porte-reparti-moteur** | oui | **oui, et elle affirme l'égalité** | **corrigée** (§34) |
| **porte-topologie** | oui | **non — elle imprime côte à côte** | **corrigée ici** |
| porte-flux | non | non : elle lit la « référence **locale** » du run réparti | sain par construction |
| 11 autres | non | non : elles comparent réparti à réparti | sains par construction |

**`porte-topologie` avait le piège à l'état latent** : son fichier d'identifiants contient
**255** jetons et sa limite en annonçait **128**, donc la perplexité de référence (premiers
128 jetons) et celle du découpage (derniers 128) **portaient sur deux passages différents**
— affichées l'une sous l'autre, comme si elles se comparaient. La porte ne l'affirmait pas,
donc elle passait ; mais elle **invitait à une comparaison fausse**, ce qui est exactement le
genre de piège que ce dépôt refuse.

Après correction (le nombre de jetons est compté) : **référence 5,3719 · découpage 5,3719**,
écart de flux **0,00e0** — les deux nombres affichés parlent enfin du même texte.

**La règle, écrite une fois pour toutes** : dans une porte, `--limit` doit valoir **le nombre
de jetons du fichier** (compté, pas écrit à la main) dès qu'un chemin réparti intervient. Les
deux portes qui le faisaient à la main s'étaient trompées toutes les deux.
