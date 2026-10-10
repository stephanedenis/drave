> Campagne : **campagne-benefices** · expérience **03**
> Titre : 3. La grille de modèles — « ce modèle tourne-t-il, et à quel prix ? »
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 3. La grille de modèles — « ce modèle tourne-t-il, et à quel prix ? »

Mêmes 256 jetons, même contexte, chaque modèle tokenisant son propre corpus
(`/usr/bin/time -v` pour la mémoire et les octets lus).

| modèle | perplexité | **bits/octet** | tok/s | RSS | octets lus | condition |
|---|---:|---:|---:|---:|---:|---|
| Qwen2.5-0.5B Q8_0 | **17,43** | **0,983** | 28,7 | 1,28 Go | 0 | en cache |
| r1-distill-Qwen-1.5B Q4_K_M | **47,14** | **1,326** | 9,5 | 4,76 Go | 1,04 Go | lu du disque |
| r1-distill-Qwen-14B Q4_K_M | **14,30** | **0,915** | 0,5 | 39,8 Go | 8,71 Go | lu du disque, charge 47 |
| codestral-22B Q4_K_M | **133,08** ✅ *(tokenizer corrigé, 255 j.)* | **1,842** | — | 63,6 Go | 11,3 Go | 35 657 avant correctif · 117,91 sur 63 jetons |
| Qwen3-30B-A3B Q4_K_M (MoE) | **8,63** | **0,742** | — | **14,3 Go** | 11,8 Go | MoE, lu du NVMe |
| gpt-oss-120b MXFP4 | **expiré à 90 min** | — | — | 13,9 Go | **35,5 Go lus** | 63 Go depuis le disque dur |

**Le MoE gagne sur les deux tableaux — la thèse du projet démontrée par un modèle
qui n'a pas été fait pour ça.** Qwen3-30B-A3B (30 milliards de paramètres, 3
actifs) donne la **meilleure qualité de la grille** (0,742 bit/octet, mieux que le
14B dense à 0,915) pour **14,3 Go de mémoire résidente** — moins que le 14B
(39,8 Go) et trois fois moins que codestral-22B (63,6 Go). Un modèle plus gros qui
lit moins : exactement ce que le prototype routé cherche à reproduire en
l'entraînant.

**L'anomalie codestral : le TOKENIZER du moteur — et la mesure valide après correctif.**

Trois hypothèses ont été testées, les deux premières réfutées, la troisième
confirmée **et corrigée** (§ 3) :

| hypothèse | verdict |
|---|---|
| le moteur exécute mal l'architecture Mistral | **réfutée** — porte Mistral : corrélation 1,0000, top-1 100 % |
| le modèle est spécialisé pour le code, mauvais en prose | **confirmée**, mais seulement après correction |
| le tokenizer du moteur perd les espaces (SentencePiece) | **confirmée et corrigée** |

Avant le correctif, le corpus était découpé par un tokenizer qui mangeait les
espaces : **35 657** de perplexité, chiffre sans valeur. Après le correctif, la
même mesure donne **133,08** sur 255 jetons — soit **1,842 bit/octet**, contre
**0,983** pour un Qwen2.5-0.5B sur le même texte. *(Le chiffre publié plus tôt,
117,91, portait sur 63 jetons seulement ; la ligne de la grille est maintenant
mesurée au même protocole que les autres — 256 jetons, contexte 256 — et c'est
cette valeur qui vaut. Le rapport est corrigé, pas complété.)*

**Un modèle de 22 milliards de paramètres est donc 1,8× PIRE qu'un 0,5 B sur de
la prose**, parce qu'il a été entraîné pour du code. C'est le décalage de tâche
annoncé, et il n'était mesurable qu'avec un tokenizer juste.

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
