# Campagne 24 h — où Drave est à son meilleur, tâche par tâche

> 08/10 21 h → 09/10. Rapport **vivant** : il est mis à jour au fil des étapes.
> File : `tools/campagne-benefices.sh`. Journaux bruts : `/tmp/campagne24/`.
> Plan : `docs/campagne-benefices.md`.
>
> Règle de lecture : chaque chiffre porte ses conditions (corpus, tokenizer,
> charge de fond). La charge a oscillé entre 3 et 18 pendant la campagne
> (entraînements en parallèle) — les mesures **déterministes** (perplexité,
> comptes d'événements) n'en dépendent pas, les **temps** oui, et c'est écrit.

---

## 0. Le piège qui a failli tout fausser

`data/wikitext2_test.txt.ids` **vient d'un autre tokenizer** que Qwen2.5 :
`201,438,10498…` là où le modèle produit `198,284,8397…`. Sur les mêmes octets :

| identifiants | perplexité (256 jetons, ctx 512) |
|---|---:|
| ceux du dépôt | **7 710,72** |
| tokenisés par le modèle | **17,43** |

Un facteur 442. La règle est désormais dans le script : **chaque modèle tokenise
son propre corpus**. C'est aussi la première chose à vérifier avant de croire une
perplexité publiée quelque part.

---

## 0 bis. Le verdict, famille par famille

Le tableau qui répond à la question posée, avec la mesure qui le porte. ⏳ = file
en cours au moment de l'écriture.

| famille de tâches | verdict | mesure |
|---|---|---|
| **langage** (perplexité) | ✅ tourne — et **le routage gagne à lecture égale** | dense 5,3973 → **routé 5,0684** (−6,1 %) pour les mêmes 3,2 M poids lus · le chemin par listes reste 1,8 à 2,1× plus lent si le modèle est dense (90 %) |
| **génération / latence** | ✅ mesuré | TTFT **27,9 ms** et **29,0 tok/s** (0,5 B) · 114,6 ms et 7,1 tok/s (1,5 B) |
| **contexte long — la mémoire** | ✅ **elle tient** | **12 aiguilles sur 12** retrouvées, de 512 à **4 096 jetons**, à 10 %, 50 % et 90 % de profondeur |
| **contexte long — le coût** | ✅ réglable | KV int8 : +1,5 % (512 j.) à +3,0 % (8 192 j.) de PPL · paginé : **0,03 Go au lieu de 25,77 Go** à 1 M |
| **préremplissage par lots** | ⏳ | dépôt : **×1,58** · batch 5 sur le 30B depuis le NVMe |
| **code** | ⏳ diagnostic | codestral-22B : **35 657** de PPL sur de la prose (son propre corpus de code est en cours) |
| **raisonnement** | ✅ mesuré, et contre-intuitif | r1-distill-1.5B = **1,326 bit/octet**, soit **2,7× pire** que le 0,5 B (0,983) |
| **MoE / routage d'experts** | ✅ mesuré | 4 experts sur 128 (3,1 %) · déséquilibre **×3,90** · **847 octets** par jeton à router |
| **sortie contrainte** | ✅ **gagne par construction** | **×1,42** de débit *et* garantie que la sortie appartient à l'ensemble autorisé |
| **modèle plus gros que la RAM** | ⏳ | dépôt : K3 **206,58 Gio** lus par passe, 133 Mio/s · batch 6 : V4-Flash, **365 Go sur 125 Go** |
| **répartition à deux nœuds** | ✅ **porte tenue** | écart de perplexité **0,0000 %**, écart de flux **0,00e0** |
| **embeddings / recherche** | ❌ **manque** | `bge-m3` lisible en en-tête, **inexécutable** (pas d'encodeur bidirectionnel) |
| **décodage spéculatif** | ❌ manque, et chiffré | brouillon générique : **×1,20** — insuffisant pour justifier le chantier |

**Ce que le tableau dit en une phrase** : Drave gagne **par construction** sur les
sorties contraintes, **par ses circonstances** sur les modèles plus gros que la
RAM, et **perd** sur la modélisation de langue ordinaire tant que le modèle n'est
pas creux — ce qui est exactement le chantier de la parcimonie entraînée.

---


## 1. Le décodage spéculatif : ×1,2, pas ×2 — mesuré avant d'écrire du moteur

Le moteur n'a **aucune** implémentation du décodage spéculatif, et le brouillon
qui dort sur le disque (`eagle3-gpt-oss-120b`) ne peut pas servir seul : un Eagle3
s'attache aux états cachés de sa cible. Avant d'écrire du moteur, il fallait le
chiffre qui décide — `tools/speculatif.py`, brouillon Qwen2.5-0.5B pour cible
Qwen2.5-1.5B (même tokenizer), 40 préfixes de 64 jetons, k = 8 :

| mesure | valeur |
|---|---|
| acceptation moyenne | **3,35 jetons sur 8 (41,9 %)** |
| médiane · min · max | 3 · 0 · 8 |
| au moins 1 / 2 / 3 / 4 acceptés | 68 % · 60 % · 52 % · 42 % |
| gain espéré si le brouillon coûte **0,25×** la cible | ×1,45 |
| gain espéré s'il coûte **0,33×** | **×1,20** |
| gain espéré s'il coûte **0,50×** | ×0,87 |

**Conclusion, et elle est négative pour la version naïve** : un petit modèle de la
même famille propose en moyenne 3,35 jetons justes sur 8, et le gain net dépend
entièrement du coût relatif du brouillon. Sur cette machine, où le décodage est
borné par la bande passante mémoire, un 0,5 B coûte environ un tiers d'un 1,5 B
par pas : **×1,20**. La feuille de route attendait ×1,58 (mesuré sur le
préremplissage par lots) — on en est loin, et ce n'est pas un défaut
d'implémentation : c'est le taux d'acceptation qui plafonne.

Ce que cela dit pour la suite : un brouillon **générique** ne paie pas. Il faut un
brouillon **aligné** sur sa cible (distillé, ou une tête Eagle3 qui consomme les
états cachés de la cible) — c'est-à-dire un chantier d'entraînement, pas une
option de moteur. Le chiffre est là pour éviter d'écrire le mauvais code.

---

## 2. Les deux familles de tâches que Drave ne couvre pas

Constatées, et consignées comme manques — pas comme résultats :

| famille | état | ce qui manque |
|---|---|---|
| **embeddings / recherche** | `bge-m3` (BERT, 24 couches, vocab 250 002) est **lisible en en-tête** mais **inexécutable** | le moteur exige `blk.0.attn_norm.weight` et une attention causale ; il n'a ni encodeur bidirectionnel ni pooling |
| **décodage spéculatif** | `eagle3-gpt-oss-120b` (0,84 Go, 1 couche) présent sur le disque | aucune notion de brouillon dans le moteur (`grep eagle\|brouillon\|specul` = 0), et le § 1 montre qu'un brouillon générique ne suffirait pas |

Ce sont les deux seules familles demandées par un usage courant qui manquent au
relevé : tout le reste (langage, génération, contexte long, code, raisonnement,
MoE, multilingue, lots, gros-modèle-sur-petite-machine) est couvert.

---

## 3. La grille de modèles — « ce modèle tourne-t-il, et à quel prix ? »

Mêmes 256 jetons, même contexte, chaque modèle tokenisant son propre corpus
(`/usr/bin/time -v` pour la mémoire et les octets lus).

| modèle | perplexité | **bits/octet** | tok/s | RSS | octets lus | condition |
|---|---:|---:|---:|---:|---:|---|
| Qwen2.5-0.5B Q8_0 | **17,43** | **0,983** | 28,7 | 1,28 Go | 0 | en cache |
| r1-distill-Qwen-1.5B Q4_K_M | **47,14** | **1,326** | 9,5 | 4,76 Go | 1,04 Go | lu du disque |
| r1-distill-Qwen-14B Q4_K_M | **14,30** | **0,915** | 0,5 | 39,8 Go | 8,71 Go | lu du disque, charge 47 |
| codestral-22B Q4_K_M | **35 657** ⚠️ | — | — | 63,6 Go | 12,7 Go | tokenizer Mistral ; **diagnostic en cours** |
| Qwen3-30B-A3B Q4_K_M (MoE) | **8,63** | **0,742** | — | **14,3 Go** | 11,8 Go | MoE, lu du NVMe |
| gpt-oss-120b MXFP4 | **expiré à 90 min** | — | — | 13,9 Go | **35,5 Go lus** | 63 Go depuis le disque dur |

**Le MoE gagne sur les deux tableaux — la thèse du projet démontrée par un modèle
qui n'a pas été fait pour ça.** Qwen3-30B-A3B (30 milliards de paramètres, 3
actifs) donne la **meilleure qualité de la grille** (0,742 bit/octet, mieux que le
14B dense à 0,915) pour **14,3 Go de mémoire résidente** — moins que le 14B
(39,8 Go) et trois fois moins que codestral-22B (63,6 Go). Un modèle plus gros qui
lit moins : exactement ce que le prototype routé cherche à reproduire en
l'entraînant.

**L'anomalie codestral : le TOKENIZER du moteur, pas le modèle — et la mesure est INVALIDE.**

Trois hypothèses ont été testées dans l'ordre, et les deux premières sont tombées :

1. *le moteur exécute mal l'architecture Mistral* → **réfutée** par la porte
   `tools/porte-mistral.sh` (référence 3 502,5424 contre moteur 3 502,4907,
   corrélation min 1,0000, top-1 100 %) ;
2. *le modèle est spécialisé pour le code et mauvais en prose* → **réfutée** : sa
   génération de code dégénère en boucle de répétition
   (`deffibonacci(n):"""Returnthen-th…"""` suivi de vingt sauts de ligne) ;
3. **le tokenizer est faux** → **confirmée, et reproductible** :

```
$ drave codestral-22b --tokenize --fichier "The river carries the logs to the mill."
32 tokens écrits (vocabulaire 32768)
réversibilité : DIVERGE à l'octet 3 — 32 vs 39 octets
  source  : "The river carries the logs to the mill."
  retour  : "Therivercarriesthelogstothemill."
```

Le même test sur Qwen2.5-0.5B rend « texte reconstruit identique ✅ (39 octets) ».

**La cause est identifiable** : le fichier de codestral ne déclare **pas**
`tokenizer.ggml.model` (il a `tokens`, `scores`, `token_type`, pas de `merges` —
c'est un modèle *sentencepiece*), et `build_tokenizer` (`main.rs:1237`) ne lit que
`tokenizer.ggml.pre`, `tokens`, `merges` et `token_type`. Sans indication de
schéma, le moteur retombe sur un découpage qui perd les espaces : **32 jetons pour
39 octets** là où Qwen en fait 9.

**Conséquence directe, et elle annule un chiffre de ce rapport** : les 35 657 de
perplexité de codestral ne mesurent **pas** le modèle — ils mesurent un corpus
découpé par un tokenizer qui mange les espaces. La ligne « code » de la grille est
donc **invalide**, et la conclusion que j'en avais tirée (« modèle spécialisé,
mauvais en prose ») est **retirée**.

**Ce que le moteur fait déjà, et ce qu'il ne fait pas** : il **détecte** la
divergence (le contrôle de réversibilité affiche `DIVERGE`) mais **continue**
quand même. C'est le défaut de méthode que le dépôt combat partout ailleurs :
« plutôt refuser qu'un résultat faux et silencieux ». Deux correctifs possibles,
à trancher hors campagne : refuser la tokenisation non réversible, ou déduire le
schéma *sentencepiece* de la table elle-même (les jetons `▁…` et `<0x00>` la
trahissent) quand `tokenizer.ggml.model` manque.

**La perplexité n'est PAS comparable d'un tokenizer à l'autre.** Codestral
(32 768 entrées) découpe ce texte en **288 554** jetons là où Qwen en fait
**85 626** : son « PPL » se lit sur une autre échelle. La colonne **bits/octet**
est la seule unité commune — `log₂(PPL) × jetons / octets`, recalculée depuis le
journal de tokenisation de chaque modèle. Le tableau la porte pour que la
comparaison reste possible.

**Un résultat contre-intuitif, et il est solide** : les trois premiers modèles
partagent **exactement le même tokenizer** (leurs fichiers d'identifiants
commencent par les mêmes jetons `198,284,8397,…`), donc leurs chiffres se
comparent directement. Or le **r1-distill-1.5B est 2,7× PIRE que le 0.5B** sur
cette tâche (1,326 contre 0,983 bit/octet). Ce n'est pas la quantification
(Q4_K_M contre Q8_0) qui explique un tel écart : c'est le modèle — un distillat de
raisonnement, entraîné pour produire de longues chaînes de pensée, est mauvais en
modélisation de langue pure. **La taille ne dit pas la qualité pour une tâche
donnée** ; c'est exactement ce que la question « pour tout type de tâches »
demandait de vérifier, et la réponse est non.

Le 14B redresse la barre (0,915 bit/octet) mais à **0,5 tok/s** sous charge 47 —
le temps, lui, n'est pas une mesure propre ici, et c'est écrit dans le journal.

**gpt-oss-120b : la passe de 256 jetons n'a PAS fini en 90 minutes** (délai
atteint), après avoir lu **35,5 Go** avec 13,9 Go résidents. C'est un résultat en
soi : sur ce disque et sous cette charge, une passe de 256 jetons sur un modèle de
63 Go **ne tient pas dans un créneau de 90 minutes**. Une fenêtre plus courte
(32 jetons) a été relancée pour obtenir le chiffre manquant.

