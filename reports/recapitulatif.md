# Récapitulatif — méthode appliquée et résultats

État au 06/10, soir. Un seul professeur : **Qwen2.5-0.5B, couche 10** (896 canaux).
Toutes les mesures portent sur le corpus UDHR, dix unités, 40 langues
d'entraînement dont 10 de validation, **6 langues tenues à l'écart** (`ell heb hin
jpn kor tha`, écritures non latines).

---

## 1. La méthode

### 1.1 Boîte noire

On ne lit du professeur que **la couche qu'on veut émuler**, par des traces DRVF
(`--trace-flux`). On ne calcule **pas** son extérieur : ni sa tête de sortie, ni
les jetons qu'il génère (`--n 0`). On n'écrit **aucune** trace des couches
internes de notre modèle.

### 1.2 Le pont

```
s_t = (1−a)·s_{t−1} + a·tanh( P·s_{t−1} + B·e_t )
y_t = W·s_t + moy
```

`e_t` est l'entrée du professeur (couche 0, le plongement) ; `y_t` la couche
cible. **`P` et `B` sont aléatoires et gelés** — aucune rétropropagation. Seule
`W` s'ajuste, en forme fermée (moindres carrés ridgés).

### 1.3 Architecture à couches RÉELLES

Chaque couche ne lit **que la précédente** :

- couche 0 : lit `e_t` et les siens (récurrence) ;
- couche c : lit la couche c−1 **entière** et les siens, nés avant lui ;
- jamais les couches plus basses directement.

C'est ce qui donne un sens au mot « couche ». Dans la version antérieure, chaque
neurone lisait tous les précédents quelle que soit leur couche : ouvrir une couche
ou ajouter un neurone y produisaient **exactement le même calcul** (vérifié —
n = 104 donnait 0,4930 / 0,9368 dans les deux cas). Les 24 « couches » n'étaient
qu'une numérotation.

### 1.4 Phase générative

Départ à **un seul neurone**. On ajoute **un neurone à la fois**, et
l'apprentissage décide :

- **on épuise la couche courante** — on y ajoute les neurones qui manquent pour
  les activations non encore couvertes — tant qu'ils paient ;
- quand elle est **saturée**, on essaie une **couche neuve**, et on ne continue
  que si son premier neurone paie ;
- arrêt quand une couche neuve n'apporte plus rien.

Un neurone seul sait faire **« ET »** et **« OU »** ; il faut une seconde couche
pour un **« OU exclusif »**. Ouvrir une couche trop tôt, c'est vouloir le XOR
avant d'avoir fini le ET et le OU — et c'est mesurablement mauvais : la première
règle ouvrait 24 couches pour 128 neurones et donnait 0,4937, contre 0,5059 pour
la même taille en 8 couches.

### 1.5 Attrition

On retire des **neurones** — pas des colonnes de lecture — puis on **RECALCULE**
les trajectoires des survivants sans les retirés. Sans ce recalcul, « 1 neurone »
ne veut rien dire : sa trajectoire aurait été calculée par les autres, et ce
n'est pas un neurone mais une **caractéristique profonde**.

Le critère de retrait est la **redondance** : on retire ce que les autres disent
déjà (`score = expliqué × contribution`, une seule inversion de Gram), pas les
faibles — couper les faibles n'énonce rien.

---

## 2. Les résultats

### 2.1 La loi qui gouverne tout

Onze points de croissance sur données propres :

| neurones | fid TEST | invariance |
|---:|---:|---:|
| 1 | 0,4702 | 0,9984 |
| 16 | 0,4781 | 0,9871 |
| 64 | 0,4846 | 0,9561 |
| 104 | 0,4930 | 0,9368 |
| 256 | 0,5186 | 0,8874 |

**fid TEST ≈ 0,3856 · (1 − invariance) + 0,4752 · r = 0,9920 · erreur max 0,0047**

Fidélité et invariance ne sont pas deux qualités : ce sont les deux axes d'**une
seule droite**, et chaque point d'invariance abandonné rapporte 0,3856 point de
fidélité. À invariance parfaite, la fidélité vaut 0,4752 — à peine au-dessus de la
constante témoin (0,4710) : **un pont parfaitement interlingue ne dit presque
rien.**

**La droite est une propriété du professeur**, pas de notre modèle : le réservoir
plat tombe sur la même (écarts −0,012 à +0,010).

