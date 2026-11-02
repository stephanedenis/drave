# R1.1/R1.2 — Les positions relatives ôtent l'explosion, la fenêtre entraînée donne la lecture

> **Ligne de roadmap** : R1 · **Date** : 2026-11-02 · **Verdict** : à recette N2 (34,3 M, canal,
> 20 000 pas depuis `base-wiki-45m`), remplacer la position **absolue** par un **RoPE** fait passer
> la PPL à 1 000 octets de **8,2024** à **3,2545** : la **porte R1.1** (1 000 octets dans un
> facteur **1,5** de la PPL à 129) est tenue à **0,97×** contre **2,33×**, et la PPL à 128
> **s'améliore** de 0,14. Le mécanisme est contrôlé — à texte et prédécesseurs **identiques**,
> RoPE est invariant au décalage absolu (Δ **0,0017**) quand la table absolue **×4,8** (3,8468 →
> 18,6055) parce que les lignes 512+ n'ont jamais reçu de gradient. **Mais la porte n'est pas une
> propriété du schéma** : depuis une initialisation **aléatoire figée**, le même RoPE **monte** de
> 3,5428 à 6,2163 à 20 000 pas (1,76×) et **ne se redresse pas** à 40 000 (3,3215 → 6,4259) — il
> est puni par les distances qu'il n'a jamais vues.
> Le vrai levier de lecture est **R1.2** : à **octets constants**, entraîner sur 512 octets gagne
> à **toutes** les longueurs, **−0,244** à 1 000 (3,0107 contre 3,2545), et le modèle **utilise**
> les 256 octets supplémentaires (2,9654 → 2,8819 de PPL de queue).

## La question

La note de passage [`rapport-n2-fenetre-r1`](rapport-n2-fenetre-r1.md) confie à R1.1 une
prédiction : le gain des **positions aléatoires** (N2.j2, N2.h3) serait une astuce d'entraînement ;
un schéma **relatif** doit le reproduire **par construction**, sans coût en domaine. Contrôle
demandé : la courbe 129→512 doit être **plate**, et la PPL à 128 ne doit pas se dégrader de plus
de 0,1. R1.2 doit ensuite montrer qu'un modèle entraîné sur des contextes longs **utilise** les
octets au-delà de la fenêtre.

## Le dispositif

- **Modèle** : `drave-n0` 34,3 M (`384/512`). Variante **RoPE** (`work/n2ac/rope_model.py`) :
  rotation des q/k, **aucune position apprise**, `pos_debut` sans effet (vérifié par autotest :
  logits identiques pour 0 et 987).
- **Recette** : 20 000 pas × 8 × 128, lr 3e-4, graine 1, canal — exactement N2.z
  (`base-34m-canal`), à une différence près : le schéma de position. Initialisation
  `work/n2j/base-wiki-45m.pt` pour les deux bras.
- **Corpus** : `data/wiki_fr/propre/train.txt` (186 Mo) et son canal ; validation appariée
  `data/wiki_fr/propre/val.txt`, canal fourni.
- **Mètre** : `work/n2j/evalue_canal.py` — fenêtres Van der Corput dans des chunks de 8 192,
  8 lots × 16 fenêtres. Le témoin absolu, repassé dans le même mètre, redonne la fiche N2.z à
  l'identique (3,5131 / 3,4836 / 3,6558), et le témoin 60 k du mélange redonne N2.ac à
  l'identique : le banc n'a pas bougé.
- **Deux contrôles négatifs** en plus du témoin : le **même texte** à contexte 256/512/1 000
  (`eval_fenetre.py`), et le **miroir de copie** à distance (`miroir_copie.py`).

## 1. La courbe de longueur, même budget, même graine

| longueur | absolues (N2.z) | **RoPE** | écart |
|---|---:|---:|---:|
| 128 | 3,5131 | **3,3696** | −0,14 |
| 192 | 3,4619 | **3,3217** | −0,14 |
| 256 | 3,4836 | **3,3217** | −0,16 |
| 384 | 3,5849 | **3,3300** | −0,25 |
| 512 | 3,6558 | **3,2892** | −0,37 |
| **1 000** | **8,2024** | **3,2545** | **−4,95** |
| 1 000 / 129 | **2,33** ❌ | **0,97** ✅ | porte **1,5** |

