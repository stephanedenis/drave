> Campagne : **campagne-benefices** · expérience **24**
> Titre : 24. Mémoire épisodique (C6) : ce qui marche, et ce qui ne marche PAS
> Date réelle : **2026-10-09 22:30 HAE** (source : commit `7d7837e`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 24. Mémoire épisodique (C6) : ce qui marche, et ce qui ne marche PAS

Ajouté après la campagne, dans le sprint « cerveau ». Le module `episodique.rs`
(clé creuse k-WTA + index inversé) est mesuré sur des **états réels** du
Qwen2.5-0.5B-Q8, 300 états d'un même texte, clé de **64 canaux sur 896** (7,14 %).
Toutes les valeurs ci-dessous sont reproduites par `tools/porte-episodique.sh`.

**Ce qui marche, et c'est exact au bit près :**

- **round-trip 300/300** — relire avec sa propre clé rend l'état écrit, au bit près,
  y compris après passage par le disque (300/300 lectures identiques) ;
- **rappel** : 100 % à 0 % et 10 % de dégradation de l'indice, **96,7 % à 25 %**,
  **69,3 % à 50 %**, **15,3 % à 75 %** (N = 300 ; hasard = 0,33 %) ;
- **nouveauté** : un indice jamais écrit obtient un recouvrement moyen de
  **41,5/64** contre **64,0/64** pour un épisode connu — le magasin sait donc
  distinguer « je me souviens » de « ça ressemble »… **en moyenne**, car le pire des
  indices nouveaux atteint **57/64** : il existe des faux positifs.

**Ce qui ne marche PAS, et c'est le résultat le plus utile :**

- **l'index inversé n'élague RIEN.** Sur les 300 états, chaque lecture examine
  **300 candidats sur 300 (100 % du magasin)**, soit 19 200 comparaisons de canaux.
  La raison est mesurable : les états de langue naturelle sont **corrélés** — deux
  états différents partagent en moyenne **23,9 canaux sur 64** (37 %), donc toute
  clé d'indice recouvre presque tout le magasin. Le « plus proche voisin
  approximatif » prévu au plan n'a donc rien à approximer ici : c'est un balayage
  complet déguisé. La conséquence pratique est que le coût d'une lecture est
  **N × k comparaisons d'entiers** (0,3 M pour N = 10⁴) — acceptable — mais que la
  **mémoire** du magasin est N × dim × 4 octets (3,6 Go pour 10⁶ épisodes à 896
  canaux) : c'est la mémoire qui limite, pas le temps de lecture ;
- **à petit k, l'invariant de round-trip CASSE.** k = 8 : **81 des 300 états
  partagent la clé d'un autre** (pire multiplicité 7) et le round-trip tombe à
  **219/300**, tous les échecs expliqués par ces collisions. k = 16 : 288/300 ;
  k = 32 : 299/300 ; k = 64 : 300/300. Autrement dit : **l'invariant du plan n'est
  pas une propriété du code, c'est une propriété du couple (données, k)**, et la
  porte le vérifie au lieu de le supposer.

**Deux hypothèses testées, deux réfutations utiles** (mesures directes) :

| variante | séparation | élagage | rappel 50 % | rappel 75 % |
|---|---|---|---|---|
| référence (300 états consécutifs) | 23,9/64 | **100 % du magasin** | 69,3 % | 15,3 % |
| états **espacés** d'un jeton sur 8 (150 états, 1 200 jetons) | **24,0/64** | **100 %** | 87,3 % | 22,0 % |
| **décorrélé** (moyenne des états retirée) | **20,3/64** | **100 %** | 78,3 % | 22,0 % |

- **L'espacement ne change RIEN au recouvrement** (24,03 contre 23,88) : la
  corrélation des clés n'est donc **pas** un effet de voisinage de texte. C'était
  l'hypothèse naturelle, et elle est fausse — les états d'un modèle partagent une
  composante commune qui ne dépend pas de la distance entre les jetons ;
- **la décorrélation aide la qualité** (séparation 23,9 → 20,3, nouveauté 41,5 →
  37,5, rappel à 50 % 69,3 → **78,3 %**) **mais ne fait toujours éluder aucun
  candidat** : 100 % du magasin reste examiné. La raison est arithmétique et se
  calcule : 300 épisodes × 64 canaux = 19 200 entrées réparties sur 896 canaux
  (≈ 21 par canal), donc une clé d'indice touche 64 × 21 ≈ 1 340 entrées qui
  couvrent **tous** les épisodes. **Avec 64 canaux sur 896, l'index inversé ne peut
  pas éluder** — ce n'est pas un défaut du code, c'est un défaut de densité.

**Ce que cela indiquait pour la suite** : pour que l'index élude réellement, il faut
**plus de canaux et des clés plus creuses** — une **expansion** comme celle du gyrus
denté. L'expérience a été faite, et elle a demandé **trois** ingrédients, pas un.

### 24 bis. L'expansion du gyrus denté, et ce qu'elle exige en plus

L'expansion seule (896 → 4 096, 8 entrées signées par canal, hachage déterministe)
**améliore la séparation mais n'élague presque pas** :

| configuration (300 états) | séparation | candidats examinés | rappel 50 % | rappel 75 % |
|---|---|---|---|---|
| 896 canaux, k = 64 (référence) | 23,9/64 | **300/300 (0 % éludé)** | 69,3 % | 15,3 % |
| 4 096, k = 32 | 6,5/32 | 256/300 (15 %) | 36,3 % | 3,7 % |
| 8 192, k = 64 | 13,0/64 | 282/300 (6 %) | 33,7 % | 7,0 % |
| 16 384, k = 64 | **9,0/64** | 267/300 (11 %) | 48,7 % | 10,3 % |
| **16 384, k = 64, canaux ÉGALISÉS** | **0,38/64** | **51/300 (83 % éludé)** | **96,3 %** | **69,0 %** |

La cause de l'échec de l'expansion seule est **visible dans la distribution des
listes de l'index** : quelques canaux sont systématiquement grands (la projection les
rend sensibles à une direction commune), ils entrent dans presque toutes les clés, et
leur liste devient un « hub » — 7× la longueur moyenne. Toute clé d'indice tombe sur
eux, et l'index redevient un balayage complet. **Centrer et réduire chaque canal de
clé sur le magasin** (une égalisation d'usage, ce que le gyrus denté obtient par
normalisation et inhibition latérale) fait tomber la séparation à **0,38/64** — le
plancher théorique du hasard pour 64 canaux sur 16 384 étant 0,25 — et l'élagage
passe à **83 %**.

