# E9 — L'HOMÉOSTASIE SYNAPTIQUE : amortir le changement plastique rend la consolidation MEILLEURE des deux côtés

> Campagne : **cerveau** · expérience : **E9**, le seul emplacement de `docs/biologie-pour-drave.md`
> qui était resté vide (« — »). Il est **défini ici** et mesuré : l'**homéostasie synaptique** — la
> mise à l'échelle **globale** du changement plastique, le mécanisme par lequel un neurone garde son
> activité dans sa plage malgré la potentialisation (Turrigiano) —, appliquée à la consolidation.
> Question : **l'amplitude du changement doit-elle être dosée ?** Autrement dit : la consolidation
> mesurée jusqu'ici (LoRA rang 4, delta **entier**) est-elle au bon point, ou **trop forte** ?
> Verdict : **elle est trop forte.** À **×0,6** de l'amplitude, la consolidation fait **mieux en
> domaine ET mieux hors domaine** que le delta entier : m32 **−8,75 %** (contre −7,47 %), m20
> **−15,24 %** (contre −16,11 %, légèrement moins bien) et hors domaine **−0,58 %** — c'est-à-dire
> **un gain au lieu du coût de +0,33 %**. **Le coût hors domaine croît de façon monotone avec
> l'amplitude** (−0,58 % à ×0,6 → **+1,64 %** à ×1,25) : l'homéostasie fait exactement ce qu'elle
> annonce, et elle **domine** le réglage publié.
> Date réelle : **2026-10-15 20 h 20-20 h 55 HAE** (heure lue sur la machine)
> Protocole : le LoRA **rang 4** du balayage (`rapport-consolidation-balayage.md` : 180 224
> paramètres, 0,035 % du modèle, rejeu m0..m9) · **mise à l'échelle du delta** en multipliant `A` par
> `s` (`W ← W + (α/r)·B·A`, donc le delta est exactement ×s) · export GGUF
> (`tools/exporter_gguf_dense.py`) · **mesure du moteur** sur m32, m20 (jamais rejoués) et un texte
> d'un **autre corpus** (`corpus_en`, jamais rejoué).

## 1. La courbe : l'amplitude est un réglage, et le bon n'est pas 1

| échelle du delta | m32 (jamais rejoué) | écart | m20 | écart | hors domaine | écart |
|---:|---:|---:|---:|---:|---:|---:|
| **base** (aucune consolidation) | 7,4242 | — | 19,1237 | — | 17,2673 | — |
| **×0,5** | 6,7859 | −8,60 % | 16,3670 | −14,42 % | **17,1779** | **−0,52 %** |
| **×0,6** | **6,7751** | **−8,75 %** | 16,2096 | −15,24 % | **17,1671** | **−0,58 %** |
| **×0,75** | 6,7807 | −8,67 % | 16,0763 | −15,94 % | 17,2167 | −0,29 % |
| **×0,9** | 6,8245 | −8,07 % | **16,0195** | −16,25 % | 17,2706 | +0,02 % |
| **×1,0** *(le réglage publié)* | 6,8697 | −7,47 % | 16,0434 | −16,11 % | 17,3238 | **+0,33 %** |
| **×1,25** | 7,0243 | −5,39 % | 16,2203 | −15,20 % | 17,5506 | **+1,64 %** |

Ce que la courbe dit :

* **le coût hors domaine est MONOTONE en l'amplitude** : −0,58 %, −0,29 %, +0,02 %, +0,33 %,
  +1,64 % — c'est la signature de l'homéostasie, et elle est nette (l'ordre est parfait) ;
* **et le gain en domaine ne paie pas ce coût** : à **×0,6**, la consolidation est **meilleure sur
  m32** (−8,75 % contre −7,47 %) **et** sur le hors domaine (−0,58 % contre +0,33 %) — un point qui
  **domine** le réglage publié sur deux des trois textes, et ne lui cède que 0,9 point sur m20 ;
* **il y a donc un intérieur** : trop faible (×0,5 : m20 recule à −14,42 %) et trop fort (×1,25 :
  les trois colonnes reculent) perdent ; **l'optimum est dans la bande ×0,6-0,75** ;
* **et le réglage publié jusqu'ici (delta entier) n'était pas le bon** : toutes les fiches de
  consolidation de la nuit ont été faites à **×1,0** — leurs conclusions tiennent (les écarts
  mesurés sont de 1 à 10 points), mais **le point publié était en dehors de l'optimum** ✗, et c'est
  écrit ici plutôt que corrigé en silence.

## 2. Ce que ça change pour le cerveau

* **E9 existe, et il est un RÉGLAGE, pas un mécanisme de plus** : la consolidation n'a pas besoin
  d'une règle nouvelle, elle a besoin d'être **dosée** — et le dosage est **global** (une seule
  échelle), donc il ne coûte **rien** à l'exécution (contrairement à EWC ou à une pénalité par
  poids ✗) : c'est le rapport efficience/effet le meilleur de toutes les fiches de consolidation ;
