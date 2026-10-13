# Dessin H — les sorties précoces (8 et 4) : la question ouverte est tranchée, et le verdict ne change pas

> Campagne : **cerveau** · expérience : la carte des sorties, points précoces
> Question : la fiche de la première carte ([`rapport-design-H-carte-sorties.md`](rapport-design-H-carte-sorties.md))
> laissait ouvert « les sorties **plus précoces** (8, 4 — la tendance du produit plaide pour l'aller
> voir) ». Sortir plus tôt épargne plus de couches ; l'accord de l'oracle, lui, s'effondre. Qui
> gagne ?
> Verdict : **personne.** Le produit théorique monte bien (17,0 % des paires au mieux à la sortie
> **8**, contre 3,53 % à 22), mais le **routeur réel** y **perd 0,30 point** de justesse (47,43 %
> contre 47,73 % pour le chemin long) : aux sorties précoces, aucun seuil de confiance n'atteint la
> parité. Le facteur limitant n'est donc pas la profondeur de sortie, c'est la **qualité du chemin
> court** — le manque **N4**, comme la fiche le disait déjà.
> Date réelle : **2026-10-13, 02 h 27-02 h 34 HAE** (heure lue sur la machine)
> Protocole : `SORTIES="8 4" tools/carte-sortie-profondeur.sh` (N = 8 192 jetons, 30 époques,
> test sur les positions 1 000-3 000, graine 0, modèle Qwen2.5-0.5B-Q8_0) — mêmes réglages que la
> première carte, seule la liste des sorties change

## 1. La courbe complète (les deux cartes réunies)

| sortie | couches sautées | perplexité du court | justesse du court | **accord** (borne) | **paires au mieux** | seuil 0,99 : part sortie | justesse globale |
|---|---:|---:|---:|---:|---:|---:|---:|
| **4 / 24** | 20 | 1 809,2412 | 15,79 % | 19,79 % | **16,49 %** | 3,4 % | 47,38 % |
| **8 / 24** | 16 | 864,6236 | 18,74 % | 25,44 % | **16,96 %** | 2,5 % | 47,43 % |
| 12 / 24 | 12 | 762,0132 | 20,34 % | 25,19 % | 12,60 % | 5,0 % | 47,13 % |
| 16 / 24 | 8 | 499,0613 | 23,19 % | 30,93 % | 10,31 % | 5,1 % | 47,33 % |
| 20 / 24 | 4 | 228,5551 | 30,58 % | 41,98 % | 7,00 % | 6,6 % | 47,23 % |
| 22 / 24 | 2 | 167,1173 | 28,94 % | 42,33 % | **3,53 %** | 4,7 % | **47,78 %** |

*(les deux lignes en gras sont celles mesurées cette nuit ; les quatre autres sont de la première
carte, mêmes réglages.)* « paires au mieux » = accord × couches sautées / 24 : ce qu'un routeur
**parfait** épargnerait sans changer une seule décision.

## 2. Ce que la courbe dit

* **la tendance du produit se retourne, et son maximum est à 8** : 16,96 % des paires au mieux —
  soit **4,8×** la sortie 22 (3,53 %) et **1,35×** la sortie 12 (12,60 %). La sortie 4 redescend
  (16,49 %) : la chute de l'accord (19,79 %) commence à coûter plus que les quatre couches gagnées ;
* **mais le routeur réel ne suit pas** : au seuil 0,99, la sortie 8 envoie **2,5 %** des jetons sur
  le chemin court avec une justesse globale de **47,43 %**, contre **47,73 %** pour le chemin long
  seul — **−0,30 point**. C'est *pire* que ne rien router. La seule sortie où le routeur réel
  atteignait la parité était **22** (+0,05 point, dans le bruit) ;
* **donc la borne elle-même n'est pas le problème** : même avec un routeur **parfait**, on
  n'épargnerait que **17 %** des paires. Le chemin court doit d'abord *valoir* quelque chose : sa
  justesse est de 18,74 % à la sortie 8 et 42,33 % à la sortie 22, contre 47,73 % pour le long.
  C'est le manque **N4** (la qualité du chemin court), pas le choix de D.

## 3. Ce que cette fiche ferme, et ce qu'elle n'ouvre pas

* **fermé** : « aller voir les sorties précoces ». C'est fait, la réponse est non — et elle est
  maintenant chiffrée plutôt que supposée ;
* **non ouvert** : la génération libre (au lieu du contexte imposé), qui reste la seconde piste de
  la fiche d'origine — elle demande un autre protocole (décodage, pas perplexité), donc une autre
  expérience ;
* **rappel de lecture** : toutes ces colonnes mesurent une **borne** (ce qu'un routeur parfait
  épargnerait) et un **seuil réel** (ce qu'un routeur entraîné atteint). Les deux doivent être lus
  ensemble : la première dit si le dessin a un avenir, la seconde s'il a un présent. Ici : un
  avenir modeste (17 %) et pas de présent (−0,30 point).
