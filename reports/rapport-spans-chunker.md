# Chunker seul et les 94 spans REL/SUB/GP — 0 exact, deux règles en récupèrent 84 sans perdre un span déjà bon

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Territoire** : **L** (bloc
> linguistique, chunker) · **Date** : 2026-11-05 · **Verdict** : sur les **94** cibles du gold
> sans segment prédit au bon span (**48 REL, 33 SUB, 13 GP**), le chunker seul
> (`Heuristique(segmenter_s=False)`) en couvre **0 exactement** — et c'est structurel : le mode
> par défaut est l'union du générateur S et du chunker, donc un span exact du chunker serait déjà
> bon. Deux règles simulées sur une copie locale en récupèrent **84/94** (47 REL, 32 SUB, 5 GP),
> soit **229/239** cibles au bon span, **sans perdre aucun** des 77 spans déjà exacts du chunker
> seul ni des 145 du mode par défaut. Le prix est mesuré : +9 faux positifs pour (a), −201 pour
> (b), −207 pour (a)+(b).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (lecture seule),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`),
> [`generateur.py`](../tools/structures/generateur.py) (lecture seule) ; copie locale
> `/tmp/spans/bloc_linguistique_copie.py`, règles dans `/tmp/spans/regles.py` ; **aucun fichier
> du dépôt modifié**. JSON : [`pensee-spans-chunker.json`](pensee-spans-chunker.json).

## 1. La question

Le mode par défaut (`Heuristique()`, générateur S **et** chunker) laisse **94** des **239**
cibles du gold sans segment prédit au bon span. Combien de ces 94 le **chunker seul**
(`_syntagmes_simple`, sans S) peut-il couvrir exactement ? Quels marqueurs sont en tête ? Quelles
causes ? Et deux règles implémentables dans le chunker — (a) marqueur de tête + frontière, (b)
« un prédicat par clause » — combien en couvriraient, pour quel risque sur les spans déjà bons ?

## 2. Le dispositif

- **Gold** : `charger()` = 612 phrases (20 `hand`, 432 `reel`, 160 `synthetique`) ; **239**
  segments porteurs d'une cible (REL 74, SUB 69, GP 96), dont **94** sans segment prédit au bon
  span dans le mode par défaut : **48 REL, 33 SUB, 13 GP**.
- **Chunker seul** : `Heuristique(segmenter_s=False)`, c'est-à-dire `_syntagmes_simple` : GN, GP,
  GV, REL, et **aucune branche SUB**.
- **Copie locale** : `tools/bloc_linguistique.py` copié dans `/tmp/spans/`, jamais modifié dans
  le dépôt ; les deux règles sont des sous-classes qui remplacent `_syntagmes_simple`. La
  simulation est donc **hors du code de production** : rien n'est committé, aucun fichier
  existant n'est touché.
- **Mesures** : exactitude au span (`type`, `debut`, `fin`), P/R/F1 sur **tous** les segments du
  gold, et attachement (`evaluer_bloc`) en mesure secondaire.

## 3. Le chunker seul : 0/94, 77/239

| mesure | valeur |
|---|---:|
| cibles du gold | 239 |
| spans exacts, mode par défaut | 145 |
| spans perdus (mode par défaut) | **94** (REL 48, SUB 33, GP 13) |
| spans exacts, chunker seul | **77** (77 GP, 0 REL, 0 SUB) |
| **spans exacts du chunker seul sur les 94** | **0** (0 REL, 0 SUB, 0 GP) |

Les 77 exacts du chunker seul sont **tous des GP** ; sur les 239 cibles, il ne produit **aucun**
REL ni SUB au bon span. Ses 18 REL ne tombent jamais juste : 8 recouvrent un REL du gold, 10 n'ont
aucun répondant. Sur les 94, le résultat **0** n'est pas un plafond caché : le mode
par défaut contient déjà le chunker par union, donc un span exact du chunker seul serait déjà
compté bon. Pour gagner, le chunker doit produire des spans **neufs** — un type SUB, des bornes
REL — pas retrouver les mêmes.

### Les marqueurs en tête des 94

| type | marqueurs (nombre) | reconnus par le chunker | hors lexique / hors branche |
|---|---|---|---:|
| **REL** (48) | qui 17, that 14, where 6, whom 3, who 2, que 2, dont 1, whose 1, when 1, she 1 | **36** (qui, that, who, que, dont) | **12** : where 6, whom 3, whose 1, when 1, relative zéro 1 |
| **SUB** (33) | that 9, que 5, when 4, because 4, although 3, if 2, while 2, as 2, car 1, qu'il 1 | **32** (CONJ/DET/PRON) | **1** : qu'il (élidé) — et **aucune branche SUB** |
| **GP** (13) | to 2, since 2, les 2, du 1, au-dessus 1, en 1, for 1, on 1, il 1, le 1 | **6** (PREP) | **3** (since 2, au-dessus 1) + **4** sans préposition (gold) |

À noter : `whom` et `whose` sont dans `RELATIFS` mais **pas dans la branche REL** ; `where` et
`when` ne sont dans aucun des deux. Les quatre GP « les jardin », « les ancienne lettre », « le
renard », « il » sont des **GP du gold synthétique sans préposition** : aucun chunker ne peut les
produire sans produire un GP qui commence par un déterminant.

## 4. Les 94 par cause

Les catégories « même type » du défaut reproduisent la fiche B13 : **65 aucun / 24 plus large /
4 plus étroit / 1 coupé**. La table ci-dessous est la lecture **par cause réparable**, priorité
fixe (le premier drapeau vrai l'emporte) :

| cause primaire | REL | SUB | GP | total |
|---|---:|---:|---:|---:|
| segment **avalé par un GN** | 31 | — | — | **31** |
| **type SUB absent** (aucune branche) | — | 33 | — | **33** |
| **marqueur hors lexique/branche** | 12 | — | 3 | **15** |
| **règle de fin de clause** (frontière) | 4 | — | 3 | **7** |
| **tête avalée par le GN** | 1 | — | — | **1** |
| segment **avalé par un GV** | — | — | 3 | **3** |
| **gold : GP sans préposition** | — | — | 4 | **4** |
| **total** | **48** | **33** | **13** | **94** |

Drapeaux **transversaux** (ils se recouvrent, ils ne partitionnent pas) :

| drapeau | spans |
|---|---:|
| contenu dans un GN | **45** |
| contenu dans un GV | **3** |
| tête hors lexique/branche | **16** |
| frontière sur le même type | **12** |
| tête avalée par un GN | **9** |

Exemples :

- **avalé par un GN** : « that I read » (GN « The book that I read »), « qui nage » (GN « un
  chemin qui nage prépare »), « que j'ai vu » (GN « Le chat que j'ai vu dormait ») ;
- **type SUB absent** : « because she is happy », « que les fenêtre ouvre » — le marqueur est
  connu (CONJ/DET), mais le chunker n'a aucun type SUB ;
- **marqueur hors lexique/branche** : « where we live », « whom I mention », « whose car is
  red », « she talks about » (relative zéro), « since yesterday », « au-dessus du lac » ;
- **règle de fin de clause** : « dont la voiture est rouge » (le REL va jusqu'à « arrive »),
  « qui marche » (le REL va jusqu'au verbe suivant), « du voisin » (le GP va jusqu'à « la nuit »),
  « en gare » (le GP commence à « entre », lu comme préposition) ;
- **tête avalée par le GN** : « that is on the table » (GN « The book that ») ;
- **avalé par un GV** : « to eat » (GV « is ready to eat »), « on the wall » (GV « is hung on
  the wall ») ;
- **gold : GP sans préposition** : « les jardin », « les ancienne lettre », « le renard », « il ».

## 5. Les deux règles

### (a) Un REL/SUB par son marqueur de tête et sa frontière

1. **Lexiques** (par langue) : REL = qui, que, qu, dont, où, which, that, who, whom, whose,
   where, when ; SUB = that, when, because, if, although, while, as, since, car, que, qu'il,
   parce, puisque, quand, lorsque, comme, si, quoique.
2. **Pré-passe** sur les tokens : tout marqueur ouvre une REL/SUB, **même s'il est dans un GN**
   que la boucle principale va avaler ; le type est tranché par le marqueur et le contexte
   gauche (après un verbe/AUX → SUB ; après DET + nom → REL ; `that`/`when`/`que` ambigus).
3. **Frontière** : du marqueur à la fin du **premier noyau prédicatif** ; on s'arrête avant le
   second noyau (verbe conjugué ou AUX après un prédicat complet) ou avant un pronom sujet ; la
   ponctuation ferme. Un temps composé (AUX + participe) et une copule + attribut comptent pour
   **un** noyau.
4. Les segments sont **ajoutés** à ceux du chunker (recouvrement permis, comme l'union S +
   chunker le fait déjà).

### (b) Un prédicat par clause

1. Chaque chunk contient **au plus un noyau prédicatif**.
2. **GN** : s'arrête au premier verbe fini, AUX ou marqueur relatif — plus seulement à
   PREP/CONJ/AUX ; il ne va plus jusqu'à la ponctuation en avalant la relative.
3. **GP** : s'arrête au premier noyau ; un infinitif collé à la préposition reste dans le GP
   (« to eat ») ; une préposition homographe d'un verbe (« entre ») n'ouvre pas un GP.
4. **GV** : part de l'AUX (plus du pronom sujet qui précède), s'arrête au second noyau, et ferme
   avant un PREP + infinitif (second prédicat).
5. **REL** : même frontière que (a), avec le lexique de marqueurs **d'origine** ; pas de branche
   SUB (b) seule ne peut donc pas produire les 33 SUB.

Les deux règles partagent `noyau()` (lexique + POS + contexte : après pronom sujet = verbe,
après AUX = participe/attribut, après un noyau = morphologie) et `frontiere()` (automate de
bornes ci-dessus).

| règle | gain / 94 | REL | SUB | GP | exacts en union / 239 |
|---|---:|---:|---:|---:|---:|
| **(a)** marqueur + frontière | **79** | 47/48 | 32/33 | 0/13 | **224** |
| **(b)** un prédicat par clause | **41** | 36/48 | 0/33 | 5/13 | **186** |
| **(a)+(b)** | **84** | 47/48 | 32/33 | 5/13 | **229** |

La répartition est nette : (a) prend les **81 REL/SUB** (moins la relative zéro et l'adverbe
final) et **aucun GP** ; (b) prend les **36 REL** que son lexique d'origine connaît, **5 GP**,
et **aucun SUB**. Les deux se recouvrent sur 36 REL ; le type SUB de (a) tranche le REL homonyme
de (b) sur les mêmes bornes.

## 6. Le risque de régression

| mode | exacts / 239 | perdus / 77 (chunker seul) | perdus / 145 (défaut) | FP | P | R | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| chunker seul | 77 | — | — | 502 | 0,2585 | 0,0939 | 0,1378 |
| défaut (S + chunker) | 145 | — | — | 1059 | 0,3154 | 0,2619 | 0,2862 |
| (a), union | 224 | **0** | **0**\* | 1068 | 0,3468 | 0,3043 | 0,3242 |
| (b), union | 186 | **0** | **0**\* | 858 | 0,4291 | 0,3462 | 0,3832 |
| (a)+(b), union | **229** | **0** | **0**\* | **852** | **0,4468** | **0,3693** | **0,4043** |

\* En union, la règle **ajoute** ses segments à ceux de S : elle ne peut pas retirer un span de S,
donc 0/145 est structurel. Le coût réel est le **FP ajouté** : +9 pour (a) (des SUB de « bien
qu'/pendant qu' » démarrés à « qu'il », et deux « since + GN » lus comme SUB), −201 pour (b) (le
GN n'avale plus les verbes), −207 pour (a)+(b). En mode chunker seul, les 77 spans exacts sont
conservés (0 perdu) par les deux règles.

F1 par type, tous les segments du gold (union) :

| type | défaut | (a) | (b) | (a)+(b) |
|---|---:|---:|---:|---:|
| REL | 0,3714 | 0,7807 | 0,7006 | **0,8439** |
| SUB | 0,6852 | 0,9262 | 0,6852 | **0,9262** |
| GP | 0,7841 | 0,7841 | 0,8034 | **0,8034** |
| GN | 0,2840 | 0,2840 | 0,4480 | **0,4480** |
| GV | 0,1834 | 0,1834 | 0,2075 | **0,2075** |

(a) ne touche ni GN, ni GV, ni GP ; (b) fait monter le GN de 0,284 à 0,448 parce qu'il ne avale
plus le verbe ni la relative.

## 7. Contrôles négatifs

| contrôle | résultat | lecture |
|---|---|---|
| (a) **sans frontière** (marqueur → ponctuation) | gain **32** (SUB seulement), REL **0** ; F1 0,1621 | la frontière est décisive pour les REL (47 → 0) et pour la précision |
| (b) **sans arrêt du GN sur le marqueur relatif** | gain **5** (GP seulement), REL **0** ; F1 0,2829 | l'arrêt du GN est décisif pour les REL (36 → 0) |
| **hasard** : mêmes longueurs, même phrase, 5 000 tirages | **304/5000 = 6,08 %** de cibles touchées | le plancher du hasard sur ce gold ; (a)+(b) est à 84/94 = **89,4 %** |
| **décalage +1** de chaque span perdu | **0/94** | la mesure est bien exacte, pas une mesure de recouvrement |
| **oracle de frontière** : tête du gold donnée | REL **48/48**, SUB **32/33** | la frontière n'est pas le goulot ; ce sont le marqueur et le type qui manquent |

L'oracle REL à 48/48 inclut la relative zéro « she talks about » (la frontière part de « she ») ;
le seul SUB manqué est « that she would come », où le gold exclut l'adverbe final « yesterday »
alors qu'il inclut « demain » dans « qu'il vient demain ». C'est une **convention du gold**, pas
un échec de l'automate.

## 8. L'attachement (mesure secondaire)

| mode | labels (couverture) | top1 global | top-k global | top-k sur span juste |
|---|---:|---:|---:|---:|
| défaut | 145 (0,6067) | 0,5983 | 0,5941 | **0,9793** |
| (a) | 224 (0,9372) | 0,6485 | 0,6946 | 0,7411 |
| (b) | 186 (0,7782) | 0,6109 | 0,6192 | 0,7957 |
| (a)+(b) | **229 (0,9582)** | **0,6485** | **0,7071** | 0,7380 |

Le top-k global gagne **+11,3 points** et la couverture **+35 points**, mais le top-k
**conditionnel au bon span** tombe de 0,979 à 0,738 : les 84 spans récupérés sont **plus durs à
attacher** que ceux que S réussissait déjà. C'est le miroir : segmenter n'est pas attacher ; le
prochain goulot est l'attachement des REL/SUB récupérées, pas leur segmentation.

## 9. Ce qui pourrait rendre cette fiche fausse

- **In-sample** : les deux règles ont été conçues et itérées sur ce même gold (612 phrases, 94
  spans) ; les 25 spans synthétiques viennent d'un lexique disjoint, mais les règles y ont aussi
  été ajustées. Il faut un **gold tenu à l'écart** (autre corpus, autre langue) avant de conclure.
- **La copie locale n'est pas le code** : rien n'est porté dans `bloc_linguistique.py`, aucune
  porte n'est lancée. Les portes à nombre absolu (77 GP, 145 labels, 169/169) bougeront : il
  faudra les mettre à jour **volontairement**, pas les laisser casser.
- **Le détecteur de verbe** reste lexical + morphologique : les homographes nominaux (« la
  ferme », « le fait », « le lit ») sont la limite nommée ; le 0/77 est mesuré sur ce gold, pas
  sur un autre domaine.
- **Les conventions du gold** plafonnent : 4 GP synthétiques sans préposition, 1 relative zéro,
  1 adverbe final exclu (mais « demain » inclus ailleurs). Ces 6 spans ne sont pas réparables par
  les deux règles.
- **Le hasard** touche 6,1 % des tirages : le span exact est une mesure permissive sur des
  segments courts ; 89,4 % est loin au-dessus, mais ce n'est pas une preuve linguistique.
- **L'attachement** des spans récupérés n'est correct qu'à 67–74 % : un span juste ne suffit pas
  à résoudre la cible.

## 10. La suite

1. **Porter (a) et (b)** dans `bloc_linguistique.py` (territoire L), avec `noyau()` et
   `frontiere()` ; ajouter `since` et `au-dessus` au lexique PREP, et la déflexion PP pour
   « on the wall ».
2. **Mesurer les portes** : les 169 portes, dont celles qui codent 77/145 ; mettre à jour les
   références de non-régression et l'attachement.
3. **Gold** : corriger les 4 GP synthétiques sans préposition ; trancher la convention d'adverbe
   final (« hier » exclu, « demain » inclus).
4. **Gold tenu à l'écart** (autre corpus ou autre langue) avant tout commit de la règle.

## 11. Fichiers

- **Cette fiche** : `reports/rapport-spans-chunker.md`.
- **JSON** : [`pensee-spans-chunker.json`](pensee-spans-chunker.json) — agrégats, causes,
  marqueurs, règles, contrôles, et le détail des 94 spans.
- **Lecture seule** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
  [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
  [`generateur.py`](../tools/structures/generateur.py),
  [`gold*.json`](../tools/tests/linguistique/).
- **Simulation non commitée** : `/tmp/spans/` (copie du chunker, `regles.py`, `analyse.py`,
  `simuler.py`) — aucun fichier du dépôt n'y est modifié.
