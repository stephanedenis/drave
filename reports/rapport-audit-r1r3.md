# Audit R1/R2/R3 — les chiffres rejouent, l'attribution des règles ne rejoue pas

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit audité** : `f908d7b0613c8a5eb8fae7fab514bfdc5fa4668b` (parent `69bd865ec1bae1958b6f617bde4bf685a15d7d67`) ·
> **HEAD observé en fin de rédaction** : `b551cf3b` (journal/état, sans `tools/`) — l'audit reste ancré sur `f908d7b0` ·
> **Date** : 2026-11-05 · **Verdict** : chiffres ✅, règles ❌.
> **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
> [`pensee-audit-r1r3.json`](pensee-audit-r1r3.json).

**En une phrase.** Les **valeurs** de la fiche [`rapport-pensee-r1r3.md`](rapport-pensee-r1r3.md)
et de [`pensee-r1r3.json`](pensee-r1r3.json) rejouent **toutes** au chiffre près (212/212,
0,8870, 0,5763, 27 spans, 177 top-k, 183/183 portes). Mais la **table des règles** ne rejoue
pas : elle annonce **+27 exacts** (donc 222), alors que le code livré en produit **+24 gains
bruts pour 7 pertes**, soit **+17** (212). R1a perd **6 spans français**, R1c en perd **1**,
R2 en perd **1**, R3a est **inerte**, R3b n'est **pas intégré**. Sur les 27 spans restants,
**10 ne sont pas inatteignables** : 7 régressions nouvelles et 3 gains A17 non intégrés.

## 1. Dispositif et fidélité du harnais

- **Gold vivant** : `evaluer_gold.charger()` — 612 phrases (20 `hand`, 432 `reel`,
  160 `synthetique`), 239 cibles, 3 179 tokens.
- **Gold gelé** : `evaluer_gold.charger_gele()` — 602 phrases, mêmes 239 cibles ; les 10
  phrases ajoutées après le gel n'ont aucune cible.
- **Mesure** : `evaluer_gold.evaluer_bloc` pour les valeurs officielles ; harnais local pour
  les ensembles d'identifiants et les ablations.
- **Ablations** : le module [`bloc_linguistique.py`](../tools/bloc_linguistique.py) est copié
  dans `/tmp`, une seule modification est réintroduite par variante, puis le module copié est
  importé et mesuré. Aucun patch du dépôt.
- **Fidélité** : la variante « toutes règles éteintes » ne diffère du fichier parent
  `69bd865e` que par deux constantes ajoutées et inutilisées (`SUB_PAR_LANGUE`, `MODAUX`) ;
  elle redonne **196 labels, 195 exacts, couverture 0,8201, F1 0,5555 (vivant) / 0,5595
  (gelé), tête 0,7152 / 0,7205, 43 spans (21 REL, 17 SUB, 5 GP), top-k 166** — exactement la
  ligne « v7 ». C'est le contrôle de fidélité du harnais.
