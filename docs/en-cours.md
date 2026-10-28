# En ce moment

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 203 fichiers / 270 JSON, 54 documents**), chemins archivés
> corrigés (`docs/archive/`), B10–B12 réintégrés dans les cartes. **Les règles d'`AGENTS.md`
> ne changent pas.** *Spécifique : la date, les compteurs et les lignes ouvertes sont mis à
> jour ci-dessous ; les chiffres B12 restent pilotés par le chantier en cours.*

**Mis à jour : 2026-10-27, 16 h 30 HAE (heure locale, EDT).**

> Cette page dit **où l'on va, ce qui est en cours, où l'on en est, et ce qu'il reste**. Les chiffres, les séries et
> les contrôles vivent dans [`reports/`](../reports/) ; le plan dans [`roadmap.md`](roadmap.md). **Ici, l'actualité
> seulement** — le détail se charge à la demande.

## Où l'on va

**Démontrer que la structure bat la taille, et construire le bus d'événements qui rend les blocs observables,
décomposables, répartissables et rejouables.** Le bus accepte des blocs **neuronaux** (l'intuition, la langue) et
**classiques** (une règle, un solveur, une opération exacte) ; il les rend substituables, comparables et mesurables.
La vision complète est dans [`vision.md`](vision.md).

## Ce qui est en cours

**La phase B12 est mesurée** ; les suites sont dans [`roadmap.md`](roadmap.md).

- **A7 la grappe déportée** — **faite** : le relais rend le même chiffre, la grappe exacte à 21 %, le transport à
  4,22×.
- **B4 les opérateurs abstraits** — **close** : six mesures, dont le LoRA qui **inverse**.
- **A8 l'ordonnanceur place et perte** — **fait, opt-in**.
- **B5/B6 les jeux symboliques** — **faits** : surface → RSN-jeu → pensée, cinq jeux, 112 items.
- **B7/B8 les langues et les maîtres** — **faits** : 71 langues, 449 surfaces, 17 principes, les négatifs nommés.
- **B9 le banc externe** — **mesuré** : DeepSeek sert le langage, `route` reste sur GPU. Le **meilleur écart** de
  distillation est **4,40 % à 31,63 M / 610 exemples** ; la **fenêtre** (3,71 % à 500 pas, 1,29 % à 750, −0,49 % à
  1 000) et le **négatif 30 langues** sont nommés. Détail : [`rapport-deepseek.md`](../reports/rapport-deepseek.md).
- **B10 le protocole sémantique** — **premier passage** : l'**encodeur converge** sur 10 langues (rappel
  **0,426** contre 0,167 ; sonde de langue **0,100**) ; le **décodeur est négatif** (chrF **14,0 / 5,4** contre un plancher **38,8** (référence tronquée)) ; les ablations montrent que `z` 512, le préfixe 64 et 8 unités linéaires n'aident pas, et que `z` est un
  **code d'identité** plus qu'un code de contenu ; le prochain levier est une **attention de requêtes**. Le diagnostic multilingue est sous le plancher. Le raisonnement sur `z` n'est pas
  branché. Protocole : [`protocole-semantique.md`](protocole-semantique.md) ; fiche :
  [`rapport-semantique.md`](../reports/rapport-semantique.md).

- **B11 la base d'universaux typés** — **premier passage** : schéma fixe de **15 champs / 502 classes**,
  sortie déterministe ; le **codec classique** lit **100 %** des coups B5/B7 (79/79, 449/449) et restitue
  la **surface originale** dans **33/79** cas ; le **parseur natif typé** surapprend en réel seul (**48,3 % train / 0 % validation**) mais la
  **distillation synthétique** le débloque : **45,1 %** de code exact sur les **528 surfaces réelles** jamais
  vues, `jeu` **83,1 %**, `de`/`vers` **90,0 / 89,4 %** ; l'**invariance par paire** reste **7,4 %**. La **normalisation lexicale** (concepts canoniques) porte le natif à **55,7 %** de code exact et
  **37,0 %** d'invariance, contre **45,1 % / 7,4 %** ; la **consistance softmax** (38,3 %, invariance 0) et
  l'**adversaire de langue** (39,6 %, invariance 0) restent deux **négatifs**. Le codec reste à **100 %**. Avec le **contexte**, le codec lit **528/528** (100 %) ; sans contexte, **374/528**
  (70,8 %) : le contexte est décisif, et le natif ne le reçoit pas encore. En **suffixe**, le contexte porte le natif à **59,8 %** de code exact et
  **40,7 %** d'invariance ; en **préfixe**, il collapse (0,4 % / 88,9 %) ; en **vecteur séparé**, **59,1 % / 40,7 %**,
  aucun gain. Le verrou restant est `carte` (**69,3 %**) et les ambiguïtés de surface. La **restitution du code
  (aller-retour RSN)** est **100 %** : **79/79** et **449/449** rendus, **aller-retour RSN exact** ; la **surface
  originale** n'est reproduite qu'à **33/79**. Note : [`semantique-universaux.md`](semantique-universaux.md) ; fiche :
  [`rapport-universaux.md`](../reports/rapport-universaux.md).

