# Le balayage de la consolidation — un optimum INTÉRIEUR de capacité (rang 4) et de pas (3e-4), qui ne composent PAS

> Campagne : **cerveau** · expérience : les deux réglages que toutes les fiches de consolidation
> laissaient en défaut (« le taux d'apprentissage et le rang ne sont pas balayés »).
> Question : quel est le **plus petit** adaptateur qui donne le **plus grand** gain — et les deux
> optima se composent-ils ?
> Verdict : **un optimum INTÉRIEUR de capacité, et il est spectaculaire.** À réglages égaux (10
> morceaux, 10 époques, graine 0), le **rang 4** (180 224 paramètres, **0,035 %** du modèle) donne
> **−7,63 %** sur m32, quand le rang **32** (1 441 792 paramètres, **huit fois plus**) donne
> **−5,28 %** : **plus de capacité NUIT** (2,35 points, très au-dessus du bruit de graine de 0,14).
> Le pas d'apprentissage a aussi un optimum intérieur (**3e-4** : −7,57 %, contre −6,41 % à 1e-4 et
> −5,66 % à 3e-3). Et **les deux optima ne composent pas** : rang 4 + pas 3e-4 donne **−7,31 %**,
> moins que chacun pris séparément — la leçon classique, et elle est mesurée ici.
> Date réelle : **2026-10-15 03 h 55-04 h 15 HAE** (heure lue sur la machine)
> Protocole : `tools/n4_dessin_b.py --objectif plein --train 10 --val 29 --test 32,20` · rejeu
> m0..m9, validation m29, test **m32** et **m20** (jamais rejoués) · 10 époques, graine 0, époque
> choisie sur la validation · LoRA sur les **32 projections** des 8 premières couches · perplexité
> du **modèle complet** (harnais ; les chiffres moteur de la même recette sont dans
> `rapport-consolidation-structure-partagee.md`).

## 1. Le rang — et plus de capacité NUIT

| rang | paramètres | part du modèle | m32 | écart | m20 | écart |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 90 112 | 0,018 % | 6,7039 | −6,61 % | 15,5413 | −15,81 % |
| **4** | **180 224** | **0,035 %** | **6,6310** | **−7,63 %** | **15,5195** | **−15,93 %** |
| 8 | 360 448 | 0,071 % | 6,6812 | −6,93 % | 15,5950 | −15,52 % |
| 16 | 720 896 | 0,141 % | 6,7427 | −6,07 % | 15,7507 | −14,68 % |
| 32 | 1 441 792 | 0,283 % | 6,7998 | −5,28 % | 15,9583 | −13,56 % |

* **le rang 4 est le meilleur, et le rang 32 est le pire** : 2,35 points d'écart sur m32 pour
  **huit fois moins** de paramètres. Le classement est **monotone** au-delà de 4 (8 > 16 > 32) ;
* **c'est la face « capacité » de ce que la fiche du budget du sommeil disait de la donnée** :
  « la limite est la donnée, pas l'entraînement ». Ici, la capacité **au-delà** du nécessaire est
  non seulement inutile mais **nuisible** (elle surapprend dix morceaux) ;
* **et c'est le plus petit adaptateur entraîné du dépôt** : 180 224 paramètres, **0,035 %** du
  modèle, pour −7,6 % en domaine et −15,9 % sur un autre morceau jamais vu.

## 1bis. Le MOTEUR confirme le point retenu (et il est même meilleur sur m20)

La discipline du dépôt : un chiffre de tête se vérifie **au moteur**. Le rang 4 exporté
(`exporter_gguf_dense.py`) et relu par `drave` :

| modèle | m32 (moteur) | m20 (moteur) |
|---|---:|---:|
| base (`models/Qwen2.5-0.5B-Q8_0.gguf`) | 7,4242 | 19,1237 |
| **rang 4 consolidé** | **6,8697 (−7,47 %)** | **16,0434 (−16,11 %)** |
| *(harnais, pour mémoire)* | −7,63 % | −15,93 % |