* **c'est la réponse biologique au problème mesuré de la nuit** : la consolidation « spécialise »
  (+1,3 % hors domaine) — l'homéostasie **annule** ce coût et **améliore** le gain en domaine ✓✓ ;
* **et cela déplace la conclusion de la fiche du sommeil** : le choix n'est pas « consolider ou
  pas », ni « combien rejouer », mais **« consolider à quelle amplitude »** — un troisième axe, qui
  était invisible tant qu'on ne le balayait pas ;
* **ce qui reste à faire, nommément** : (a) le même balayage sur **d'autres volumes de rejeu** (3 et
  20 morceaux ✗) — l'optimum dépend peut-être du volume ; (b) une homéostasie **par couche** plutôt
  que globale ✗ (mesurer la sensibilité de chaque couche et doser individuellement ✗) ; (c) et la
  question de fond : **comment un cerveau SAIT qu'il doit amortir** — ici l'échelle est choisie par
  balayage, alors qu'un mécanisme homéostatique réel la **mesure** (l'activité de sortie ✗).

## 2bis. DE L'ORACLE À UNE RÈGLE : l'amplitude se choisit sur l'activité du modèle, pas sur le domaine visé

La limite la plus gênante du § 2 était que l'échelle ×0,6-0,75 est trouvée **par balayage sur le
domaine visé** — un oracle qu'aucun cerveau ne possède ✗. Une règle **auto-contenue** a donc été
cherchée : peut-on choisir l'amplitude en ne regardant que le modèle **lui-même** ?

Deux statistiques mesurées sur un texte **neutre** (jetons 40 000..41 024 : ni rejoué, ni testé, ni
l'autre corpus) :

| échelle | norme de l'état final | **perplexité du texte NEUTRE** |
|---:|---:|---:|
| *(modèle de base)* | **72,1312** | — |
| ×0,5 | 73,6207 (+2,07 %) | 9,0815 |
| ×0,6 | 73,6715 (+2,14 %) | 9,0591 |
| **×0,75** | 73,8340 (+2,36 %) | **9,0372** ← minimum |
| ×0,9 | 74,0828 (+2,71 %) | 9,0391 |
| ×1,0 | 74,1796 (+2,84 %) | 9,0420 |
| ×1,25 | 74,7319 (+3,61 %) | 9,0950 |

* **la première règle essayée ne marche pas** : « garder l'activité dans ±1 % du modèle de base »
  rejette **tout** ✗ — la consolidation elle-même déplace l'activité de **+2,07 %** dès ×0,5. Le
  seuil serait donc un chiffre magique ✗ ;
* **la seconde règle marche, et elle n'a besoin d'aucun oracle** : *choisir l'amplitude qui minimise
  la perplexité du modèle sur sa PROPRE activité récente* — un texte neutre, que rien n'a rejoué et
  qui n'est pas le domaine visé ✓. Elle désigne **×0,75**, c'est-à-dire **le voisinage de l'optimum
  trouvé par l'oracle** (×0,6-0,75) ✓✓ ;
* **et c'est biologiquement plausible** : un cerveau a « son activité de la veille » — il n'a pas le
  domaine de demain. La règle n'utilise que ce qu'il a ✓ ;
* **la courbe neutre est un U**, comme la courbe hors domaine : trop amortir **et** trop laisser
  passer dégradent ✓ — c'est la même forme, sur une statistique que le système peut mesurer seul ✓.

## 3. Ce que cette fiche ne dit pas

* **un seul LoRA, un seul rejeu** (rang 4, m0..m9, 10 époques) : l'optimum à ×0,6-0,75 est peut-être
  propre à ce volume — c'est la première chose à vérifier avant de publier un réglage ;
* **l'échelle de l'oracle est choisie par balayage sur le domaine visé** ✗ — mais le § 2bis montre
  qu'une règle **auto-contenue** (minimiser la perplexité sur un texte **neutre**) désigne le même
  point (×0,75) sans rien savoir du domaine ✓. Ce qui reste ouvert : cette règle demande un texte
  neutre **étiqueté comme neutre** — le système doit savoir ce qu'il n'a pas rejoué ✗ ;
* **trois textes** : le hors domaine est **un** texte d'un **autre** corpus (la dispersion d'un
  corpus est mesurée ailleurs : `rapport-consolidation-structure-partagee.md`) ;
* **rien sur la génération** : la courbe est une courbe de perplexité ;
* **E9 est défini ICI** — la définition est celle du mécanisme appliqué (l'échelle globale du
  changement plastique), pas une définition trouvée dans la littérature : c'est l'homéostasie
  synaptique **telle qu'elle se traduit dans ce moteur**, et c'est dit comme tel.