- **Portes** — passe complète **49 portes : 47 vertes, 2 rouges structurelles** (`porte-indice`, `porte-melange`) ; aucune régression (27/10 14 h 33).
- **A7.15 64 jetons K/V int8** — **64/64** jetons greedy identiques, accord 1,0, texte identique ; un prompt.
- **A7.14 génération K/V int8** — 16/16 jetons greedy identiques, accord 1,0 ; un prompt, pas d'échantillonnage.
- **A7.13 K/V int8 512 jetons** — PPL **4,6979356** base et int8, Δ **0,0** sur 511 jetons et 24 couches ; un seul texte.
- **A7.12 PPL K/V int8** — 24 couches, 85 jetons : PPL **2,6792016 → 2,6792004**, Δ **−1,17e-6** ; pas de perte mesurable, mais échantillon court.
- **A7.11 attention KV int8** — diff max **0,0154**, **argmax 97,66 %**, corrélation **0,99998**, ratio **0,266** ; Q aléatoire, pas de modèle.
- **A7.10 KV int8** — **17 420 o** contre **65 548** (ratio **0,266**), **272 o/jeton**, **25,5 Mio** contre **96,0 Mio** pour 4 096 jetons ; diff max **0,0155** ; fidélité modèle non mesurée.
- **A7.9 cache KV** — une couche **1 024 o/jeton** (0,25× hidden) ; **24 couches 24 580 o/jeton**, **96 Mio pour 4 096 jetons** ; transfert naïf négatif, garder le KV côté serveur ou le quantifier.
- **A7.8 int8 par canal** — ratio **36–39 %**, argmax **1,0**, diff max **0,5–1,7**, KL **~1e-3** ; lossy, décision stable, PPL non mesurée ; 896 échelles f32.
- **A7.7 hidden int8** — par tenseur : argmax **0**, KL **10,2** ; par jeton : argmax **0,83–0,93**, KL **0,12–0,37** ; volume **34,6 %** mais fidélité insuffisante. **Négatif** ; bf16 reste meilleur.
- **A7.6 couche à distance** — Qwen 0.5B couche 12 dans un second processus : logits **bit-à-bit** 3/3, **ΔPPL +0**, RTT **4,052 ms**, **4 105 o/jeton**, **3 987,6 tok/s** ; sparse/dense **1,027×** (hidden réel dense).
- **A7.5b seuil réseau** — sparse **1 672 o** vs **7 416**, encodage/décodage plus rapides, **1,94× à 0 ms**, **1,006× à 100 ms**, seuil **−0,60 ms** : gagne toujours sur ce lien.
- **A7.5 grappe réseau** — flux sparse **1 672 o** contre **7 416** dense (**4,44×**), fidélité **1 792/1 792**, **5/5** messages identiques, **0,125 ms** loopback ; contrôle dense.
- **B26 M6 conflit** — réplication d'A6 : **94,95 %**, conflit **0**, commutation **0** ; sélecteur sans compétition, pas de contrôle exécutif.
- **B25 M8 rejeu** — 23/6 codes : M8 exact **0**, champs **74,6 %** ; rejeu **0**, hybride **0** ; le rejeu ne compose pas un code neuf.
- **B24 routeur confiance** — typo **56,2→63,7 %** (+7,5) mais espaces **41,8→34,2 %** (−7,5) ; round-trip ne détecte que **31 %** des typos ; oracle **79,45 %**.
- **C3.2e sous-familles autres** — uralic côtier **100 %** contre **46,7 %** ; benue-congo **88 %** contre 94 ; austronesian **60,3** contre 61 ; afro-asiatic ouest **53,5** contre 60,2. Le découpage explique l'uralic.
- **C3.2d sous-familles IE** — indo-iranien **100 %**, baltique **95,3**, italique **87,6**, celtique **79,9**, germanique **54,6** ; l'IE entier à **14,7 %** est un **effet de composition**.
- **C3.2c 9 familles** — **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤0,5 %** ; indo-européen **14,7 %**, quechuan **88,2 %**, mayan **64,4 %**, afro-asiatic **60,2 %**, uralic **46,7 %**. L'hétérogénéité interne reste le facteur.
- **B23 routeur** — original **100 %**, casse **99,3 %**, phrase **92,5 %**, espaces **41,8 %** vs M1 **11,6 %**, typo **56,2 %** < M2 **68,3 %** ; collision de lexique, pas un oracle.
- **B22 M2 typos** — M1 **24–45 %** sur suppression/substitution/insertion/transposition ; M2 `de` **62–73 %**, `vers` **66–80 %** ; avantage **+21,9 à +46,5 pts**. Niche robuste, pas un étage.
- **B21 M9 dose** — M3 span **0/4/8/12/12** (tautologique) ; M5 ordre 0/1/2 **13,81/15,70/18,06 %** (+4,25 pts) ; sham **nul** ; double lésion non additive.
- **B19 M2 secours** — M1 **100 %** original, **98,7 %** casse, **86,6 %** phrase ; M1 espaces **34,8 %**, typo **36,6 %** ; M2 typo **71,2 / 76,7**, espaces **41,8 / 45,2**, phrase **0 / 0,7**. Niche typos, pas secours général.
- **B18 restitution** — **528/528** rendus et relus, **0** échec ; c'est l'involution du codec, pas un décodeur neuronal (B10 négatif).
- **B17 mémoire LFU** — LFU **9,28 %** suffixe surface vs FIFO **5,03 %**, suffixe code **74,69 vs 71,70 %** ; M8 couverture **70,75 %**, exact sur couverts **100 %** (lookup), généralisation **0 %**. LFU filtre, M8 ne généralise pas.
- **B16 M7-bis** — LFU bat FIFO : **+23,1 pts** répétés (30/30), **+4,25** suffixe, **+8,7** nouveaux utiles ; LFU+récence **= LFU** ; contexte **−8,5 / −42,9** ; c'est la **fréquence**, pas la neuromodulation.
- **B14 M2 dans la chaîne** — **n'ajoute rien** : M1 **100 %** (`de`/`vers`), M2 **93,4 / 93,6 %**, aucun étage ne consomme M2 ; M5 plateau **18,70 % vs 12,60 %** ; M6 **94,32 / 94,95 %** ; le « M5 M1-lésé 28,03 % » est une couverture 51,4 %, pas un gain. M2 est un rameau, pas un étage.
- **B15 multilingue** — M1 sur **66 langues** : **528/528** avec contexte, **70,8 %** sans ; **26/26** variantes et **15/15** interlangues invariantes ; contrôle permuté **0 %** attendu / **90 %** donneur ; baseline surface **71,8 %**. Détail : [`rapport-multilingue.md`](../reports/rapport-multilingue.md).
- **B13 chaîne sémantique** — M1 → M5 → M6 → M8 : **528/528**, M5 contexte **18,7 % vs 12,6 %**, M6 **94,3 %**, M8 **57,95 %** (borne haute, non tenue à l'écart). Intégration, pas preuve.
- **B12 les modules cerveau-langage** — **corrigé** : M1 **528/528** solide ; M2 vu seulement ; M3
  **tautologique** ; M4 **lookup** ; M5 contexte ; M6 langue, commutation 0 ; M7 plafond 3,64 % ;
  M8 **96,48 % marginal**. Détail : [`rapport-cerveau-corrections.md`](../reports/rapport-cerveau-corrections.md).
- **Bilan B11** : le codec lit **528/528** et la **restitution du code** fait **100 %** d'aller-retour ; la **surface
originale** reste à **33/79** ; le natif normalisé + contexte reste à **59,8 %** de code exact et **40,7 %**
d'invariance ; le raisonnement n'est **pas branché**. Bilan : [`bilan-b11.md`](../reports/bilan-b11.md).

## Les chiffres de l'état

> **Source unique.** Ces cinq valeurs sont vérifiées par `tools/revue_documentation.py` ; les
> autres pages y renvoient au lieu de les recopier.

| invariant | valeur | contrôle |
|---|---:|---|
| portes | **49** (47 vertes, 2 structurelles) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/synthese/0*.md` |
| fichiers / JSON de résultats | **203** / **270** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **54** (hors archive et README) | `docs/**/*.md` |
| dernière passe complète | **1 h 48** (27/10 14 h 33) | `docs/references-non-regression.md` |

## Où l'on en est

| | |
|---|---:|
| portes (passe complète) | **49** — **47 vertes, 2 structurelles** (27/10 14 h 33) |
| porte-deepseek | **verte** (20 tests), incluse dans la passe |
| fichiers / JSON de résultats | **203** / **270** |
| la sonde, au pic du 1,5 B | **0,7256** (XNLI) |
| le pont, au pic du 14 B | **0,8715** — il plafonne à 0,87 |
| la sémantique des jeux (B5/B6) | **112 items, 100 % au niveau 4, 33/33 paires** |
| les langues (B7) | **71 langues, 35 concepts, 449/449, 11/11** |
| les maîtres (B8) | **d4, livre 10/10, go 9×9 10/10, dames 0 défaite, cartes 44,7 % (négatif)** |
| le banc externe (B9) | **DeepSeek 310/310, chrF 82,82 contre 15,64 ; 31,63 M/610 : 4,40 %** |
| le protocole sémantique (B10) | **encodeur 0,426 contre 0,167 ; décodeur négatif 14,0/5,4 contre 38,8** (référence tronquée) |
| la base typée (B11) | **codec 100 %** (79/79, 449/449) ; natif **59,8 % / 40,7 %** ; surface **33/79** |
| B22/B23 — M2 et le routeur | **M2 typos 62–80 % vs M1 24–45 %** ; routeur espaces **41,8 % vs 11,6 %**, typo **56,2 % < M2 68,3 %** |

## Les sept chantiers, en une ligne

| chantier | état |
|---|---|
| **C1** corpus et généalogie | ✅ fait (UDHR, Glottolog) |
| **C2** traduction | ✅ mesuré (juge, plancher, marge) |
| **C3** restitution | ✅ mesuré ; **C3.2** : un module par famille, **4/5** au-dessus de la référence |
| **C4** dialectes et styles | ✅ mesuré ; la date reste à contrôler |
| **C5** qualité par domaine | ✅ six registres + dialogue spontané |
| **C6** documentation | ✅ fait — revue du 27/10 : compteurs et chemins corrigés ; fiche [`rapport-coherence-docs-3.md`](../reports/rapport-coherence-docs-3.md) ; l'outil de présentation [docwatch](https://github.com/stephanedenis/docwatch) est un dépôt public autonome, épinglé en sous-module dans `tools/docwatch/`, seul serveur de documentation : **multi-racines** (`/drave/`, `/docwatch/`) et **génération des SVG** `.mmd`/`.puml` |
| **C7** pensée abstraite | ✅ mesuré — la carte, **B4** close, **B5/B6** faits, **B10–B12** premier passage |

## Ce qui reste

**Court terme** — **B23** : un score de confiance M1 (la collision de lexique laisse la typo à 56,2 %) ;
**B22** : typos réelles et secours conditionnel ; **B21** : reproduire la dose M5 sur une autre lésion ;
**B10.3** : un décodeur au-dessus du plancher, puis le raisonnement sur `z` ; **B12.10** : M2 équilibré,
M3 répétitions, M5 ordre 2, M6 conflit, M7 capacité, M8 rejeu ; **B9** : 31,63 M / 610 à 750/1 000 pas,
plus de données avec la capacité, masque dans le trainer, export du 31,63 M.

**Moyen terme** — les suites des jeux hors plan (corpus externe, MCTS budgété, portage Rust), les **9 familles** de
C3, la **prose scientifique** (bloquée par le corpus), le **FPGA**, la **démonstration distante** (compte Colab), le
**MoE** local.

**Objectif final** — une entrée-sortie **fiable** (étage 1), puis une **pensée abstraite** jugée sur des
**opérations** (étage 2) ; un moteur **décomposable, répartissable, observable et rejouable**, tenu par ses mesures.

## Les questions ouvertes

- **Bloquées par une ressource** : B1.5 (corpus scientifique humain), A3.4 (compte Colab), A5.4 (carte Stratix V),
  A6.2 (MoE local).
- **Ouvertes sans blocage** : **B10.3** (décodeur au-dessus du plancher), **B12.10** (les six suites des modules),
  le **pic du 32 B** (nommé, non forcé), les limites des jeux (détection sur cases seules, ko simple, MCTS à
  60 playouts), le **portage Rust** du contrat RSN.
- **Tranchée** : les styles à époque contrôlée — la surface capte l'époque (+0,138) plus que la filiation (+0,049) ;
  c'est une règle de méthode.

## La carte

[`carte.md`](carte.md) — les sujets, bloc par bloc ; [`README.md`](README.md) — l'inventaire ; [`roadmap.md`](roadmap.md)
— le plan ; [`synthese/index.md`](synthese/index.md) — la théorie ; [`reports/`](../reports/) et
[`journal/`](../journal/) — les preuves et le récit.
