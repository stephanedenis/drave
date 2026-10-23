# 5. La pensée sans verbaliser — le travail de la nuit du 16 octobre

## La question, et pourquoi elle n'est pas abstraite

Un modèle de langue « réfléchit » en **écrivant** : chaque pas de pensée est un jeton, qu'il relit ensuite.
Un cerveau d'expert fait l'inverse — il pense **sans dialogue intérieur**. Peut-on obtenir la même chose
d'un modèle ?

C'est une question **exécutable** avec Drave, parce que le moteur sait déjà **écrire et relire un état** :
on peut faire évoluer la pensée **sans qu'aucun jeton ne soit émis**.

![Penser sans verbaliser](schemas/pensee.svg)

## Ce que la nuit a mesuré, dans l'ordre

| étape | le résultat | ce qui a été appris |
|---|---|---|
| **réinjecter l'état brut** | la prédiction détruit de 5 ordres de grandeur (×30 000) | et **normer n'y change rien** : ce n'est pas l'échelle |
| **apprendre un pont** | l'état mappé bat le mot (68,6 % contre 122,9 %) | la sortie prélinguistique **dit mieux** que le **jeton de sortie** |
| **mesurer l'écart** | facteur **648** d'échelle, cosinus **+0,14** | les deux espaces ne sont pas le même |
| **aligner** | cosinus **0,70**, échelle **1,015** — et la langue **s'améliore** | l'alignement est un régularisant, pas un coût |
| **boucler quand même** | λ = **7 311**, contenu détruit | aligner les espaces ne suffit pas : il faut la **dynamique** |
| **opérateur post-hoc** | λ = **0,997** (le premier pas contractant) et +15 points… sur **un** pas | l'itération n'accumule pas |
| **récurrence à l'entraînement** | itération **plate** (88,4 · 88,2 · 88,5) | l'état devient **habitable** — au prix de 5 points |
| **la falaise** | **pas de premier pas linéaire** : l'opérateur prédit la **moyenne** (mesure 113) | l'état d'une phrase ne porte pas la suivante ; il faut un état qui porte le **plan** |
| **la cause** | déplacement 44,8 % contre 77,5 % | les modèles plats ont appris un **point fixe** |

## Les trois piliers, et ce qu'ils valent

Après avoir **réparé l'instrument** (un λ de ridge choisi par validation croisée, et une batterie de
longueurs), trois conclusions **survivent** :

1. **l'état porte le sens** : 16 jetons d'avance à **80,3 %**, quand le mot est à **118,4 %** — 38 points
   d'écart ; et l'empreinte de copie à **49,3 % contre 76,9 %** en lecture (trois exécutions) ;
2. **l'itération s'obtient et se paie** : plate, contre **+3,2** points de lisibilité à 2,43 M et **+2,4** à
   9,57 M — le prix **baisse** avec la capacité, lentement ;
3. **la récurrence n'est pas qu'un coût** : elle **améliore** le modèle de langue (2,73 contre 2,76
   bits/octet). *Le modèle qui pense est aussi un meilleur lecteur.*

