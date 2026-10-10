> Campagne : **campagne-benefices** · expérience **27**
> Titre : 27. OÙ COUPER le modèle ? Le point de coupe est neutre — sauf à cause du lien
> Date réelle : **2026-10-09 23:48 HAE** (source : commit `22d6151`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 27. OÙ COUPER le modèle ? Le point de coupe est neutre — sauf à cause du lien

Le découpage en régions (C1) et le pont (C9) avaient chacun été mesurés à **un seul
endroit** : 12 couches locales, 12 distantes. Rien ne disait que 12/12 soit le bon
endroit. Mesure sur Qwen2.5-0.5B-Q8 (24 couches), 48 jetons, huit points de coupe.

**1. Avec un lien SANS PERTE (dense f32), le point de coupe ne change RIEN :**

| coupe locale/distante | 4/20 | 6/18 | 8/16 | 10/14 | 12/12 | 15/9 | 18/6 | 20/4 |
|---|---|---|---|---|---|---|---|---|
| perplexité | 113,0068 | 113,0068 | 113,0068 | 113,0068 | 113,0068 | 113,0068 | 113,0068 | 113,0068 |

Huit valeurs identiques à la quatrième décimale : c'est l'invariant de C1, vérifié
sur huit coupes et non sur une seule. Le découpage est une affaire de **répartition du
calcul**, pas de résultat.

**2. Avec un lien ENCODÉ (listes par blocs), le même découpage s'écarte de 8,9 % :**

| coupe | 4/20 | 6/18 | 12/12 | 18/6 |
|---|---|---|---|---|
| perplexité | 116,3407 | **108,8721** | 111,9225 | **118,5275** |

Ce n'est donc pas le découpage qui change le résultat, c'est **l'erreur de
quantification du lien**, et elle dépend de l'état échangé — donc de la profondeur à
laquelle on coupe. À noter que trois coupes sur quatre font **mieux** que le lien sans
perte (108,87 et 111,92 contre 113,01) : la quantification du lien agit ici comme une
perturbation, pas seulement comme une perte.

**3. Le coût d'un pont de 448 fibres dépend aussi du point de coupe — et fortement :**

| coupe | 12/12 | 15/9 | 18/6 |
|---|---|---|---|
| coût du pont (448 fibres sur 896) | +2,81 % | **+17,09 %** | **+0,52 %** |

**Il y a donc un bon endroit pour couper, et ce n'est pas le milieu** : couper après
18 couches (6 distantes) rend le pont presque gratuit (+0,52 %), couper après 15 le
rend très cher (+17,09 %) — trente fois plus. Interprétation : l'état échangé à la
couche 18 est **redondant** (on peut en jeter la moitié), celui de la couche 15 ne
l'est pas. C'est cohérent avec la mesure de C8 : la direction de l'état se construi
tardivement (cos 0,145 avec l'état final à 16 couches, 0,320 à 20).

**Conséquence pratique pour distribuer** : couper **tard** si le lien est étroit, et
vérifier le coût du pont *au point de coupe choisi* — il varie d'un facteur 30 sur le
même modèle. La référence de perplexité d'un découpage encodé n'est pas celle du
modèle entier : elle doit être mesurée pour chaque coupe.

**Conditions** : un seul modèle (0,5 B, 24 couches), 48 jetons, encodage « listes par
blocs », pont symétrique (le même `--pont-k` des deux côtés). Les huit coupes sont
testées en dense f32, quatre en encodé ; les points intermédiaires (13, 14, 16, 17) ne
sont pas mesurés.
