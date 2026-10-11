# Dessin H — profondeur routée : la borne de l'oracle vaut ≈ 31 % des jetons, et le chemin court reste derrière le chemin long même là où il est le plus sûr

> Campagne : **cerveau** · expérience : sortir à **16 couches** au lieu de 24, **jeton par jeton**
> Question : le dessin H (`docs/modele-pour-drave.md` § 3) promet qu'une couche sautée vaut **zéro
> paire**. Mais **qui** saute quoi ? Un routeur parfait ne se trompe jamais ; un routeur réel ne
> dispose que de la **confiance** du chemin court. Alors : **combien un oracle épargnerait-il, et
> qu'atteint un routeur qui ne sait rien ?**
> Verdict : **quatre résultats, dont un seul est positif.**
> (1) **la chaîne hors-ligne reproduit le moteur** — 0,013 % (24 couches) et 0,006 % (16 couches) :
> les chiffres qui suivent sont ceux du moteur, pas ceux d'une relecture plausible ;
> (2) **la borne de l'oracle vaut 30,93 %** des jetons : sur ces 619 jetons sur 2 001, sortir à
> 16 couches ne change pas la décision. Au mieux **≈ 10,3 % des paires** (un tiers des couches sur
> 31 % des jetons) — et il faudrait un routeur **parfait** ;
> (3) **aucun seuil de confiance n'atteint la qualité du chemin long** : le meilleur (seuil 0,99,
> 5,1 % des jetons sortis) rend **47,33 %** contre **47,73 %**. Le résultat est négatif ;
> (4) **mais le seuil sélectionne, et de plus en plus juste** : sur les 5 % de jetons les plus sûrs,
> l'écart court/long tombe de **24,5 points** (global) à **7,9 points**. C'est le chiffre que le
> dessin H devrait **renverser** pour exister — et il nomme l'ennemi : ce n'est pas le routeur,
> c'est le **chemin court**.
> Date réelle : **2026-10-10 22:08 HAE** (heure lue sur la machine).
> Protocole : `tools/profondeur_routee_oracle.py` · vérification de la chaîne :
> `tools/verifier_chaine_etat.py` · porte : `tools/porte-profondeur-routee.sh`.

## 1. Le dispositif : deux chemins, les mêmes jetons

| | chemin **long** | chemin **court** |
|---|---|---|
| état lu | après **24** couches (le modèle entier) | après **16** couches |
| lecture | norme finale + tête liée du modèle, **gelées** | **adaptateur entraîné** 896×896, puis les mêmes norme et tête |
| coût des couches | 24 | 16 (soit **8 de moins, un tiers**) |

Les deux chemins lisent **les mêmes jetons**, aux mêmes positions, dans le même contexte imposé.
L'adaptateur du chemin court s'entraîne sur la **fin** du texte (3 743 états, positions 3 512 à
7 254) et se teste sur le **début** (2 001 jetons, positions 1 000 à 3 000), jamais vu, avec
512 positions de marge et 936 états de validation entre les deux.

**Avant de mesurer quoi que ce soit**, la relecture hors-ligne est comparée au moteur sur la même
capture — sinon les nombres qui suivent seraient plausibles et faux :

| profondeur | perplexité hors-ligne | perplexité du **moteur** | écart |
|---|---:|---:|---:|
| 24 couches | 14,6477 | **14,6496** | 0,013 % |
| 16 couches (tête appliquée à la fin de la plage) | 429 660,5721 | **429 684,6614** | 0,006 % |

## 2. La mesure

| chemin | perplexité (test) | justesse@1 |
|---|---:|---:|
| **long** — 24 couches, tête du modèle | **11,9921** | **47,73 %** |
| **court** — 16 couches, adaptateur entraîné | 499,0613 | 23,19 % |

- **accord court/long : 30,93 %** (619 jetons sur 2 001). Sur ceux-là, sortir à 16 couches rend
  **exactement la même réponse** : c'est la borne de l'oracle, et elle ne dépend d'aucun routeur.
- **oracle par jeton** (le meilleur des deux, choisi en connaissant la réponse) : **51,92 %**, soit
  **+4,19 points** sur le chemin long seul. Même avec un oracle, le gain de justesse reste modeste —
  les deux chemins se ressemblent plus qu'ils ne se complètent.