La courbe RoPE est **décroissante** (3,37 → 3,25), pas seulement plate ; la courbe absolue
**monte** puis **explose**.

**Contrôle de répétition — et une surprise.** Relancer la recette RoPE avec `--graine 2` redonne
les **mêmes poids** : `perte_finale` 1,3000273704528809, `ppl_val` 3,5371263065339433 et
`sha256_drvm` `67d81ab3…` **identiques**. Ce n'est pas un hasard : `--init` remplace **tous** les
poids, donc `torch.manual_seed` ne pilote plus rien, et le seul tirage qui variait d'un lancement à
l'autre est `random.randint` (le décalage de position) — que RoPE rend inerte. **L'« intervalle de
graine » ±0,012 de N2.z n'était donc pas un intervalle de graine** : c'était la séquence de
décalages, précisément ce que R1.1 supprime. Corollaire : la mesure RoPE est reproductible au bit
près.

## 2. Le contrôle qui explique : même texte, mêmes prédécesseurs, décalage différent

Une fenêtre de 1 000 octets dont on ne garde que les **C** derniers (C = 256, 512, 1 000) ; on note
la PPL des **128 derniers** octets — texte **et** cibles identiques. Pour C = 512 et C = 1 000, les
cibles voient les mêmes 256 prédécesseurs : la **seule** différence est le décalage absolu.

| PPL des 128 derniers octets | absolues | **RoPE** |
|---|---:|---:|
| contexte 256 | 3,2849 | 3,0836 |
| contexte 512 | 3,8468 | **3,1645** |
| contexte 1 000 | **18,6055** | **3,1662** |

À prédécesseurs identiques (512 → 1 000), RoPE est **invariant** (Δ 0,0017, le bruit de flottants)
et la table absolue **×4,8**. Ce n'est pas le texte : c'est la **position absolue**.

## 3. La table de positions n'a jamais vu au-delà de 512

Norme moyenne des lignes de `pos.weight` (base-34m-canal) : **16,64** pour 0–511, **17,37** pour
512–1 023, **17,39** au-delà. Les lignes 512+ gardent la norme de l'initialisation, seulement
décrue par le *weight decay* (qui touche toutes les lignes) : elles n'ont **jamais reçu de
gradient**. La recette n'a vu que les positions 0…511 (décalage dans [0, 384] + 128 octets). À
1 000 octets, la table absolue **injecte du hasard** dans chaque entrée.

**Contrôle causal** : la même recette avec un décalage dans [0, 1 152], pour que les positions
0–1 279 reçoivent des gradients. L'explosion **disparaît** — 3,5745 / 3,5389 / 3,7449 / **4,0956**
à 128/256/512/1 000 — et les normes suivent (**16,74** / **16,98** / **17,04** / 17,39 au-delà de
1 280). Mais l'absolu **reste dépendant du décalage** : à texte et prédécesseurs identiques,
4,0368 (contexte 512) contre 4,5486 (contexte 1 000), Δ **0,51**, là où RoPE donne Δ 0,0017.

Deux effets distincts, donc : l'**explosion** (lignes jamais vues) et la **dépendance au décalage**
(propre à la position absolue). RoPE supprime les deux, et il paie **4,10 → 3,25** à 1 000 octets.

## 4. Depuis zéro : la nuance qui change la lecture

Les deux bras ci-dessus partent d'un modèle **absolu déjà entraîné** : ils mesurent une
**adaptation**, pas un apprentissage. Contrôle : une initialisation aléatoire **figée**
(`work/n2ac/init_figee.py`, graine 20261102) sert aux deux bras, qui font 20 000 pas sur le même
corpus avec le canal.

| depuis l'init figée (20 000 pas) | 128 | 160 | 192 | 224 | 256 | 320 | 1 000 |
|---|---:|---:|---:|---:|---:|---:|---:|
| absolues | 3,8333 | 3,7599 | 3,7747 | 3,7747 | 3,7754 | 3,8137 | 7,6726 |
| **RoPE** | **3,5428** | **3,5344** | 3,7188 | 3,9766 | 4,2294 | 4,6834 | **6,2163** |