* **l'accord est à 0,2 point** (−7,47 % au moteur contre −7,63 % au harnais), et le moteur est
  **meilleur** sur m20 (−16,11 % contre −15,93 %) : la quantification Q8_0 n'a pas coûté le gain de
  la consolidation, elle l'a légèrement servi ici ;
* **c'est le point efficient du dépôt, vérifié des deux côtés** : **180 224 paramètres (0,035 %)**,
  10 époques, 10 240 jetons rejoués → **÷1,08** de perplexité en domaine et **÷1,19** sur un autre
  morceau jamais vu.

## 2. Le pas d'apprentissage — optimum intérieur aussi

| pas (rang 8) | m32 | écart |
|---:|---:|---:|
| 1e-4 | 6,7188 | −6,41 % |
| **3e-4** | **6,6352** | **−7,57 %** |
| 1e-3 | 6,6812 | −6,93 % |
| 3e-3 | 6,7726 | −5,66 % |

* **3e-4 bat 1e-4 ET 1e-3** : un optimum **intérieur** des deux côtés (trop petit n'apprend pas
  assez, trop grand surapprend) — et la différence 1e-4 ↔ 3e-4 (1,16 point) montre que la borne
  basse n'est pas plate ;
* **le pas par défaut du dépôt (1e-3) n'est pas le meilleur** : il coûte 0,64 point par rapport à
  3e-4, à rang égal. Toutes les fiches de consolidation de la nuit ont été faites à 1e-3 — les
  conclusions tiennent (elles portent sur des écarts de 1 à 10 points), mais l'optimum est ailleurs.

## 3. Et les deux optima NE composent PAS

| réglage | m32 | écart | m20 | écart |
|---|---:|---:|---:|---:|
| rang **4**, pas 1e-3 | 6,6310 | **−7,63 %** | 15,5195 | **−15,93 %** |
| rang 8, pas **3e-4** | 6,6352 | −7,57 % | 15,6152 | −15,41 % |
| rang **4** + pas **3e-4** | 6,6541 | **−7,31 %** | 15,5754 | −15,63 % |

* **la combinaison des deux optima est MOINS bonne que chacun** (−7,31 % contre −7,63 % et
  −7,57 %) : les deux réglages **interagissent**, et un balayage à une dimension ne se compose pas ;
* l'écart (0,32 point) est au-dessus du bruit de graine (0,14) mais petit : la conclusion honnête
  est « **pas de composition démontrée** », pas « la combinaison nuit » ;
* **le point retenu pour la nuit est donc (rang 4, pas 1e-3)** — et c'est celui qui a été mesuré le
  plus finement ici.

## 4. Ce que ça change pour le cerveau

* **« le plus efficient » a maintenant un chiffre** : une consolidation qui apprend 0,035 % des
  poids, en 10 époques, sur 10 240 jetons, pour −7,6 % de perplexité en domaine — et c'est le
  **meilleur** point d'un balayage de 8 configurations ;
* **la règle « la donnée est la limite » a sa réciproque** : la capacité **au-delà** de la donnée
  est un coût, pas une réserve. Un cerveau qui dors sur peu d'expérience n'a pas besoin de beaucoup
  de synapses nouvelles — et en ajouter **dégrade** ;
* **et la méthode est écrite** : les deux optima ne composent pas ⇒ tout nouveau réglage de
  consolidation doit être **mesuré**, pas déduit d'un balayage précédent.

## 4bis. LA REPRODUCTIBILITÉ DU HARNAIS — un DÉFAUT trouvé, nommé et CORRIGÉ (pas du bruit)

Trouvé en fin de nuit, en vérifiant qu'un chiffre de la **boucle du cerveau** ne bougeait pas entre
deux exécutions : **il bouge.** Deux exécutions **identiques** (mêmes morceaux, mêmes époques, même
graine 0, même époque retenue — la 3ᵉ) :

| exécution | m4 (modèle complet) | écart |
|---|---:|---:|
| 1 | 12,6829 | −6,11 % |
| 2 | 12,7362 | −5,72 % |

