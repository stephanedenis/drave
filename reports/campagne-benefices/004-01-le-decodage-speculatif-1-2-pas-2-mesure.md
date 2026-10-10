> Campagne : **campagne-benefices** · expérience **01**
> Titre : 1. Le décodage spéculatif : ×1,2, pas ×2 — mesuré avant d'écrire du moteur
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

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

### 1 bis. Le même chiffre, mesuré PAR LE MOTEUR — et il est bien plus dur

`tools/speculatif_moteur.py` refait la mesure sans HuggingFace : deux GGUF, le
moteur, `--temp 0`, et la comparaison porte sur les **identifiants générés**
(`--- ids générés`), donc sans re-tokenisation. Le vocabulaire partagé est
**vérifié** avant de conclure (même sonde → mêmes identifiants, sinon l'outil
refuse).

Paire mesurée : brouillon **Qwen2.5-0.5B Q8_0** (modèle de base) → cible
**R1-distill-Qwen-1.5B Q4_K_M** (distillat de raisonnement), 8 invites de prose,
48 jetons, k = 8 :

| mesure | valeur |
|---|---|
| acceptation moyenne | **0,88 jeton sur 8 (11 %)** |
| P(préfixe ≥ 1 / 2 / 5) | 38 % · 12 % · 12 % |
| coût relatif du brouillon | 0,210× (14,47 vs 3,04 tok/s, sous charge 30-40) |
| gain net attendu | **×0,70** — il COÛTE |

**Pourquoi 11 % ici et 41,9 % en § 1 : la paire, pas le moteur.** La mesure HF
comparait Qwen2.5-0.5B à **Qwen2.5-1.5B** — même famille *et* même post-
entraînement. Ici la cible a reçu une distillation de raisonnement que le
brouillon n'a pas : les deux modèles divergent **au premier jeton**. Vérifié sur
une invite, texte en clair : le brouillon propose « …which were **not accepted** by
the Convention », la cible « …which were **later used** by other poets » — deux
continuations également plausibles, acceptation nulle.

**La leçon est plus dure que celle du § 1** : ce n'est pas la taille du brouillon
qui décide, c'est **le partage de son post-entraînement**. Un brouillon de la même
famille mais d'une autre recette ne propose rien d'acceptable — et un brouillon
rejeté coûte plus qu'il ne rapporte.

**La paire ALIGNÉE, mesurée le 9 octobre** (brouillon R1-distill-1,5 B → cible
R1-distill-14 B : même famille, même distillation, même tokenizer, 8 invites de
48 jetons) :

| mesure | paire alignée (1,5 B → 14 B) | paire mal appariée (0,5 B → 1,5 B) |
|---|---:|---:|
| acceptation moyenne | **1,25 jeton sur 8 (15,6 %)** | 0,88 sur 8 (11 %) |
| P(préfixe ≥ 1 / 2 / 8) | 38 % · 12 % · 12 % | 38 % · 12 % · 0 % |
| coût relatif du brouillon | **0,134×** (7,05 vs 0,95 tok/s) | 0,210× |
| **gain net attendu** | **×1,09** | ×0,70 |

**L'alignement aide, mais il ne suffit pas** : 15,6 % au lieu de 11 %, et un gain
net qui passe de ×0,70 (il coûte) à ×1,09 (il ne rapporte presque rien). Le
brouillon ne coûte pourtant qu'un dixième de la cible — c'est bien
**l'acceptation** qui plafonne, pas l'économie de calcul.

**Une réserve, et elle est de taille** : cette acceptation est la borne **gloutonne**
(`--temp 0`), le critère le plus sévère possible — il exige que le brouillon
choisisse *exactement* l'argmax de la cible à chaque position. Le décodage
spéculatif réel échantillonne et accepte selon un rapport de probabilités : son
taux est **plus élevé** que celui-ci. Ce qui est mesuré ici est donc un plancher,
et il dit déjà que la version gloutonne ne paie pas.

**Et la troisième paire renverse le verdict — mais pas par l'acceptation.** Un
brouillon **minuscule** (Qwen2.5-0.5B Q8, 0,53 Go) pour la **même grande cible**
(R1-14B, 9 Go) :

| paire | acceptation | **coût relatif du brouillon** | gain net |
|---|---:|---:|---:|
| 0,5 B → 1,5 B | 11 % | 0,210× | **×0,70** (il coûte) |
| 1,5 B → 14 B (même recette) | 15,6 % | 0,134× | ×1,09 |
| **0,5 B → 14 B** | 12,5 % | **0,039×** | **×1,52** |

**C'est le RAPPORT DE COÛT qui décide, pas l'acceptation.** Avec un brouillon qui
coûte 4 % de sa cible, accepter un jeton sur huit suffit à gagner 1,5× — et cette
paire est la *moins* bien appariée des trois. À l'inverse, la paire la mieux
appariée (1,5 B → 14 B) ne rapporte que ×1,09 parce que son brouillon coûte 13 %.

**Et c'est exactement le régime que Drave vise** : quand la cible est plus grosse
que la RAM, elle est bornée par le **disque**, et le brouillon — qui tient en
mémoire — devient relativement gratuit. Le décodage spéculatif n'est donc pas mort
(§ 1) : il est **intéressant précisément là où le modèle cible ne tient pas en
mémoire**, ce qui est la niche du projet.

**Quatre réserves, toutes mesurées ou nommées :**
1. l'acceptation est la borne **gloutonne** (la plus sévère) ; le décodage réel
   échantillonne et accepte davantage ;
2. le coût relatif dépend de la charge (26,93 vs 1,05 tok/s ici) — c'est un ordre
   de grandeur, pas une constante ;
3. vérifier k jetons d'un coup demande le **préremplissage par lots** sur la cible,
   qui existe (`--lot`) mais n'est pas branché sur le décodage ;
4. la mémoire du brouillon s'ajoute : 0,53 Go pour un 0,5 B, à côté d'une cible de
   9 à 63 Go, c'est négligeable — mais ce n'est pas zéro.

**Ce qu'il faudrait pour aller plus loin** : un brouillon entraîné *sur les sorties
de sa cible* (distillation croisée, ou tête Eagle3 branchée sur les états cachés de
la cible). Les trois mesures donnent le cahier des charges : à 0,04× de coût
relatif, accepter 25 % à k = 8 donnerait **×2,0**.

*(Le taux d'acceptation est déterministe — `--temp 0` — donc exact malgré la
charge ; le coût relatif, lui, dépend de la charge et n'est qu'un ordre de
grandeur : 0,210 ici contre 0,245 en § 1 pour la même paire de tailles.)*

---