**Ce que la mémoire gagne, et ce qu'elle paie** (16 384 canaux, k = 64, N = 300) :

- comparaisons par lecture : **3 237** au lieu de 19 200 — **÷5,9** ;
- rappel à 25 % de dégradation : **100 %** (contre 96,7 %) ; à 50 % : **96,3 %**
  (69,3) ; à 75 % : **69,0 %** (15,3) ;
- nouveauté : un indice jamais écrit tombe à **16,2/64** (contre 41,5) — le pire des
  nouveaux passe de 57/64 à **40/64**, donc les faux positifs reculent sans disparaître ;
- round-trip : **300/300 au bit près**, y compris à travers le disque. Le magasin
  stocke les **états exacts** (896 canaux) ; seule la **clé** est dilatée — sinon le
  magasin coûterait 18× plus cher et ne pourrait plus rendre l'état d'origine.

**Le coût de l'expansion est FIXE, celui du balayage croît** : 131 072 additions par
lecture contre N × 64 comparaisons. Le seuil de rentabilité se calcule —
**N ≈ 2 048 épisodes** — et **en dessous, le balayage complet est moins cher**. Une
expansion n'est donc pas « meilleure » : elle est meilleure *à partir d'une certaine
taille de mémoire*, et le chiffre est écrit dans la sortie du programme pour que
personne ne l'oublie.