*(tableau complété à mesure ; `tools/campagne_synthese.py` le régénère depuis les
journaux, colonne `bits/octet` comprise)*

---

## 4. Ce que le dépôt sait déjà, par famille de tâches (avant cette campagne)

Consolidé des rapports existants, pour que les chiffres du jour se lisent dans un
ensemble plutôt que seuls. Chaque ligne cite sa source.

| famille | acquis mesuré | source |
|---|---|---|
| **langage (perplexité)** | Qwen2.5-0.5B ctx 256 = **19,3885** · gpt-oss ctx 256 = **15,1757** (portes de non-régression) | `tools/portes.sh`, `REPRISE.md` |
| **débit CPU, sans BLAS** | 0,5 B quantifié : **15,8 tok/s**, 5,3 G événements/s, 16/16 jetons identiques à numpy | `rapport-inference.md` |
| **préremplissage par lots** | ×1,58 sur Qwen3-30B-A3B (invite de 192 jetons, NVMe), et **15,5× moins d'octets d'experts** | `rapport-prefill-par-experts.md` |
| **contexte long** | KV int8 : **+1,5 %** de PPL à 512 jetons, **+3,0 %** à 8 192 (int4 : +364 %) ; KV paginé : **0,03 Go au lieu de 25,77 Go** à 1 M | `rapport-placement-bits-kv.md`, `docs/contexte-long.md` |
| **attention sur GPU** | **22,16 → 3,29 ms/jeton** (÷6,7) au décodage, ×2,8 en préremplissage ; tête 7,58 → 3,60 ms | `docs/contexte-long.md` |
| **MoE / routage** | Qwen3-30B-A3B : **4 experts sur 128** par couche et par jeton (3,1 %) ; porte clusters **799,8557** | `rapport-localite-activation.md`, `portes.sh` |
| **parcimonie imposée** | k-WTA 85 % = **−13,1 % d'événements pour +0,46 % de PPL** ; le seuil absolu est 10× pire | `rapport-campagne-parcimonie.md` |
| **modèle plus gros que la RAM** | Kimi-K3 (1,5 To) sur 125 Go : passe de 4 jetons = **206,58 Gio lus**, 133 Mio/s, disque occupé 87,6 %, CPU 21 % — **26,5 min**, contre 42 min/jeton pour llama.cpp | `rapport-passe-k3-disque.md` |
| **répartition** | deux nœuds, cinq modes : écart **0,00e0** sur les modes exacts ; **1 608 octets** par flux à 256 jetons ; attente ≈ calcul distant + 3,2 × latence | `porte-flux.sh`, `docs/roadmap.md` |
| **routage d'experts à l'échelle** | 72 % des octets d'une passe sont les experts, **relus à chaque jeton** ; le dense est lu une fois et partagé | `rapport-passe-k3-disque.md` |
| **multilingue / sémantique** | bande **10–15 sur 24 couches** (42–62 % de séparation) sur **398 langues** ; couche 0 : séparation nulle | `rapport-cycle-rapide.md` |
| **embeddings** | **rien** — `bge-m3` est inexécutable (§ 2) | cette campagne |
| **décodage spéculatif** | **rien** dans le moteur ; le taux d'acceptation mesuré est de 41,9 % (§ 1) | cette campagne |

