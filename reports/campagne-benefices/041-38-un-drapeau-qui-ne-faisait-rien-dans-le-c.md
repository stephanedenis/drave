> Campagne : **campagne-benefices** · expérience **38**
> Titre : 38. Un drapeau qui ne faisait RIEN dans le chemin réparti (`--ffn-gain`)
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 38. Un drapeau qui ne faisait RIEN dans le chemin réparti (`--ffn-gain`)

En cherchant à mesurer l'interaction du gain d'entrée (§37) avec le **découpage**, la mesure
a rendu **exactement le même chiffre avec et sans le drapeau** (42,5477 dans les deux cas).
Ce n'était pas une absence d'effet : c'était une absence de **câblage**.

`--ffn-gain` était appliqué dans `run_infer` et dans `run_ppl`, et **pas** dans
`run_ppl_reparti` : dans le chemin réparti — celui sur lequel porte tout ce sprint — le
réglage ne faisait **rien, en silence**. C'est la famille de défauts que ce dépôt traque
(« un drapeau qui ne fait rien »), et celui-ci comptait double : un réglage fin qui ne survit
pas à la distribution est exactement ce qu'on ne veut pas découvrir en production.

**Corrigé** (le même câblage que les deux autres chemins), et mesuré :

| chemin | sans réglage | avec `0:0.75` |
|---|---|---|
| réparti (2 nœuds, 12/12 couches) | **180,5245** | **222,3496** — le drapeau **agit** |

Le signe de l'effet en réparti (222 > 180, sur 32 jetons) n'est pas celui du chemin local
(−11,5 % sur 128 jetons) : la fenêtre de 32 jetons est trop courte pour conclure quoi que ce
soit sur la qualité, et **cette comparaison-là n'est pas une mesure de qualité** — c'est un
contrôle de CÂBLAGE. La porte le traite comme tel : elle exige que les deux chiffres
**diffèrent**, pas qu'ils s'améliorent.

**Et le piège de fenêtre a mordu une troisième fois** dans cette même tentative : `--ppl` avec
`--limit 128` note les **128 premiers** jetons d'un fichier qui en compte 85 625, tandis que
`--ppl-reparti` **tronque aux 128 derniers**. Une comparaison entre les deux chemins doit donc
toujours porter sur un fichier dont la longueur **est** la limite — ou sur la « référence
locale » du même run. C'est écrit dans trois portes maintenant, et c'est écrit ici.

**La porte** : `tools/porte-gain.sh`, cas 8 (le drapeau doit agir en réparti), 8 cas verts.
