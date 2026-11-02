# La nuit N2 — du corpus propre au corpus réel

> Récit de la session `0b0a6a0d` (N2) dans la nuit du 1er au 2 novembre. Les fiches portent les
> chiffres ; ce fichier dit l'enchaînement et ce qui a été appris en chemin.

**Le problème de départ.** N2 mesurait sur un jeu contaminé (32,8 % de validation dans
l'entraînement). La première moitié de la nuit a reconstruit le mètre : corpus dédupliqué
(`corpus_propre.py`), chaîne refaite (professeur, base, distillation × 3), porte honnête **3,09** —
pas 2,85 — et profil hors domaine **16,70**. Puis les leviers : diversité (16,70 → 3,85), positions
aléatoires (256 octets 14,11 → 3,25), décomposition (tête du 6e bloc avant la boucle : 3,05 contre
3,12), capacité (−0,06, peu), combinaison des deux (3,47 / 4,10 / 3,49).

**Le tournant.** Le recensement a dit : il y a **27,7 Mo** de français unique dans le dépôt, mais
surtout **132 Go de Wikipédia** sur le disque. L'inventaire local a donné le corpus réel : 120 000
articles, 186 Mo d'entraînement, 0 fuite. La base passe de 12,29 à **7,42** en littérature et de
32,90 à **12,41** en anglais (×1,7 à ×2,6). Le corpus élargi du dépôt (N2.i) avait déjà montré la
direction ; le corpus réel l'a confirmée.

**Les lois qui se dégagent.**
- **La donnée avant la capacité** : 21,65 M ne gagnait que −0,06 sur 3,24 Mo (N2.h5) et gagne
  −0,19 sur 186 Mo (N2.j3). Un modèle plus gros a besoin de plus de texte pour amortir ses
  paramètres.
- **La position est un défaut d'architecture** : le verrou de longueur tombe à l'échelle (256 :
  9,28 → 4,49 ; 512 : 13,37 → 5,67) pour +0,36 en domaine.
- **La distillation transporte, elle ne crée pas** : −0,5 PPL sur une langue seule (3,88 en
  français, 3,94 en anglais), mais deux fois moins en multilingue (5,41) parce que le professeur a
  la même dilution.
- **La structure peut s'ajouter au texte** : un canal de 6 classes par octet (1 344 paramètres)
  donne −0,22 de PPL — modeste, mais réel, et le placebo (canal mélangé) est *pire* que l'absence
  de canal. En revanche, le canal ne rend pas le modèle robuste au mélange des lettres : il reste un
  lecteur de lettres.

**Ce qui n'a pas marché, et qui est écrit.**
- Filtrer les phrases **non ambiguës** : 15 à 30 % des phrases, les courtes, et un transfert moins
  bon qu'un témoin aléatoire de même taille ; en curriculum, tout baisse légèrement.
- La **capacité** sur le petit corpus : −0,06 seulement.
- La **typoglycémie** ne s'améliore pas avec le canal (×5,6 partout).

**Ce qui reste ouvert.** La **fenêtre locale de 256 octets** est le plafond de longueur (5,7 à 512
sur le corpus réel, 6,35 en anglais) ; la distillation du canal (tuée par la pression mémoire) ; la
loi d'échelle multilingue à 21,65 M ; et la restitution (R31), qui n'est toujours pas construite.

**Les commits de la nuit** : `e36e8185` (N2.h), `52cf5853` (combinaison), `3a6ae9ca` (capacité),
`d2613e8f` (fenêtre), `18f28437` (recensement), `17ececfc` (corpus élargi), `c96eb475` (corpus
réel), `4db5aac0` (longueur réelle), `1520b875` (capacité réelle), `7a083904` (canal),
`0e5c89be` (distillation réelle), `e0e71213` (anglais), `902349b0` (anglais distillé),
`…` (multilingue distillé), `fa1b74a4` (structures).

## La seconde moitié : les lois

Après le corpus réel, la nuit a cherché les **lois** — et elles sont venues, dans l'ordre :

**La capacité paie quand les données suivent.** 11,47 M → 21,65 M → 34,3 M sur 186 Mo :
4,3893 → 4,2013 → **3,9973**, soit **−0,19 par palier**, sans rendement décroissant. Et le gain
n'est pas que le domaine : à 512 octets, 5,67 → 5,03 → **4,19** ; la courbe de longueur s'aplatit
avec la taille. Le « verrou » de longueur est donc aussi une affaire de capacité, pas seulement de
positions.

**La distillation se compose avec tout.** Sur 11,47 M : 3,88 ; sur 34,3 M : **3,69** — le meilleur
modèle de la nuit (6,78 en littérature, 10,92 en anglais, 4,10 à 512). Un professeur **plus petit**
que l'élève suffit : les étiquettes douces régularisent, l'élève a la capacité de les exploiter.

**L'anglais suit la même loi.** Base 4,42 → distillé 3,94 ; la chaîne est portable d'une langue à
l'autre, et le plafond de longueur aussi (4,19 à 512 pour le 34,3 M français).

**Le multilingue paie la dilution, et la capacité l'adoucit.** À recette égale, 11,47 M → 21,65 M
→ 34,3 M en français multilingue : 6,68 → 5,89 → **5,58** — le rendement décroît (première
saturation de la loi). La distillation multilingue (5,41) ne récupère pas la dilution parce que le
professeur a la même. À paramètres égaux, un modèle par langue reste devant (3,69 contre 5,58).

**La structure en entrée aide un peu.** Le canal de 6 classes par octet (1 344 paramètres) donne
−0,22 de PPL ; le placebo est *pire* que l'absence de canal ; mais la robustesse au mélange est
identique. C'est un prior, pas une lecture de formes.

**Ce que le meilleur modèle écrit.** Du français grammatical — mais en glouton il **boucle** sur
les gabarits wiki (« la commune de Saint-Germain-de-Commune… ») et à température 0,8 il **colle**
des fragments. Une PPL de 3,69 ne fait pas un rédacteur.

**Les portes.** Passe complète du 02/11 00 h 03 : **77 vertes, 4 rouges** — les quatre connues
(homeostasie, indice, mélange, réparti-moteur). Aucune régression.

## La fin de nuit : l'anglais, le professeur, la structure

**L'anglais suit le français, chiffre pour chiffre.** Base 34,3 M : 4,2396 ; distillée (2 graines) :
**3,7651**, avec 4,394 sur le banc anglais et **4,185 à 512 octets** — la même courbe plate que le
français (4,09). Les deux meilleurs modèles de la nuit : **français 3,685** (N2.r), **anglais
3,765** (N2.w), tous deux à 34,3 M distillé.

**Le professeur plus gros ne paie presque pas.** Un professeur de 30,29 M (au lieu de 23,57 M) donne
3,8888 en domaine (3,8761) et gagne 0,3 hors domaine (N2.u) : l'élève de 11,47 M a saturé sa
capacité. Pour gagner en domaine, il faut doubler l'élève, pas le professeur.

**Le multilingue sature.** À recette égale, le français multilingue passe de 6,68 (11,47 M) à 5,89
(21,65 M) puis 5,58 (34,3 M) : −0,79 puis −0,31, le premier rendement décroissant de la loi. La
distillation à 34,3 M (4,79) réduit l'écart au monolingue (3,69) sans l'annuler.

**La structure.** L'analyseur du banc de structures retrouve **7/7** séquences de types et couvre
**93,9 %** des octets des structures écrites à la main (après trois corrections : l'adverbe de
temps, le « qu'elle » élidé, la coordination). Le sous-projet est fusionné (pragmatique, export,
analyseur) avec **19 tests**.

**Ce qui reste ouvert** : la distillation du canal (relancée à 03 h 30), la fenêtre (R1, note de
passage écrite), et la restitution (R31) — toujours pas construite.

## Le meilleur modèle de la nuit

C'est le **34,3 M avec canal de structure** (N2.z) : **3,5131** en domaine, **3,4836** à 256,
**3,6558** à 512 octets. Le canal seul bat la distillation (3,6852) et la combinaison des deux
(3,5277, N2.y) : à capacité égale, **donner la structure en entrée** vaut mieux que **distiller un
professeur deux fois plus petit**. La courbe de longueur est la plus plate de la nuit (4 % de perte
à 512 octets).

Le canal était pourtant tranché à 11,47 M (N2.x : absorbé par la distillation). C'est le renversement
de la nuit : le levier dépend de la **taille** — la structure se paie quand le modèle a la capacité
de l'exploiter, et la distillation quand il ne l'a pas.

## Ce que la nuit laisse

- **Quatre lois** : les données (×1,7 à ×2,6 hors domaine), la capacité (−0,19 par palier, sature en
  multilingue), la distillation (−0,3 à −0,5, saturée par l'élève), la structure (−0,22 à −0,48,
  croît avec la capacité).
- **Un mètre honnête** : le corpus propre, 0 fuite, la porte < 2,5 à 0,59.
- **Deux meilleurs modèles** : français 3,51 (canal, 34,3 M), anglais 3,77 (distillé, 34,3 M).
- **Ce qui n'a pas marché** : le filtre non ambigu, le canal + KD, le professeur plus gros en
  domaine, la porte < 2,5.
- **Ce qui reste** : la fenêtre (R1), la restitution (R31), le corpus d'un autre ordre.