### 24 ter. Le résultat tient-il sur PLUSIEURS documents ? Oui — 240 états, 3 corpus

Les mesures ci-dessus portaient sur un seul texte, et c'était une condition à lever :
un magasin qui ne marche que sur un document n'est pas une mémoire, c'est un index.
Les 240 états viennent donc de **trois corpus différents** (code, français,
multilingue), chacun repartant d'un **cache neuf** — donc sans contexte partagé entre
documents.

| mesure | un texte (300 états) | **trois corpus (240 états)** |
|---|---|---|
| round-trip | 300/300 | **240/240 au bit près** |
| séparation | 0,38/64 | **1,22/64** (hasard : 0,25) |
| candidats examinés (dernier N) | 17 % du magasin | **15 %** (35 sur 240) |
| rappel 25 % / 50 % / 75 % | 100 / 96,3 / 69,0 % | **99,2 / 95,0 / 73,8 %** |
| nouveauté (jamais écrit / pire) | 16,2 / 40 | **10,6 / 38** |
| ligne de base nulle | 0,33 % | 0,42 % |

Le résultat **ne dépend donc pas d'un texte unique** : il tient sur des corpus
différents, avec des états qui ne partagent plus le contexte du document.

### 24 ter bis. À QUELLE DISTANCE la mémoire se trompe-t-elle ? (utile, et mesuré)

Savoir si la mémoire rend l'épisode **exact** est une chose ; savoir à quelle
**distance** elle se trompe en est une autre, et c'est celle qui décide de l'usage :
un épisode voisin de deux jetons situe un passage, un épisode à cinq cents jetons ne
situe rien. Les épisodes sont numérotés dans l'ordre du texte, donc la distance entre
identifiants **est** une distance en jetons. Deux documents mesurés (clés de 64 canaux
sur 16 384, expansion + égalisation) :

| configuration | rappel 25 % | rappel 50 % | rappel 75 % | Δ à 50 % | Δ à 75 % | candidats examinés |
|---|---|---|---|---|---|---|
| 300 états, sans expansion (64/896) | 96,7 % | 69,3 % | 15,3 % | 26 jetons | 71 | 100 % |
| 300 états, expansion + égalisation | 100 % | 96,3 % | 69,0 % | **2 jetons** | 24 | 17 % |
| **2 048 états**, expansion + égalisation | 99,9 % | **95,4 %** | 64,5 % | **11 jetons** | 86 | 19 % |

L'expansion et l'égalisation n'améliorent donc pas seulement le rappel et l'élagage :
elles rendent la mémoire **treize fois plus précise** en localisation (Δ 26 → 2 jetons
à 50 % de dégradation, à N = 300).

**La précision RELATIVE s'améliore avec la taille du document** : 2 jetons sur 300
valent 0,67 % du texte, 11 jetons sur 2 048 en valent **0,54 %**. Autrement dit :
quand la mémoire se trompe, **elle se trompe de près** — le voisinage du bon moment
reste retrouvé. C'est exactement la propriété qui rend une mémoire de contenu utile
pour situer un passage : elle n'a pas besoin d'être exacte pour être utilisable, et
elle le dit en jetons.

Sur ce même magasin de **2 048 épisodes** : round-trip **2 048/2 048 au bit près**,
séparation 0,37/64, élagage **81 %** (382 candidats sur 2 048), et un indice jamais
écrit tombe à 8,8/64 contre 64/64 pour un connu. La consolidation par rejeu y donne,
en mode **exemplaire**, 62,5 % du magasin pour 93,4 % de rappel (seuil 16) et 87,8 %
pour 99,1 % (seuil 32) — la conclusion du §24 quater tient donc à l'échelle.

### 24 ter ter. Un indice ÉTRANGER retrouve-t-il le bon passage ? Oui, grossièrement

