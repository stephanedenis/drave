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

## 10. L'ÉTAPE −1 EST LANCÉE : le LoRA de recopie (`tools/lora_recopie.py`)

**Ce qu'il fait** ✓ : un LoRA (rang 8, **168 projections**, **4,40 M paramètres**, soit **0,88 %** du
modèle ✓) sur des paires tirées du corpus —
* **positive** : « Recopie exactement le texte suivant :\n<texte>\nRecopie :\n<texte> » ✓ (la cible
  **est** la copie ✓) ;
* **de contrôle** ✗ : « Résume en une phrase : … » avec une cible **différente** ✓ — sans elle, le modèle
  apprendrait « répète toujours l'entrée » ✗✓, c'est-à-dire un **perroquet** ✓, ce qui **détruirait** la
  mesure d'empreinte ✓ (on croirait lire une copie alors qu'on lirait un réflexe ✗).
La perte ne porte **que sur les jetons de la cible** ✓, et l'évaluation se fait sur des textes **jamais
vus** ✓.

**L'essai à blanc, et il est déjà parlant** ✓✓ :

| | recopie (plus long préfixe exact) | contrôle (résumé) |
|---|---:|---:|
| avant | **0,5 %** | 1,2 % |
| **après UN seul pas** | **39,3 %** | **0,0 %** ✓ |

* **la copie s'installe immédiatement** ✓✓ (0,5 % → **39,3 %** en un pas ✓) — la capacité est **latente**
  dans le modèle ✓, elle ne demande qu'à être révélée ✓ ;
* **et le contrôle reste à zéro** ✓✓ : le modèle **ne répète pas** quand on lui demande de résumer ✓ — donc
  ce qui s'installe est **une copie commandée** ✓, pas un perroquet ✓✓. C'est exactement la condition pour
  que l'**empreinte** soit mesurable ✓ (§ 9 ✓).

