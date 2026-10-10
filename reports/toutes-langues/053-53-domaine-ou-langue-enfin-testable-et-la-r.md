> Campagne : **toutes-langues** · expérience **53**
> Titre : 53. Domaine ou langue ? Enfin testable, et la réponse est « à égalité »
> Date réelle : **2026-10-06 18:13 HAE** (source : commit `75cc1b7`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 53. Domaine ou langue ? Enfin testable, et la réponse est « à égalité »

### 53.1 Pourquoi il fallait un autre corpus

L'hypothèse — « certains mots et groupes de mots sont spécifiques à leur domaine ; ils
sont plus communs à leur domaine qu'à leur langue » — était **intestable sur l'UDHR** :
c'est **un seul texte** traduit en 392 langues, donc ses « contenus différents » (les
dix unités) restent le même texte juridique. Le §25 l'avait signalé sans pouvoir aller
plus loin.

Le corpus Wikipedia apparié (§45) lève l'obstacle : **61 articles distincts**
(science, histoire, géographie, personnes…) traduits dans **six** langues latines.

Deux similarités, mesurées sur les mêmes représentations :
- `S_langue` — **même article, langues différentes** : 915 paires ;
- `S_domaine` — **même langue, articles différents** : 10 980 paires.

### 53.2 Le résultat

| couche | S_langue | S_domaine | écart | verdict |
|---:|---:|---:|---:|---|
| **0** | 0,0489 | 0,0535 | **−0,0046** | **LANGUE domine** |
| **8** | **0,2158** | 0,2131 | **+0,0026** | **CONTENU domine** — de justesse |

**À la couche 0 — l'entrée du professeur — la LANGUE domine.** Deux articles différents
dans la même langue se ressemblent plus que le même article dans deux langues.

**À la couche 8, l'ordre s'inverse, mais de 0,0026 seulement** — soit 1,2 % en relatif.
C'est **une égalité à l'épaisseur du trait**, pas une domination.

### 53.3 Ce que cela dit de l'hypothèse, et du §25

**L'hypothèse est très faiblement soutenue à la couche 8, et réfutée à la couche 0.**
Autrement dit : le fait que deux textes parlent du même sujet ne les rapproche
quasiment pas plus, dans la représentation, que le fait d'être écrits dans la même
langue.

**Et cela disqualifie le chiffre de l'UDHR.** Le §25 rapportait `S_langue` 0,6132 contre
`S_domaine` 0,8578, soit **+0,19** en faveur du contenu. Sur un corpus réellement
multi-domaine, le même écart tombe à **+0,0026** — **70 fois moins**. L'écart de l'UDHR
ne mesurait pas le domaine : il mesurait que les dix « contenus différents » de l'UDHR
sont **le même texte**.

C'est la deuxième fois de la session qu'un corpus mono-contenu donne un chiffre qui ne
veut pas dire ce qu'il semble dire — après la constante témoin du §27.

### 53.4 Réserve

61 articles, six langues **apparentées** (toutes latines). Le résultat vaut pour ce
voisinage. Entre familles éloignées, `S_langue` baisserait probablement, ce qui
donnerait plus de poids au contenu — mais ce n'est pas mesuré, et l'appariement par
titre est stérile en écriture non latine (§45.2).

### 53.5 Une erreur de ma part dans la chaîne, corrigée

La construction des caches a d'abord produit **six caches à zéro langue**, sans
planter. Cause : j'intersectais les **noms de fichiers** (`de_A` contre `en_A`) au lieu
des **slugs** (`A`) — une intersection vide **par construction**. Corrigé, et la
construction rapporte maintenant les 71 articles communs aux six langues.

Leçon : un cache vide ne lève aucune erreur ; il faut que l'outil **dise combien** il a
trouvé, ce que celui-ci fait (« 0 langues · 0 pas »).


---