- **Portes** : `PYTHONPATH=. python3 -m tools.pensee.autotest` → **183/183**, exit 0.
  (`python3 tools/pensee/autotest.py` échoue sur l'import relatif : la bonne invocation est
  `-m`, contrairement à l'usage affiché en tête du fichier.)

**Note d'arbre de travail (importante).** Les mesures ont été prises entre 21:27 et 21:44,
alors que `tools/bloc_linguistique.py` était **identique à `f908d7b0`** : la copie de base du
harnais (`/tmp/audit_r1r3/mods/base.py`) est **byte-identique** au fichier du commit. Pendant
la rédaction, deux **modifications non commitées** sont apparues : `tools/bloc_linguistique.py`
(mtime `22:14:32`, diff `+9/−2` : candidat GP génitif et déplacement de `prec = s`) et
`tools/pensee/autotest.py` (assertions top-k `177 → 211`, cible `35 → 1`). Elles **ne sont
pas de cet audit** et n'entrent pas dans les chiffres ci-dessous. Sur l'arbre courant,
`evaluer_bloc` donne toujours 212/212 et 0,887, mais **top-k 211** au lieu de **177** (les
portes ont été ajustées en conséquence). Les valeurs de cette fiche sont celles du
**commit**, pas celles de l'arbre courant ; le propriétaire de ces changements doit les
vérifier et les committer.

## 2. Rejeu des valeurs — 0 écart

### 2.1 État « après » (fiche et JSON)

| grandeur | fiche / JSON | vivant 612 | gelé 602 | écart |
|---|---:|---:|---:|---:|
| labels au bon span | 212 | **212** | **212** | 0 |
| exact / labels | 212/212 = 1,0000 | **212/212** | **212/212** | 0 |
| couverture (labels / cibles) | 0,8870 | **0,8870** | **0,8870** | 0 |
| F1 union | 0,5763 | 0,5720 | **0,5763** | 0 sur la base gelée |
| S (F1) | 0,4966 | 0,4910 | **0,4966** | 0 sur la base gelée |
| chunker (F1) | 0,6057 | 0,6018 | **0,6057** | 0 sur la base gelée |
| tête (F1) | 0,7316 | 0,7262 | **0,7316** | 0 sur la base gelée |
| français | 129/129 | **129/129** | **129/129** | 0 |
| anglais | 83/83 | **83/83** | **83/83** | 0 |
| spans restants | 27 (16 REL, 6 SUB, 5 GP) | **27 (16/6/5)** | **27 (16/6/5)** | 0 |
| top-k | 177 ; 0,7406 | **177 ; 0,7406** | **177 ; 0,7406** | 0 |
| top-k strict (hors fiche) | — | **177** | **177** | — |
| « inatteignables » | 17 | **17** (même ensemble que A17) | **17** | 0 |

**Base des mesures.** `labels`, `exact`, `couverture` et `top-k` sont identiques sur les deux
golds (les 10 phrases ajoutées après le gel n'ont pas de cible). `F1`, `S`, `chunker` et `tête`
sont donnés par la fiche sur le **gelé 602** ; sur le vivant 612 ils valent respectivement
0,5720 / 0,4910 / 0,6018 / 0,7262. La fiche indique « gelé 602 » sur la ligne F1 ; elle ne
l'indique pas pour `tête` (valeur citée dans l'intro et dans le JSON), ce qui peut faire
comparer 0,7316 (gelé) à des F1 vivantes. **Écart de forme, pas de valeur.**

### 2.2 État « avant » (vérifié par la variante tout-éteint)

| grandeur | fiche / JSON | mesuré vivant 612 | mesuré gelé 602 | écart |
|---|---:|---:|---:|---:|
| labels | 196 | **196** | **196** | 0 |
| exact / labels | 195/196 = 0,9949 | **195/196** | **195/196** | 0 |
| couverture | 0,8201 | **0,8201** | **0,8201** | 0 |
| F1 union | 0,5595 | 0,5555 | **0,5595** | 0 sur la base gelée |
| S / chunker | 0,4741 / 0,5858 | 0,4688 / 0,5822 | **0,4741 / 0,5858** | 0 sur la base gelée |
| tête | (0,7205) | 0,7152 | **0,7205** | 0 |
| spans perdus | 43 | **43 (21 REL, 17 SUB, 5 GP)** | **43** | 0 |
| top-k | 166 | **166 ; 0,6946** | **166** | 0 |

La F1 vivante 0,5555 est exactement celle que la fiche [dev/test v7](rapport-dev-test-v7.md)
signale pour le vivant 612 (§ 1) ; la valeur 0,5595 est bien la valeur gelée. **Aucun écart.**

## 3. Ablations — l'effet réel de chaque règle

**Lecture.** On part du code livré (212 exacts). « Gain » = cible exacte dans le code livré
qui **cesse** de l'être quand on retire la règle (ce que la règle apporte). « Perte » = cible
exacte **rétablie** quand on retire la règle (ce que la règle casse). Les identifiants sont
`phrase:type`. F1 = union, vivant 612 (base 0,5720).

| ablation | labels | exact | Δ exact | gains dev/test | pertes dev/test | F1 vivant (Δ) |
|---|---:|---:|---:|---:|---:|---:|
| **R1a** `SUJETS` (pronom) | 203 | 203 | −9 | 12 / 3 | **3 / 3** | 0,5643 (−0,0077) |
| **R1b** modaux | 211 | 211 | −1 | 1 / 0 | 0 / 0 | 0,5711 (−0,0009) |
| **R1c** second prédicat | 209 | 209 | −3 | 2 / 2 | **1 / 0** | 0,5685 (−0,0035) |
| **R1** (R1a+R1b+R1c) | 199 | 199 | −13 | 14 / 5 | **3 / 3** | 0,5602 (−0,0118) |
| **R2** SUB sans précédent | 209 | 209 | −3 | 4 / 0 | **1 / 0** | 0,5704 (−0,0016) |
| **R3a** subordonnants par langue | 212 | 212 | **0** | 0 / 0 | 0 / 0 | 0,5720 (0) |
| **R3c** `fall`/`call` | 212 | 210 | **−2** | 2 / 0 | 0 / 0 | 0,5688 (−0,0032) |
| *tout éteint* | 196 | 195 | −17 | 19 / 5 = 24 | **4 / 3 = 7** | 0,5555 (−0,0165) |
| *R3a fidèle (contrefactuel)* | 213 | 213 | +1 | 1 / 0 | 0 / 0 | 0,5727 (+0,0007) |

> **R3a fidèle** n'est pas le code livré : c'est la règle d'A17 appliquée pour de vrai
> (`SUBORDONNANTS − {car}` en anglais, dans les quatre usages de `_syntagmes_simple`). Elle
> récupère **r280** (+1 exact). Le code livré, lui, ne fait rien (voir § 3.6).

### 3.1 Identifiants

- **R1a** — gains : `r034 r074 r114 r205 r219 r240 r243 r247 r278 r285 r296 r299` (dev),
  `r214 r216 r281` (test) ; **pertes** : `r273 s069 s135` (dev), `s032 s072 s115` (test).
- **R1b** — gain : `r247` (dev) ; aucune perte.
- **R1c** — gains : `r224 r291` (dev), `r115 r239` (test) ; **perte** : `g017` (dev).
- **R1 (faisceau)** — gains : les 15 de R1a + `r224 r291` (dev) + `r115 r239` (test) ;
  pertes : les 6 de R1a.
- **R2** — gains : `r215 r245 r279 r294` (dev) ; **perte** : `s037` (dev).
- **R3a** — aucun gain, aucune perte.
- **R3c** — gains : `r102 r245` (dev) ; aucune perte.
- **Tout éteint** — 24 gains (`r034 r074 r102 r114 r115 r205 r214 r215 r216 r219 r224 r239
  r240 r243 r245 r247 r278 r279 r281 r285 r291 r294 r296 r299`) et **7 pertes**
  (`r273 s037 s069 s135` en dev, `s032 s072 s115` en test).

### 3.2 R1a — le pronom : +15 gains, mais 6 pertes françaises

Le code livré **retire `who, that, which, qui, qu` de `SUJETS`** (diff de `f908d7b0`). Il ne
applique pas la règle R1a décrite par A17 (« un pronom n'est jamais un verbe par la règle de
position », garde `n in PRON` dans `est_verbe`). Conséquence : le mot qui suit un relatif
n'est plus reconnu comme verbe **par position**. Les six pertes sont exactement des REL
françaises dont le verbe n'est pas au lexique (`crie`, `dessine`, `observe`, `pousse`…) :
elles étaient exactes en v7 et ne le sont plus. **Net R1a : +9**, pas +15 ; et **6 pertes**,
pas 0.

### 3.3 R1b — les modaux : +1, et une constante morte

Les modaux sont ajoutés à `AUXILIAIRES` (ligne 449) ; c'est ce qui produit l'effet. La
constante `MODAUX` (ligne 464) n'est **utilisée nulle part** : elle est décorative. La fiche
la cite pourtant dans le dispositif. Effet réel : **+1** (`r247`), pas un gain de masse.

### 3.4 R1c — le second prédicat : +4, mais `g017` perdu

Le code livré diffère du pseudocode A17 : il autorise les auxiliaires consécutifs
(`prec_aux`) et ne compte un verbe collé à son auxiliaire que dans `predicat_vu`, **pas dans
`verbes_vus`**. La garde d'adverbe final teste `verbes_vus >= 1`. Sur `g017` (« that she would
come yesterday »), `come` suit `would` et n'incrémente pas `verbes_vus` : `yesterday` reste
dans la SUB, span prédit `[9:38]` au lieu de `[9:28]`. En enlevant R1c, `g017` redevient
exact. **Net R1c : +3** (4 gains, 1 perte), pas 0 perte.