**L'entraînement complet est en cours** ✓ (600 pas, évaluation tous les 100 ✓, une carte ✓, journal
`/tmp/lora-recopie.log` ✓). Ce qu'on lira à la fin : **le taux de recopie** ✓ (viser > 90 % ✓) et **le
contrôle** ✗ (qui doit **rester bas** ✓ — s'il monte, le LoRA est à jeter ✗).

## 11. L'EMPREINTE : **OUI**, la copie littérale fait porter le texte par l'état — et de plus en plus avec la profondeur ✓✓

Étape −1 **réussie** ✓✓ : le LoRA de recopie atteint **100,0 %** sur ses textes et **0,0 %** au contrôle
(perroquet évité ✓) — mais **60,9 %** sur des textes neufs ✗✓ (sur-apprentissage : la mesure porte donc sur
le **préfixe exact** ✓). Étape A, `tools/empreinte.py` ✓ : on génère la copie, **une** passe avant sur
`invite + copie` ✓ donne l'état à chaque position **émise** `q_j` ✓ (le jeton source `j` ✓), on ajuste
`état → embedding(jeton source j+k)` ✓, et on compare à la **contre-épreuve** ✗ (le même état confronté à
un jeton source **décalé de 7** ✓).

**2 698 positions** ✓, couche 16 ✓, **60 textes** ✓, trois couches ✓ :

| couche | régime | **k = 0** (contre ✗) | **k = 1** (contre ✗) |
|---:|---|---:|---:|
| 8 | COPIE | 43,1 % (78,0) | 69,5 % (78,0) |
| 8 | lecture | 44,2 % (78,0) | 69,8 % (78,0) |
| **16** | **COPIE** | 46,2 % (77,6) | **62,5 %** (77,9) ✓ |
| 16 | lecture | 46,8 % (77,8) | 69,6 % (78,1) |
| **23** | **COPIE** | 53,4 % (77,9) | **42,1 %** (77,9) ✓✓✓ |
| 23 | lecture | 51,5 % (78,0) | 68,8 % (78,1) |

* **L'EMPREINTE EXISTE, ET ELLE EST FRANCHE** ✓✓ : partout, le **vrai** alignement (42-53 %) est **très**
  au-dessous de la **contre-épreuve** (78 % ✓, remarquablement **plate** ✓ — c'est ce qui rend la
  comparaison solide ✓). L'état porte donc bien **l'empreinte du jeton qu'il reproduit** ✓✓ — la question
  de Stéphane a une réponse **positive** ✓ ;
* **ET LA COPIE BAT LA LECTURE, DE PLUS EN PLUS AVEC LA PROFONDEUR** ✓✓ : à la couche **23**, k = 1,
  **42,1 %** en copie contre **68,8 %** en lecture ✓✓ — **26 points** d'écart ✓. À la couche 16 l'écart
  est plus faible (62,5 contre 69,6 ✓) et à la couche **8 il disparaît** (69,5 contre 69,8 ✗) →
  **l'avantage de la copie se construit avec la profondeur** ✓✓, dans les couches **prélinguistiques
  tardives** ✓ — exactement le régime que la question visait ✓ ;
* **« présenter littéralement » n'est donc pas un détour** ✓✓ : c'est un **régime de lecture plus fort** ✓
  — demander au modèle de **reproduire** un texte rend son contenu **plus lisible dans l'état** que le
  simple fait de le lire ✓✓ (à condition, bien sûr, qu'il **sache** recopier ✓ — étape −1 ✓) ;
* **les horizons longs restent à faire** ✗ : les cellules k = 4 et k = 16 sont **bloquées** ✗✓ — non par
  la mesure, mais par **mon plan de textes** ✓ : `1 000 + t × 3 000` sort du corpus (85 626 jetons ✓) au
  28ᵉ texte ✓, ce qui plafonne à **2 698 positions** — et la garde (n > 2 688 ✓) refuse **un cheveu**
  au-dessus (2 687 ✓✗). Il suffit de **rapprocher le pas** (ou d'élargir le corpus ✓) pour que k = 4 et
  k = 16 tombent ✓ ;
* **et la leçon de méthode de la soirée, troisième occurrence** ✓✓ : une mesure peut se **déguiser** en
  résultat ✗ — (1) la position **avec elle-même** (0,0 % trivial ✓), (2) **moins de positions que de
  coefficients** (le ridge interpole ✓, 0,0 % encore ✓), (3) **un plan de textes qui sort du corpus**
  (« n = 149 » sur 24 textes demandés ✓). Les trois fois, c'est **la même règle** qui a sauvé la mesure :
  **écrire à côté du chiffre ce qui pourrait le rendre faux** ✗✓.

## 12. L'EMPREINTE EST **LOCALE** : nette à un jeton, nulle au-delà — et la copie **concentre** l'état

Les horizons longs sont maintenant débloqués (pas de textes resserré ✓, **5 365 positions** ✓) :

| couche | régime | **k = 0** (contre ✗) | **k = 1** (contre ✗) | k = 4 (contre ✗) | k = 16 (contre ✗) |
|---:|---|---:|---:|---:|---:|
| 8 | COPIE | 50,0 (87,8) | 77,5 (88,1) | 86,6 (88,2) | 88,1 (88,3) |
| 8 | lecture | 51,2 (87,8) | 77,9 (88,1) | 86,7 (88,2) | 88,0 (88,2) |
| **16** | **COPIE** | 53,1 (87,5) | **70,0** (87,8) | 85,8 (87,9) | 88,0 (88,0) |
| 16 | lecture | 53,7 (87,8) | 77,7 (88,0) | 86,9 (87,9) | 88,1 (88,0) |
| **23** | **COPIE** | 60,4 (87,7) | **49,3** (88,1) | 85,9 (88,0) | 88,1 (88,2) |
| 23 | lecture | 58,6 (88,0) | 76,9 (88,0) | 86,9 (88,1) | 88,0 (88,1) |

* **l'empreinte à un jeton est reproduite** ✓✓ : couche 23, k = 1 → **49,3 %** en copie contre **76,9 %** en
  lecture ✓ (27,6 points ✓ ; la mesure précédente donnait 26 points ✓ — **deux exécutions, même
  conclusion** ✓✓) ;
* **ET ELLE EST LOCALE** ✗✓ : dès **k = 4**, le vrai alignement rejoint la contre-épreuve (85,8-86,9 contre
  87,9-88,2 ✓, soit **2 points** ✗) — l'état, **pendant la copie**, ne porte **pas** le texte à quatre
  jetons d'avance ✗. Ce n'est pas un défaut de mesure ✓ (la contre-épreuve est **stable à 88 %** ✓, la
  mesure est donc bien déterminée ✓) : c'est **la nature de ce que la copie fait à l'état** ✓ ;
* **et c'est un FAIT important, en contradiction apparente avec le § 5** ✓✓ : en **lecture simple**, le
  même type de mapping portait la suite à **16 jetons** d'avance (84,7 % ✓). Ici, **la copie
  CONCENTRE l'état sur le jeton qu'il émet** ✓✓ — elle **aiguise** l'empreinte locale (49 contre 77 ✓) et
  **aplatit** la trajectoire longue (88 = rien ✗). *Copier, c'est braquer le projecteur sur le mot suivant ;
  lire, c'est garder le champ large* ✓✓ ;
* **conséquence pour le projet** ✓ : la copie est **le bon régime pour obtenir des empreintes à
  reproduire** ✓✓ (c'est la question posée ✓), mais **pas** le régime d'une **pensée** qui garde la suite
  ✗ — les deux sont **complémentaires** ✓✓ : la copie pour **extraire** l'empreinte d'un texte ✓, la
  lecture pour **conserver** sa trajectoire ✓. Et l'alignement entrée = sortie (§ 8, étape A ✓) devra se
  faire **sur l'état de lecture**, pas sur celui de la copie ✗✓ — sinon on aligne un état **appauvri** en
  contenu long ✓.

## 13. L'ALIGNEMENT RÉUSSIT (étape 3 ✓✓) MAIS LA BOUCLE DIRECTE ÉCHOUE ENCORE (étape 4 ✗) — il faut entraîner le PAS

### 13.1 L'alignement, mesuré ✓✓

`tools/entrainer_moteur.py --alignement λ` ✓ (deux termes : **cosinus** ✓ et **rapport d'échelle** ✓, cible
**détachée** ✗). Deux jouets de **2,43 M paramètres** ✓ (dim 256, 4 couches, octets ✓), mêmes données, mêmes
1 500 pas, **une carte chacun** ✓ :

| | validation (bits/octet) | cosinus(état, embedding suivant) | rapport d'échelle |
|---|---:|---:|---:|
| **témoin** (λ = 0) | 4,69 | — | — |
| **aligné** (λ = 1) | **4,30** ✓✓ | **+0,701** ✓✓ | **1,015** ✓✓ |
| *rappel : Qwen2.5-0.5B, sans alignement* | — | *+0,14* ✗ | *648* ✗✗ |

* **l'alignement fait ce qu'il promet** ✓✓ : cosinus **+0,14 → +0,70** et échelle **648 → 1,015** ✓ ;
* **et il NE dégrade PAS la langue** ✓✓ — il l'**améliore** (4,30 contre 4,69 bits/octet ✓) : le terme
  d'alignement agit comme un **régularisant** ✓, ce qui est connu mais se mesure ici ✓ ;
* **et le contenu long survit** ✓✓ (`pont_abstrait.py --norme` ✓, horizons ✓) : à **k = 16**, l'aligné fait
  **88,3 %** contre **89,0 %** pour le témoin ✓ — l'**effondrement au mot** ✗ que la fiche annonçait comme
  risque principal **n'a pas eu lieu** ✓✓. Et à **tous** les horizons l'aligné est **meilleur** (69,9 vs
  74,2 · 84,3 vs 85,3 · 88,3 vs 89,0 ✓) ✓.

### 13.2 La boucle directe, et son échec ✗

`tools/boucle_directe.py` ✓ : on **remplace l'embedding** du dernier jeton par `norm(h)` ✓ (aucun pont ✗),
on itère, et on mesure λ (perturbation infime ✓) et le **contenu** (ce que l'état itéré dit du jeton à
venir ✓, mapping appris sur une moitié et mesuré sur l'autre ✓) :

| modèle | **λ** (un pas direct) | contenu à 1 pas | 2 pas | 4 pas | 8 pas |
|---|---:|---:|---:|---:|---:|
| **aligné** | **7 311** ✗✗ | 140,7 % | 144,8 % | 131,2 % | 124,5 % |
| témoin (sans alignement) | 4 265 ✗✗ | 103,0 % | 107,3 % | 105,0 % | 107,4 % |

* **λ reste énorme dans les deux cas** ✗✗ (7 311 et 4 265 ✓) : **un passage complet du réseau est
  expansif** ✓ — c'est cohérent avec tout ce que la nuit a mesuré (cycle : λ ≥ 3,7e4 ✓ ; le pas
  `h_p → h_{p+1}` : λ de 30 à 120 ✓) ;
* **et le contenu se détruit** ✗ (le témoin est à ~105 %, c'est-à-dire **pire que l'embedding moyen** ✓✗ ;
  l'aligné à 124-145 % ✗). Autrement dit : **l'état itéré ne dit plus rien** du jeton à venir ✓ ;
* **pourquoi** ✓ : l'alignement garantit `norm(h_p) ≈ e_{p+1}` pour les états **produits par une passe
  normale** ✓ — il ne dit **rien** de ce que devient un état **réinjecté comme entrée** ✗✓, un régime que
  l'entraînement n'a **jamais vu** ✗. Et un passage de 4 couches **amplifie** la perturbation ✓✗.

### 13.3 La conclusion, et le pas suivant qui est maintenant précis

**L'alignement des espaces est NÉCESSAIRE mais PAS SUFFISANT** ✗✓ : il règle le **vocabulaire** (les deux
espaces se ressemblent ✓) mais pas la **dynamique** (le pas amplifie ✗). C'est **exactement** ce que la
fiche annonçait (§ 8, étape B : « il faut **entraîner le pas**, pénalité de contraction » ✓) et ce que le
cycle réclamait de son côté ✓ — **les trois fils demandent le même objet** ✓✓ :

> **un opérateur de pensée APPRIS** ✓ — une petite cellule récurrente sur l'état ✓, entraînée avec
> **deux** objectifs : **conserver le contenu** (prédire l'embedding à venir ✓ — ce que l'alignement fait
> déjà pour un pas ✓) **et contracter** (λ < 1 ✓, par pénalité de différences finies ✓).

C'est la prochaine étape, et elle est **précise** : la cellule, sa pénalité, et la même batterie de
mesures (λ ✓, contenu ✓, et la perplexité de la suite après k pas ✓).

## 14. L'OPÉRATEUR DE PENSÉE : il existe, il **contracte** (λ = 0,997 ✓✓), il **améliore** le contenu d'un pas (87 → 72 %) — et il ne vaut que pour **un** pas

`tools/operateur_pensee.py` ✓. L'objet est **différent** de la boucle directe ✗ (qui repassait par le
modèle à chaque pas ✓ et explosait : λ = 7 311 ✗) : ici, `C = I + f` ✓ (f un petit MLP, pas borné à 0,1 ✓)
itère **sur l'état seul** ✓, sans aucun passage dans le modèle ✗ — c'est le « mode de fonctionnement
complètement différent » que la question visait ✓. Entraîné sur le jouet **aligné** ✓, avec **deux**
exigences qui ne se satisfont pas l'une sans l'autre ✓ :

* **progresser** ✓ : après un pas, l'état doit dire le jeton à venir **mieux** qu'avant ✓ — sans quoi la
  solution triviale `C = identité` (λ = 1 ✓, contenu intact ✓) gagnerait ✗✗ en ne pensant rien ✓ ;
* **contracter** ✓ : λ(C) ≤ 1 (pénalité de différences finies ✓).

| | résultat |
|---|---|
| **λ de l'opérateur** | **0,9972** ✓✓ — **le premier pas contractant de toute la nuit** ✓ (contre 7 311 en boucle directe ✗, 30-120 pour `h_p → h_{p+1}` ✗, 206-136 pour le cycle ✗) |
| **contenu sans opérateur** (identité ✓) | 87,0 % d'écart |
| **contenu après 1 pas** | **72,0 %** ✓✓ — **15 points de mieux** ✓ |
| contenu après 2 · 4 · 8 pas | 75,1 · 85,7 · **97,2** ✗ (pire que l'identité dès 4 pas ✓✗) |

* **CE QUI MARCHE** ✓✓ : un opérateur **contractant** qui **améliore** la lecture de l'état existe, et il
  s'entraîne ✓. C'est la première fois que les trois exigences de la nuit (contracter ✓, progresser ✓,
  itérer sans le modèle ✓) se rencontrent ✓✓ ;
* **CE QUI NE MARCHE PAS** ✗ : l'itération **n'accumule pas** — 72,0 → 75,1 → 85,7 → 97,2 ✗. La raison est
  **dans la conception** ✓ et il faut le dire : l'opérateur a été entraîné pour **un** pas ✓ (le terme de
  contenu ne regarde que `C(x)` ✓). Rien ne l'oblige à ce que `C(C(x))` reste bon ✗✓ — et c'est
  exactement ce que la mesure montre ✓ ;
* **et la lecture honnête** ✓✓ : *le modèle a **un** pas de pensée, pas une itération* ✓ — l'opérateur
  exploite ce pas (15 points ✓), puis la représentation **cesse d'être pensable** ✗. Ce n'est pas
  l'opérateur qui est en cause ✗ : c'est la **structure de l'état** que l'entraînement du modèle a
  laissée ✓ (un état « à un coup », pas un espace de travail itérable ✗) ;
* **le pas suivant, précis** ✓ : entraîner l'opérateur **pour k pas** (le terme de contenu porte sur
  `C^k(x)` ✓, pour k tiré aléatoirement entre 1 et 8 ✓ — c'est la technique des « états latents
  récurrents » ✓), **et** laisser le modèle s'y adapter ✗ (l'état doit être **habitable** par
  l'itération ✓ — c'est le pont entre « aligner les espaces » ✓ et « entraîner la dynamique » ✓✓).

## 15. L'ITÉRATION EST IMPOSSIBLE SUR CET ÉTAT — la preuve par la solution triviale

L'opérateur du § 14 ne valait que pour **un** pas (72,0 % ✓ puis 75,1 · 85,7 · 97,2 ✗). La correction
évidente a été appliquée ✓ : entraîner le contenu sur `C^k(x)` ✓, k **tiré entre 1 et 8** ✓ — l'opérateur
doit rester bon **après l'itération** ✓. Résultat **sans ambiguïté** ✗ :

| | résultat |
|---|---|
| λ de l'opérateur | **0,9994** ✓ (contracte ✓) |
| contenu après **1** pas | **87,0 %** = **exactement l'identité** ✗ |
| contenu après 2 · 4 · 8 pas | 87,0 · 87,0 · **86,9** ✗ — identiques à l'identité ✓✗ |
| *(rappel : l'opérateur d'un pas donnait 72,0 % à 1 pas ✓)* | |

* **l'optimisation a trouvé la solution triviale** ✓✗ : `f ≈ 0` ✓, c'est-à-dire `C = identité` ✓ — et elle
  est **la seule** qui reste bonne à k = 8 ✓✓, parce que **tout déplacement de l'état dégrade** sa
  lisibilité ✓ ;
* **donc « itérer aide » est FAUX sur cet état** ✗✓, et ce n'est pas une question d'entraînement de
  l'opérateur ✗ : **c'est une propriété de l'état lui-même** ✓✓ — un état **à un coup** ✓ (un « one-shot
  readout ») ✓, pas un espace de travail ✓ ;
