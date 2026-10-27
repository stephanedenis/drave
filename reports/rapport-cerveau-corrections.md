# Corrections B12 — ce que le stress des sous-agents a changé

> **Objet.** Les premiers chiffres B12 (M2 93,2 %, M3 12/12, M4 1,0, M8 96,48 %) étaient
> **gonflés par la structure du corpus**. Trois sous-agents ont refait les mesures avec des
> splits par code, des leurres, du bruit et des permutations. Ce document corrige, il n'efface pas :
> les anciens chiffres restent dans la fiche, avec leur cause.

## 1. Ce qui reste solide : M1

| mesure | valeur |
|---|---:|
| surfaces lues avec contexte | **528 / 528** |
| sans contexte | **70,8 %** |
| canonique | **100 %** |
| invariance | **100 %** |
| événements de bus | **1 584** |

M1 est le **codec classique** avec un bus. C'est exact, ce n'est pas neuronal.

## 2. M2 — le 93,2 % était du recouvrement de surfaces

Le test B5/B7 contient **146 items `de`** ; **126 sont des surfaces normalisées déjà vues** à
l'entraînement synthétique, **20 sont inédites**.

| mesure | valeur |
|---|---:|
| `de` moyen 3 graines | **93,6 %** |
| `de` sur surfaces vues | **126 / 126** |
| `de` sur surfaces inédites | **10,7 / 20 = 53,3 %** |
| `vers` moyen 3 graines | **94,3 %** |
| `vers` inédit | **11,7 / 20 = 58,3 %** |
| `point` | 95,7 % **< majorité 97,1 %** |
| `chemin_0` | 84,3 % **< majorité 97,1 %** |

- **Double dissociation** : valide sur les surfaces vues (lésion ventrale → action au hasard, lésion
  dorsale → `de` au hasard), mais **elle ne prouve pas la généralisation**.
- **Dernier état** : le gain honnête à 1 000 pas est **+2,7 pts** sur `de`, **+3,4** sur `vers`,
  **+1,4** sur `point`, **−2,9** sur `chemin_0` ; `mean` seul atteint 89,7 % sur `de` à 1 000 pas.
  Le « 6,2 → 93,2 » était un **sous-entraînement** du mean à 300 pas, pas une propriété du dernier état.
- **Contexte** : aucun gain mesuré ; le contexte synthétique est constant par jeu.
- **Négatifs** : `point`, `chemin_0` sous la majorité.
- **Plus d'entraînement dégrade l'inédit** : à 1 000 pas, `de` tombe à **9,3/20** (46,7 %)
  contre 10,7/20 à 300 pas ; les formes vues restent à 100 %. Le split inédit est un **priori de
  classe**, pas une lecture.
- **Piège du split inédit** : les 20 items inédits `de`/`vers` ne contiennent que **2 classes**
  (`de` : 52 ×6, 62 ×6, 57 ×1) et **3** (`vers` : 36 ×6, 45 ×6, 42 ×1). Les 10,7/13 et 11,7/13
  sont donc surtout un **priori de classe par famille de surface**, pas une lecture ; le plafond
  honnête est **13/20**, avec ~2 items de gain possible pour `de` et ~1 pour `vers`. Ce split ne
  mesure presque rien ; `point` et `chemin_0` sont les vrais gisements.

## 3. M3 — le 12/12 est tautologique

- `charger()` copie exactement, `span` ne teste que `n ≤ capacité` : **40 séquences de codes
  aléatoires donnent aussi span=12, exact=1,0**.
- Le n-back « contrôle » à 1,0 venait des **5 premiers items du corpus, qui ont le même code**.
- **Interférence** : similaires et dissemblables donnent **exactement le même taux** (effet 0,0) ;
  seule compte la position (`L+D` vs capacité). C'est un **tampon FIFO**, pas une mémoire de travail.
- **Bruit** : p50(span 12) = **5,5 %** (analytique 5,6 %) ; à p=5 %, les champs restent à 99,64 %
  mais les 12 codes exacts tombent à **52,5 %** : aucune correction.