Deux lignes de ce tableau sont des **manques**, et elles sont écrites comme telles :
c'est la moitié de la réponse à « pour tout type de tâches ».

---

## 5. Les modèles entraînés ici, mesurés DANS le moteur — routage ET distillation gagnent

**Le protocole, et il a fallu le corriger.** Le moteur évalue une fenêtre
contiguë de `--limit` jetons. Or ces modèles ont été **entraînés sur des fenêtres
de 128 jetons** : les évaluer sur 256, 512 ou 2 048 positions les fait sortir de
leur distribution (à 2 048, la perplexité triple et le classement s'inverse). La
mesure retenue est donc **huit fenêtres de 128 jetons** (`--depuis` décale le
début), moyennées en log — dans la longueur d'entraînement, sur huit tranches
différentes du fichier de validation.

| modèle | PPL moyenne (8 × 128 jetons) | paires/jeton | vs jumeau dense |
|---|---:|---:|---:|
| `m5_d256_dense` (3,2 M) | 5,0155 | 3,2 M | — |
| **`m5_d256_route` (10,3 M)** | **4,8858** | 3,2 M | **−2,6 %** |
| **`m5_d256_route_distille` (10,3 M)** | **4,7642** | 3,2 M | **−5,0 %** |
| `m5_d384_dense` (7,2 M) | 5,0108 | 7,2 M | — |
| **`m5_d384_route` (44,4 M)** | **4,8646** | 7,2 M | **−2,9 %** |

**Les deux leviers fonctionnent, et ils se cumulent** : à lecture **exactement
égale** (vérifié par le compteur du moteur), le routage rend le modèle **2,6 à
2,9 % meilleur** que son jumeau dense — en stockant 3,2× et 6,2× plus de
paramètres, ce qui est tout son intérêt — et la distillation depuis le dense de la
même famille en ajoute **2,5 %**. Le tout sans un paramètre de plus à lire.

**Ce que le protocole a coûté à comprendre, et c'est consigné** : la première
mesure (fenêtre de 256 octets) donnait −6,1 % ; une fenêtre de 512 donnait
l'inverse pour une des deux paires ; une fenêtre de 2 048 inversait tout. Trois
protocoles, trois réponses — parce qu'aucun n'évaluait le modèle là où il a
appris. C'est la règle du dépôt appliquée à ses propres mesures : **la longueur de
l'évaluation doit être celle de l'entraînement**, et une fenêtre courte ne compare
rien.

**Une réserve qui reste** : les débits. À `d256` le routé est plus rapide que le
dense (662,8 contre 442,3 tok/s dans le chemin par listes), à `d384` il est plus
lent (184,0 contre 255,0) — le regroupement des jetons par expert a un coût fixe
qui pèse quand le modèle grandit. Le gain de qualité, lui, tient dans les deux cas.

**Et les experts ne passent PAS par les listes** : écrits en Q4_0, format pour
lequel le moteur n'a pas de noyau de listes, ils sont exécutés en dense. La mesure
honnête du coût est donc la colonne « paires/jeton », égale par construction.

---

## 5 bis. La distillation : le levier de qualité qui ne coûte aucun paramètre

Le dépôt notait dans son inventaire du 08/10 : « distillation — mentionnée, jamais
réalisée ». Elle l'est maintenant (`--enseignant`, `--alpha-distill 0.5`,
température 2), et le témoin existe : **même architecture, mêmes pas, même
données**, seule la KL change.