**Mesure 77 (20 octobre)** : sur **Qwen2.5-3B** et **139 paragraphes en 12 langues** (corpus JW 2026), un **pont
linéaire** par langue atteint un **cosinus de 0,78-0,92** et retrouve la bonne traduction dans **28-67 %** des cas
(hasard 0,7 %), le contrôle négatif restant à ~0 — *la représentation neutre existe mais doit être alignée*, comme
le pont de la nuit du 16, retrouvé ici à plus grande échelle. **Mesure 78** : le passage du 3 B au 7 B ne change
presque rien (+3,7 en lecture, +1,4 en écriture), **lire ≈ écrire**, et la meilleure couche est **la couche 4** pour
cinq langues — *le sens partagé est tôt et stable ; c'est une base d'architecture, pas un effet de taille*.
**Mesure 79** : la **composition** n'est pas démontrée — seuls les paragraphes **complets** s'alignent (0,2-0,78),
les préfixes de caractères restent près du hasard et la trajectoire est plate ; le test est **confondu** (les
préfixes ne sont pas des unités de sens). **Mesure 80** : sur des phrases **alignées** (Verne FR/EN, 200 phrases),
la composition **est là** — retrieval **0,61** (hasard 0,5 %), **ordre 0,84** (hasard 25 %) à la **couche 18** ; le
pont est inutile (0,42) et la dernière couche s'effondre (0,09) : *le sens est au milieu, la langue à la fin*.
**Mesure 81** : la composition **profite de la taille** — 0,76 / 0,865 au 7 B (couche 14 sur 28, soit 50 % de la
profondeur) contre 0,61 / 0,84 au 3 B (couche 18 sur 36) ; la fin s'effondre encore plus (0,125). *Le sens neutre
vit à mi-profondeur, et la composition est un levier de taille, pas un plafond.* **Mesure 87** : la courbe **plafonne** entre 7 et 14 B
(0,68 / 0,855 au 14 B contre 0,76 / 0,865 au 7 B, avec un OOM de répartition) — *le levier de la composition est la
profondeur et la taille **jusqu'à 7 B**, pas les paramètres au-delà*.
**Le pas de pensée linéaire n'existe pas** (mesure 113, après l'**erratum 6**) : les mesures 82-85, 88 et 108
lisaient les états Verne avec 200 noms pour 400 lignes — les « séries de quatre phrases » étaient en réalité
`fr0, en0, fr1, en1`, des paires de **traduction** ✗✗. Sur la carte correcte, l'opérateur ridge **prédit la moyenne** :
son cosinus est celui du prédicteur constant à ±0,03 près, ses sorties sont **effondrées** (cosinus moyen 0,89-0,99),
et le retrieval de la phrase suivante reste au **hasard** (0-8,9 % contre 2,2 %), aux trois tailles ; un opérateur
**contrastif** (InfoNCE) ne fait pas mieux (2,2-11,1 %) — *l'objectif n'est pas la cause* ✗✓. Un MLP contrastif
**mémorise** les transitions (perte 0,03) mais ne **généralise** pas (mesures 114-115) ; avec **630 séries** et
**1 323 transitions** (mesure 115), ni le linéaire — qui reste la moyenne (cos 0,827-0,940 contre 0,821-0,939,
effondrement 0,933-0,995) — ni le MLP (retrieval 0-1,15 %, dans la série 14-27 % contre 25 %) ne retrouvent la
phrase suivante : *ce n'est ni l'échantillon, ni la forme, ni l'objectif* ✗✗. **En revanche**, l'**état latent
entraîné avec la tâche** (mesure 109) **collapse** bel et bien en **point fixe** : le pas 3 monte à 0,60-0,67, mais
le pas 1 tombe à 0,00 ; la pénalité de point fixe (mesure 110) ne le débloque pas ✗✗. *Ce n'est donc pas le modèle ni
la forme de l'opérateur : c'est le **pas** qui n'est pas une fonction de l'état d'une phrase — il manque le **plan**
de la série.*

## Ce qui reste à construire

Une **dynamique qui avance d'un pas à la fois** suppose un état qui porte le **plan** de la série, pas seulement la
phrase courante. Trois mesures l'ont tranché : l'état d'une **phrase** ne porte pas la suivante, même avec
**1 323 transitions** et un MLP (mesure 115) ; le **contexte** (moyenne du préfixe + ridge, GRU) ne porte pas le
**contenu** de la suite — 0,14 contre 0,125 (mesure 116) ✓✗ ; et un **code de 32 dimensions** reconstruit la
trajectoire à 0,86-0,89, à peine au-dessus de la **moyenne** (0,83-0,88) : le plan est un **mince résidu** (mesure 117)
✗✗. Une **dissociation** le résume (mesure 118) : la **langue** est parfaitement décodable (1,00) alors que la
**position** dans la série ne l'est pas (0,13 contre 0,125) — *l'état porte la langue, pas la structure*. *Le plan
n'est pas extractible des états figés — il n'y est même pas un objet de faible dimension : il faut l'entraîner dans
le modèle.* C'est fait (mesure 119) : un LoRA contrastif entraîné à retrouver la 5ᵉ phrase depuis les 4 premières
monte le retrieval de contenu de **0,239 à 0,443** (hasard 0,125 ; contrôle à cibles mélangées : 0,227) — **le plan
s'entraîne**, premier résultat positif de l'étage 2. Mieux : le **même** état de plan porte **trois pas** (mesure 120 :
0,443 / 0,295 / 0,341 pour les 5ᵉ, 6ᵉ et 7ᵉ phrases) — *la dynamique n'est plus bloquée à un pas*. Mais les contrôles **tempèrent** : le
transfert aux cibles figées est de +0,05 à +0,08 selon la graine (mesures 121 et 123), et **nul à 16 phrases**
(0,193 contre 0,189, mesure 122) ; *le gain principal est donc l'adaptation de l'espace cible, pas un plan
transférable*. **La correction marche** (mesure 124) : entraîné **contre des cibles figées**, le plan transfère —
**0,324 / 0,273 / 0,216** en moyenne de deux graines (hasard 0,125 ; avant 0,205 / 0,216 / 0,165), même signe aux
deux découpages ; mais seul **h1** est solide (z ≈ 2,0), h2/h3 restent dans le bruit de 88 items. *Ce n'était pas
l'information qui manquait, c'était la cible qui bougeait.* La suite : plus de séries de test, horizons au-delà de 3,
et un état de plan **récurrent**.

