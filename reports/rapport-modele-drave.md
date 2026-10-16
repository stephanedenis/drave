# DÉVELOPPER UN MODÈLE **NATIF DRAVE** — étude, et le plan pour le mesurer

> Demande de Stéphane (16/10) : « étudie un moyen de développer ton propre modèle optimisé pour
> Drave ». Ce document est **l'étude** ✓ — pas un vœu ✗ : chaque exigence est **tirée d'une mesure du
> dépôt** ✓ (avec son chiffre ✓), l'architecture en découle ✓, et **chaque étape est mesurable avec un
> outil qui existe déjà** ✓✓.
> Date réelle : **2026-10-16** (heure lue sur la machine)

## 1. Ce qu'un modèle « natif Drave » doit savoir faire — et ce que le dépôt a mesuré

Un modèle optimisé pour Drave n'est **pas** un bon modèle de chat ✗ : c'est un modèle qui **exploite
l'architecture de Drave** ✓ (régions ✓, liens ✓, coupes ✓, horloges ✓, budgets ✓, sparsité ✓).

| ce que Drave sait faire | ce que la mesure dit | ce que le modèle devrait avoir |
|---|---|---|
| **couper** un modèle en régions ✓ | **8 coupes, une seule perplexité** (113,0068 ✓) ; le pont coûte **+0,52 %** tard contre **+17,09 %** tôt ✓ (facteur **30** ✓) ; **448 fibres = +2,81 %** et **÷1,8** en octets ✓ | des **blocs homogènes** ✓ et un **pont appris** ✓ (pas une simple troncature ✓) |
| **court-circuiter** (le réflexe, C8 ✓) | le chemin tronqué tombe d'accord **0 %** jusqu'à 16 couches, **8,3 %** à 20 ✓ ; une **tête empruntée** plafonne à **267,98** ✓ ; distillé, le réflexe atteint **30,0 %** ✓ | des **têtes de sortie anticipée** entraînées **avec** le modèle ✓✓ (l'adaptateur du dépôt **est** une tête précoce ✓ — la machinerie existe ✓) |
| **itérer** sans verbaliser (C2 ✓, 16/10 ✓) | le pas d'état **amplifie** (λ ≥ **3,7e4** ✗) ; `h_p → h_{p+1}` est « lire un jeton de plus » ✗, pas « penser » ✗ ; et **aucun** modèle ne contient d'opérateur de pensée ✗ | un **bloc de pensée** dédié ✓, entraîné à être **contractant** (λ < 1 ✓) **et** à conserver le contenu ✓ |
| **calculer sans multiplieur** ✓ | la contrainte est **satisfaite** : signes figés ✓, décalages + additions ✓, « aucun DSP, aucune multiplication » ✓ | des **signes figés** ✓ (1 bit ✓) et un **vocabulaire d'octets** (256 ✓) — les deux sont **déjà** dans l'entraîneur ✓ |
| **activer creux** ✓ | k-WTA 25 % : **399 M paires** contre 1 586 M, soit **÷3,97** ✓, perplexité inchangée (3,9139 contre 3,9152 ✓) | **k-WTA** ✓ et **experts** ✓ (l'entraîneur les fait ✓, le moteur les exécute ✓) |
| **tenir dans la machine** ✓ | 16 Go de carte ✓, et l'entraîneur construit des modèles de **2 M** ✓ (dense ou routé ✓) | commencer **petit** ✓ : le premier objet est un **démonstrateur de mécanismes** ✓, pas un assistant ✓ |

## 2. Le modèle proposé (v0 — un démonstrateur de mécanismes, pas un chat)

Tout est **déjà constructible** avec `tools/entrainer_moteur.py` ✓ (qui bâtit du **Qwen3 dense ou MoE de
zéro** ✓, en **octets** ✓, avec k-WTA ✓, signes figés ✓, poids log-normaux ✓, ratio E/I ✓) :

| trait | choix | pourquoi |
|---|---|---|
| entrée | **octets** (vocab 256 ✓) | pas de tokeniseur ✓, tête de sortie minuscule ✓, et c'est **déjà** le cas ✓ |
| taille | `dim 512 · 8-12 couches · MoE` ✓ | itérable sur cette machine ✓ ; les mécanismes se mesurent **petit** ✓ |
| **têtes précoces** | **3 têtes** (adaptateurs ✓) posées après les couches **2, 4, 6** ✓ | rend le **réflexe** utilisable ✓✓ (aujourd'hui : 0 % ✗) — et l'outil `--accord` mesure le gain ✓ |
| **bloc de pensée** | une petite cellule récurrente sur l'état final ✓ | le rendre **contractant** (pénalité sur λ ✓) **et** garder le contenu ✓ (prédire les embeddings à venir ✓) — **les deux objectifs mesurés le 16/10** ✓ |
| **pont de région** | une projection apprise ✓ entre deux moitiés ✓ | le dépôt a mesuré que le pont **tardif** coûte 30× moins cher ✓ |
| contraintes | **signes figés** ✓ + **k-WTA 25 %** ✓ | le chemin le moins cher du moteur ✓, et la mesure dit que k-WTA 25 % est **gratuit** en perplexité ✓ |

## 3. Le plan, en quatre étapes — **chacune mesurable avec un outil existant**

| # | étape | ce qu'on mesure | avec quoi (déjà écrit ✓) | coût |
|---|---|---|---|---|
| **1** | **têtes précoces** : entraîner le 2 M en octets avec 3 têtes ✓ | l'**accord** par profondeur ✓ (aujourd'hui 0 % / 8,3 % ✗) | `n4_dessin_b.py --accord` ✓, `exporter_gguf_dense.py --adapter-sortie` ✓ | quelques heures GPU ✓ |
| **2** | **bloc de pensée** : cellule récurrente + pénalité de contraction ✓ | **λ** ✓ et le **contenu après k pas** ✓ | `cycle_sensibilite.py` ✓ (λ ✓), `pas_latent.py` ✓ (contenu ✓) | idem ✓ |
| **3** | **pont de région** appris ✓ | le **coût du pont** en octets ✓ et la perplexité ✓ | `porte-coupe.sh` ✓, `carte_coupe.sh` ✓ | court ✓ |
| **4** | **passer à l'échelle** (20-50 M) ✓ | les mêmes chiffres ✓ | les mêmes ✓ | journées GPU ✗ |

## 4. Ce qui pourrait tuer l'idée — écrit d'avance

* **un modèle de 2 M en octets ne « parle » pas** ✗ : il ne produira jamais de texte utile ✓ — c'est un
  **banc**, pas un assistant ✓. La valeur est dans les **mécanismes** ✓ (réflexe ✓, pensée ✓, coupes ✓),
  et il faut l'assumer ✗✓ ;
* **la qualité ne suit pas toujours la taille** ✗ : le passage à l'échelle (étape 4 ✓) peut montrer que
  les têtes précoces ou le bloc de pensée **cessent de payer** quand le modèle grossit ✗✓ — c'est une
  mesure à faire, pas une hypothèse à croire ✓ ;
* **le vocabulaire d'octets** ✗ : très économique ✓, mais il **allonge** les séquences (÷3 à ÷4 de
  contexte utile ✗) — l'étape 4 devrait probablement passer à un **BPE** ✗, ce qui **casse** la
  simplicité de la tête ✓ et doit être décidé explicitement ✓ ;
* **et la contrainte la plus dure** ✗ : un modèle vraiment optimisé pour Drave devrait être **entraîné
  avec** l'objectif de décomposition ✗ (pertes locales par région ✓) — ce que **personne n'a fait** ici ✓.
  C'est la partie **originale** du projet ✓✓, et la plus risquée ✗.

## 5. Pourquoi ça vaut le coup, en une phrase

Drave a mesuré que **la quantité domine le placement** ✓ (volume de rejeu ✓, profondeur ✓, clés ✓) — sauf
pour **une** chose : **le contenu** ✓ (la politique par texte ✓, la diversité ✓, l'amplitude ✓). Or ces
trois-là sont exactement ce qu'**un modèle entraîné pour ça** ferait mieux qu'un modèle générique
**adapté** ✗✓ : un modèle **natif** n'aurait pas besoin d'apprendre à être coupé ✓, à avoir un réflexe ✓,
ni à être contractant ✓ — il le serait **par construction** ✓✓.

## 6. L'ÉTAPE 0, TROUVÉE EN ESSAYANT : le aller-retour entraîneur → moteur n'est PAS câblé

L'étude ne vaut que si elle est **exécutable** ✓ — alors l'essai a été fait **tout de suite** ✓, avec
l'entraîneur existant ✓ :

```bash
python tools/entrainer_moteur.py --famille route --dim 256 --couches 4 --tetes 4 --cache 512 \
    --cache-perle 256 --experts 4 --k 2 --seq 128 --lot 8 --pas 60 --kwta 0.25 \
    --donnees data/wikitext2_test.txt --sortie /tmp/drave-v0.gguf
```

**Ce qui marche** ✓✓ : l'entraînement tourne (60 pas, **5 s**, perte 2,5741, validation **4,8948
bits/octet** ✓), il applique **k-WTA 25 % sur 17 projections** ✓, et il annonce un modèle de **4,00 M
paramètres** ✓.

**Ce qui manque** ✗✓ : il **n'écrit pas un GGUF** ✗ — il écrit un **dossier au format HuggingFace**
(`config.json`, `model.safetensors` de 15,3 Mo ✓), et le moteur **ne peut donc pas le lire** ✗ (essai
fait : la commande de perplexité ne rend rien ✓). Autrement dit : **l'aller-retour
entraîneur → moteur n'est pas câblé pour ce modèle** ✗✓ — un **modèle routé en octets** n'a pas
d'exporteur ✓ (l'exporteur du dépôt, `exporter_gguf_dense.py` ✓, est écrit pour du **dense** ✗ et part
d'un modèle HuggingFace ✓).

**C'est donc l'étape 0 du plan** ✓ — et elle est **petite** : le format GGUF du moteur est **déjà lu par
lui** ✓ (les modèles Qwen3-MoE de l'entraîneur ont la même architecture que ceux qu'il exécute ✓), il
manque **l'écriture** ✗. Tant qu'elle n'est pas faite, aucun des quatre étapes du § 3 ne peut être
mesurée **dans le moteur** ✗✓ — et mesurer **hors** du moteur, c'est renoncer à la règle du dépôt
(« une implémentation qu'on ne peut pas comparer à une seconde est une implémentation qu'on ne peut pas
vérifier » ✓).

### Le plan corrigé

| # | étape | état |
|---|---|---|
| **0** | **écrire le GGUF** d'un modèle routé en octets (et vérifier que le moteur rend la même perplexité que l'entraîneur ✓) | **à faire** ✗ — le chaînon manquant, trouvé en essayant ✓ |
| 1 | têtes précoces ✓ | après l'étape 0 ✓ |
| 2 | bloc de pensée contractant ✓ | après ✓ |
| 3 | pont de région appris ✓ | après ✓ |
| 4 | échelle ✓ | après ✓ |