* **et cela referme la boucle de la nuit** ✓✓ : les quatre voies essayées (boucle directe ✗, pas
  `h_p → h_{p+1}` ✗, cycle ✗, opérateur post-hoc ✗) échouent **toutes** pour la même raison ✓ — **aucune
  ne rend l'état habitable par l'itération** ✗, parce qu'**aucun modèle entraîné ici n'a jamais eu
  l'itération dans sa boucle** ✗✓ ;
* **la conséquence est nette, et c'est le programme** ✓✓ : il ne suffit pas d'**aligner** les espaces ✓ ni
  d'**ajuster** un opérateur après coup ✗ — il faut **entraîner le modèle avec la récurrence dans sa
  boucle** ✓✓ (un bloc **répété** ✓, comme les « looped transformers » ✗✓) : l'état doit être **habitable**
  par l'itération **parce qu'il a été entraîné à l'être** ✓. C'est la seule voie que la nuit n'a pas
  essayée ✓ — et elle est **mesurable avec les outils déjà écrits** ✓✓ (λ ✓, contenu ✓, horizon ✓).

**Ce que la nuit a établi, en une phrase** ✓ : *on peut unifier le vocabulaire d'entrée et de sortie
(cosinus 0,14 → 0,70 ✓), on peut extraire une empreinte du texte (42 % contre 77 % ✓), on peut même
trouver un pas contractant qui améliore la lecture (λ = 0,997 ✓) — mais **la pensée itérative ne
s'ajoute pas** à un modèle qui ne l'a pas apprise : elle se **construit** dans son entraînement* ✗✓.