**0,4 point d'écart pour la MÊME configuration** — c'est-à-dire **plus** que le « bruit de graine »
de 0,14 point que les fiches de la nuit citaient (celui-là mesurait deux **graines différentes**).

**La cause a été trouvée, et ce n'était pas du bruit** : `torch.manual_seed` était appelé **dans
`entrainer`**, c'est-à-dire **APRÈS** la construction du banc — donc après le tirage aléatoire des
matrices LoRA, qui consommait un RNG **non semé**, différent à chaque processus. *Semer après avoir
tiré ne seme rien.* Le diagnostic a écarté l'autre suspect (le mode déterministe de PyTorch : avec
`use_deterministic_algorithms(True)` **strict**, l'entraînement passe sans erreur — toutes les
opérations ont un noyau déterministe).

**Corrigé** : la graine (et les trois réglages de déterminisme) sont posés **avant** `Banc(a)`. Deux
exécutions identiques rendent désormais **le même nombre, au bit près** — mesuré :
`12,732836173028936` deux fois (m4), là où l'outil rendait 12,6829 puis 12,7362. Et les deux autres
outils d'entraînement (`cycle_entraine.py`, `memoire_travail.py`) étaient **déjà** dans le bon ordre :
le défaut ne concernait que le banc de consolidation.

**Ce que ça recalibre, dans les deux sens** :

* **au-dessus du bruit (conclusions tenues)** : le balayage de rang (**2,35 points** entre rang 4 et
  rang 32), le seuil de diversité (**6,6 points** sur m20), la distillation (22,1 % contre 51,0 %
  d'accord), la courbe du rejeu (4,4 points entre 3 et 20 morceaux), les deux nuits (−7,85 % puis
  −0,30 %) ;
* **dans le bruit (conclusions à lire comme « rien de démontré »)** : **les deux optima qui ne
  composent pas** (0,32 point — écrit comme « pas de composition démontrée », et c'est encore plus
  juste maintenant), **le rang 2 contre le rang 8** (−6,61 % contre −6,93 %), **le pas 1e-3 contre
  1e-4** (−6,93 % contre −6,41 %... hmm, 0,52 point, à la limite), et **l'ordre des règles de
  sélection** (−5,51 % contre −4,82 %, soit 0,7 point — au-dessus du bruit, mais pas de beaucoup) ;
* **et la leçon pour la suite** : un écart qu'on n'explique pas n'est pas une « mesure bruitée » —
  c'est une **question ouverte**. Ici, 0,4 point inexpliqué est devenu un **défaut corrigé** en une
  heure, et le harnais est maintenant **exact**. Les comparaisons de moins d'un point qui ont été
  publiées **avant** la correction (les deux optima qui ne composent pas, rang 2 contre rang 8)
  gardent leur formulation prudente — elles peuvent maintenant être **refaites à l'identique**, ce
  qui n'était pas possible avant.

## 5. Ce que cette fiche ne dit pas

* **huit configurations, une graine, un jeu de morceaux** : l'optimum de rang (4) et de pas (3e-4)
  sont des points de grille, pas des courbes ajustées — et la graine unique borne la résolution à
  0,14 point ;
* **rien sur le nombre d'époques couplé au pas** : à 3e-4, plus d'époques aiderait peut-être (le
  surapprentissage arrive plus tard) — la grille 2D (pas × époques) n'est pas faite ;
* **rien sur l'alpha** (le facteur d'échelle du LoRA) : il a été fixé à 2 × rang pour que l'échelle
  du déplacement soit constante — c'est un choix, pas une mesure ;
* **un seul corpus et un seul domaine** : `corpus_en` n'a pas été balayé (et il ne transfère pas,
  cf. fiche « structure partagée ») ;
* **aucune mesure moteur dans cette fiche** : les huit points sont mesurés dans le harnais, comme
  les autres balayages ; la recette retenue (rang 8) a, elle, été vérifiée au moteur.
