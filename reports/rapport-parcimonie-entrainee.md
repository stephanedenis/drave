# La parcimonie entraînée — premier banc, et la loi du coût par événement

> 08/10. Premier essai de la phrase du `docs/programme-recherche.md` § 2 ter :
> **« la parcimonie ne s'impose pas, elle s'entraîne »**. Le dépôt n'avait
> jusqu'ici jamais entraîné un seul modèle (zéro rétropropagation dans `tools/`) :
> il imposait la parcimonie après coup, ou exécutait des modèles denses.
>
> Banc : `tools/essai_decharge.py`. Corpus : `tools/corpus_wikipedia.py`
> (100 Mo d'apprentissage, 2 Mo de validation, chapitres de validation retirés).

---

## 1. Ce que le banc compare, et pourquoi ces deux-là

Deux modèles de **mêmes formes et mêmes paramètres** :

| | dense (jumeau) | décharge |
|---|---|---|
| normalisation | LayerNorm | **normalisation par lot** (celle des SNN) |
| attention | softmax | **sans softmax**, Q/K/V discrets (Spikformer) |
| FFN | GELU | **Heaviside** de la pré-activation normalisée |
| résiduel | flottant | flottant, mais **toute entrée de couche linéaire est discrète** (Spikingformer) |
| entraînement | rétropropagation | **gradient de substitution** (sigmoïde rapide, α = 4) |

Le seuil vaut 1,0 **après** normalisation par lot : à l'initialisation, une
gaussienne centrée réduite dépasse 1,0 dans ~15,9 % de ses cas — le R̂ ≈ 0,15 de
SpikeGPT, obtenu sans le poser à la main.

Corpus lu en **octets UTF-8** (256 symboles) : pas d'alphabet à choisir, pas de
caractère inconnu, et la mesure (bits/octet) reste comparable d'un corpus à
l'autre. Le corpus Wikipedia complet porte 3 237 caractères distincts — un
embedding de cette taille coûterait plus cher que le reste du modèle.

Protocole : 20 000 pas, lot 32, séquence 128, AdamW, clip 1,0, **meilleur point
de validation conservé** (comparer deux modèles au pas final mesurerait la
vitesse de surapprentissage), deux taux d'apprentissage balayés.

---

## 2. Résultat — la parcimonie s'entraîne, et elle ne paie pas

dim 192, 1,88 M paramètres, 1,77 M poids linéaires par jeton :

| taux | modèle | val (bits/octet) | coût | R̂ |
|---|---|---:|---|---:|
| 3·10⁻³ | dense | 2,4420 | 1,77 M MACs | — |
| 3·10⁻³ | décharge | 3,2004 | 0,27 M événements | 0,170 |
| **10⁻³** | **dense** | **2,2572** | 1,77 M MACs | — |
| 10⁻³ | décharge | 3,2128 | 0,29 M événements | 0,178 |
| 10⁻³ | décharge, **poids binaires** | 3,4924 | 0,32 M événements | 0,195 |
| 10⁻³ | décharge, **poids ternaires** (α = 0,5) | 3,5091 | 0,30 M événements | 0,185 |

**Les poids signés coûtent 0,28 à 0,30 bit/octet de plus** que les poids valués,
à densité égale — et ils ne rapportent rien **aujourd'hui**, parce que le noyau
signé du moteur est plus lent par événement que le noyau valué (§ 3, point 3).
Le gain de stockage (1,99 bit/poids contre 8,00) est réel mais n'est pas encore
monnayable en temps.

**La parcimonie est bien obtenue par l'entraînement** — R̂ = 0,17, là où la
parcimonie imposée après coup plafonnait à −15 % d'événements (donc 85 % de
densité) pour +0,6 à +1,2 % de perplexité. Et le seuil est un vrai bouton, mesuré
sur le petit corpus à dim 192 :

| seuil | R̂ | événements/token | val (bits/octet) |
|---|---:|---:|---:|
| 1,0 | 0,165 | 0,26 M | 3,4828 |
| 1,5 | 0,090 | 0,14 M | 3,5704 |
| 2,0 | 0,029 | 0,05 M | 3,6765 |

Diviser le coût par cinq ne coûte que **+0,19 bit/octet**. Mais le jumeau dense
du même corpus/taille est à 2,44–2,26 : **l'écart est de 0,76 à 0,96 bit/octet**.
Ce n'est donc pas la parcimonie qui manque, c'est le prix de l'opération.

---

## 3. La loi du coût, mesurée dans le moteur (le chiffre qui manquait)

Banc du moteur, `blk.0.ffn_gate.weight` (4 864 × 896 = 4,36 M poids), 16 fils,
bande passante mesurée **20,8 Go/s**, binaire du 07/10 :

| densité | pull dense | push valué (int8) | push **signe** (FusedSign) |
|---:|---:|---:|---:|
| 1 % | 0,312 ms | 0,023 ms | 0,032 ms |
| 5 % | 0,313 ms | 0,060 ms | 0,082 ms |
| 10 % | 0,312 ms | 0,104 ms | 0,142 ms |
| 25 % | 0,312 ms | 0,240 ms | 0,340 ms |
| 100 % | 0,311 ms | 0,916 ms | 1,322 ms |

Le pull est **au mur mémoire** : 14,0 Go/s de poids lus, soit 67 % du repère.
Aux faibles densités, les deux push sont linéaires en événements :

- **valué** : `0,0137 ms + 0,210 ns × événements` par couche ;
- **signe** : `0,0110 ms + 0,305 ns × événements` par couche ;
- **dense** : `0,0716 ns × poids`.