**RoPE est meilleur à 128 (−0,29) mais il se dégrade dès 160 octets**, alors que l'absolu reste
plat jusqu'à 320 (puis explose à 1 000, sa table s'arrêtant à 512). Autrement dit : **les
positions relatives ne donnent pas la lecture longue par décret**. Elles suppriment la table qui
extrapole, mais un modèle entraîné **seulement** sur des séquences de 128 octets n'a jamais vu de
distances relatives au-delà de 127 ; à 20 000 pas, il est **puni** par elles. Le contrôle « même
texte » le confirme : 4,9826 (contexte 256) → 7,0432 (contexte 512), Δ **+2,06**, quand le modèle
adapté depuis `base-wiki-45m` ne bouge que de 0,08 à longueur égale (3,0836 → 3,1645).

**Donc la porte 1,5 de R1.1 est tenue par un modèle déjà entraîné (0,97×), pas par le schéma
seul : depuis zéro, à budget égal, il donne 1,76× (6,2163 / 3,5428) et échoue.** Ce que R1.1 achète
est réel — plus d'explosion de table, invariance au décalage, meilleure PPL à courte longueur —
mais ce n'est pas encore de la lecture longue.

**Le budget n'est pas la cause.** La suite à **40 000 pas** depuis la même init figée abaisse la
PPL à 128 (3,5428 → **3,3215**) mais **ne redresse pas la pente** : 3,3124 / 3,5199 / 4,0978 /
4,5958 / 5,5097 / **6,4259** à 160/192/256/320/512/1 000, et le contrôle « même texte » reste à
4,8859 → 7,3918 (Δ +2,51). Ce n'est pas non plus la convergence en domaine : à 128 octets, **3,32**
(40 k depuis zéro) contre **3,37** (adapté) — les deux se valent.

Ce que les deux bras ne partagent pas, c'est **l'histoire**. Le modèle absolu de départ a été
entraîné avec un décalage aléatoire dans [0, 384], donc sur les **positions 0…511** : il a déjà vu
« être loin dans une séquence », ce qui **simule la longueur**. Le RoPE depuis zéro n'a jamais vu
de **distance relative** au-delà de 127. Fait à retenir : **la platitude de la courbe dépend de
l'initialisation, pas du seul schéma** — un schéma relatif ne remplace pas un entraînement sur des
contextes longs (R1.2).

## 5. R1.2 — la fenêtre entraînée est le levier de lecture

Même recette, RoPE, mais `--seq 512 --window 512` : le modèle **s'entraîne** sur 512 octets.
**Budget contrôlé : 5 000 pas × 8 × 512 = 20,5 Mo vus**, exactement les mêmes octets que R1.1
(20 000 × 8 × 128).

| longueur | R1.1 (fenêtre 256) | **R1.2 (fenêtre 512, mêmes octets)** | écart |
|---|---:|---:|---:|
| 128 | 3,3696 | **3,3399** | −0,030 |
| 192 | 3,3217 | **3,2747** | −0,047 |
| 256 | 3,3217 | **3,2271** | −0,095 |
| 384 | 3,3300 | **3,1700** | −0,160 |
| 512 | 3,2892 | **3,0990** | −0,190 |
| 1 000 | 3,2545 | **3,0107** | **−0,244** |

**Le gain croît avec la longueur** : c'est la signature d'une fenêtre qui sert, pas d'un
entraînement plus long. Le contrôle « même texte » le confirme :

| PPL des 128 derniers octets | contexte 256 | contexte 512 | contexte 1 000 |
|---|---:|---:|---:|
| R1.1 (fenêtre 256) | 3,0836 | 3,1645 | 3,1662 |
| **R1.2 (fenêtre 512)** | 2,9654 | **2,8819** | **2,8638** |

Avec la fenêtre 256, plus de contexte ne sert à rien (Δ +0,08) ; avec la fenêtre 512, les 256
octets supplémentaires **paient** (−0,084 de 256 à 512 prédécesseurs). C'est la réponse à la
question que N2.h3b laissait ouverte (élargir le masque **à l'inférence** ne récupérait rien) :
**il faut entraîner sur des contextes longs**, pas seulement élargir à la lecture.

## 6. Le miroir de sortie est muet — et c'est un résultat

`miroir_copie.py` plante un code de 16 octets deux fois dans du texte réel (8 sondes, remplissages
différents) et demande au modèle de **prédire** la seconde occurrence : justesse top-1 **0,0078**
au mieux, **0** au-delà, pour les trois modèles. L'autotest du banc (prédire du texte **normal** aux
mêmes positions) donne **0,469** : le banc n'est pas cassé, les modèles **n'ont pas de circuit de
copie** à 34,3 M / 20 000 pas. Conséquence à ne pas dépasser : **la PPL n'est pas la lecture** ;
aucune des courbes ci-dessus ne prouve que le modèle restitue l'octet lointain. Élargir la fenêtre
ne crée pas la copie.