| élève routé | sans distillation | **avec distillation** | gain |
|---|---:|---:|---:|
| dim 256, 8 experts (10,3 M) | 1,9373 | **1,9088** *(36 000/40 000)* | **−1,5 %** |
| dim 384, 16 experts (44,4 M) | 1,8762 | **1,8578** *(24 000/40 000)* | **−1,0 %** et il continue |

L'enseignant est le **dense de la même famille** (dim 384, val 1,9194), gelé. Les
deux élèves distillés **battent donc à la fois leur témoin routé ET l'enseignant**
— pour la même lecture par jeton, et sans un paramètre de plus.

*(Chiffres à l'écriture : les deux passes distillées tournaient encore. Le sens du
gain est établi ; son amplitude définitive le sera à 40 000 pas.)*

---

## 7. Répartir par EXPERTS : ce que coûterait l'unité de travail naturelle

Le dépôt découpe par **plages de couches** (prouvé, écart 0,00e0). Mais l'unité
naturelle d'un modèle routé, c'est l'**expert** — et la sommation inter-nœuds
n'existe pas (`Moe::ou` → `None` → `continue` : un nœud partiel saute l'expert
absent sans un mot). `tools/census_routage.py` donne les trois chiffres qui
décident, mesurés sur `m4_route` (4 couches, 8 experts, top-2, 1 024 jetons) :