- **Saturation** : C=3/5/7/12 → span=3/5/7/12, mur net ; au-delà, les items sont décalés.

## 4. M4 — le 1,0 est un lookup de doublons

- 528 items mais **29 codes uniques** (~18 surfaces par code) : le rappel 1,0 retrouve un doublon.
- La complétion 97,9 % s'explique par **72,35 % `vers=None`** (15/15) et **27,65 % à 14/15** :
  0,7235 + 0,2765 × 14/15 = **0,9816** ; c'est de l'identité, pas de la complétion.
- Split par code (23 train / 6 test) : codes non stockés rappelés **0/6** ; complétion exacte
  **0/10** ; **0/7** valeurs de champ inédites.
- **Fausse mémoire** : 98,96 % des leurres à 1 champ reçoivent une valeur fausse ; 65,4 % renvoient
  exactement le code source. Aucun seuil ne sépare un cue partiel légitime d'un leurre.
- **M4 ne généralise pas** ; c'est une table de hachage exacte.

## 5. M5 — l'action est une constante de format

`action()` classe le coup par la **forme** du code (présence de `de`/`vers`, `chemin`, `case`), pas
par sa sémantique : échecs = toujours `deplacer`, dames = toujours `prendre`, morpion = une valeur.
Prédire `action` ne peut pas battre la majorité : **97,46 % = 97,46 %** sur 1 538 transitions,
ordre 2 compris.

Sur des cibles qui varient, il y a un gain **mécanique**, pas sémantique :
`source` ordre 1 **12,60 % vs 6,49 %** (+6,10 pts), ordre 2 **14,42 %** ; `cible` ordre 1
**7,92 % vs 5,80 %** (+2,12 pts) mais **surprisal −0,04 nat** (gain de mode). Les dames portent
l'essentiel (`source` +8,8 pts, `cible` +6,1 à +12,9 pts) ; aux échecs le gain est **sous la
baseline tour**. L'oracle avec plateau (H 1,1–2,8 nats) reste inatteignable : le code observé ne
contient pas le plateau, et le tirage est uniforme parmi les coups légaux.

## 6. M6 — la porte est une détection de langue

- Nouvelle tâche de conflit fr/en (88 essais, 4 conditions) : **94,32 %** de conjonction,
  **88,64 %** équilibrée, VP 17, FP 0, FN 5 ; mais les politiques « langue seule », « sens seul » et
  « tout non » sont **toutes à 75 %** : chaque canal seul a 25 % de faux positifs.
- **Tâche de gate de tâche** (sens/langue, 792 essais) : **94,95 %**, base 50 % ; conflit **0,000**, commutation **0,000** ; la langue seule est à 88,6 %, le sens à 100 %. C'est un **sélecteur de tâche**, pas un contrôle exécutif.
- **Coût de commutation apparié = 0,000** ; l'ancien −0,15 était un artefact de composition.
- Deux surfaces sont identiques fr/en (`go D4`, `tic-tac-toe A1`) : plafond exact **95,45 %** ; la
  porte est à **1 essai du plafond**. Les 5 FN sont **perceptifs**, pas inhibiteurs.
- `MULTI.detecte_langue` est **non déterministe** (`PYTHONHASHSEED`), le canal de la porte est
  déterministe. La détection lexicale n'est pas du contrôle exécutif.

## 7. M7 — la métrique était le plafond

- La mémoire à 16 places ne peut retenir que **16/439 = 3,64 %** des surfaces : toutes les
  politiques atteignent ce plafond, la métrique ne peut pas les départager.
- L'ancien `MemoireLimitee` triait par poids et gardait les **16 premiers** : ce n'était pas FIFO.
- Sur 30 permutations appariées, **LFU** est la seule politique qui améliore les répétés
  (+23,1 pts, 30/30) ; nouveauté **−19,6 pts**, incertitude **−38,7 pts** de suffixe code,
  récompense **−53,3 pts**. Aucun signal neuromodulateur ne bat FIFO sur l'utilité ; c'est la
  **fréquence**, pas la modulation.