**Le même résultat tient sur trois découpages différents du même texte** (l'accord vaut 28,76 %,
30,20 % et 30,93 % selon la zone de test et le sens de l'entraînement) : ce n'est pas un artefact
d'un découpage.

## 3. La cascade : ce qu'un routeur réel atteint

Un routeur réel ne connaît pas la réponse, mais il a la **confiance** du chemin court (le maximum
du softmax de ses logits). On sort tôt si `confiance ≥ seuil`, sinon on va jusqu'au bout.

| seuil | sortis tôt | justesse globale | **court** sur les sortis | **long** sur les sortis | témoin au hasard |
|---|---:|---:|---:|---:|---:|
| 0,00 | 100,0 % | 23,19 % | 23,19 % | 47,73 % | 23,19 % |
| 0,50 | 47,2 % | 39,13 % | 38,24 % | 56,46 % | 35,89 % |
| 0,70 | 30,7 % | 42,78 % | 47,23 % | 63,36 % | 40,09 % |
| 0,90 | 15,3 % | 45,63 % | 58,17 % | 71,90 % | 43,94 % |
| 0,95 | 11,1 % | 46,33 % | 61,71 % | 74,32 % | 45,03 % |
| 0,99 | 5,1 % | **47,33 %** | **80,39 %** | **88,24 %** | 46,50 % |

Trois lectures, et la troisième est la seule qui compte pour la suite :

1. **aucun seuil n'atteint 47,73 %** : à 5,1 % de jetons sortis on perd 0,40 point, à 47,2 % on en
   perd 8,60. Sortir tôt **coûte** de la qualité, toujours ;
2. **le seuil sélectionne vraiment** : à part de jetons égale, il bat le tirage au hasard de
   **+3,24 points** (seuil 0,50 : 39,13 % contre 35,89 %). La confiance du chemin court porte donc
   une information réelle sur le jeton — ce n'est pas un mécanisme mort ;
3. **les deux colonnes du milieu portent sur LES MÊMES JETONS**, et c'est là que tout se joue :
   globalement le court est à **24,5 points** derrière le long (23,19 contre 47,73), mais sur les
   5 % de jetons où il est le plus sûr, l'écart tombe à **7,9 points** (80,39 contre 88,24). Le
   seuil ne trouve **aucun** sous-ensemble où sortir tôt soit neutre — mais il s'en rapproche à
   mesure qu'il se resserre.

**Ce que le seuil mesure vraiment, cependant** : sur ces 5 % de jetons, le chemin **long** passe de
47,73 % à **88,24 %**. La confiance du chemin court identifie donc surtout des jetons **faciles**,
pas des jetons où les deux chemins **divergent**. C'est une nuance qui change la conception : un
routeur entraîné sur la seule confiance apprendra « ce jeton est facile », pas « ce jeton n'a pas
besoin des couches 17 à 24 ».

## 4. Ce que ça dit du dessin H

- **La borne est ≈ 10,3 % des paires**, et c'est un plafond, pas une promesse : 30,93 % des jetons
  × un tiers des couches. À comparer aux autres leviers déjà chiffrés — la fenêtre d'attention
  (384 + 64 puits = **+0,3 %** de perplexité pour **÷1,33** de clés notées) ou la mémoire de C8
  (**zéro paire** de plus, R² 1,000). Le dessin H n'est donc pas le levier le plus violent sur les
  paires ; il le devient seulement si un routeur **appris** s'approche de sa borne.
- **Le facteur limitant n'est pas le routeur, c'est le chemin court.** Le seuil de confiance bat le
  hasard dès 47 % de jetons sortis : la sélection fonctionne. Ce qui échoue, c'est qu'un adaptateur
  linéaire posé sur l'état de la couche 16 rende 23,19 % de justesse quand huit couches de plus en
  rendent 47,73 %. Un vrai modèle routé (mixture-of-depths) n'aurait pas ce défaut : ses couches
  **apprendraient** à rendre la sortie de la couche 16 exploitable, au lieu de laisser un adaptateur
  réparer après coup — c'est exactement le manque **N4** (« les dessins H/I/J ne sont jamais
  entraînés »).
- **Le chiffre à renverser est nommé** : au seuil 0,99, le court est à **80,39 %** et le long à
  **88,24 % sur les mêmes jetons**. Si un modèle entraîné pour la sortie anticipée ramenait ces deux
  colonnes à l'égalité, la porte se réécrirait et le gain deviendrait réel — sur 5 % des jetons
  d'abord, puis sur la part que la confiance sait reconnaître.

## 5. Les limites, écrites ici pour ne pas être relues ailleurs

- **Un seul texte** (les 8 192 premiers jetons de `data/wikitext2_test.txt`, tokenisé par le modèle
  lui-même — 85 626 jetons disponibles), **un seul point de sortie** (16 couches sur 24). Un autre
  point de sortie (20 couches) donnerait un chemin court bien meilleur, donc une borne plus haute :
  **ce n'est pas mesuré ici**, et c'est la suite la plus directe.
- **La borne de 30,93 % dépend du chemin court** : un chemin court parfait donnerait 100 % d'accord.
  Le chiffre mesure donc **ce qu'on sait construire aujourd'hui** avec un adaptateur linéaire, pas
  la borne du dessin H en général. C'est une borne **basse**, et c'est dit.
- **La comparaison est jeton par jeton, en contexte imposé** : elle dit si la **décision** de chaque
  position change, pas ce que deviendrait une génération libre dont les jetons changeraient en
  route. Un routeur qui se trompe tôt peut entraîner la suite ailleurs — cet effet n'est pas mesuré.
- **Le chemin court surapprend** : à la meilleure époque (10), la perte d'entraînement vaut 2,00 de
  perplexité et la validation 480,05. Le chiffre du chemin court est celui d'un adaptateur entraîné
  sur 3 743 exemples, pas d'un modèle.
- **Un faux pas écarté en route** : `data/wikitext2_test.txt.ids`, présent dans le dépôt, vient d'un
  **autre tokenizer** ; le modèle complet y rend **7 379** de perplexité au lieu de 16,6. Deux
  mesures y avaient été faites avant que l'écart ne soit vu — elles sont **jetées**, et la porte
  **tokenise désormais elle-même** le texte avec le tokenizer du modèle au lieu de faire confiance
  à un fichier d'identifiants trouvé dans le dépôt.