### 3.5 R2 — le SUB sans précédent : +4, mais `s037` perdu

Le code livré réduit R2 à `precedent is None → SUB`. A17 prescrivait
`REL si (marqueur ∈ DURS) ou (marqueur ∈ RELATIFS et précédent = GN), sinon SUB`. Sur
`s037` (« Paul qui marche marche »), le `qui` initial n'a pas de précédent : le code livré en
fait une **SUB** `[5:15]`, alors que le gold attend une **REL** `[5:15]` ; sans R2, la REL
`[5:15]` est exacte. **Net R2 : +3** (4 gains, 1 perte) : le net coïncide avec le « +3 » de la
fiche, mais la composition est fausse (4/1, pas 3/0).

### 3.6 R3a — subordonnants par langue : **inerte**

`SUB_PAR_LANGUE` n'est consulté que dans la condition d'entrée du marqueur. Or **tous ses
membres sont déjà dans `RELATIFS` ou `SUBORDONNANTS`** (`car`, `parce`, `puisque`, `comme`,
`quand`, `si`, `lorsque`, `because`, `although`, `though`, `if`, `while`, `as`, `since`,
`unless`, `whether`, `when`). La condition est donc **redondante** : le résultat est
identique au bit près (212/212, mêmes spans, même F1). En particulier, `car` reste dans
`SUBORDONNANTS` et reste testé **sans condition de langue** : « The car that I bought runs »
produit toujours la SUB `[4:21]` qui coupe le GN. La règle A17 (retirer `car` des
subordonnants **anglais**) n'est pas implémentée. Mesure : **0 gain, 0 perte** ; la règle
fidèle récupère `r280` (+1 exact), pas +2.

