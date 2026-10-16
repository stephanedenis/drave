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

## 7. L'OBJECTIF D'IDENTITÉ (directive du 16/10) — mesuré : les deux espaces sont à un facteur **648**

La directive de Stéphane ✓ : *« l'idéal est d'arriver à avoir un modèle post-linguistique et
prélinguistique IDENTIQUE afin de pouvoir coupler directement pendant les itérations d'inférence. Il faut
donc travailler sur les modèles linguistiques d'entrée et de sortie afin d'arriver à une abstraction
parfaite. »* — c'est-à-dire : **ne pas apprendre un pont** ✗, **rendre les deux espaces le même** ✓✓.

Mesure faite immédiatement sur le modèle disponible (Qwen2.5-0.5B ✓, 4 095 couples état → embedding du
jeton suivant ✓) :

| | valeur |
|---|---:|
| norme moyenne de l'**état** (prélinguistique, avant la norme finale) | **285,533** |
| norme moyenne de l'**embedding** (postlinguistique, entrée) | **0,440** |
| **rapport des deux** | **648,7** ✗✗ |
| **cosinus direct** état ↔ embedding du jeton suivant | **+0,1387** ✗ |
| identité **brute** (l'état tel quel) | écart **64 830 %** ✗✗ |
| identité à **une** échelle globale | 99,10 % ✗ |
| identité + une échelle + un décalage globaux | 127,52 % ✗ |
| témoin bête (embedding moyen) | 97,05 % |

* **les deux espaces ne sont PAS le même** ✗✓ — et de deux façons **indépendantes** : un **facteur
  d'échelle de ~650** ✗ (l'état vit à 285 ✓, l'embedding à 0,44 ✓) **et** des **directions presque
  étrangères** ✗ (cosinus **+0,14** ✓ — *sous* le témoin de l'embedding moyen, 0,24 ✗✓) ;
* **c'est la raison de tous les échecs de la journée** ✓✓ : la boucle silencieuse éclatait (×30 000 ✓)
  **parce que** l'état n'est pas une entrée ✗ — normer n'y changeait rien ✓ **parce que l'échelle n'est
  que la moitié du problème** ✗✓, et la direction est l'autre moitié ✓ ;
* **et l'identité, dans ses formes les plus pauvres, est PIRE que le témoin bête** ✗ (99 % et 127 %
  contre 97 % ✓) : il n'y a **rien à espérer** d'un alignement a posteriori ✗ — ni d'une échelle ✗, ni
  d'un décalage ✗, ni d'un ridge (69 % ✓, mais c'est un **lecteur**, pas un **inverse** ✗) ;
* **donc la seule voie est celle que la directive indique** ✓✓ : **entraîner** le modèle pour que les
  deux espaces **coïncident**, au lieu de les raccorder après coup ✗.

### L'objectif d'entraînement qui en découle (pour le modèle natif ✓)

L'entraîneur du dépôt a **déjà** la moitié de la réponse ✓ : `tie_word_embeddings=True` ✓ — la matrice
d'entrée **est** la matrice de sortie ✓. Il manque **deux** choses, et elles sont petites ✓ :

1. **une norme finale CALIBRÉE** ✗ : la couche qui précède la tête doit sortir des vecteurs **à l'échelle
   des embeddings** ✓ (aujourd'hui ×650 ✗) — c'est une contrainte sur l'initialisation et sur la
   normalisation ✓, pas une couche de plus ✓ ;
2. **une perte d'ALIGNEMENT** ✗✓ : ajouter à la perte de langue un terme `‖norme(état_p) − e_{p+1}‖` ✓ —
   le modèle apprend alors que **son état final EST une entrée** ✓✓, et la boucle devient **directe**
   (aucun pont ✗) : `état → (entrée) → état → …` ✓✓.

**Ce qui se mesure ensuite, et dans cet ordre** ✓ : (a) le **cosinus** état ↔ embedding (0,14 today ✗ →
viser >0,9 ✓) et le **rapport d'échelle** (648 ✗ → viser 1 ✓) ; (b) l'erreur de l'**identité** (64 830 %
✗ → viser moins que le témoin bête ✓, puis moins que le jeton ✓) ; (c) **λ du pas direct** ✓
(`cycle_sensibilite.py` ✓) — la boucle n'est utile que si elle **ne diverge pas** ✓ ; (d) et alors
seulement, la **perplexité de la suite** après k pas silencieux ✓ (`pensee_silencieuse.py` ✓).

*C'est la différence entre raccorder deux langues ✗ et n'en parler qu'une ✓✓.*

## 8. LE PLAN DE TRAVAIL DU « MODÈLE LINGUISTIQUE UNIFIÉ » (entrée = sortie)

Parce que **la mesure a dit de combien** les deux espaces diffèrent (§ 7 : facteur **648** d'échelle,
cosinus **+0,14** ✗), et parce que la plomberie existe déjà ✓, le plan tient en **quatre étapes**, chacune
avec **son critère de réussite chiffré** ✓ et **son critère d'échec** ✗.

### Ce qui est DÉJÀ en place (vérifié dans le code, pas supposé ✓)

| pièce | état |
|---|---|
| **matrice d'entrée = matrice de sortie** | ✅ **déjà fait** ✗✓ : `tie_word_embeddings=True` ✓ et `lm_head.weight` **est** `model.embed_tokens.weight` ✓ (le même objet ✓, noté dans le code depuis le 10/10 ✓) |
| **perte auxiliaire** | ✅ **le patron existe** ✓ : `--enseignant` + `--alpha-distill` ajoutent déjà un terme KL à la perte ✓ — l'alignement est **le même genre d'édition** ✓ |
| **mesure de l'écart** | ✅ **écrite** ✓ : écart d'échelle, cosinus, erreur de l'identité ✓ (le script de ce soir ✓) |
| **mesure de la boucle** | ✅ **écrite** ✓ : λ (`cycle_sensibilite.py` ✓), contenu après k pas (`pas_latent.py` ✓), perplexité de la suite (`pensee_silencieuse.py` ✓) |
| **aller-retour entraîneur → moteur** | ❌ **absent** ✗ : l'entraîneur écrit du HuggingFace, le moteur lit du GGUF ✓ (étape 0 ci-dessous ✓) |

### Les quatre étapes

| # | ce qu'on fait | critère de **réussite** | critère d'**échec** ✗ | coût |
|---|---|---|---|---|
| **0** | **écrire le GGUF** d'un modèle routé en octets ✓, et vérifier que le moteur rend **la même perplexité** que l'entraîneur ✓ | la perplexité du moteur = celle de l'entraîneur ✓ (à l'arrondi de quantification près ✓) | un écart inexplicable ✗ → la lecture GGUF du routé est en cause ✓ | court ✓ |
| **A** | **l'alignement**, sur le modèle **jouet** (2 M, octets ✓) : ajouter `--alignement λ_a` ✓ — la perte `λ_a · ‖n(h_p) − e_{p+1}‖²` **avec la cible DÉTACHÉE** ✗ (sinon les embeddings s'effondrent ✗✗ : on aligne l'état **vers** l'embedding, pas les deux l'un vers l'autre ✓) | **cosinus(n(h_p), e_{p+1}) > 0,9** ✓ et **rapport d'échelle ≈ 1** ✓ (aujourd'hui 0,14 et 648 ✗) | la langue se dégrade ✗ (bits/octet qui s'envolent ✓) → l'alignement **combat** la prédiction ✓, et il faut un poids plus faible ✓ | **minutes** ✓ (2 M ✓, une carte ✓) |
| **B** | **la boucle directe** : itérer **sans aucun pont** ✓ (`h ← n(h)` réinjecté ✓) sur le modèle aligné ✓ | **λ ≤ 1** ✓ (la boucle ne diverge pas ✓) **et** le contenu survit après 4-16 pas ✓ | λ ≫ 1 ✗ → l'alignement n'a pas suffi ✗, et il faut **entraîner le pas** (pénalité de contraction ✓) | heures ✓ |
| **C** | **l'échelle** : 20-50 M ✓ sur **deux cartes** ✓, puis décision **octets ou BPE** ✗ | les mêmes chiffres à l'échelle ✓ | les mécanismes cessent de payer en grandissant ✗ → ils restent des curiosités de banc ✓ | jours ✓ |

### Le risque principal, nommé d'avance ✗✗

**Aligner l'état sur l'embedding du jeton SUIVANT fait de l'état ≈ « l'embedding prédit »** ✗ — c'est-à-dire
**exactement une information de jeton** ✓. Or toute la mesure du § 5 dit l'inverse de ce qu'on veut ✗✓ :
l'état porte **une trajectoire** (16 jetons d'avance à 84,7 % ✓), le mot n'en est qu'un **résumé pauvre**
(122,9 % ✗). **Le risque est donc un EFFONDREMENT vers le niveau du jeton** ✗✗ — et il se mesure ✓ : après
alignement, refaire le **balayage par horizon** (`pont_abstrait.py --couches … --horizons 1,4,16` ✓) et
vérifier que le **k=16 tient** ✓. S'il s'effondre ✗, la variante à essayer est un **alignement multi-pas** ✗
(état ⇄ *moyenne pondérée des embeddings des k prochains jetons* ✓, ou un **vecteur de pensée** appris ✓)
— c'est-à-dire : **unifier les espaces sans réduire la pensée au mot** ✓✓.