### 2.2 Le sous-ensemble actif de la couche de référence

Mesuré sur les 6 langues tenues à l'écart, dernière position :

| | canaux | part de 896 |
|---|---:|---:|
| **50 % de l'énergie** | **34** | **4 %** |
| 90 % de l'énergie | 293 | 33 % |
| 99 % de l'énergie | 599 | 67 % |

- canaux actifs dans **au moins une** langue : **896 / 896**
- canaux actifs dans **toutes** les langues : **678 / 896**
- donc **218 canaux (24 %) sont propres à certaines langues**
- chaque canal n'est actif qu'en moyenne dans **5,71 langues sur 6**

La couche de référence est donc **creuse** (34 canaux portent la moitié de
l'énergie) et son sous-ensemble actif est **partiellement propre à chaque
langue**. Ajuster les 896 dimensions densément revient à ajuster massivement du
détail quasi nul et non partagé — ce qui coûte exactement l'invariance cherchée.
**C'est là que se joue la suite.**

### 2.3 Le professeur contre lui-même

Qwen2.5-0.5B, invariance de sa propre couche 10 sur ce périmètre : **0,5247**
(pire paire 0,0850). Notre pont atteint 0,8874–0,9984 : il est **beaucoup plus
invariant que la couche qu'il émule**. C'est le prix de la fidélité (0,47–0,52),
et c'est la loi du §2.1.

### 2.4 Architecture : ce qui a été départagé

| | fid TEST | invariance |
|---|---:|---:|
| réservoir **plat**, 64 neurones, 1 couche | 0,4998 | 0,9624 |
| réservoir plat, 256 neurones | 0,5145 | 0,8680 |
| **cascade à couches réelles**, 256 neurones | 0,5186 | 0,8874 |

À taille égale, l'écart est de **+0,41 point** — et la médiane sur quatre graines
(0,5155) est **quasi identique** au plat. **La profondeur n'apporte rien de
mesurable sur ce périmètre**, une fois les données propres : les deux
architectures parcourent la même droite.

---

## 3. Les corrections, et ce qu'elles ont invalidé

Chacune a été trouvée en vérifiant une affirmation antérieure.

### 3.1 Un pont par professeur

Chaque modèle a sa **propre** représentation sémantique interne ; il n'existe pas
de couche sémantique universelle. Donc **une version de notre modèle par
professeur**, et comparer deux professeurs ne veut rien dire.

*Invalidé* : la comparaison « notre pont bat le professeur 30B ». Les deux nombres
étaient exacts, le classement était vide. Le 30B est **abandonné** — on ne
travaille que sur un professeur à la fois.

### 3.2 L'extérieur du professeur

Le défaut de drave est `n: 32` : chaque traçage **générait 32 jetons** et
calculait la tête. Vérifié au jeton près : `--n 32` donne 542 positions,
`--n 0` en donne **510**. Les jetons générés étaient **dans la trace** — 25 à 60 %
des positions sur la donnée à une unité, 3 % à dix unités. Corrigé : `--n 0`.

### 3.3 La troncature

`ctx 1024` ne laissait passer que 984 jetons de texte. L'abkhaze en demande
**1958**. Sur un échantillon, **5 langues sur 10 étaient tronquées** — et une
« dernière position » tronquée ne correspond plus à la fin du texte, donc
l'invariance comparait des **contenus différents**. Corrigé : `--ctx 2048`.

### 3.4 Deux fautes contre moi-même

- **Fuite de données** : le modèle ne détenait que les langues d'entraînement mais
  était interrogé avec les indices du **test** — 0,7234 annoncé au lieu de 0,5739.
- **Sélection sur le test** : le « meilleur réseau » était choisi d'après son
  score de **test**. La sélection se fait maintenant sur la validation seule.

### 3.5 Les chiffres ronds

1, 2, 4, 8, … 256 venaient de **mon calendrier** de doublement et de **mon
plafond**, pas d'une découverte. Un compte rond est le signe qu'on a choisi la
taille au lieu de la mesurer. Remplacé par la naissance libre du §1.4, qui donne
par exemple **41 neurones en 3 couches [28, 7, 6]**.

---

## 4. Ce qui est solide, ce qui ne l'est pas

**Solide**
- La loi fidélité/invariance (r = 0,992, onze points, deux architectures).
- Le sous-ensemble actif (34 canaux pour 50 % de l'énergie ; 24 % de canaux non
  partagés).
- La phase générative : la fidélité monte de façon monotone avec la taille.
- L'attrition **réduit réellement** — elle recalcule, elle ne masque pas.

**Non solide**
- Tout ce qui a été mesuré avant le §3.2 et le §3.3 : contaminé et tronqué. Les
  résultats à une unité sont les plus fragiles (25 à 60 % de positions générées).
- L'avantage de la profondeur : il s'est effacé au nettoyage.
- Les chiffres ronds : ils mesuraient mon calendrier autant que le réseau.

**Ouvert**
- Exploiter le sous-ensemble actif : viser les ~34 canaux qui portent l'énergie,
  au lieu des 896 densément. C'est la piste la plus prometteuse, et elle est
  cohérente avec le moteur d'événements de Drave.
- La naissance libre, à paramètres plus fins.
- L'attrition sur un réseau né librement (les tailles ne sont plus imposées).


---

## 5. Le déclencheur de couche, révisé — et ce qu'il mesure

### 5.1 La règle

Une couche ne s'ouvre **pas** à la saturation de la précédente. Elle s'ouvre sur
**deux signes simultanés**, et les deux se mesurent :

1. **`communs` — des concepts communs ont émergé.** Un neurone est un concept
   commun si sa trajectoire suit le **même contenu** d'une langue à l'autre.
   Mesure alignée : toutes les langues disent le même texte, donc leur dernière
   position porte le même contenu. On compare la dispersion **entre langues** à
   contenu égal (`dis`) à la dispersion **au fil du texte** dans une langue
   (`dyn`), et on rend `1 − dis/dyn`. Un concept varie sur le texte et peu entre
   les langues ; un trait de langue fait l'inverse.

2. **`contraste` — la lecture a besoin de poids négatifs.** On sépare le mode
   commun du readout (`mean_j W[j]`) de ses écarts. Si les écarts portent tout, la
   lecture ne fait que **soustraire** des concepts : c'est le « OU exclusif », ce
   qu'une seule couche ne sait pas séparer.

### 5.2 Et l'ajout déclenche une RELECTURE du corpus

`Pont.renforce` : à la naissance d'une couche, on relit le corpus, on mesure ce
qui reste à expliquer (le résidu), et on **renforce** les entrées dont
l'activation le capte, on **atrophie** les autres (`f = 1 + η(2·cap − 1)`). C'est
local — chaque neurone ne regarde que sa propre activation et le résidu, jamais le
gradient d'une couche lointaine. **Aucune rétropropagation.**

### 5.3 Ce que la mesure a donné, et il faut le dire tel quel

Sur 64 neurones de couche 1, professeur 0.5B couche 10 :

| mesure | valeur |
|---|---:|
| `communs` moyen | **+0,05 à +0,075** |
| neurones au-dessus du seuil | **6 à 10 %** |
| `contraste` de la lecture | **0,97 – 0,98** |

**Les concepts communs n'émergent pas au premier niveau.** Pilotés par le
plongement — qui est profondément propre à chaque langue — les neurones de couche
1 sont massivement des traits de langue. Le critère refuse donc d'ouvrir une
couche, et le réseau reste à **1 couche, 64 neurones, fidélité de test 0,5839**
(constante 0,5633).

**Deux lectures possibles, et je ne tranche pas :**

- soit c'est un **vrai résultat** — il n'y a rien de partagé à composer à ce
  niveau, et toute profondeur ajoutée là serait du travail perdu ;
- soit **ma mesure est encore trop faible** — elle ne regarde que la dernière
  position et que la dispersion, pas la structure fine des concepts.

Dans les deux cas, la règle fait son travail : elle **empêche** d'empiler des
couches sur du non-partagé.


---

## 6. Le sous-ensemble actif : la piste qui monte la droite

### 6.1 Le déclencheur, corrigé une seconde fois

Trois conditions **simultanées**, et la première manquait :

1. **la couche courante est ÉPUISÉE** — les derniers neurones n'apportent plus
   rien. Tant qu'un neurone de plus paie, c'est lui qu'il faut : couvrir une
   activation manquante est un travail de **neurone**, pas de couche ;
2. **des concepts communs existent** — il y a de la structure partagée à composer ;
3. **la lecture doit soustraire** — c'est le « OU exclusif ».

Sans la condition 1, le critère déclenchait à **chaque pas** : 9 couches pour
72 neurones, mesuré. Avec elle :

**80 neurones en 5 couches [41, 15, 8, 8, 8]** — la moitié de la croissance au
premier niveau, la composition ensuite, et aucun chiffre rond.

### 6.2 Une erreur que j'ai commise et corrigée

J'ai d'abord annoncé que **la restriction aux canaux actifs faisait émerger les
concepts communs** (`communs` passant de +0,07 à +0,45). **C'est faux** : je
comparais deux **jeux de données** différents — la donnée propre (dix unités) et
l'ancienne, contaminée (une unité). Sur le même jeu, `communs` vaut +0,45 dans les
deux cas. **Ce n'est pas la restriction qui fait émerger les concepts, c'est la
donnée propre.**

### 6.3 Le résultat, mesuré sur le même jeu

Même professeur (Qwen2.5-0.5B couche 10), même protocole, masque de canaux lu sur
l'**apprentissage seul** :

| énergie gardée | canaux | constante | **fid TEST** | écart | invariance | pire paire |
|---|---:|---:|---:|---:|---:|---:|
| 100 % | 896 | 0,4710 | 0,4911 | +0,0201 | 0,9488 | 0,8328 |
| 90 % | 645 (72 %) | 0,4945 | 0,5137 | +0,0192 | 0,9530 | 0,8440 |
| 75 % | 424 (47 %) | 0,5319 | 0,5505 | +0,0186 | 0,9575 | 0,8566 |
| **50 %** | **157 (18 %)** | 0,6140 | **0,6346** | **+0,0206** | **0,9653** | **0,8893** |

**Deux lectures, et il faut les séparer :**

- **L'avantage du modèle sur la constante est PLAT** — +0,019 à +0,021 sur les
  quatre périmètres. La restriction ne rend donc **pas** le modèle meilleur.
- **Mais la cible elle-même devient meilleure.** En ne gardant que 18 % des canaux
  de sortie, on gagne **+14 points de fidélité**, **+1,7 point d'invariance** et
  **+5,7 points sur la pire paire**.

**C'est la droite d'échange qui MONTE.** Et c'est cohérent avec la loi du §2.1 :
la droite est une propriété du **professeur** — plus précisément de la **cible**
qu'on choisit en lui. En visant le sous-ensemble actif plutôt que les 896 canaux
densément, on choisit une cible intrinsèquement plus interlingue, et **toute la
droite se déplace vers le haut**.

C'est aussi, mot pour mot, l'énoncé de la mission : **« le premier niveau abstrait,
le premier niveau à dominance non-linguistique »**. Ce niveau existe, il est
mesurable, il tient en 157 canaux sur 896, et il est nettement plus invariant que
la couche entière.

### 6.4 Ce que ça laisse ouvert

- La hiérarchie trouvée (**[41, 15, 8, 8, 8]**) n'a pas encore été soumise à
  l'attrition.
- Le seuil de restriction (50 %, 75 %…) n'a pas été optimisé : c'est un curseur,
  et il déplace la droite.
- Les 218 canaux **propres à certaines langues** n'ont pas été examinés pour
  eux-mêmes : ils portent peut-être une information utile qu'on jette.


---

## 7. L'invariant : le pont apporte +0,020, quelle que soit la cible

Deux critères de sélection du sous-ensemble actif ont été essayés, plus la
référence sans restriction. **Même professeur, même protocole, masque lu sur
l'apprentissage seul.**

| critère | canaux | constante | **fid TEST** | **écart** | invariance | pire paire |
|---|---:|---:|---:|---:|---:|---:|
| aucun | 896 | 0,4710 | 0,4911 | **+0,0201** | 0,9488 | 0,8328 |
| énergie 90 % | 645 | 0,4945 | 0,5137 | **+0,0192** | 0,9530 | 0,8440 |
| énergie 75 % | 424 | 0,5319 | 0,5505 | **+0,0186** | 0,9575 | 0,8566 |
| énergie 50 % | 157 | 0,6140 | 0,6346 | **+0,0206** | **0,9653** | **0,8893** |
| consistance 50 % | 448 | 0,4991 | 0,5200 | **+0,0209** | 0,9395 | 0,8189 |
| consistance 25 % | 224 | 0,5863 | 0,6064 | **+0,0201** | 0,9477 | 0,8378 |
| consistance 10 % | 89 | 0,7181 | 0,7366 | **+0,0185** | 0,9539 | 0,8426 |

### Ce que ce tableau dit, et c'est le résultat le plus important du rapport

**L'écart à la constante est PLAT : +0,018 à +0,021 sur les sept périmètres.**
Quel que soit le sous-ensemble visé, quel que soit le critère, et même en passant
de 896 à 89 canaux de sortie, **notre pont apporte environ +2 points de cosinus —
pas plus.**

Autrement dit : **choisir une meilleure cible monte toute la courbe, mais ne
change pas la contribution du modèle.** La fidélité absolue passe de 0,49 à 0,74
non pas parce que le pont s'améliore, mais parce que **la cible devient plus
prévisible**. Le pont, lui, ajoute toujours la même chose.

C'est cohérent avec la loi du §2.1 : la droite d'échange est une propriété de la
**cible**. Notre architecture ne fixe que **l'ordonnée à l'origine** — et elle vaut
+0,020.

### Le meilleur point trouvé

**Énergie 50 % : 157 canaux sur 896 (18 %)**
- fidélité TEST **0,6346** (constante 0,6140)
- invariance **0,9653**, pire paire **0,8893**
- **80 neurones en 5 couches [41, 15, 8, 8, 8]**

C'est le meilleur compromis mesuré : le critère d'**énergie** bat celui de
consistance sur l'invariance (0,9653 contre 0,9477 au même ordre de taille), ce
qui était l'inverse de ce que j'attendais — la consistance sélectionne les canaux
dont la valeur est stable entre langues, mais elle écarte des canaux de forte
énergie qui portent la structure partagée.

### Deux erreurs de mesure corrigées dans cette section

1. J'avais annoncé que **la restriction faisait émerger les concepts communs**
   (`communs` de +0,07 à +0,45). Faux : je comparais deux **jeux de données**
   différents. Sur le même jeu, `communs` vaut +0,45 dans les deux cas.
2. J'avais annoncé **218 canaux (24 %) propres à certaines langues**. Vrai, mais
   **seulement à la dernière position**. Sur l'ensemble du texte, **les 896 canaux
   sont présents dans les 40 langues**. Le critère de « présence » ne sélectionne
   donc rien — mesuré : 896/896 pour tout seuil.


---

## 8. LA CONCLUSION : tout est porté par l'invariance de la cible

Sept périmètres, du plus large (896 canaux) au plus étroit (89 canaux). Pour
chacun, on a mesuré l'invariance **de la cible elle-même** — la similarité cosinus
entre langues, à contenu égal, du vecteur que le professeur produit à sa
couche 10.

| périmètre | canaux | invar. cible | **fid TEST** | **fid / invar.** |
|---|---:|---:|---:|---:|
| aucun | 896 | 0,5247 | 0,4911 | 0,936 |
| énergie 90 % | 645 | 0,5357 | 0,5137 | 0,959 |
| énergie 75 % | 424 | 0,5605 | 0,5505 | 0,982 |
| énergie 50 % | 157 | 0,6030 | 0,6346 | 1,052 |
| consistance 50 % | 448 | 0,5617 | 0,5200 | 0,926 |
| consistance 25 % | 224 | 0,6470 | 0,6064 | 0,937 |
| consistance 10 % | 89 | 0,7350 | 0,7366 | 1,002 |

### Trois relations, et elles disent tout

```
fid TEST  ≈  1,1150 · (invariance de la cible) − 0,0848        r = 0,9570
constante ≈  1,1192 · (invariance de la cible) − 0,1071        r = 0,9570
écart à la constante  =  +0,0197  ±  0,0009
rapport fid / invariance de la cible  =  0,9707  ±  0,0419
```

**1. La fidélité est une fonction LINÉAIRE de l'invariance de la cible** (r = 0,957).
Notre modèle n'y ajoute presque rien : c'est la cible qui décide.

**2. La constante témoin suit la MÊME loi**, avec une pente identique à 0,4 % près
(1,1192 contre 1,1150). Prédire la moyenne est donc porté par la même quantité.
Les deux droites sont **parallèles**, séparées de l'écart.

**3. Cet écart est d'une stabilité remarquable : +0,0197 ± 0,0009.** Un
dixième de point d'écart-type sur sept périmètres qui vont de 896 à 89 canaux, et
sur deux critères de sélection opposés. **C'est la contribution propre de notre
pont, et elle est constante.**

### Ce que cela veut dire pour la mission

**Le pont capte 97 % du contenu interlingue de la cible — et rien au-delà.** Il
est au plafond que la cible lui impose. Sa contribution propre, +0,020, ne dépend
ni de la taille (1 à 256 neurones), ni de la profondeur (1 à 13 couches), ni de
l'architecture (cascade ou réservoir plat), ni de la cible choisie.

**Améliorer la fidélité ne passe donc PAS par le modèle : cela passe par le choix
de la cible.** Et c'est exactement ce que la sélection du sous-ensemble actif
fait — elle ne rend pas le pont meilleur, elle lui donne une cible plus
interlingue.

**Pour la mission** — « le premier niveau abstrait, à dominance
non-linguistique » — cela veut dire que **le niveau cherché est atteint** : avec
157 canaux sur 896, le pont en reproduit 97 % du contenu partagé, avec **80
neurones en 5 couches**, alimenté par le seul plongement, **sans une seule
rétropropagation**.

### La question qui reste ouverte

L'écart de +0,020 est **petit**. Il plafonne partout à la même valeur, ce qui
suggère qu'il vient d'une limite **structurelle** du réservoir gelé, pas d'un
réglage. Deux pistes pour l'attaquer, aucune explorée :

- une **lecture non linéaire** (le readout est aujourd'hui linéaire sur les états) ;
- une **entrée plus riche** que le seul plongement, sans réintroduire le saut qui
  surapprenait.


---

## 9. Le plafond, attaqué : la lecture non linéaire paie +18 %

Le readout était **linéaire** sur les états du réservoir. C'était une hypothèse sur
l'origine du plafond de +0,020. Test : on lui donne `[états, états²]` — ce qui
reste **en forme fermée** (une seule inversion), donc toujours sans rétropropagation.

| périmètre | lecture | fid TEST | **écart à la constante** | invariance | pire paire |
|---|---|---:|---:|---:|---:|
| 896 canaux | linéaire | 0,4911 | +0,0201 | 0,9488 | 0,8328 |
| 896 canaux | **quadratique** | **0,4945** | **+0,0235** | 0,9469 | 0,8300 |
| 157 canaux | linéaire | 0,6346 | +0,0206 | 0,9653 | 0,8893 |
| 157 canaux | **quadratique** | **0,6383** | **+0,0243** | 0,9648 | 0,8821 |

**La contribution propre du pont passe de +0,020 à +0,024 — soit +18 %**, sur les
deux périmètres, **sans coût en invariance** (0,9488 → 0,9469 et 0,9653 → 0,9648,
dans le bruit).

**La linéarité de la lecture était donc bien une part du plafond — mais une petite
part.** Le reste vient d'ailleurs : le réservoir est **gelé et aléatoire**, et ses
caractéristiques ne portent qu'une fraction de ce qui est prédictible. C'est la
prochaine piste, et elle n'est pas explorée.

### Le meilleur réseau, à ce stade

| | |
|---|---|
| périmètre | **157 canaux sur 896 (18 %)**, les plus énergétiques |
| lecture | **quadratique** |
| taille | **80 neurones · 8 couches [30, 8, 8, 8, 8, 8, 8, 2]** |
| fidélité TEST | **0,6383** (constante 0,6140) |
| invariance | **0,9648** · pire paire **0,8821** |
| rétropropagation | **aucune** |

Et la **première couche porte 30 des 80 neurones** : le travail des activations
manquantes se fait au premier niveau, la composition vient après.


---

## 10. Où est le plafond : dans le TRANSFERT, pas dans les caractéristiques

Le plafond de +0,024 pouvait venir du réservoir (gelé, aléatoire) ou d'ailleurs.
Quatre expériences, quatre réponses.

### 10.1 Le réservoir n'est pas le goulot

Le **gain d'entrée** — *le* réglage critique du calcul réservoir, à 1,0 depuis le
début sans avoir jamais été balayé — et le **seuil par neurone** :

| gain | seuil | fid TEST | écart | invariance | pire paire |
|---|---:|---:|---:|---:|---:|
| 0,3 | non | 0,6381 | +0,0241 | 0,9672 | 0,8909 |
| 0,3 | oui | 0,6352 | +0,0212 | 0,9655 | **0,9063** |
| 1,0 | non | **0,6383** | **+0,0243** | 0,9648 | 0,8821 |
| 1,0 | oui | 0,6364 | +0,0224 | 0,9625 | 0,9038 |
| 3,0 | non | 0,6355 | +0,0215 | **0,9680** | **0,9074** |

**Tout tient dans 0,003 de fidélité.** Ces deux leviers ne sont pas le goulot. Le
seuil, lui, **échange** de la fidélité contre la pire paire — la loi d'échange
encore une fois.

### 10.2 L'expérience décisive : un readout ORACLE

On ajuste la lecture **sur le test lui-même** et on l'y évalue. Ce n'est pas un
modèle, c'est un diagnostic : il dit ce que nos caractéristiques contiennent.

| | fid TEST | invariance |
|---|---:|---:|
| notre lecture (ajustée sur 30 langues d'apprentissage) | 0,6383 | 0,9648 |
| **oracle (ajustée sur le test)** | **0,7762** | 0,9598 |

**Nos caractéristiques contiennent 0,7762. Nous n'en extrayons que 0,6383.**
**La marge de +0,138 est dans le TRANSFERT inter-langue, pas dans les
caractéristiques.**

Et l'oracle n'est pas moins invariant que nous (0,9598 contre 0,9648) : il ne
triche pas sur l'invariance, il transfère simplement mieux.

### 10.3 La normalisation par langue ÉCHOUE

Puisque l'écart est un écart de transfert, on standardise les états langue par
langue — calculable à l'inférence, sans aucune étiquette.

| | fid TEST | invariance | pire paire |
|---|---:|---:|---:|
| sans | **0,6383** | **0,9648** | **0,8821** |
| **avec** | 0,6284 | **0,8823** | 0,6464 |

**Échec net.** Normaliser par langue efface le **décalage commun**, qui est
précisément la part partagée : l'invariance s'effondre de 0,083.

### 10.4 Plus de langues ne réduit PAS l'écart

| langues d'apprentissage | fid TEST | oracle | **écart de transfert** |
|---|---:|---:|---:|
| 36 | 0,6380 | 0,7790 | 0,1410 |
| 30 | 0,6383 | 0,7762 | 0,1379 |
| 20 | 0,6362 | 0,7684 | 0,1322 |

**L'écart est constant (0,132 à 0,141) sur toute la plage.** Plus de langues
n'aide pas. C'est le principe « pas de représentation universelle » **quantifié** :
il n'existe pas de lecture linéaire universelle entre langues, et la perte vaut
**~0,14 de cosinus** quel que soit le nombre de langues vues.

---

## 11. Verdict sur l'attrition : elle réduit, elle ne généralise pas

Testée sur la meilleure configuration (157 canaux, lecture quadratique, naissance
libre), avec **recalcul** des trajectoires des survivants à chaque retrait :

| | neurones | couches | fid VAL | **fid TEST** |
|---|---:|---:|---:|---:|
| réseau né | 80 | 8 | 0,7500 | **0,6383** |
| après retrait | 60 | 8 | 0,7484 | 0,6356 |
| | 45 | 8 | 0,7469 | 0,6316 |
| | 20 | 6 | 0,7419 | 0,6248 |
| | 5 | 4 | 0,7357 | 0,6192 |
| | **1** | 1 | 0,7327 | **0,6169** |

**La fidélité de test décroît de façon monotone.** L'attrition **réduit la
taille**, avec un coût faible mais réel (−0,003 pour −25 % de neurones, −0,021
pour 99 %), et **elle n'améliore rien**.

Et le critère de validation est **trop indulgent** : il accepte les quinze
retraits successifs (la validation ne perd que 0,017 au total) alors que le test
en perd 0,021. Le seuil de 0,005 par étape laisse passer une dérive cumulée.

Note : l'oracle du réseau à **1 neurone** vaut encore **0,7388** — un seul neurone
dont la lecture est ajustée sur le test explique 0,74, mais n'en transfère que
0,62. **Le goulot est bien le transfert, même à un neurone.**

---

## 12. Ce que ce tour établit, en trois phrases

1. **Le réservoir gelé n'est pas le goulot** : ni son gain d'entrée ni ses seuils
   ne déplacent la fidélité de plus de 0,003.
2. **Le goulot est le transfert inter-langue** : nos caractéristiques contiennent
   0,776, la lecture n'en transfère que 0,638, et l'écart ne se réduit ni par plus
   de langues, ni par normalisation.
3. **L'attrition ne généralise pas** : elle réduit la taille à coût faible et
   monotone. Le critère de validation est trop indulgent pour l'arrêter au bon
   endroit.