### 3.7 R3c — `fall`/`call` : la seule règle dont l'effet annoncé est juste

Ajout de `fall/falls/fell/fallen/falling` et `call/calls/called/calling` à `VERBES_CONNUS` :
**+2 exacts** (`r102` : cible `falls` corrigée ; `r245` : `call` avec R2), **0 perte**. La
fiche annonce +2 : conforme.

### 3.8 La table de la fiche ne somme pas

| règle | fiche | mesuré sur le code livré | verdict |
|---|---|---:|---|
| **R1** | +15 dev, +5 test, **0 perte** | +14 dev, +5 test ; **3+3 pertes** ; net **+13** | faux |
| **R2** | +3 | +4 gains, **−1 perte** ; net **+3** | net juste, perte omise |
| **R3a** | +2 | **0** (R3a fidèle : +1) | faux |
| **R3c** | +2 | **+2**, 0 perte | juste |
| **somme** | **+27** → 195+27 = **222** | +24 gains, −7 pertes, net **+17** → **212** | **contradiction arithmétique** |

Les nombres des lignes R1, R2 et R3a **coïncident avec ceux du harnais A17** (R1 : +15/+5/0 ;
R2 : +3 ; R3a : le +2 du faisceau R3), pas avec les mesures du code livré ; R2 tombe sur le
même net par compensation (4 gains/1 perte au lieu de 3/0), et R3c correspond, lui, au code
livré. Additionner ces lignes est doublement faux : les règles interagissent (`r245` exige R2
**et** R3c) et certaines mesures A17 ne sont pas reproductibles dans l'intégration. Le total
mesuré est **+24 gains bruts − 7 pertes = +17**, pas +27.

## 4. Décomposition : d'où viennent les 212 et les 27

### 4.1 Arithmétique des ensembles

```
exacts : 195 (v7) − 7 (régressions nouvelles) + 23 (des 26 gains A17) + 1 (r102 corrigé) = 212
labels : 196 (v7) − 7 (régressions nouvelles) + 23 (des 26 gains A17)                      = 212
```

- **7 régressions nouvelles** (toutes françaises, toutes REL, toutes exactes en v7) :
  `r273 s032 s037 s069 s072 s115 s135` — 6 dues à R1a, 1 à R2 (`s037`).
- **26 gains A17** : 20 R1 + 4 R2 (dont `r245` avec R3c) + 1 R3a (`r280`) + 1 R3b (`r153`).
  **23 sont intégrés** ; les 3 manquants sont `g017` (R1c), `r153` (R3b absent), `r280`
  (R3a inerte).
- **`r102`** n'était pas un span manquant : il avait un label avec la mauvaise cible ; R3c le
  corrige (+1 exact, +0 label).

A17 attendait **222 exacts / 222 labels** (195+27 et 196+26) ; le code livré donne **212**.
L'écart de 10 = **7 régressions + 3 gains A17 non intégrés**.

### 4.2 Les 27 spans, classés

| classe | n | types | identifiants |
|---|---:|---|---|
| **A17 non récupérables** (13) + hors périmètre (4) | **17** | 8 REL / 5 SUB / 4 GP | `r035 r255 r264 r288 s010 s027 s035 s044 s061 s065 s112 s114 s125 s141 s146 s148 s160` |
| **Régressions nouvelles** | **7** | 7 REL | `r273 s032 s037 s069 s072 s115 s135` |
| **Gains A17 non intégrés** | **3** | 1 REL / 1 SUB / 1 GP | `g017 r153 r280` |

**Langues / sources** : 22 français, 5 anglais (`r035`, `g017`, `r153`, `r280`, `r288`) ;
19 synthétiques, 7 réels, 1 `hand` (`g017`). Les 27 contiennent bien les 17 identifiants
d'A17 (même ensemble, mêmes types) ; les 10 autres sont les 7 régressions et les 3 gains A17
non intégrés.