**Mesure 125 — le raisonnement transitif est dans l'état, pas dans une géométrie commune.** Sur un corpus contrôlé
(chaînes d'ordre, prémisses mélangées, FR/EN), une sonde linéaire retrouve la conclusion dans l'état : **1,00 / 0,92 /
0,84 / 0,78 / 0,51** (FR) et **1,00 / 0,98 / 0,85 / 0,52 / 0,53** (EN) pour 2 à 6 entités, contre **5 %** de hasard ;
le contrôle à étiquettes mélangées est au hasard. Mais le **transfert FR→EN est au hasard** (0,02-0,09) : le
raisonnement est là, sa **géométrie** ne l'est pas — il faut un pont d'alignement. *La tête bien faite n'est pas la
grosse tête : c'est un état qui compose, et un pont qui le rend indépendant de la langue.*

**Mesure 126 — un pont linéaire rend le raisonnement indépendant de la langue.** Sur **2000 chaînes appariées**
FR/EN, un pont ridge EN→FR appris sur les états permet à la sonde FR de lire l'état EN : **1,00 / 0,91 / 0,68 /
0,52 / 0,46** pour 2 à 6 entités, contre **0,04-0,08** sans pont ; le contrôle (paires mélangées) reste au hasard.
*La géométrie est alignable par une petite structure — la tête bien faite, c'est un état qui compose + un pont qui
le rend commun.*

**Mesure 127 — l'alignement est structurel.** La même expérience avec une **autre relation** (la taille) donne
**1,00 / 0,85 / 0,67 / 0,56 / 0,44**, superposable à l'ordre (1,00 / 0,91 / 0,68 / 0,52 / 0,46) : le pont n'aligne
pas des mots, il aligne la **structure** du raisonnement. *Un même pont sert deux relations.*

**Mesure 128 — le pont n'est pas propre à une langue.** FR/ES donne **1,00 / 0,92 / 0,72 / 0,56 / 0,50**,
superposable à FR/EN : l'alignement est **langue-général** (au moins pour trois langues indo-européennes). *La tête
bien faite est portable : un état qui compose, un pont par langue.*

**Mesure 129 — le pont doit rester linéaire.** Un MLP EN→FR (2048 → 512 → 2048) ne dépasse pas le hasard
(0,04-0,17) : avec ~250 paires par longueur, la capacité non linéaire **sur-apprend**. *La petite structure linéaire
est la bonne — ce n'est pas la capacité qui manque, c'est la régularisation.*

**Mesure 130 — le pont n'est pas une couche.** Il marche aux couches **12, 18 et 24** ; la **couche 12** est la
meilleure aux longues chaînes (0,74 / 0,64 / 0,48) et in-langue. *La tête bien faite a une profondeur : le milieu du
réseau.*

**Mesure 131 — quatre langues.** FR/DE donne **1,00 / 0,94 / 0,74 / 0,65 / 0,52**, comme FR/EN et FR/ES :
l'alignement est **langue-général** sur quatre langues indo-européennes, dont une à ordre des mots différent. *Le pont
n'est pas un artefact du couple FR/EN.*

**Mesure 132 — le pont ne se transpose pas au plan.** Sur les 307 séries Verne appariées, le pont EN→FR des prompts
donne **0,148**, contre **0,250** sans pont (hasard 0,125) : il aligne le **raisonnement**, pas l'**état de plan**.
*Le plan reste à entraîner dans le modèle (mesures 119-124) ; le pont n'est pas un mécanisme universel.*

**Mesure 133 — l'arabe.** Le pont tient pour une langue **non indo-européenne** et d'une autre écriture :
**1,00 / 0,90 / 0,73 / 0,48 / 0,41** (pont AR→FR), contre 0,04-0,08 sans pont. *L'alignement n'est pas un effet de
voisinage.*

**Mesure 134 — la géométrie n'est pas partagée entre tâches.** Un pont appris sur le **raisonnement** donne
**0,125** (le hasard) sur le **plan** : les tâches de l'étage 2 ont des géométries **locales** ; il faut un pont par
tâche, ou un plan entraîné dans le modèle.

**Mesure 135 — un seul pont pour toutes les longueurs.** Pont et sonde **poolés** sur toutes les longueurs :
**0,94 / 0,91 / 0,81** pour 4 à 6 entités (contre 0,46-0,68 avec un pont par longueur) ; un pont appris sur les
chaînes de 2 entités **seul** échoue (0,03-0,12). *Une seule carte linéaire, calculée une fois sur toutes les
longueurs, suffit : c'est la version la plus économique de la tête bien faite.*

**Mesure 136 — le multi-tâches ne suffit pas.** Un pont appris sur le raisonnement **et** les paires de plan donne
**0,136** (hasard 0,125) sur le plan : ajouter des paires de plan ne l'aligne pas ; il faut aligner les **cibles**, ou
entraîner le plan dans le modèle.

**Mesure 137 — le pont marche au 7 B.** Au 7 B, pont et sonde poolés donnent **0,95 / 0,87 / 0,81** pour 4 à
6 entités (sans pont 0,06-0,10) : la taille améliore le raisonnement in-langue, mais l'alignement reste la même
**carte linéaire**. *La tête bien faite ne remplace pas la grosse tête : elle la rend utilisable dans toutes les
langues.*

**Mesure 138 — un code partagé non supervisé ne suffit pas.** Une ACP commune FR+EN (64 ou 256 dims) suivie du
pont donne **0,14-0,98** (64) et **0,34-1,00** (256), contre **0,46-1,00** pour le pont pleine dimension : la
compression non supervisée perd l'information de raisonnement. *La tête bien faite n'est pas une réduction de
dimension, c'est une carte alignée.*

**Mesure 139 — la CCA aligne, mais 64 dimensions perdent l'information.** Un code CCA de 64 dimensions (sur une
ACP 256) porte le raisonnement d'une langue à l'autre au niveau de son **in-langue** (0,281 contre 0,306 à 6 entités,
92 %), mais ce code est plus faible que l'espace plein (0,306 contre 0,653) : *l'alignement est supervisé et réel ;
le problème est la **capacité**, pas l'alignement.*

