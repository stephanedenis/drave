> Campagne : **campagne-benefices** · expérience **29**
> Titre : 29. La mémoire QUI SERT : retrieval → injection, de bout en bout
> Date réelle : **2026-10-10 04:20 HAE** (source : commit `089c52a`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 29. La mémoire QUI SERT : retrieval → injection, de bout en bout

Après la correction du §28 (la greffe d'état transfère bien le contenu), la chaîne
complète devient mesurable : **indexer un document long, le retrouver par le contenu,
et injecter l'état retrouvé dans un calcul qui n'a pas vécu l'épisode**. Nouveau drapeau
`--episodique-extraire F` : il écrit l'état de l'épisode RETROUVÉ, en reconstruisant
l'état vécu (la moyenne est rajoutée si le magasin est décorrélé — sans quoi on
injecterait un état centré, qui n'est celui d'aucun moment).

Protocole : magasin de **1 750 états** de l'invite A (code `ZQ-4471-KX` au jeton 740,
expansion 16 384 + décorrélation + égalisation), indice **extérieur** = l'état final de
l'invite B (le même texte SANS le code), puis injection de l'état retrouvé dans une
invite qui ne contient aucun code.

| étape | mesure |
|---|---|
| rappel | épisode **437**, recouvrement 25/64, **303 jetons** de l'aiguille (hasard 448) |
| état extrait | 896 valeurs, norme **306,31** |
| injection α = 0 | `150px` — aucun effet (témoin) |
| **injection α = 0,2 et 1** | **`The vault access code is`** |
| injection α = 5 | `"150px` (saturé) |

**Ce que la chaîne fait, et ce qu'elle ne fait pas.** Injecter l'état retrouvé fait
**dire au modèle la phrase-cadre de l'aiguille** (« The vault access code is ») alors que
le contexte injecté ne contient ni le code ni cette phrase : l'information a donc bien
voyagé de la mémoire jusqu'à la sortie. Mais **le code lui-même n'est pas produit** — et
la raison est en haut du tableau, pas en bas : l'épisode retrouvé est à **303 jetons** de
l'aiguille, et à cette position le préfixe ne contient pas encore le code.

**Le goulot est donc le RAPPEL, pas la greffe.** La chaîne
`index → retrouver → injecter` fonctionne de bout en bout ; c'est la qualité du rappel
par un indice purement sémantique qui limite (303 jetons contre 448 de hasard, soit
1,5× — faible, et cohérent avec le §24 ter ter qui mesurait 136 et 378 selon la
formulation de l'indice).

**Deux réserves, écrites** : (1) l'état stocké est la sortie **normalisée** du moteur
(norme 306) alors que la greffe injecte un résidu brut (norme 54-66) — l'échelle est
absorbée par la normalisation finale, mais un magasin qui stockerait le résidu brut
serait plus cohérent, et ce n'est pas fait ; (2) un seul indice, un seul texte.