| id | lg | type | source | span | texte | cible | classe |
|---|---|---|---|---:|---|---|---|
| `r153` | en | GP | reel | 8:19 | « for the bus » | `wait` | A17 non intégré (R3b) |
| `r035` | en | REL | reel | 9:24 | « she talks about » | `film` | A17 hors périmètre (relative zéro) |
| `r255` | fr | REL | reel | 11:27 | « que j'ai achetée » | `voiture` | A17 hors périmètre (lexique réel) |
| `r264` | fr | SUB | reel | 8:26 | « qu'il vient demain » | `sais` | A17 hors périmètre (tokenisation) |
| `r288` | en | SUB | reel | 7:29 | « that he comes tomorrow » | `know` | A17 hors périmètre (adverbe final) |
| `s010` | fr | REL | synthetique | 10:18 | « qui nage » | `chemin` | A17 non récupérable (lexique) |
| `s035` | fr | REL | synthetique | 10:19 | « qui ferme » | `papier` | A17 non récupérable (lexique) |
| `s061` | fr | REL | synthetique | 9:18 | « qui saute » | `nuage` | A17 non récupérable (lexique) |
| `s065` | fr | REL | synthetique | 5:17 | « qui commence » | `elle` | A17 non récupérable (antécédent) |
| `s125` | fr | REL | synthetique | 11:21 | « qui compte » | `renard` | A17 non récupérable (lexique) |
| `s141` | fr | REL | synthetique | 5:15 | « qui trouve » | `Emma` | A17 non récupérable (lexique) |
| `s027` | fr | GP | synthetique | 31:33 | « il » | `marche` | A17 non récupérable (gold) |
| `s146` | fr | GP | synthetique | 25:35 | « les jardin » | `observe` | A17 non récupérable (gold) |
| `s148` | fr | GP | synthetique | 20:39 | « les ancienne lettre » | `nage` | A17 non récupérable (gold) |
| `s160` | fr | GP | synthetique | 20:29 | « le renard » | `nage` | A17 non récupérable (gold) |
| `s044` | fr | SUB | synthetique | 17:29 | « que ils crie » | `nage` | A17 non récupérable (lexique) |
| `s112` | fr | SUB | synthetique | 24:39 | « que Lucas ferme » | `nage` | A17 non récupérable (lexique) |
| `s114` | fr | SUB | synthetique | 22:43 | « que les avocat compte » | `dessine` | A17 non récupérable (lexique) |
| `r273` | fr | REL | reel | 9:23 | « qui pousse ici » | `fleur` | régression R1a |
| `s032` | fr | REL | synthetique | 11:19 | « qui crie » | `village` | régression R1a |
| `s069` | fr | REL | synthetique | 15:23 | « qui crie » | `canard` | régression R1a |
| `s072` | fr | REL | synthetique | 20:31 | « qui dessine » | `chanson` | régression R1a |
| `s115` | fr | REL | synthetique | 19:30 | « qui observe » | `fenêtre` | régression R1a |
| `s135` | fr | REL | synthetique | 11:22 | « qui dessine » | `fenêtre` | régression R1a |
| `s037` | fr | REL | synthetique | 5:15 | « qui marche » | `Paul` | régression R2 |
| `g017` | en | SUB | hand | 9:28 | « that she would come » | `said` | A17 non intégré (R1c) |
| `r280` | en | REL | reel | 8:21 | « that I bought » | `car` | A17 non intégré (R3a) |

### 4.3 Ce que la fiche dit des 27 — et ce qu'elle omet

- **Le compte est juste** : 27 = 16 REL + 6 SUB + 5 GP ; les 17 « inatteignables » sont bien
  les 17 d'A17. Mais **4 de ces 17 ne sont pas inatteignables** : ce sont les 4
  « récupérables hors périmètre » d'A17 (`r035`, `r255`, `r264`, `r288`) ; seuls 13 sont
  non récupérables sans changer le gold ou le lexique.
- **La décomposition de la fiche somme à 20, pas 27** : « 12 synthétiques + 4 GP + 1
  tokenisation + 1 relative zéro + 1 adverbe final + 1 couverture verbale » = 20. Il manque
  **3 SUB synthétiques** (`s044`, `s112`, `s114`) et **4 cas** (`r273`, `g017`, `r153`,
  `r280`). Le « 12 synthétiques » ne compte que les REL synthétiques : les 27 contiennent
  **19 synthétiques** (12 REL + 4 GP + 3 SUB).
- **Les 10 non-A17 ne sont pas des inatteignables** : 7 régressions (dont 6 dues à R1a) et
  3 gains A17 non intégrés. La fiche les compte dans les 27 sans les nommer.

### 4.4 L'effet par langue : le français recule

