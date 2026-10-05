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
