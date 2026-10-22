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
réseau.* L'outillage est en place :
`tools/pas_de_pensee_corrige.py`, `tools/pas_de_pensee_non_lineaire.py`, `tools/etat_de_plan.py`,
`tools/plan_entrainement.py` et `tools/composition_latente.py`.