| langue | cibles | labels v7 → v8 | exacts v7 → v8 | couverture v7 → v8 |
|---|---:|---:|---:|---:|
| **fr** | 151 | 135 → **129** (−6) | 135 → **129** (−6) | 0,8940 → **0,8543** |
| **en** | 88 | 61 → **83** (+22) | 60 → **83** (+23) | 0,6932 → **0,9432** |

La phrase « les deux langues sont parfaites (1,0 / 1,0) sur les 212 labels prédits » est vraie
au sens `exact / labels` (129/129, 83/83), mais elle masque le **recul français de 6 exacts**
et une couverture française (0,854) désormais **inférieure** à l'anglaise (0,943). Le gain net
de +17 exacts est un gain anglais (+23) moins une perte française (−6).

## 5. Contrôles négatifs

La fiche et le JSON n'en contiennent **aucun** ; c'est un manque au regard de la règle 2
(« sans contrôle négatif, ce n'est pas un résultat »). Les contrôles ci-dessous ont été
exécutés sur le code livré, gold vivant 612.

| contrôle | tirage | observé | référence nulle | p |
|---|---|---:|---:|---:|
| **permutation globale des cibles** | 2 000 (graine 0) | **212/212 = 1,0** | moyenne **2,04/212 = 0,96 %** ; max 9 ; p95 5 | **0/2 000** |
| **candidat aléatoire** (top-1) | 2 000 | **212/212 = 1,0** | moyenne **76,1/212 = 35,9 %** (516 candidats) | **0/2 000** |
| **permutation des listes de candidats** (top-k) | 2 000 | **177/212 = 83,49 %** | moyenne **1,81/212 = 0,85 %** ; max 7 | **0/2 000** |
| **hasard officiel** (`evaluer_gold`) | 1 tirage graine 0 | top-1 **212/239 = 88,70 %** | **1/239 = 0,42 %** | — |

**Lecture.** L'attachement livré n'est pas un artefact du hasard : une permutation des cibles
divise l'exact par plus de 100, un candidat aléatoire par 2,8, et le top-k par 98. Les 27 spans
sont bien ceux listés ci-dessus (identifiants, langues, types vérifiés). Le contrôle de
permutation redonne d'ailleurs l'ordre de grandeur du contrôle A17 (2,011/222 = 0,91 %), ce
qui valide le harnais.

## 6. dev/test — re-mesure des deux moitiés

Split `crc32(id) % 3 == 0` (test) : **422 dev + 190 test = 612**, aucune duplication,
**163 + 76 = 239 cibles**.

| moitié | phrases | cibles | labels | exact | couverture | F1 | tête |
|---|---:|---:|---:|---:|---:|---:|---:|
| **dev v7** (fiche) | 422 | 163 | 134 | 133/134 = 0,9925 | 0,8221 | 0,5512 | 0,7132 |
| **dev courant** | 422 | 163 | **148** | **148/148 = 1,0** | **0,9080** | **0,5723** | **0,7270** |
| **test v7** (fiche) | 190 | 76 | 62 | 62/62 = 1,0 | 0,8158 | 0,5651 | 0,7196 |
| **test courant** | 190 | 76 | **64** | **64/64 = 1,0** | **0,8421** | **0,5714** | **0,7241** |
| **tout v7** | 612 | 239 | 196 | 195/196 = 0,9949 | 0,8201 | 0,5555 (vivant) | 0,7152 |
| **tout courant** | 612 | 239 | **212** | **212/212 = 1,0** | **0,8870** | **0,5720** | **0,7262** |

**Écarts v7 → courant** : dev **+14 labels, +15 exacts** (le +1 vient de `r102` corrigé),
couverture +0,0859, F1 +0,0211, tête +0,0138 ; test **+2 labels, +2 exacts**, couverture
+0,0263, F1 +0,0063, tête +0,0045.

**Écart au programme A17** : A17 annonçait **dev 154/154** et **test 68/68**. Le code livré
donne **dev 148/148** et **test 64/64** : **−6 dev, −4 test**. La ventilation est exacte :
- dev : 4 régressions (`r273`, `s037`, `s069`, `s135`) + 2 gains A17 non intégrés (`g017`,
  `r280`) = −6 ;
- test : 3 régressions (`s032`, `s072`, `s115`) + 1 gain A17 non intégré (`r153`) = −4.

La fiche [dev/test v7](rapport-dev-test-v7.md) est ancrée sur `69bd865e` ; elle n'est pas
mise à jour par `f908d7b0`. La fiche R1/R2/R3 dit « dev/test à re-mesurer » (§ 5) : c'est fait
ici. Les deux moitiés sont désormais à **1,0 exact/labels**, mais le test reste **non
aveugle** (A17 a diagnostiqué sur dev **et** test).

**Par langue** (courant) : dev fr 89/89 (101 cibles, couv. 0,8812), en 59/59 (62 cibles,
couv. 0,9516) ; test fr 40/40 (50 cibles, couv. 0,8000), en 24/24 (26 cibles, couv. 0,9231).
Les pertes françaises de R1a/R2 sont donc concentrées en dev (fr 92 → 89) et en test
(fr 43 → 40).

## 7. Portes — 183/183, mais des docstrings périmées

`PYTHONPATH=. python3 -m tools.pensee.autotest` : **183/183 portes tenues**, exit 0. Le
compte est exact (T0–T180 + les deux T1 supplémentaires). En revanche, **15 docstrings du
périmètre attachement/segmentation contredisent leur propre assertion** ; la porte passe,
mais le texte qui la décrit est faux :

| porte | docstring | mesure affichée |
|---|---|---|
| T111 | tête F1 0,4183 | **0,7402** |
| T112 | F1 0,5595 | **0,5763** |
| T113 | F1 0,5595, tête 0,7205 | **0,5763 / 0,7316** |
| T114 | F1 0,5864, tête 0,7285 | **0,6033 / 0,7399** |
| T115 | 0,455 contre 0,441 | **0,6822** |
| T153 | top1 0,8159, exact 0,8159, couv. 0,8201 | **0,887 / 0,887 / 0,887** |
| T161 | 195/196 | **212/212** |
| T162 | 166/239 | **177/239** |
| T163 | 43 de span, 30 de cible | **27 de span, 35 de cible** |
| T166 | 21 REL, 17 SUB, 5 GP (43) | **16 REL, 6 SUB, 5 GP (27)** |
| T167 | exactitude spans ÷ 196 | **÷ 212** |
| T172 | exact 195/196 | **0 échec** |
| T173 | 166/196 ; 166/239 | **177/177** |
| T177 | 88 → 166 | **177** |
| T179 | exact_any 195/196 | **212/212** |

T180 est qualitativement ambigu : « la couverture anglaise non » — l'anglaise est
maintenant **0,943**, au-dessus de la française (0,854). Ces docstrings ne changent pas le
verdict des portes, mais ils font dire au banc le contraire de ce qu'il mesure. Le commit
`638ac8e8` annonçait 13 docstrings corrigées ; **15 sont périmées au commit audité**.

**Ce que les portes ne prouvent pas** : elles encodent les valeurs courantes (212, 27 spans)
et passent par construction ; elles ne testent ni la fidélité aux règles A17, ni l'attendu
222/17. T163 et T166 en particulier **entérinent** les 27 au lieu de signaler les 10
récupérables.

## 8. Écarts, par gravité

1. **Majeure — la table des règles contredit le total.** +27 annoncés, +17 mesurés ; 222
   annoncés par la somme, 212 dans la ligne « après ». Le chiffre 222 est exactement celui
d'A17, pas celui du code livré.
2. **Majeure — R1a perd 6 spans français** (0 perte annoncée). Le mécanisme (`SUJETS` sans
   relatifs) n'est pas la garde `PRON` d'A17 ; il transforme des REL synthétiques exactes en
   spans manquants.
3. **Majeure — R1c perd `g017`** : `verbes_vus` n'est pas incrémenté après un auxiliaire, donc
   la garde d'adverbe final ne s'applique pas et « yesterday » reste dans la SUB.
4. **Majeure — R2 perd `s037`** : le `precedent is None → SUB` généralisé classe une REL
   initiale en SUB ; la règle DURS/RELATIFS d'A17 n'est pas intégrée.
5. **Majeure — R3a est inerte** (0 effet) alors que la fiche annonce +2 ; la règle fidèle vaut
   +1 (`r280`), pas +2.
6. **Majeure — R3b n'est pas intégré** : `r153` reste absent ; la fiche parle pourtant des
   « quatre règles de la fiche A17 intégrées ».
7. **Majeure — le français recule** : 135 → 129 exacts (couverture 0,894 → 0,854), masqué par
   le « 1,0 / 1,0 » qui est un taux `exact/labels`.
8. **Moyenne — les 27 ne sont pas 17 + 10 inatteignables** : 7 régressions nouvelles + 3
   gains A17 non intégrés. La décomposition de la fiche somme à 20 et compte 12 synthétiques
   au lieu de 19.
9. **Moyenne — aucun contrôle négatif** dans la fiche ni le JSON ; les contrôles de § 5 le
   corroborent, mais ils manquent au résultat publié.
10. **Moyenne — 15 docstrings de portes périmées**, qui contredisent toutes leur propre
    assertion (T111 à T179).
11. **Mineure — `MODAUX` est une constante morte**, citée dans le dispositif.
12. **Mineure — bases de mesure** : `F1` et `tête` ne sont pas annoncés comme « gelé 602 »
    dans le JSON ; le vivant vaut 0,5720 / 0,7262.
13. **Mineure — « 17 inatteignables »** : 13 non récupérables + 4 récupérables hors
    périmètre (A17 les distingue).
14. **Mineure — l'usage affiché d'`autotest.py`** (`python3 tools/pensee/autotest.py`) échoue
    sur l'import relatif ; il faut `-m`.

## 9. Ce qui pourrait rendre cet audit faux

- **In-sample** : les règles ont été dessinées sur ce gold ; le test n'est pas aveugle (A17 a
  diagnostiqué sur dev **et** test). L'audit ne corrige pas ce biais, il mesure l'intégration.