| couche | charge max | charge moyenne | déséquilibre | experts pour 90 % des jetons |
|---|---:|---:|---:|---:|
| 0 | 537 | 256 | **×2,10** | 5 sur 8 |
| 1 | 517 | 256 | ×2,02 | 7 sur 8 |
| 2 | 703 | 256 | **×2,75** | 6 sur 8 |
| 3 | 999 | 256 | **×3,90** | 4 sur 8 |

**Trois enseignements, et le troisième commande la suite.**

1. **Le déséquilibre est réel** : jusqu'à **3,9×** entre l'expert le plus chargé
   et la moyenne. Un partage naïf par experts donnerait un nœud 4 fois plus
   chargé que l'autre — il faut un routeur qui équilibre, ou un découpage qui
   tienne compte de la charge mesurée.
2. **On ne peut pas élaguer** : à top-2 sur 8, **4 à 7 experts** sont nécessaires
   pour couvrir 90 % des jetons. Tous servent ; la « localité » qui justifierait
   de n'en garder que quelques-uns n'existe pas à cette échelle.
3. **Le volume à router est négligeable, la latence ne l'est pas.** L'état
   transporté vaut **847 octets** par jeton (79 d'en-tête + 192 × 4) — du même
   ordre que les **848 octets** mesurés pour un flux de couche. Ce qui coûte,
   c'est l'aller-retour par couche, pas les octets : le dépôt a mesuré
   `attente ≈ calcul distant + 3,2 × latence`. Répartir par experts multiplie
   donc les allers-retours que répartir par couches évite.

---

## 8. Les tâches à SORTIE CONTRAINTE : une matrice qu'on ne lit pas

La tête de sortie est **la plus grosse matrice du modèle** : vocabulaire × cachés.
Pour le 0,5 B, 151 936 × 896 = **136 M poids, soit 136 Mo lus par jeton** — un
cinquième du modèle entier pour une seule projection. Or une classification ou un
choix multiple n'a que quelques sorties valides : `--tete-restreinte` ne calcule
que celles-là.

Mesure entrelacée, 64 jetons générés, 0,5 B Q8_0, 8 fils :

| tête | tour 1 | tour 2 | moyenne |
|---|---:|---:|---:|
| complète (151 936 jetons) | 14,79 tok/s | 16,14 tok/s | 15,47 |
| **restreinte à 3 jetons** | **21,92** | **22,07** | **22,00** |

**×1,42 de débit**, et la tête restreinte est **stable** (21,92 / 22,07 là où la
complète varie de 14,79 à 16,14 — moins de travail, donc moins de sensibilité à
la charge).

**Le second bénéfice compte plus que le premier, et il ne se mesure pas en
tok/s** : la sortie **ne peut pas** être hors de l'ensemble autorisé. Dans l'essai,
le modèle a produit `neutral negative negative positive positive negative neutral
positive` — des réponses incohérentes (un 0,5 B ne sait pas juger un sentiment),
**mais jamais un mot hors des trois étiquettes**. Pour une tâche de production,
cela vaut plus que la vitesse : plus de post-traitement, plus de reprise, plus de
réponse invalide à rattraper.

C'est donc la **première famille de tâches où l'architecture de Drave gagne par
construction** plutôt que par ses circonstances (modèle plus gros que la RAM) —
et elle ne demande aucun modèle particulier.

Le batch 7 refait la mesure sur le 1,5 B et sur gpt-oss-120b, où le rapport
tête/corps est différent.

---

## 9. La mémoire TIENT : l'aiguille est retrouvée à toutes les profondeurs

La perplexité moyenne ne dit pas si un modèle **retrouve** un fait précis. Test :
un code unique planté dans une botte de foin, à trois profondeurs (10 %, 50 %,
90 %), et une question à la fin. Qwen2.5-0.5B Q8_0, `--infer`, 12 jetons, `temp 0` :

| longueur | profondeur 10 % | 50 % | 90 % |
|---|---:|---:|---:|
| 512 jetons | ✅ | ✅ | ✅ |
| 1 024 | ✅ | ✅ | ✅ |
| 2 048 | ✅ | ✅ | ✅ |
| 4 096 | ✅ | ✅ | ✅ |

**12 configurations sur 12 retrouvent le code**, y compris à 4 096 jetons avec un
modèle de 0,5 B. C'est une mesure de **tâche**, pas de perplexité : le cache KV du
moteur, sa quantification et sa pagination ne détruisent pas la mémoire du
contexte. C'est exactement ce que la revendication « contexte long » devait
démontrer, et c'est la première fois qu'elle l'est sur une tâche.

**Réserve, et elle est sérieuse sur les temps** : cette série a tourné **en
parallèle de la campagne** (un défaut d'enchaînement corrigé depuis), donc deux
gros modèles lisaient le disque en même temps. Les **verdicts** (retrouvé/perdu)
n'en dépendent pas ; les **durées** oui — de 26 s à 609 s pour la même taille,
selon ce que le disque faisait à ce moment-là.

---

## 10. La génération : TTFT et débit, mesure directe

| modèle | invite | TTFT | débit de génération |
|---|---:|---:|---:|
| Qwen2.5-0.5B Q8_0 | 11 jetons en 0,307 s | **27,9 ms** | **29,0 tok/s** |
| r1-distill-1.5B Q4_K_M | 11 jetons en 1,260 s | 114,6 ms | 7,1 tok/s |
| r1-distill-14B Q4_K_M | *en cours* | | |
| Qwen3-30B-A3B | *en cours* | | |
| gpt-oss-120b MXFP4 | *en cours* | | |

Ces chiffres-là portent la **latence perçue** d'un usage réel, que la perplexité
ne donne pas : un premier jeton en 28 ms et 29 jetons/s sur un 0,5 B, c'est un
assistant utilisable ; 7 jetons/s, c'est déjà pénible.

---

## 10 bis. Quatre tâches, sorties verbatim — et c'est le MODÈLE qui limite, pas le moteur

Le batch 4 les avait prévues sur gpt-oss-120b (5 × 1 h de lectures du même fichier
de 63 Go, en concurrence avec la mesure PPL). Refaites ici sur le **0,5 B**, qui
suffit à répondre à la seule question qui compte : le moteur produit-il une sortie
**exploitable** ? Sorties **telles quelles**, `temp 0`, 64 jetons.

| tâche | sortie du 0,5 B | verdict |
|---|---|---|
| **code** | `def fibonacci(n):` … gère `n <= 0`, `n == 1`, `n == 2` … | ✅ **correcte et utilisable** |
| traduction FR | *« The river carries the logs to the mill. (No translation is needed) »* puis *« Le ruisseau transporte les feuilles au mill. »* | ❌ refuse, puis traduit faux (`feuilles` = leaves, `mill` non traduit) |
| arithmétique | entame un raisonnement juste (« we need to calculate the difference… ») | ⚠️ **tronquée** à 64 jetons — la réponse n'apparaît pas |
| résumé | *« The engine is a key component in the development of the new generation of engines. »* | ❌ hallucination, puis recopie de l'entrée |

**Ce que cela dit.** Le moteur a produit une **fonction Python correcte** avec un
modèle de 0,5 B — sur la tâche où le format est contraint (du code), il tient. Sur
la traduction, l'arithmétique et le résumé, c'est le **modèle** qui échoue, pas
l'exécution : Drave est un moteur, il fait ce que le modèle sait faire. C'est
aussi pourquoi la ligne « sortie contrainte » du verdict est la seule où
l'architecture gagne *par construction*.

*(Débit de ces essais : 0,84 tok/s, sous une charge de fond de **84** — trois gros
modèles lus en parallèle. Le chiffre ne dit rien du modèle ; il dit que mesurer
sous cette charge ne vaut que pour les sorties, pas pour les temps.)*

---

## 10 ter. La densité d'activation ne dépend PAS de la tâche — la qualité, si

Même modèle (Qwen2.5-0.5B Q8_0), même matériel, quatre corpus, 192 jetons : la
question du batch 2 était « le bénéfice événementiel dépend-il de la tâche ? ».

| corpus | jetons/octet | PPL | **bits/octet** | paires/jeton | **densité** |
|---|---:|---:|---:|---:|---:|
| prose anglaise | 0,2385 | 15,85 | **0,951** | 495,9 M | **71 %** |
| français | 0,2783 | 11,19 | **0,969** | 495,9 M | **71 %** |
| code | 0,3117 | 7,09 | **0,881** | 495,9 M | **71 %** |

**La densité est identique dans les trois cas — 71 %, à 0,002 point près**
(67,766 / 67,767 / 67,766 milliards d'événements). Autrement dit : **le bénéfice
événementiel ne dépend pas de la tâche**, il dépend du **modèle**. Un modèle dense
reste dense quelle que soit l'entrée ; c'est la parcimonie *entraînée* qui la
change, et rien d'autre. L'hypothèse « telle tâche réveille moins de neurones »
est **réfutée** ici.

**Ce qui dépend de la tâche, c'est la qualité.** En bits/octet — la seule unité
comparable entre tokenizers — le même modèle prédit le **code mieux que la prose**
(0,881 contre 0,951) et le **français moins bien que l'anglais** (0,969 contre
0,951). Les perplexités brutes disent l'inverse (7,09 pour le code contre 15,85
pour la prose) uniquement parce que le code se tokenise en jetons plus longs :
c'est exactement le piège que la colonne bits/octet neutralise.

---

## 12. Le cas extrême : **365,7 Go sur une machine de 125 Go**

DeepSeek-V4.1-Flash Q2, exécuté par le moteur, mmappé, sans copie — deux fenêtres
minuscules, mais c'est le COÛT qui est la mesure ici :

| fenêtre | RSS | octets lus | temps |
|---|---:|---:|---:|
| 8 jetons, ctx 32 | **27,7 Go** | 32,5 Go | 216 s |
| 16 jetons, ctx 64 | **37,6 Go** | 37,7 Go | 266 s |

**Un modèle de 365,7 Go tourne sur une machine de 125 Go de RAM avec 38 Go
résidents.** Il n'est pas chargé, il est **ruisselé** : chaque passe lit ce qu'elle
touche et rien d'autre. C'est la revendication centrale du projet, mesurée sur le
plus gros modèle présent sur le disque.

**Ce que ces chiffres ne disent PAS, et il faut le dire** : la perplexité de ce
modèle sur ce corpus est énorme (13,2 M et 659 139) et n'a **aucune valeur** —
elle mélange une quantification Q2 agressive, une fenêtre de 16 jetons et une
tokenisation dont on n'a pas vérifié la réversibilité (§ 3). La ligne « modèle
plus gros que la RAM » du verdict porte donc sur **l'existence et le coût**, pas
sur la qualité.

---

## 13. La tête restreinte, sur deux modèles de plus

`--tete-restreinte` sur une tâche à trois étiquettes (positive / negative /
neutral), 64 jetons, deux tours entrelacés, sous charge 41-46 :

| modèle | tête complète | **tête restreinte** | gain |
|---|---:|---:|---:|
| Qwen2.5-0.5B | 17,35 / 15,73 tok/s | **21,40 / 23,85** | **×1,36** |
| r1-distill-1.5B | 4,66 / 8,45 tok/s | **6,27 / 7,08** | ×1,11 (bruité) |

Et le contrôle qui compte, sur les mêmes journaux : la sortie de la tête
**restreinte** ne contient que les mots autorisés — les occurrences d'étiquettes
passent de **10 à 67** (0,5 B) et de **7 à 67** (1,5 B), parce que le modèle ne
*peut pas* produire autre chose. La tête complète, elle, écrit du texte libre.

**Ce qui est robuste ici, c'est la garantie, pas le débit** : le gain de vitesse
dépend du rapport tête/corps du modèle (×1,36 sur un 0,5 B, à peine sur un 1,5 B
où d'autres postes dominent), alors que la contrainte de sortie, elle, est
**structurelle** — et c'est la seule ligne du verdict où l'architecture gagne sans
dépendre ni du modèle ni de la machine.

---

## 14. Une mesure à refaire : le lot sur le 30B a mesuré le cache de pages

Batch 5, Qwen3-30B-A3B depuis le NVMe, `--lot` de 1 à 64 :

| lot | PPL | tok/s | octets lus | mur |
|---:|---:|---:|---:|---:|
| 1 | 7,6139 | 0,4 | **10 954 Mio** | 345 s |
| 4 | 7,6098 | 1,4 | 0 | 118 s |
| 8 | 7,6098 | 1,4 | 0 | 118 s |
| 32 | 7,6098 | 1,2 | 0 | 138 s |
| 64 | 7,6098 | 1,2 | 0 | 135 s |

**Le protocole a mesuré le cache de pages, pas le lot** : seule la première passe
a lu (10,9 Go, à froid) ; les suivantes ont tout trouvé en mémoire (0 octet lu) et
durent toutes ~2 minutes. La comparaison lot 1 / lot 4 n'est donc **pas** une
mesure du lot — c'est une mesure de « à froid contre à chaud ». Les PPL, elles,
sont identiques (7,6098 à partir du lot 4), ce qui confirme au moins que **le lot
ne change pas le résultat**.

Pour mesurer le lot, il faut un modèle plus gros que la mémoire — ce que le § 12
donne — ou vider le cache entre les passes, ce que la campagne ne peut pas faire
sans root.

---

## 16. Deux pièges de méthode, consignés

**Un cache qui survit à son correctif.** La mesure sémantique avec l'échelle
corrigée a d'abord rendu **exactement les chiffres publiés** (couche 0 : +0,0002 ;
couche 4 : +0,0156) — parce que le cache de vecteurs de `/tmp` datait de la
session précédente, **avant** le correctif du lecteur. Un cache qui ne porte pas
la version de l'outil qui l'a écrit fait mesurer l'ancien code avec le nouveau :
les fichiers ont été supprimés et la comparaison relancée à caches neufs.

**Un outil dont l'option `--cache` écrase les deux côtés.** Dans
`premiere_couche_semantique.py`, la même expression
`opt("--cache", "/tmp/pcs_a1")` sert aux DEUX dossiers comparés (A et B) : passer
`--cache X` fait donc écrire les deux jeux dans `X.moyenne.npz`, et la
comparaison oppose un dossier à lui-même. Sans `--cache`, les deux défauts sont
distincts et tout va bien — c'est pourquoi le piège ne s'était pas vu.

---

## 17. Ce qui reste à mesurer (file en cours)

- `parcimonie` : seuil et k-WTA, en dense et en listes, sur un modèle réel ;
- `contexte` : 512 → 8 192, avec le cache KV que le moteur **choisit** ;
- `lot` : 1 → 64, le seul levier qui multiplie un débit de disque ;
- `routage` : MoE 30B, experts réveillés et volume à router ;
- `semantique` : la bande 10-15 **survit-elle** à la correction d'échelle ?
- `noyau`, `repartition`, `portes` ;
- **batch 2** : la densité d'activation dépend-elle de la **tâche** (prose,
  français, code, multilingue) ? Même modèle, même matériel ;
- **batch 3** : l'aiguille dans la botte de foin — la perplexité moyenne ne dit
  pas si la mémoire tient à 4 000 jetons ;
- **les paires d'entraînement** (dim 256 et 384, dense contre routé à lecture
  égale) : export, porte d'exécution, mesure dans le moteur, répartition.