**Mesure 140 — la CCA à 256 dims récupère.** Le code CCA de 256 dimensions donne **0,57-1,00** (contre 0,28-1,00
à 64 dims) : la capacité était le problème ; le transfert reste à 68-76 % de l'in-langue, et le pont poolé garde
l'avantage à 6 entités (0,81). *Deux petites structures, deux compromis : le pont garde la performance, la CCA donne
un code commun.*

**Mesure 141 — le 14 B est quasi parfait.** Au 14 B, pont et sonde poolés donnent **1,00 / 1,00 / 1,00 / 1,00 /
0,975** (sans pont 0,03-0,08) : le raisonnement est parfait in-langue et le pont le transfère quasi sans perte. *La
petite structure linéaire suffit à toutes les échelles testées (3, 7 et 14 B).*

**Mesure 142 — entraîner en français ne suffit pas.** Un LoRA + tête entraîné 500 pas sur les chaînes **FR** garde
une sonde FR forte (0,974), mais la sonde FR→EN reste à **0,092** (hasard 5 %) et le pont **baisse à 0,513** (0,81
figé) : le fine-tuning monolingue n'aligne pas, il **dégrade** l'alignement. *Il faut un objectif **multilingue**, pas
seulement réussir en français.*

**Mesure 144 — le multilingue ne suffit pas.** Un entraînement **alterné FR/EN** (500 pas) garde une sonde FR à
0,989, mais la sonde FR→EN reste à **0,042** et le pont baisse à **0,451** : la supervision de la tâche, même
bilingue, **n'apprend pas l'alignement**. *Il faut un objectif explicitement contrastif entre les paires FR/EN.*