Toutes les mesures précédentes interrogent la mémoire avec un indice **issu de
l'épisode cherché** (une version dégradée de sa propre clé) : c'est de la complétion de
motif, et elle réussit. La question qui décide de l'usage est autre : **un indice qui ne
ressemble pas au contenu cherché le retrouve-t-il ?** Mesure sur l'invite A du §28
(1 750 jetons, code planté au jeton **740**) :

| indice | épisode rendu | recouvrement | distance à l'aiguille | hasard |
|---|---|---|---|---|
| l'état de la question, **pris dans le magasin** | 1749 (lui-même) | 64/64 | 1 009 jetons | 448 |
| l'état de la question, **EXTÉRIEUR** (la même question posée dans un contexte qui n'a PAS l'aiguille) | 604 | **4/64** | **136 jetons** | 448 |

Le premier cas ne testait rien : l'indice était dans le magasin, il s'y retrouvait
lui-même (recouvrement 64/64) et sa distance de 1 009 jetons ne dit rien — c'est
pourquoi `--episodique-indice` accepte un état **extérieur**, qui n'est pas dans le
magasin.

Avec un indice extérieur qui ne partage que **4 canaux sur 64**, la mémoire rend un
épisode à **136 jetons** de l'information — **3,3× mieux que le hasard** (448).

**Et cette marge n'est PAS robuste — corrigé après une deuxième mesure.** En écrivant la
porte de ce résultat, la question a été écrite avec un **point d'interrogation** de plus
(« Answer with the code only? » au lieu de « … only. ») : le même protocole donne alors
un épisode à **378 jetons** de l'aiguille, toujours sous le hasard (448) mais **2,8 fois
plus loin**. Un état de question change donc beaucoup pour un caractère de différence.

| indice extérieur (contexte sans l'aiguille) | rendu | recouvrement | distance à l'aiguille | hasard |
|---|---|---|---|---|
| question terminée par « only. » | 604 | 4/64 | **136** | 448 |
| question terminée par « only? » | 362 | 3/64 | **378** | 448 |

**Conclusion honnête, et elle remplace la première** : le rappel par le contenu
**n'est pas sémantique** (il ne trouve pas l'aiguille depuis la seule question), et
l'effet de voisinage qu'on croyait tenir **dépend de la formulation exacte de l'indice**.
Ce qui reste solide, c'est le reste : l'écho (un indice pris dans le magasin s'y
retrouve lui-même, 64/64), la complétion de motif depuis une clé dégradée (§24 ter), et
la localisation en jetons quand l'indice VIENT du contenu cherché.

**Conditions** : deux indices extérieurs seulement, un seul texte, position de l'aiguille
plantée par construction. La mesure suivante — plusieurs questions, plusieurs textes, et
la **moyenne** des distances plutôt qu'un cas — n'est pas faite.

### 24 quater. Consolider par rejeu : garder un CAS bat résumer par une MOYENNE

C7, au sens du plan, veut rejouer des épisodes pour modifier des **poids**. Ce n'est
pas ce qui est mesuré ici, et il faut dire pourquoi : le moteur n'entraîne pas, et
les règles locales qu'il possède déjà (hebbien différentiel) ont été mesurées
**dégradantes** sur la perplexité (`docs/hebbien-differentiel-et-biologie.md` :
8,8246 avec la règle contre 8,3869 sans). Rejouer pour ajouter du bruit n'est pas
consolider. Ce qui se mesure ici est la consolidation **de la mémoire** : rejouer les
épisodes et **fusionner ceux dont les clés co-activent** — deux souvenirs que le même
indice rappelle n'en sont qu'un.

La fusion demande une décision, et les deux réponses possibles ne se valent pas.
300 états, clés de 64 canaux sur 16 384 (expansion + égalisation) :