### L'ordre que je propose, et pourquoi

**0 puis A sur le jouet** ✓✓ : l'étape 0 débloque la mesure **dans le moteur** ✓ (la règle du dépôt ✗), et
l'étape A se fait en **minutes** sur un modèle de 2 M ✓ — donc on sait **ce soir** si l'alignement tient
sa promesse ✓ ou s'il effondre la représentation ✗. **B** n'a de sens qu'après ✓ (sans alignement, la
boucle directe explose — c'est mesuré ✗✓). **C** ne se discute qu'avec A et B acquis ✓.

## 9. LA SONDE DE RECOPIE (question de Stéphane) : la prémisse est FAUSSE sur ce modèle — et ma mesure était dégénérée

**La question** ✓ : *« peut-on demander à un LLM de présenter littéralement un texte soumis en entrée afin
d'aller chercher des empreintes à reproduire ? »* — c'est-à-dire : utiliser la **recopie littérale** comme
sonde ✓, puisqu'on est dans un régime **sens → texte** (Mel'čuk ✓, mais abstrait ✓) où l'entrée est
**propre** ✓ (pas de bruit à gommer ✓), le problème étant de **boucler** sur l'entrée ✗.

**Deux mesures, faites immédiatement** ✓ :

| ce qui a été mesuré | résultat |
|---|---|
| **le modèle recopie-t-il ?** (128 jetons, consigne « Recopie exactement… puis Recopie : » ✓) | **0 / 128 jetons identiques** ✗✗ |
| l'état dit-il le jeton qu'il **lit** (même position ✓) ? | **0,0 % d'écart, cosinus +1,000** ✗ — à toutes les couches ✓ |