## 8. M8 — le 96,48 % est la marginale, pas la généralisation

- 12/15 champs sont constants ; le score **96,48 %** est dominé par la marginale.
- Exact réel : **65,1 %** (pas 0 %) ; champs non nuls : **85,96 %**.
- Baseline **par jeu** : **96,10 %** de champs, exact **63,2 %** ; le groupe `(jeu, action)` n'apporte
  que **+0,38 pt**. La baseline annoncée « 0 » était fausse (elle mesurait une mémoire vide, pas un
  modèle trivial).
- Sur codes jamais vus : **leave-one-code-out**, exact **0 % par construction** ; champs **90,1 %**
  en backoff type→groupe→jeu→global, mais champs **non nuls 63,5 %** et les coordonnées
  (`de`, `vers`, `point`, `carte`, `case`, `chemin`) à **0 %** ; les prototypes ne peuvent pas produire
  un code neuf. **M8 ne généralise pas** ; il résume la marginale. Le 96,48 % est un plafond de
  champs, pas une exactitude.

## 9. M9 — lésions

M9 (CPU) estime les déficits par privation : M1 **29,2 %**, M2 ventrale **13,8 %** / dorsale
**12,4 %** sur le proxy, M3 **0**, M4 **0**, M5 **?**, M6 **?**, M7 **?**, M8 **0**. M2 est un
**proxy bayésien CPU**, pas le `voies.py` neuronal ; le dire est essential.

## 10. Pipeline

M1 → M4 → M8 : **528/528**, **7 prototypes**, **96,33 %** de complétion sur 120 codes partiels.
Mais M4 ne généralise pas et M8 est la marginale : la complétion est **tautologique** pour les
mêmes raisons. C'est un test d'intégration, pas un résultat sémantique.

## 11. Verdict

- **M1** est **solide** : codec exact + bus, 528/528, 70,8 % sans contexte, 100 % canonique.
- **M2** : double dissociation **sur les surfaces vues** ; généralisation **non démontrée** —
  `de` 9,3–10,7/20, `vers` 11,7/20, `point` et `chemin` **sous la majorité**. Le split inédit
  ne porte que 2–3 classes ; plus d'entraînement **dégrade** l'inédit.
- **M3, M4** : **structurels** — tampon exact et lookup de 29 codes, pas de mémoire qui généralise.
- **M5** : **sans contexte négatif** (action constante) ; **avec le plateau**, gain réel de
  surprisal (`source` +0,626 nat, `cible` +0,411) et morpion à l'oracle. C'est un gain de
  **contexte**, pas de sémantique du code.
- **M6** : **sélecteur de tâche** à 94,95 % (base 50 %), mais **conflit 0** et **commutation 0** ;
  la langue seule est à 88,6 %. Pas d'inhibition exécutive mesurée.
- **M7** : **négatif** — 3,64 % = plafond 16/439 ; LFU +23 pts, aucun signal neuromodulateur.
- **M8** : **marginal** — 96,48 % de champs, exact 65,1 %, baseline par jeu 96,10 %,
  leave-one-code-out exact **0** ; coordonnées 0 % sur codes neufs.
- **M9** : **réel** — `voies.py` action 98,6→12,3, de 91,8→2,05, déficits 86,3/89,7, sham 0.

**Conclusion** : le prototype n'est **pas** un cerveau du langage. C'est un **échafaudage mesuré** :
un module solide (M1), un gain de contexte (M5), une table de lésions réelle (M9), et des
mécanismes structurels (M2, M3, M4, M6, M8) ou négatifs (M7) qui **nomment** ce qui manque.

## 12. Fichiers

- Mesures corrigées : [`cerveau-mesures-corrigees.json`](cerveau-mesures-corrigees.json) ;
  sous-agents : `/tmp/a1-m5-m6.json`, `/tmp/a2-m7-m8-m9.json`, `/tmp/a3-m2.json`, `/tmp/a4-m3-m4.json`.
- Code : `tools/cerveau/`.
- Ancienne fiche : [`rapport-cerveau-modules.md`](rapport-cerveau-modules.md).