| seuil (canaux partagés) | **MOYENNE** : prototypes · compression · rappel | **EXEMPLAIRE** : prototypes · compression · rappel |
|---|---|---|
| 1 | 39 · 13,0 % · **22,3 %** | 21 · **7,0 %** · **87,0 %** |
| 2 | 116 · 38,7 % · 13,3 % | 57 · 19,0 % · **87,3 %** |
| 4 | 176 · 58,7 % · 18,7 % | 107 · 35,7 % · **93,0 %** |
| 8 | 200 · 66,7 % · 34,0 % | 154 · 51,3 % · **95,3 %** |
| 16 | 234 · 78,0 % · 56,0 % | 203 · 67,7 % · **97,3 %** |
| 32 | 274 · 91,3 % · 82,7 % | 269 · 89,7 % · **98,7 %** |

Le « rappel » est le rappel d'**appartenance** : la lecture doit rendre le prototype
qui *contient* l'épisode interrogé.

**Le résultat, et son mécanisme.** L'exemplaire (garder le premier cas absorbé, clé
comprise) **compresse plus ET rappelle mieux** que la moyenne, à tous les seuils. La
raison est mécanique et se vérifie dans le tableau : la clé d'une **moyenne** est
recalculée depuis un point qui n'a jamais existé, donc elle ne coïncide avec la clé
d'**aucun** membre — un indice venu d'un membre ne retrouve plus son prototype
(22,3 % à seuil 1, et **13,3 %** à seuil 2, pire qu'à seuil 1 : la moyenne s'éloigne
quand elle agrège). L'exemplaire, lui, garde la clé d'un cas réel : 7 % du magasin
suffit à 87 % de rappel, et 51 % du magasin à 95,3 %.

Autrement dit : **abstraire par moyennage détruit la rappelabilité**, et ce n'est pas
une opinion sur la mémoire, c'est une propriété de la clé. Cela reproduit, avec un
mécanisme mesuré, le débat classique entre théorie du prototype et théorie des
exemplaires — et tranche dans le sens des exemplaires *pour cette forme de mémoire*.

**Et le rejeu RÉPÉTÉ est un POINT FIXE, pas une usure** — la question laissée
ouverte au-dessus, maintenant mesurée (mode exemplaire, seuil 4, 300 états) :

| cycle | prototypes | compression | rappel (vs épisodes d'origine) | erreur |
|---|---|---|---|---|
| 1 | 107 | 35,7 % | 93,0 % | 4,37e-1 |
| 2 | 107 | 35,7 % | 93,0 % | **0,00e0** |
| 3 à 8 | 107 | 35,7 % | 93,0 % | **0,00e0** |

Rien ne bouge à partir du deuxième cycle, et l'erreur est **exactement nulle** : après
une consolidation, chaque prototype est son propre exemplaire, et deux prototypes ne
partagent plus assez de canaux pour être fusionnés. Le rappel est mesuré contre les
épisodes **d'origine** (les appartenances sont composées à travers les cycles), et il
reste à 93,0 % — donc **rejouer une mémoire ne l'use pas**, contrairement à ce que le
rejeu fait aux poids quand la règle est mauvaise (voir plus haut : 8,8246 contre
8,3869). La stabilité est une propriété de la règle de fusion, et elle est exacte.

**Ce qui reste non mesuré, et c'est écrit** : si la fusion améliore ou dégrade le
**rappel depuis un indice bruité** (ici l'indice est toujours non dégradé), et la
reconstruction de l'état d'origine à partir d'une clé dilatée.

**Conditions** : Qwen2.5-0.5B-Q8, expansion par hachage (8 entrées signées par canal),
égalisation calculée **sur le magasin** (en déploiement il faut donc la stocker avec
lui, et la recalculer quand il grandit).

**Conditions de ces chiffres** : 300 états d'un seul texte (ou un sur huit), un seul
modèle (0,5 B), k = 64. Le rappel après consolidation, sur des épisodes venus de
**textes différents** (plusieurs documents), ou avec un indice dégradé de façon
**corrélée** plutôt qu'aléatoire, **n'est pas mesuré ici**.