- **Un seul split déterministe** (`crc32 % 3`), sans validation croisée ; les chiffres
  dev/test sont ceux de ce split.
- **Le harnais A17 n'est pas committé** (`/tmp/spans/sim3.py` selon sa fiche) : la comparaison
  porte sur ses chiffres publiés, pas sur son code. Si ses chiffres étaient faux, l'écart
  A17→livré changerait — mais la ligne de base et la ligne livrée, elles, sont reproduites
  exactement.
- **Ablations par copies** : le module copié « tout éteint » ne diffère du parent que par deux
  constantes inutilisées ; la fidélité est vérifiée au chiffre. Les variantes intermédiaires
  ne touchent qu'une chaîne à la fois.
- **Dépôt déjà modifié** : `journal/`, plusieurs `reports/` et le sous-module
  `tools/structures` portaient des modifications non commitées antérieures à cet audit. Le
  fichier `tools/bloc_linguistique.py` **était à l'état du commit pendant les mesures** (copie
  de base byte-identique) ; il a été **modifié après** (22:14:32, hors audit), ce qui porte le
  top-k de l'arbre courant à 211. `tools/pensee/autotest.py` a lui aussi été modifié après
  l'audit (assertions top-k 177 → 211). Le fichier sale du sous-module
  (`donnees/paragraphes-validations.jsonl`) n'est pas lu par `generateur.py` ; il n'affecte
  pas les mesures.