**Mesure 146 — le contraste explicite ne suffit pas non plus.** Un entraînement avec **InfoNCE FR↔EN** (500 pas,
τ = 0,07) garde une sonde FR à 0,985, mais la sonde FR→EN reste à **0,042** et le pont à **0,466** : en 500 pas,
sur un LoRA d'attention, l'alignement **appris** n'émerge pas. *Le pont externe reste la structure qui marche ;
l'alignement appris demanderait plus de pas, de négatifs, ou une projection dédiée.*

**Mesure 147 — l'alignement s'apprend.** Avec un contraste plus fort (**batch 8, poids 2, 800 pas**), la sonde
FR→EN passe de 0,058 (figé) à **0,742**, la tête à **0,734** en EN, et le pont à 0,779 ; le prix est l'in-langue
(0,776 contre 0,987). *Le raisonnement devient indépendant de la langue **dans le modèle**, sans pont — à condition
de fournir des négatifs et un poids suffisant.*

**Mesure 149 — le contrôle du contraste.** Avec des paires **mélangées**, la sonde FR→EN monte quand même à
**0,505** (paires correctes : 0,742) : l'entraînement **bilingue** aligne déjà en grande partie, et le bon appariement
ajoute **+24 points**. *Le contraste correct n'est pas la cause unique de l'alignement.*

**Mesure 150 — le bilinguisme est la cause principale.** Sans contraste, la sonde FR→EN monte à **0,656** ; le
contraste **correct** ajoute +9 (0,742), le **mélangé** coûte −15 (0,505). *L'alignement est une conséquence de la
supervision bilingue avec assez de batch et de pas ; le contraste correct affine, le mauvais dégrade.*

**Mesure 151 — la courbe.** L'alignement **émerge entre 400 et 800 pas** (0,13 → 0,66) ; à 800, le **batch 8** fait
0,656 contre 0,404 (batch 4) ; à nombre d'exemples égal, c'est le nombre de **pas** qui compte. *Il faut entraîner
assez longtemps, pas seulement voir beaucoup d'exemples.*

**Mesure 152 — la saturation.** À **1 600 pas**, la sonde FR→EN atteint **0,753** (800 : 0,656) : le gain ralentit
(+10 points pour 800 pas de plus) et l'in-langue **plafonne** à 0,826. *Le compromis se stabilise : ~0,75 en
transfert, ~0,83 en in-langue.*

**Mesure 153 — l'alignement ne transfère pas au plan.** Avec l'adaptateur aligné sur le raisonnement, l'EN→FR du
plan reste à **0,273** (figé : 0,250 ; hasard 0,125) : l'alignement est **local à la tâche**. *Il faut entraîner le
plan lui-même, pas espérer l'héritage.*

**Mesure 154 — le plan s'aligne par son entraînement.** Un LoRA entraîné sur l'objectif du plan (prompt 4 phrases →
5ᵉ parmi 8), **alterné FR/EN**, améliore l'**EN→FR** de 0,250 (figé) à **0,364**, presque le FR→FR (0,398) ; l'in-langue
monte aussi (0,398 / 0,466). *Chaque tâche a sa géométrie, mais chacune peut s'aligner par son entraînement bilingue —
le pont n'était pas la bonne structure.*

**Mesure 155 — le contrôle FR seul.** L'**EN→FR est identique** (0,364) avec le français seul : le gain de la
mesure 154 vient de l'entraînement de la **tâche** (les cibles FR deviennent plus discriminables), **pas** du
bilinguisme. *Le plan ne s'aligne pas ; son transfert apparent est un effet **côté cible**.*

**Mesure 156 — le plan résiste.** Un InfoNCE **explicite** FR↔EN n'ajoute que **+2 points** (0,386 contre 0,364) :
la géométrie du plan est **ancrée dans la langue** ; son transfert apparent vient de la tâche, pas d'un partage.
*C'est le seul endroit de l'étage 2 où l'alignement échoue à toutes les méthodes testées.*

**Mesure 157 — la profondeur.** Au 3 B, le pont tient jusqu'à **12 entités** (0,95 à 4 → **0,47** à 12) : pas de
mur, une **pente** qui suit l'in-langue. *La pente, pas la falaise.*

**Mesure 158 — la profondeur au 14 B.** La pente **s'aplatit** : 0,966 à 8, 0,862 à 10, **0,695 à 12** (3 B :
0,622 / 0,561 / 0,469) ; l'in-langue 0,836. *La profondeur dépend de la taille ; la petite structure (le pont) suit.*

