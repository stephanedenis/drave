# Quatre jours de suite — deux refusés par le protocole, un qui dégrade

> Campagne : **cerveau** · expérience : la consolidation **séquentielle** sur un corpus
> **hétérogène** (`corpus_en`, dispersion ×2,9 — `rapport-consolidation-structure-partagee.md`) —
> le cas d'une **vie** : quatre journées, chacune rejouant cinq morceaux nouveaux, chacune
> reprenant le modèle de la veille (`--lora-depart`).
> Verdict : **le protocole refuse la moitié des journées, et celle qu'il accepte dégrade le texte
> tenu à l'écart.** Jour 1 : m30 **−0,92 %** ✓. Jours **2 et 3** : **aucune époque n'améliore la
> validation**, donc le protocole **rend le modèle inchangé** (0,00 %, au chiffre près) — un
> entraînement qui ne vaut rien **ne se publie pas**. Jour 4 : accepté, et la mesure tenue à
> l'écart **monte** (m30 **+0,36 %**, m0 **+0,61 %**).
> Date réelle : **2026-10-15 03 h 35-03 h 55 HAE** (heure lue sur la machine)
> Protocole : `tools/n4_dessin_b.py --objectif plein --ids /tmp/n4/ids-en.txt` · jour *j* = rejeu des
> morceaux 5j..5j+4 (5 morceaux, 8 époques, graine 0), en **reprise** du jour précédent
> (`--lora-depart`) · validation **m24** (jamais rejouée, choisie une fois pour toutes) · test
> **m30** (jamais rejoué) et **m0** (dans le rejeu du jour 1 — donc une mesure de **mémorisation**,
> et elle est étiquetée comme telle) · LoRA rang 8 sur les 8 premières couches.

## 1. La courbe

| | rejeu du jour | époque retenue | **m30** (jamais rejoué) | écart | m0 *(rejoué au jour 1)* | écart |
|---|---|---|---:|---:|---:|---:|
| **base** | — | — | 23,1548 | — | 24,7366 | — |
| **jour 1** | m0..m4 | 1 | **22,9422** | **−0,92 %** | 23,0310 | −6,89 % *(mémorisation)* |
| **jour 2** | m5..m9 | **0 — REFUSÉ** | 22,9422 | **0,00 %** | 23,0310 | 0,00 % |
| **jour 3** | m10..m14 | **0 — REFUSÉ** | 22,9422 | **0,00 %** | 23,0310 | 0,00 % |
| **jour 4** | m15..m19 | 1 | **23,0236** | **+0,36 %** | 23,1724 | +0,61 % |

*(« époque 0 » est le nom que le protocole donne au **modèle de départ** : quand aucune époque ne
fait mieux que lui sur la validation, c'est lui qui est publié — et le modèle ne bouge pas.)

Ce que ça dit :

* **« aucune époque n'améliore la validation » est un RÉSULTAT, pas un échec** : le protocole
  compare chaque époque au modèle **de départ** (`meilleur = (ppl_depart, époque 0)`) et **rend le
  modèle inchangé** si rien ne fait mieux. Deux journées sur quatre sont donc **refusées par la
  mesure elle-même** — et c'est la garantie qu'aucun chiffre de ce dépôt ne vient d'un entraînement
  qui ne vaut rien (la même règle que la fiche du budget du sommeil : « l'époque se choisit sur la
  validation ») ;
* **et la journée acceptée DÉGRADE le texte tenu à l'écart** (+0,36 % sur m30, +0,61 % sur m0) :
  la validation (m24) s'était améliorée, le test non. C'est un **désaccord validation/test** de plus
  — et il rappelle que la validation n'est qu'un **proxy** (leçon déjà tirée dans la fiche
  « structure partagée », où la colonne « validation » gagnait −3,6 % sans que le test gagne rien) ;
* **le contraste avec wikitext2 est total** : là, une nuit donne −7,9 % et une deuxième +0 % ; ici,
  **une journée sur quatre sert**, pour −0,9 %. Ce n'est pas le mécanisme qui change, c'est le
  **corpus** : consolider suppose une structure partagée à extraire, et `corpus_en` n'en a pas
  (dispersion ×2,9) ;
* **conséquence pour un cerveau en continu** : sur un flux hétérogène, **dormir tous les jours ne
  sert à rien** — il faut soit un rejeu **choisi** (et le critère de choix reste ouvert : la
  dispersion ne marche pas, cf. § 2quater de la fiche citée), soit **ne pas toucher aux poids** et
  laisser la mémoire épisodique porter le souvenir (11 jetons sur 2 048, et rien n'est perdu).

## 2. Ce que cette fiche ne dit pas

* **quatre journées, une graine, un seul ordre** : les morceaux sont rejoués dans l'ordre du fichier ;
  un ordre tiré au hasard, ou un rejeu **répété** des mêmes journées, ne sont pas mesurés ;
* **le critère de validation est unique** (m24) : une validation sur plusieurs morceaux changerait
  peut-être les deux refus (une seule mesure à 4 811 de perplexité → l'écart-type de la validation
  n'est pas connu) ;
* **le refus est un choix de protocole, pas une propriété du monde** : un entraînement « refusé »
  aurait peut-être transféré ailleurs ; ce qui est mesuré est qu'il **n'améliore pas** la validation
  choisie ;
* **rien sur le coût** : quatre journées = quatre entraînements (≈ 8 min de GPU) pour un gain nul ou
  négatif — le coût est dit, le rapport ne l'est pas ;
* **le corpus_en n'est pas « mauvais »** : il est **hétérogène** (médiane 9,21, min 2,65, max 35,89)
  — et c'est précisément ce qui en fait le banc d'essai utile de cette fiche.