- **Portes** : seules les 183 portes d'`autotest.py` ont été rejouées, pas les 81 portes
  shell de `tools/toutes-les-portes.sh` (hors périmètre de la fiche).

## 10. Ce qu'il faudrait corriger (proposition)

1. **Réécrire la table des règles** avec deux colonnes « gains bruts / pertes » mesurées sur
   le code livré, et **supprimer la somme +27** ; le total est +24/−7 = +17.
2. **R1a** : garder les relatifs dans `SUJETS` et ajouter la garde `PRON` d'A17 dans
   `est_verbe` ; re-mesurer les 6 pertes.
3. **R1c** : compter le prédicat (pas seulement `verbes_vus`) dans la garde d'adverbe final ;
   `g017` doit redevenir exact.
4. **R2** : implémenter `DURS` + antécédent GN, ou au minimum traiter les relatifs durs
   (`qui`, `dont`, `où`, `which`, `who`…) comme REL même sans précédent ; `s037`.
5. **R3a** : conditionner réellement `SUBORDONNANTS` par la langue (retirer `car` en anglais)
   dans **tous** les usages ; +1 attendu (`r280`), pas +2.
6. **R3b** : ajouter la garde « un déterminant n'introduit pas un verbe » dans la boucle GP ;
   +1 attendu (`r153`).
7. **Mettre à jour la fiche** : 212/212, 27 spans dont **10 récupérables** (7 régressions,
   3 non intégrés), français 129/129 mais couverture 0,854 ; les 222 exacts et les 17 restants d'A17 ne sont pas atteints.
8. **Ajouter le contrôle négatif** (permutation ≥ 200 tirages) au JSON et à la fiche.
9. **Corriger les 15 docstrings** de portes et l'usage `-m` d'`autotest.py`.
10. **Supprimer ou utiliser `MODAUX`**.

## 11. Fichiers

- [`rapport-audit-r1r3.md`](rapport-audit-r1r3.md) — ce rapport.
- [`pensee-audit-r1r3.json`](pensee-audit-r1r3.json) — les chiffres, les ids et les contrôles.

**Aucun fichier existant n'a été modifié ; aucun commit n'a été fait.** Les scripts de
mesure vivaient dans `/tmp/audit_r1r3/` et ne sont pas livrés.