**Mesure 160 — le raisonnement naturel.** Sur **XNLI** (2490 paires FR/EN), l'inférence est dans l'état
(FR **0,502**, EN **0,576** contre 1/3) et le pont la transfère à **0,592** — au-dessus du FR in-langue. *Le pont ne
marche pas que sur le synthétique : il transfère aussi l'inférence naturelle.*

**Mesure 161 — le naturel au 14 B.** Pas de gain : FR 0,481, EN 0,589, pont 0,627 (3 B : 0,502 / 0,576 / 0,592).
*La taille ne change presque rien : la limite est la **sonde linéaire**, pas le modèle.*

**Mesure 162 — la sonde non linéaire ne fait pas mieux.** Le MLP donne **0,453** (contre 0,502 au linéaire) et
**0,542** au pont (0,592) : il sur-apprend. *Ce n'est pas la sonde qui limite, c'est l'état ; pour progresser sur
l'inférence naturelle, il faut entraîner le modèle, pas changer le readout.*

**Mesure 163 — le fine-tuning XNLI.** Un LoRA + tête 3 classes (400 pas bilingues) donne une tête à **0,592** (FR)
et **0,610** (EN, zéro-ressource), et le pont monte à **0,751** (figé : 0,592). *L'inférence naturelle se travaille
par l'entraînement ; le modèle apprend une représentation plus partageable.*

### La carte du raisonnement (mesures 125-163)

| question | mesures | réponse |
|---|---|---|
| le raisonnement synthétique est-il dans l'état ? | 125 | oui : 1,00 → 0,51 (FR), 1,00 → 0,53 (EN), hasard 5 % |
| un pont linéaire l'aligne-t-il ? | 126 | oui : 1,00 / 0,91 / 0,68 / 0,52 / 0,46 (2-6 entités) |
| est-ce structurel et langue-général ? | 127-128, 131, 133 | oui : « taille », FR/ES, FR/DE, **arabe** |
| le pont doit-il rester linéaire ? | 129 | oui : le MLP échoue (0,04-0,17) |
| à quelle couche ? | 130 | 12, 18 et 24 ; la 12 est la meilleure aux longues chaînes |
| un seul pont pour toutes les longueurs ? | 135 | oui, poolé : 0,94 / 0,91 / 0,81 |
| jusqu'à quelle profondeur ? | 157-158 | 12 entités : 0,47 (3 B), **0,70** (14 B) |
| à quelle échelle ? | 137, 141 | 3 B, 7 B, 14 B : 0,81-0,97 |
| l'alignement s'apprend-il ? | 142-152 | oui : bilingue **0,656**, + contraste **0,742**, sature **0,753** |
| le plan s'aligne-t-il ? | 132, 134, 153, 155-156 | **non** : ponts, bilinguisme et contraste échouent |
| le raisonnement naturel ? | 160-164 | oui : inférence 0,50-0,59, pont 0,59 → **0,77** (fine-tuning) |

**Les trois leçons.** 1. L'état porte le raisonnement — synthétique et naturel — **sans verbaliser**. 2. Un petit
pont **linéaire** l'aligne, à toutes les échelles et sur les deux tâches ; l'alignement **s'apprend** par
l'entraînement bilingue, et **sature** autour de 0,75. 3. Le **plan** est le contre-exemple : sa géométrie est
**ancrée dans la langue** ; ni les ponts, ni le bilinguisme, ni le contraste ne l'alignent — il faut l'entraîner
autrement.

**Mesure 164 — le train complet.** 13 394 paires du train MultiNLI (**hors domaine** du dev) : la sonde reste à
**0,586**, le pont monte à **0,773**, mais la tête baisse (0,456 / 0,534). *Le domaine compte plus que le volume ;
pour progresser sur l'inférence, il faut des données du même domaine.*

**Mesure 166 — le contraste seul dégrade le plan.** À chaque pas de contraste (sans la tâche), l'EN→FR tombe à
**0,318** et le FR→FR à 0,284 (alterné : 0,386 ; tâche seule : 0,364). *Le plan a besoin de sa tâche ; le contraste
n'est pas un levier — la récurrence de bout en bout reste la seule voie.*

L'outillage est en place :
`tools/pas_de_pensee_corrige.py`, `tools/pas_de_pensee_non_lineaire.py`, `tools/etat_de_plan.py`,
`tools/plan_entrainement.py` et `tools/composition_latente.py`.