Trois conséquences, toutes contraires à ce que le dépôt écrivait :

1. **Un événement coûte 2,9× (valué) à 4,3× (signé) un poids dense.** Le
   « R̂ = 0,15 → 6,7× moins d'événements → ~100 tok/s » de
   `docs/comparaison-spiking.md` § 4 supposait un événement au prix d'un poids :
   à R̂ = 0,17, le gain réel de temps est **≈ 1,4×**, pas 6,7×.
2. **Le croisement du chemin SIGNÉ est à ~9 % de densité**, pas à 22 % — le
   seuil `seuil_push = 0,22` du moteur est réglé sur le chemin valué.
3. **Le push signé est aujourd'hui plus cher par événement que le push valué**
   (0,305 contre 0,210 ns), alors qu'il stocke 1 bit au lieu de 8
   (`fused.bits_per_weight() = 8,97` pour le fusionné, `1,99` pour le bitmap).
   C'est un défaut de noyau — `FusedSign` n'a pas reçu le traitement AVX2 du
   push int8 — **pas une loi de la nature**. Tant qu'il n'est pas corrigé, les
   poids binaires ne peuvent pas montrer leur avantage.

---

## 4. Ce que cela change pour la cible

Deux façons de lire la loi du § 3, et il faut les deux :

- **au marginal** (grandes matrices, beaucoup d'événements) : un événement vaut
  2,9× (valué) à 4,3× (signé) un poids dense. Le gain de temps à densité *d*
  vaut donc `1 / (2,93·d)` pour le valué et `1 / (4,26·d)` pour le signé ;
- **au coût fixe** : chaque appel de couche paie 0,011 à 0,014 ms sur une matrice
  de 4 864 × 896 (barrière du pool, remise à zéro de l'accumulateur). Sur un
  modèle à 24 couches, c'est 0,3 ms par jeton — **plus que le temps dense total
  du même modèle** (0,127 ms pour 1,77 M poids). Un modèle creux n'a donc
  intérêt à disperser que si ses matrices sont **grandes** : c'est la taille de
  la couche, pas seulement la densité, qui décide.

La cible « un modèle à décharge parcimonieuse exécuté en listes » reste la bonne
— c'est la seule qui donne un débit variable — mais **la porte n'est pas la
densité seule** :

| chemin | gain 2× | gain 4× | condition de taille |
|---|---:|---:|---|
| valué (int8) | densité ≤ 17 % | densité ≤ 8 % | matrice ≫ 1 M poids |
| signé (1 bit) | densité ≤ 12 % | densité ≤ 6 % | idem |

Et la conclusion la plus utile du banc : **à 1,9 M paramètres, un modèle dense
tient dans le cache et le chemin par listes n'a rien à gagner.** L'avantage
structurel de Drave — ne lire que ce qui parle — ne se manifeste que sur un
modèle **plus gros que la mémoire ou le cache**, c'est-à-dire exactement la
leçon du disque de Kimi-K3. Le prochain banc doit donc être un modèle **gros en
paramètres et minuscule en activité par jeton** (routage par blocs), mesuré en
**octets lus par jeton**, pas en MACs.

---

## 5. Réserves (à lire avant de citer un chiffre)

- **un seul corpus, une seule taille, une seule graine** : l'écart de qualité
  (+0,76 à +0,96 bit/octet) est mesuré sur dim 192 et un corpus de 100 Mo ;
- **la loi du coût vient d'UNE matrice** (4,36 M poids) et d'un binaire ; les
  caches, la taille des listes et l'ordonnancement peuvent la déplacer ;
- les modèles sont **loin d'être convergés** (20 000 pas ≈ 0,8 passe sur 100 Mo) :
  les deux familles progressaient encore ;
- le jumeau dense est un transformeur dense ordinaire ; **rien ne dit qu'il est
  au meilleur de sa famille** (pas de recherche d'architecture) ;
- les temps du moteur sont mesurés **sous charge de fond** (bureau, autres
  projets) ; les comptes d'événements et les perplexités, eux, sont exacts.

---

## 6. Ce qui est ouvert

1. **Poids signés (binaire/ternaire)** — mesuré (voir § 2) : −0,28 à −0,30
   bit/octet, et aucun gain de temps tant que le noyau signé reste plus lent que
   le valué. Le stockage tombe à 1,99 bit/poids : c'est un gain de **mémoire et
   de disque**, pas encore de vitesse.
2. **Distillation** — jamais réalisée dans ce dépôt, alors que Qwen2.5-0.5B est
   sur le disque : c'est le levier de qualité le plus direct pour un petit
   modèle creux, et il ne demande aucun noyau nouveau.
3. **Noyau signé AVX2** — mesurer `FusedSign::accumulate` après optimisation :
   c'est lui qui décide si les poids binaires paient un jour.
4. **Routage par blocs sur un modèle plus gros que le cache** — le seul régime
   où l'architecture événementielle a un avantage structurel (§ 4). À mesurer en
   **octets lus par jeton**.
5. **Dimension temporelle (LIF à état)** — le banc actuel est un seuil statique
   par couche ; SpikeGPT aligne la séquence sur le temps, et c'est cette variante
   qui porte le R̂ = 0,15 avec qualité.
6. **La distribution** — un modèle creux à blocs de quelques centaines de ko rend
   caduque la limite « chaque nœud charge le modèle entier » ; l'unité de travail
   autonome reste à définir et à mesurer.