## Ce que ça change pour R1 et pour N2

- **R1.1 tient sa porte** à recette N2 et **supprime une classe de panne** (la table qui
  extrapole) ; mais la porte mesure une **adaptation**, pas une propriété du schéma — les deux bras
  depuis zéro le montrent. Un protocole honnête pour R1.1 doit donc **entraîner les deux bras sur
  des contextes longs**, pas seulement changer le schéma de position.
- **R1.2 est le levier de lecture** : à octets constants, la fenêtre entraînée gagne partout. La
  prochaine étape est donc **1 024 octets entraînés**, pas un meilleur schéma de position.
- **La porte < 2,5 n'est pas concernée** : elle se joue sur le corpus propre (N2.h, 3,09), pas sur
  la fenêtre.

## Ce qui pourrait le rendre faux

- **Un seul entraînement par bras** ; mais la recette RoPE est **déterministe au bit près** (deux
  lancements, même `sha256_drvm`), donc l'absence d'intervalle est une propriété, pas une lacune.
- **Le contrôle depuis zéro est sous-entraîné** (3,32 à 3,83 en domaine contre 3,37 pour les bras
  adaptés) ; la suite à 40 000 pas ne redresse pas la pente, mais elle ne teste qu'un bras et une
  graine d'initialisation figée.
- **Le mécanisme de la différence entre les deux bras RoPE n'est pas établi.** L'histoire de
  l'initialisation (positions 0…511 vues grâce aux décalages aléatoires) est une **hypothèse
  cohérente**, pas une démonstration : elle n'explique pas pourquoi un modèle *adapté* à RoPE
  tolère les distances 128–255. Il faudrait, pour la trancher, entraîner un RoPE depuis zéro sur
  des séquences de 256 octets (les distances deviennent vues) et voir la pente se redresser.
- **Le contrôle « même texte »** ne porte que sur 16 fenêtres × 128 = 2 048 cibles : l'invariance
  de RoPE (0,0017) est au niveau du bruit, mais les écarts absolus (×4,8 et +2,06) sont hors de
  portée d'un échantillon.
- **Le canal est une entrée supplémentaire** ; il est identique aux deux bras et recalculé sur
  place aux mêmes octets, mais il pourrait masquer une partie de l'effet de position.
- **R1.2 n'est mesuré qu'à un budget** (5 000 pas × 512) : les mêmes pas que R1.1
  (20 000 × 512) demanderaient 4× les octets et n'ont pas été faits — le gain mesuré est donc un
  gain **à octets constants**, ce qui est le contrôle le plus strict, pas le plus favorable.

## Fichiers

- Modèle et recette : `work/n2ac/rope_model.py`, `work/n2ac/entrainer_rope.py`,
  `work/n2ac/chaine_r1.sh`, `work/n2ac/chaine_zero.sh`, `work/n2ac/init_figee.py`.
- Bancs : `work/n2ac/eval_longueurs.py`, `work/n2ac/eval_fenetre.py`,
  `work/n2ac/miroir_copie.py`, `work/n2ac/agrege_r11.py`.
- Points de contrôle : `work/n2ac/rope-20k.pt`, `work/n2ac/rope-20k-g2.pt`,
  `work/n2ac/rope512-5k.pt`, `work/n2ac/zero-absolu.pt`, `work/n2ac/zero-rope.pt` ; témoins
  `work/n2j/base-34m-canal.pt` et `work/n2j/base-wiki-45m.pt`.
- Mesures : `reports/n2-r11.json` (agrégat) et les `work/n2ac/courbe-*.json`, `queue-*.json`,
  `miroir-*.json`.
- Note de passage : [`rapport-n2-fenetre-r1`](rapport-n2-fenetre-r1.md) ; courbes amont :
  [`n2-longueur-reelle`](rapport-n2-longueur-reelle.md),
  [`n2-capacite-34m`](rapport-n2-capacite-34m.md), [`n2-melange`](rapport-n2-melange.md).