* **LA PRÉMISSE EST FAUSSE SUR CE MODÈLE** ✗✓ : « si un LLM peut répéter intégralement un énoncé » ✓
  suppose qu'il **peut** ✗ — le 0,5 B disponible en est **incapable** (0 sur 128 ✓). Sa copie n'est pas
  approximative : elle est **absente** ✓✗. La sonde de recopie **exige donc un modèle qui sait recopier** ✓
  — soit **plus gros** ✗, soit **entraîné pour ça** ✓✓ (un LoRA sur des paires « recopie » se fait en
  heures sur les deux cartes ✓ — et c'est **le préalable** à toute la suite ✓) ;
* **ET MA MESURE D'EMPREINTE ÉTAIT DÉGÉNÉRÉE** ✗✓ — il faut le dire : j'ai ajusté `état_p → embedding du
  jeton de la position p` ✓, or l'état à la position p **contient** son entrée **par construction** ✓✓
  (c'est le flux résiduel ✗) → l'écart **0,0 %** et le cosinus **+1,000** ne mesurent **rien** ✓. Les
  quatre contextes (lecture ✓, recopie ✓, relecture ✓, résumé ✓) donnent donc le **même chiffre trivial** ✗ ;
* **la BONNE empreinte, celle que la question vise** ✓✓ : pendant la **génération** de la copie ✓, l'état à
  la position **émise** `q` doit dire le **jeton source** correspondant ✓ (celui qu'on est en train de
  reproduire ✓) — c'est cela, « l'empreinte à reproduire » ✓. Et elle se compare à un témoin : le même
  état confronté à un **autre** jeton source ✗ (contre-épreuve obligatoire ✓, sinon on mesure encore une
  trivialité ✓) ;
* **ce que cela change dans le plan** (§ 8 ✓) : une **étape −1** s'ajoute ✗ — **obtenir un modèle qui
  recopie** ✓ (LoRA de recopie ✓, ou modèle plus gros ✓), **puis** mesurer l'empreinte **pendant la
  génération** ✓, **puis** seulement l'alignement entrée/sortie ✓. L'ordre s'impose de lui-même : *sans
  copie, pas d'empreinte ; sans empreinte, rien à aligner* ✓✓.