## 16. LE BLOC RÉPÉTÉ : l'état devient **plus habitable**, pas encore habitable

La conclusion du § 15 donnait le programme ✓ : **entraîner la récurrence dans la boucle** ✗✓.
`--partage` a été ajouté à l'entraîneur ✓ (toutes les couches partagent les poids de la première ✓ → le
modèle **est** un bloc unique appliqué 4 fois ✓). Deux jouets, **une carte chacun** ✓, 2 000 pas ✓ :

| | validation | *(unique paramètres)* |
|---|---:|---|
| **partagé** (bloc répété ✓) | **4,74** bits/octet ✓ | **4× moins** ✓ |
| distinct (témoin ✗) | 4,69 | — |

**Qualité quasi identique avec quatre fois moins de poids uniques** ✓✓ — le partage ne coûte presque rien ✓.

Puis le test décisif ✓ (`tools/iterer_bloc.py` ✓ : on applique le bloc **t fois** ✓ en dupliquant les
couches ✓) — le **contenu** (ce que l'état dit du jeton à venir ✓) :

| modèle | **t = 1** | **t = 2** | **t = 4** |
|---|---:|---:|---:|
| **partagé** (bloc répété ✓) | **82,9** ✓ | **84,2** ✓ | **86,7** ✓ |
| distinct (témoin ✗) | 85,7 | 85,9 | 87,1 |

* **LE BLOC RÉPÉTÉ EST MEILLEUR DÈS LE PREMIER PASSAGE** ✓✓ (82,9 contre 85,7 ✓) et il **dégrade le
  moins** quand on itère ✓✓ (à t = 4 : **86,7** contre 87,1 ✓ — l'écart se réduit de 2,8 à 0,4 point ✓).
  C'est **le meilleur résultat de la nuit** sur cet axe ✓ ;
* **MAIS IL DÉGRADE QUAND MÊME** ✗ (82,9 → 84,2 → 86,7 ✓) : l'état est **plus habitable**, il n'est **pas
  habitable** ✗✓. Le partage de poids **achète de la robustesse** ✓ sans donner l'itération ✓ ;
* **et il y a deux raisons possibles, qui se départagent par une mesure** ✗ : soit l'entraînement est
  **trop court** ✓ (2 000 pas ✓, un modèle de 4 couches ✓), soit il faudrait **entraîner explicitement sur
  t** ✗ (tirer t entre 1 et 4 à chaque pas ✓, comme l'opérateur du § 15 ✓ — mais **dans le modèle** ✓✓,
  où le partage de poids rend l'itération **gratuite** ✓). C'est la prochaine expérience, et elle est
  petite ✓.

### Et une leçon d'instrument, la quatrième de la soirée ✗✓

Le premier essai a rendu **82,9 / 82,9 / 82,9** ✓ — constant au chiffre près ✗ — et j'ai failli y lire
« *l'état est habitable : le contenu ne bouge pas* » ✓✗. La vérification a montré autre chose ✓✓ : la
boucle de `Qwen3Model.forward` est **bornée par `config.num_hidden_layers`** ✓✗ (mes 8 couches étaient
**silencieusement ignorées** ✓) et `config.layer_types` est une liste **par couche** ✓✗ (IndexError
ensuite ✓). Les deux bornes corrigées, les chiffres ont **bougé** ✓✓ — et l'interprétation a changé du
tout au tout ✓.

*C'est la quatrième fois de la nuit qu'une mesure se déguise en résultat* ✓✓ — et la même règle a sauvé
les quatre : **écrire à côté du chiffre ce qui pourrait le rendre faux** ✗✓.

## 17. L'ÉTAT DEVIENT **HABITABLE** — la première itération plate de la nuit, et son prix

Le § 16 laissait deux explications ✓ ; la mesure les a départagées ✓. `--recurrence-max 4` ajouté à
l'entraîneur ✓ : à chaque pas, le bloc partagé est appliqué **t fois**, **t tiré entre 1 et 4** ✓ (les
poids sont liés **par construction** : la liste contient `t` fois le **même objet** couche 0 ✓✓).

| modèle | **t = 1** | **t = 2** | **t = 4** |
|---|---:|---:|---:|
| **partagé + récurrence aléatoire** ✓ | **88,4** | **88,2** | **88,5** ✓✓ |
| partagé (sans récurrence, § 16 ✗) | 82,9 | 84,2 | 86,7 |
| distinct (témoin ✗) | 85,7 | 85,9 | 87,1 |

* **L'ITÉRATION EST PLATE** ✓✓ — 88,4 · 88,2 · 88,5 : le contenu **ne dégrade plus** avec t, ce qui n'était
  arrivé dans **aucune** des six configurations essayées cette nuit ✓✓. **La réponse à la question du
  § 15 est donc OUI** ✓ : un état **peut** être rendu habitable par l'itération ✓ — à condition que
  l'entraînement ait mis la récurrence **dans la boucle** ✓ et pas seulement dans les poids ✓ ;
* **mais il y a un PRIX, et il est net** ✗ : à **t = 1**, le modèle entraîné sur t est **moins bon**
  (88,4) que celui qui n'a vu qu'un pas (82,9) ✓✗ — **6 points de netteté** perdus ✓. Il a **moyenné** sur
  t = 1..4 ✓ : il est **robuste** mais **émoussé** ✓ ;
* **et le témoin `distinct` reste meilleur à t = 1** ✗ (85,7 contre 88,4 ✓) : la récurrence aléatoire
  n'achète pas la netteté du modèle profond ✓, elle achète la **stabilité** ✓✓ ;
* **le compromis, en une phrase** ✓✓ : *un état peut être **itérable** ou **précis**, et l'entraînement
  choisit le point de ce curseur* ✓ — c'est la première fois que la nuit peut dire cela **avec des
  chiffres** ✓✓.

### Et le chemin de l'entraîneur, qu'il faut noter ✗

Trois échecs successifs, tous d'**outillage**, avant que le run passe ✓ : (1) la **restauration** de la
liste de couches était au mauvais endroit ✓✗ (le trainer sauvegarde le **meilleur point pendant**
l'entraînement ✓) ; (2) `safetensors` **refuse** les tenseurs partagés ✓✗ — et `safe_serialization=False`
n'y change rien, la vérification est **antérieure** au choix du format ✓ ; (3) ma première édition a
**cassé l'indentation** de l'entraîneur ✓✗ (un remplacement qui avalait un bloc imbriqué ✓) — réparé par
`git checkout` **et refait en insertions** ✓. *Un outil qu'on modifie se relit avant qu'on l'exécute* ✓✓.
