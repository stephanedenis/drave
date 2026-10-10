> Campagne : **campagne-benefices** · expérience **35**
> Titre : 35. Découverte : le registre des régions (C11)
> Date réelle : **2026-10-10 07:25 HAE** (source : commit `b1b63b0`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 35. Découverte : le registre des régions (C11)

Une topologie qui écrit `"instance": "127.0.0.1:50001"` décrit **un** déploiement ; la même
topologie sur trois machines en demanderait trois. Le plan (§3.2, ligne « découverte »)
prévoit un registre statique puis dynamique : voici le statique, `--registre FICHIER`, dont
chaque ligne donne `region hote:port`.

**Ce qui est résolu, et ce qui ne l'est pas** : une instance qui contient déjà un `:` est une
adresse et n'est **pas** touchée — les topologies existantes continuent de marcher au
caractère près. Sinon elle est cherchée dans le registre, et une région **absente est
refusée en la nommant** : un repli silencieux sur `localhost` ferait parler le moteur à la
mauvaise machine. La résolution se fait des deux côtés (pilote et nœud relais).

`tools/porte-registre.sh`, 3 cas, verts :

| cas | mesure |
|---|---|
| topologie **nommée** + registre | perplexité **113,0068**, code 0 |
| même topologie, **adresse en dur** | perplexité **113,0068** — **identique** |
| région **absente** du registre | refus en la nommant, **code 2**, rien n'est calculé |

**Un défaut trouvé en écrivant la porte** : le contrôle de cohérence (« la région distante
est sur X mais `--ppl-reparti` dit Y ») comparait l'adresse à l'instance **brute** — une
topologie qui *nomme* ses régions était donc refusée comme contradictoire (code 3), alors
que les deux sources disaient la même chose. **La résolution doit précéder le contrôle**,
et c'est maintenant écrit dans le code à cet endroit.
