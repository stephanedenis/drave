# B1 — le protocole Panini à date contrôlée : 60 paires, trois strates, et les 26 signatures qui manquent

> **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **L** · **Tâche** : **B1**, suite de la
> note 4A · **Date** : 2026-11-15 · **HEAD mesuré** : `f926b5bc` · **Verdict** : ✅ **le protocole est
> gelé et rejouable ; le §334 seul ne peut pas fournir les 60 paires signées** — 60 paires
> (20 contemporaines / 20 même tradition / 20 même langue), **59 textes**, **27 paires déjà signées**
> (1 G1, 14 G2, 12 G3), **26 textes à signer** par Panini avec le même extracteur V14. Le test n'est
> **pas exécuté** : il attend ces signatures. Le manifeste est
> [`protocole-date.json`](protocole-date.json) ; le dispositif est
> [`../tools/protocole_date.py`](../tools/protocole_date.py).

**En trois lignes.** (1) La suite de 4A n'est pas « 20 paires contemporaines de traditions
différentes » à prendre dans les 44 signatures : le §334 n'en fournit **qu'une** dont les deux
signatures soient déjà mesurées (`book_of_enoch` × `sibylline_oracles`). (2) On peut néanmoins
**geler** les 60 paires : 77 candidates G1, 266 G2, 430 G3 dans les 107 sources du §334, dont
102 acquises ; la sélection n'utilise que les métadonnées (année, tradition, langue, auteur, titre),
jamais les 14 atomes ni les distances lexicales. (3) Le protocole est écrit, pré-enregistré et
rejouable ; il ne reste que **26 textes à signer** pour que le test existe — et c'est précisément la
demande à adresser à Panini.

**Ce que cette fiche est, et n'est pas.**

- **Est** : le **protocole** de la suite commune proposée dans la note 4A — 60 paires en trois
  groupes, les hypothèses H0/H1, les contrôles négatifs et positifs, les 14 atomes, le
  pré-enregistrement, la commande de rejeu et le JSON qui gèle les 60 paires.
- **N'est pas** : une mesure. Aucun `d_sig`, aucun `p`, aucun `R²` n'est calculé ici sur les 60
  paires : le test est **en attente** des signatures. Le « noyau » déjà signé (27 paires) n'est
  **pas** testé ; il serait un sous-ensemble choisi par la disponibilité, donc biaisé.
- **Ne modifie rien chez Panini** : les sept artefacts §334 sont lus en lecture seule, leurs
  SHA-256 sont dans le JSON, et le script refuse d'écrire dans l'arborescence Panini.

## 1. La question : ce que 4A a laissé ouvert

La note 4A ([`note-panini-334.md`](note-panini-334.md)) a rejoué le §334 de Panini/Nipada : 655
lignes de paires, 495 paires uniques, 488 paires uniques non auto, 48 textes, 44 signatures V14.
Le résultat est double :

| mesure | 4A | lecture |
|---|---:|---|
| loi H0 de Panini (`d_lex ~ d_topo^0,67`) | **R² = 0,909139** (655 lignes) / **0,906307** (488) | la loi se reproduit |
| β époque de la v150 | **+0,138** publié → **−0,006** (374 paires, n.s.) | non reproduit |
| R² de l'époque seule | **0,258** | la date seule explique un quart |
| ΔR² de l'époque après topologie | **0,0089** (p = 0,86) | la topologie absorbe la date |
| colinéarité du plan | **28,7 ans** (même tradition) vs **1 189 ans** (inter-traditions) | le plan n'a pas de support commun |
| filiation à date fixe, tranche axiale | **Δ = −0,166** (p = 0,0005) | fort |
| filiation à surface contrôlée (même langue source) | **Δ = −0,135** contre un nul de **−0,129** (p = 0,335) | disparaît |
| retrieval même tradition (44 signatures) | **61,4 %** contre un nul de **50,0 %** (p = 0,0492, Holm 0,128) | marginal |
| retrieval époque (≤ 50 ans) | **56,8 %** contre **53,8 %** (p = 0,373) | non significatif |
| prédiction d'année intra-tradition | **R² = 0,042** (p = 0,0086, Holm 0,034) | seule trace qui survit |

La conclusion de 4A n'est pas « Panini a tort » : c'est que **leur corpus ne sépare pas l'époque de
la filiation**. Les paires de même tradition sont presque toutes contemporaines (28,7 ans d'écart en
moyenne), les paires inter-traditions presque toutes longues (1 189 ans). Un modèle qui met la date
et la topologie côte à côte ne peut pas identifier les deux effets : la topologie **contient** la
date, et la date **contient** la tradition.

La suite proposée dans la note 4A est donc un **plan à support commun** :

1. **20 paires contemporaines (± 10 ans) de traditions différentes** — la date est fixée, la
   filiation varie ;
2. **20 paires de même tradition à ± 200 ans** — la filiation est fixée, la date varie ;
3. **20 paires de même langue source à dates décalées** — la surface est fixée, la date varie.

C'est exactement ce que gèle ce manifeste.

## 2. Le matériau et son audit

Les artefacts sont ceux du §334, lus en lecture seule. Le JSON porte leurs SHA-256 ; le HEAD de
Panini a bougé depuis 4A (`9b80c323` au lieu de `e10d695e`), mais **les sept fichiers sont
byte-identiques** à ceux de 4A — les SHA-256 le prouvent. On pinne donc les hashes, pas le HEAD.

| objet | valeur |
|---|---:|
| sources du manifeste §334 | **107** |
| sources acquises (`ok = true`) | **102** |
| sources non acquises | **5** : `brahma_sutra_badarayana`, `atharvaveda_samhita`, `an7_64_kodhana`, `aristotle_de_anima`, `plato_republic_fr` |
| textes datés dans le graphe v35 | **1 730** (dont **106** des 107 sources) |
| signatures V14 mesurées (`analytic_sigs_v1`) | **44** |
| signatures V14 du graphe v35 (`v14_signature`) | **57** |
| œuvres communes aux deux jeux | **11** |
| cosinus sur ces 11 œuvres | **0,4198 – 0,8245** (moyenne **0,7212**) |
| distance L2 sur ces 11 œuvres | **0,1915 – 0,4519** (moyenne **0,2512**) |
| textes des 655 paires §334 | **48** |
| lignes de paires | **655** |
| paires uniques | **495** |
| paires uniques non auto | **488** |

**Le point d'instrument, à ne pas rater.** Les 44 signatures de `analytic_sigs_v1.json` et les 57
`v14_signature` du graphe v35 ne sont **pas le même instrument** : sur les 11 œuvres communes, le
cosinus va de 0,42 à 0,82. Mélanger les deux dans un même test serait une faute. Le protocole utilise
**une seule** source : `analytic_sigs_v1.json`, l'instrument de 4A. Les 57 signatures du graphe ne
servent qu'à documenter l'écart et à montrer pourquoi il faut re-signer avec **le même** extracteur.

## 3. La faisabilité : ce que le §334 peut fournir

On a appliqué les trois critères aux **106 textes datés** des 107 sources (les 5 sources non
acquises sont exclues), avec les règles de non-duplication : pas le même texte, pas le même titre
normalisé, pas le même travail auteur+titre, auteurs différents sauf anonymes.

| groupe | critère | candidats | deux signatures 44 | une seule | aucune |
|---|---|---:|---:|---:|---:|
| **G1** | \|Δannée\| ≤ 10, familles larges différentes | **77** | **1** | 30 | 46 |
| **G2** | 20 ≤ \|Δannée\| ≤ 200, même famille large | **266** | **103** | 85 | 78 |
| **G3** | \|Δannée\| ≥ 50, même langue source | **430** | **157** | 173 | 100 |

**Le résultat de faisabilité est net.** Le §334 fournit **77** paires G1 candidates, mais **une
seule** a ses deux signatures dans l'instrument de 4A. Les 20 paires G1 existent donc comme
**plan** ; elles n'existent pas comme **mesure** tant que Panini n'a pas signé les textes. C'est le
fait central de cette fiche, et il ne dépend d'aucun résultat : il se lit dans les métadonnées.

La composition des pools explique pourquoi G1 est si mince : les 77 candidates sont
**30 GRECO–INDIAN**, **14 CHINESE–INDIAN**, **14 CHINESE–GRECO**, **7 BUDDHIST–INDIAN**, **3
FORMAL_LOGIC–GRECO**, **3 COGNITIVE_SCIENCE–FORMAL_LOGIC**, **2 ABRAHAMIC–INDIAN**, puis 4 familles de paires à un seul candidat
(ABRAHAMIC–CHINESE, CHINESE–CLASSICAL_ORACULAR, EUROPE_MODERN–MILLENARIAN,
ABRAHAMIC–CLASSICAL_ORACULAR). Le corpus a assez de **paires** inter-traditions contemporaines ;
il n'a pas assez de **signatures** sur ces paires.

G2 et G3 sont largement pourvus : 266 et 430 candidates, dont 103 et 157 déjà signées. Le problème
n'est donc pas le nombre de paires ; il est **localisé sur G1**, et il est **instrumental**, pas
statistique.

## 4. Les 60 paires gelées

La sélection est **déterministe** et n'utilise que les métadonnées. Les quotas sont fixés avant
lecture des signatures :

- **G1 (20)** : 6 GRECO–INDIAN, 4 CHINESE–GRECO, 3 CHINESE–INDIAN, 2 ABRAHAMIC–INDIAN,
  1 ABRAHAMIC–CHINESE, 1 ABRAHAMIC–CLASSICAL_ORACULAR, 1 GRECO–FORMAL_LOGIC,
  1 COGNITIVE_SCIENCE–FORMAL_LOGIC, 1 EUROPE_MODERN–MILLENARIAN.
- **G2 (20)** : 8 GRECO, 6 ABRAHAMIC, 3 INDIAN, 3 CHINESE.
- **G3 (20)** : 12 anglais inter-familles, 5 grec, 2 sanskrit, 1 chinois.

Les 60 paires portent **59 textes distincts** (60 paires = 120 positions ; un texte peut servir
plusieurs paires). L'usage maximal est de **5** (`isaiah_book`, `book_of_enoch`), puis 4
(`daodejing`, `mandukya_upanishad`, `yueji`). Ce n'est pas un échantillon indépendant : l'inférence
regroupe par texte (permutation et bootstrap par texte), et le JSON donne l'usage de chaque texte.

Deux seuils opérationnalisent les libellés. **G2** exige `20 ≤ |Δannée| ≤ 200` : un décalage nul
ne testerait pas la date, et la sensibilité `1–200` est possible mais inclurait des quasi-doublons.
**G3** exige `|Δannée| ≥ 50` : un décalage de 10 ans ne serait pas une « date décalée ». Ces seuils
sont dans le JSON ; on peut les abaisser en sensibilité, jamais dans le test principal.

### G1 — 20 paires contemporaines de traditions différentes

| # | paire A × B | années | familles | langues | sig. |
|---:|---|---:|---|---|---:|
| 01 | `baudhayana_dharmasutra` × `plato_crito` | -400 / -399 (Δ1) | INDIAN / GRECO | san / grc | 0 |
| 02 | `vasistha_dharmasutra` × `plato_euthyphro_jowett` | -400 / -399 (Δ1) | INDIAN / GRECO | san / grc | 0 |
| 03 | `hiranyakesi_grhya_sutra` × `plato_charmides` | -400 / -390 (Δ10) | INDIAN / GRECO | san / grc | 1 |
| 04 | `paraskara_grhya_sutra` × `plato_crito` | -400 / -399 (Δ1) | INDIAN / GRECO | san / grc | 0 |
| 05 | `apastamba_grhya_sutra` × `plato_euthyphro_jowett` | -400 / -399 (Δ1) | INDIAN / GRECO | san / grc | 0 |
| 06 | `sankhayana_grhya_sutra` × `plato_charmides` | -400 / -390 (Δ10) | INDIAN / GRECO | san / grc | 1 |
| 07 | `daodejing` × `plato_laws` | -350 / -350 (Δ0) | CHINESE / GRECO | lzh / grc | 1 |
| 08 | `daodejing` × `plato_sophist` | -350 / -360 (Δ10) | CHINESE / GRECO | lzh / grc | 1 |
| 09 | `qiwulun` × `epicurus_letters` | -300 / -300 (Δ0) | CHINESE / GRECO | lzh / grc | 1 |
| 10 | `mengzi` × `epicurus_letters` | -300 / -300 (Δ0) | CHINESE / GRECO | lzh / grc | 1 |
| 11 | `mandukya_upanishad` × `qiwulun` | -300 / -300 (Δ0) | INDIAN / CHINESE | san / lzh | 1 |
| 12 | `mandukya_upanishad` × `mengzi` | -300 / -300 (Δ0) | INDIAN / CHINESE | san / lzh | 1 |
| 13 | `mandukya_upanishad` × `xiaojing` | -300 / -300 (Δ0) | INDIAN / CHINESE | san / lzh | 0 |
| 14 | `burnet_early_greek_philosophy` × `curry_1930` | 1930 / 1930 (Δ0) | GRECO / FORMAL_LOGIC | en / eng | 1 |
| 15 | `miller_1956` × `zadeh_1965` | 1956 / 1965 (Δ9) | COGNITIVE_SCIENCE / FORMAL_LOGIC | eng / eng | 0 |
| 16 | `ingersoll_works` × `russell_parousia_1878` | 1879 / 1878 (Δ1) | EUROPE_MODERN / MILLENARIAN | eng / eng | 1 |
| 17 | `chandogya_upanishad` × `isaiah_book` | -700 / -700 (Δ0) | INDIAN / ABRAHAMIC | san / eng | 1 |
| 18 | `brihadaranyaka_upanishad` × `isaiah_book` | -700 / -700 (Δ0) | INDIAN / ABRAHAMIC | san / eng | 1 |
| 19 | `book_of_enoch` × `yueji` | -200 / -200 (Δ0) | ABRAHAMIC / CHINESE | eng / lzh | 1 |
| 20 | `book_of_enoch` × `sibylline_oracles` | -200 / -200 (Δ0) | ABRAHAMIC / CLASSICAL_ORACULAR | eng / eng | 2 |

**sig.** = nombre de signatures déjà mesurées dans `analytic_sigs_v1` (2, 1 ou 0). G1 a **une**
paire à deux signatures (la 20), 13 à une seule, 6 à aucune.

### G2 — 20 paires de même tradition à dates décalées

| # | paire A × B | années | familles | langues | sig. |
|---:|---|---:|---|---|---:|
| 01 | `plato_gorgias` × `aristotle_posterior_analytics` | -385 / -340 (Δ45) | GRECO / GRECO | grc / grc | 2 |
| 02 | `plato_meno` × `aristotle_de_caelo` | -385 / -330 (Δ55) | GRECO / GRECO | grc / grc | 2 |
| 03 | `plato_republic_jowett` × `aristotle_parts_of_animals` | -380 / -330 (Δ50) | GRECO / GRECO | grc / grc | 2 |
| 04 | `plato_symposium_jowett` × `aristotle_categories` | -385 / -340 (Δ45) | GRECO / GRECO | grc / grc | 2 |
| 05 | `plato_republic_jowett` × `aristotle_nicomachean_ethics` | -380 / -340 (Δ40) | GRECO / GRECO | grc / grc | 2 |
| 06 | `plato_laws` × `aristotle_parts_of_animals` | -350 / -330 (Δ20) | GRECO / GRECO | grc / grc | 2 |
| 07 | `plato_gorgias` × `aristotle_prior_analytics` | -385 / -340 (Δ45) | GRECO / GRECO | grc / grc | 2 |
| 08 | `plato_phaedo` × `aristotle_de_caelo` | -380 / -330 (Δ50) | GRECO / GRECO | grc / grc | 2 |
| 09 | `isaiah_book` × `zechariah_book` | -700 / -520 (Δ180) | ABRAHAMIC / ABRAHAMIC | eng / eng | 2 |
| 10 | `jeremiah_book` × `hosea_book` | -600 / -750 (Δ150) | ABRAHAMIC / ABRAHAMIC | eng / eng | 2 |
| 11 | `ezekiel_book` × `zechariah_book` | -590 / -520 (Δ70) | ABRAHAMIC / ABRAHAMIC | eng / eng | 2 |
| 12 | `daniel_book` × `book_of_enoch` | -165 / -200 (Δ35) | ABRAHAMIC / ABRAHAMIC | eng / eng | 2 |
| 13 | `isaiah_book` × `ezekiel_book` | -700 / -590 (Δ110) | ABRAHAMIC / ABRAHAMIC | eng / eng | 2 |
| 14 | `jeremiah_book` × `zechariah_book` | -600 / -520 (Δ80) | ABRAHAMIC / ABRAHAMIC | eng / eng | 2 |
| 15 | `chandogya_upanishad` × `isa_upanishad` | -700 / -500 (Δ200) | INDIAN / INDIAN | san / san | 0 |
| 16 | `brihadaranyaka_upanishad` × `isa_upanishad` | -700 / -500 (Δ200) | INDIAN / INDIAN | san / san | 0 |
| 17 | `isa_upanishad` × `mandukya_upanishad` | -500 / -300 (Δ200) | INDIAN / INDIAN | san / san | 0 |
| 18 | `zhuangzi` × `yueji` | -300 / -200 (Δ100) | CHINESE / CHINESE | lzh / lzh | 0 |
| 19 | `xiaojing` × `yueji` | -300 / -200 (Δ100) | CHINESE / CHINESE | lzh / lzh | 0 |
| 20 | `daodejing` × `liji` | -350 / -300 (Δ50) | CHINESE / CHINESE | lzh / lzh | 0 |

G2 a **14** paires à deux signatures, **0** à une seule, **6** à aucune. Les 8 paires grecques et
les 6 paires abrahamiques sont déjà signées ; les 6 paires indiennes/chinoises ne le sont pas.

### G3 — 20 paires de même langue source à dates décalées

| # | paire A × B | années | familles | langues | sig. |
|---:|---|---:|---|---|---:|
| 01 | `2_esdras` × `miller_evidence_prophecy` | 100 / 1836 (Δ1736) | ABRAHAMIC / MILLENARIAN | eng / eng | 2 |
| 02 | `daniel_book` × `kleene_1936` | -165 / 1936 (Δ2101) | ABRAHAMIC / FORMAL_LOGIC | eng / eng | 2 |
| 03 | `book_of_enoch` × `curry_1930` | -200 / 1930 (Δ2130) | ABRAHAMIC / FORMAL_LOGIC | eng / eng | 2 |
| 04 | `sibylline_oracles` × `schank_1972` | -200 / 1972 (Δ2172) | CLASSICAL_ORACULAR / COGNITIVE_SCIENCE | eng / eng | 2 |
| 05 | `voluspa` × `isaiah_book` | 1000 / -700 (Δ1700) | NORSE_EDDIC / ABRAHAMIC | eng / eng | 2 |
| 06 | `lucretius_drn` × `holbach_systeme_en` | -55 / 1770 (Δ1825) | GRECO / EUROPE_MODERN | eng / eng | 0 |
| 07 | `hume_dialogues_nhr` × `russell_parousia_1878` | 1779 / 1878 (Δ99) | EUROPE_MODERN / MILLENARIAN | eng / eng | 1 |
| 08 | `miller_evidence_prophecy` × `bengio_2003` | 1836 / 2003 (Δ167) | MILLENARIAN / COGNITIVE_SCIENCE | eng / eng | 2 |
| 09 | `2_esdras` × `schank_1972` | 100 / 1972 (Δ1872) | ABRAHAMIC / COGNITIVE_SCIENCE | eng / eng | 2 |
| 10 | `daniel_book` × `miller_evidence_prophecy` | -165 / 1836 (Δ2001) | ABRAHAMIC / MILLENARIAN | eng / eng | 2 |
| 11 | `book_of_enoch` × `kleene_1936` | -200 / 1936 (Δ2136) | ABRAHAMIC / FORMAL_LOGIC | eng / eng | 2 |
| 12 | `sibylline_oracles` × `curry_1930` | -200 / 1930 (Δ2130) | CLASSICAL_ORACULAR / FORMAL_LOGIC | eng / eng | 2 |
| 13 | `sextus_pyrrho` × `plato_republic_jowett` | 190 / -380 (Δ570) | GRECO / GRECO | grc / grc | 1 |
| 14 | `sextus_pyrrho` × `plato_phaedo` | 190 / -380 (Δ570) | GRECO / GRECO | grc / grc | 1 |
| 15 | `sextus_pyrrho` × `plato_gorgias_jowett` | 190 / -380 (Δ570) | GRECO / GRECO | grc / grc | 1 |
| 16 | `plato_gorgias` × `aristotle_parts_of_animals` | -385 / -330 (Δ55) | GRECO / GRECO | grc / grc | 2 |
| 17 | `plato_symposium_jowett` × `aristotle_de_caelo` | -385 / -330 (Δ55) | GRECO / GRECO | grc / grc | 2 |
| 18 | `chandogya_upanishad` × `baudhayana_dharmasutra` | -700 / -400 (Δ300) | INDIAN / INDIAN | san / san | 0 |
| 19 | `brihadaranyaka_upanishad` × `baudhayana_dharmasutra` | -700 / -400 (Δ300) | INDIAN / INDIAN | san / san | 0 |
| 20 | `daodejing` × `yueji` | -350 / -200 (Δ150) | CHINESE / CHINESE | lzh / lzh | 0 |

G3 a **12** paires à deux signatures, **4** à une seule, **4** à aucune. Les 12 paires anglaises
sont **toutes inter-familles** : c'est la strate qui contrôle la surface en faisant varier la
filiation. Les 8 autres sont intra-famille (grec 5, sanskrit 2, chinois 1) : elles testent la date
**dans** une tradition, comme G2, mais à langue fixée. C'est une limite du corpus, pas un choix
théorique : il n'y a pas de paires inter-familles de même langue source en grec, sanskrit ou chinois.

## 5. Le protocole

### 5.1 Les 14 atomes et la distance

Les 14 atomes sont ceux de Panini, sans transformation :

`ÊTRE, DIFFÉRENCE, RAPPORT, ORIENTATION, SUJET, TEMPS, MODALITÉ, NOMBRE, ESPACE, OPÉRATION,
FONCTION, STRUCTURE, SYMÉTRIE, ÉQUATION`.

Chaque signature est un vecteur de 14 parts positives, de somme 1 (vérifiée à 10⁻⁶ près). La
distance principale est

`d_sig(a,b) = ||s_a − s_b||₂`.

La distance cosinus est secondaire. Aucune autre transformation, aucun centrage, aucune
normalisation : on veut la distance **brute** de l'instrument.

La distance de filiation est `d_topo`, le plus court chemin **non pondéré** dans le graphe v35
(1 753 nœuds, 19 967 arêtes). Elle corrèle à **r = 0,943** avec le `d_topo` publié des 655 paires :
c'est une approximation vérifiée, pas la quantité exacte. Elle est utilisée comme contrôle de
filiation, jamais comme variable d'époque.

### 5.2 H0 et H1

**H0.** Dans le modèle

`d_sig ~ 1 + d_topo^0,67 + 1[même famille] + 1[même langue] + |Δannée|/1000`,

le coefficient de `|Δannée|` est nul (`β_date = 0`) et le R² partiel de la date après filiation et
surface est nul (`ΔR²_date = 0`). Autrement dit : **la signature V14 est une signature de
filiation/surface, pas d'époque**.

**H1.** `β_date ≠ 0` (test bilatéral principal). **H1+** : `β_date > 0` (test directionnel
secondaire, l'avertissement de Panini). Un `β_date < 0` est rapporté comme un effet d'époque
inversé, pas comme une confirmation.

### 5.3 Les deux tests principaux

- **P1 (G2)** : dans les 20 paires de même famille, pente standardisée de `|Δannée|` sur `d_sig`,
  et R² partiel de la date. C'est le test « la date varie, la filiation est fixée ».
- **P2 (G3)** : dans les 20 paires de même langue source, même pente et même R² partiel. C'est le
  test « la date varie, la surface est fixée ».

Les deux tests sont corrigés par **Holm-Bonferroni** (m = 2). Le test pooled
`d_sig ~ 1 + d_topo^0,67 + même_famille + même_langue + |Δannée|/1000` sur les 60 paires est
**secondaire** : il ne remplace pas les strates, il les résume.

### 5.4 Le contrôle positif de G1

G1 ne contient que des paires **inter-familles** à date fixe. Si l'instrument ne voit pas la
filiation, il ne peut pas voir l'époque non plus : le test d'époque n'aurait pas d'assise. On
compare donc la moyenne de `d_sig` des 20 paires G1 à un nul où les **signatures** sont permutées
entre les textes du groupe, puis on recalcule la moyenne sur les mêmes paires. Si l'instrument voit
la filiation, la moyenne observée doit être **supérieure** au nul (les paires inter-familles sont
plus loin que des paires dont les signatures ont été mélangées). Ce contrôle est **positif** : il
doit réussir pour que P1/P2 soient interprétables.

### 5.5 Les contrôles négatifs

1. **Familles permutées dans des tranches de 250 ans** (G1) : le contraste de filiation doit
   disparaître. La date est préservée, la filiation est détruite.
2. **Années permutées dans chaque famille** (G2) : la pente de date doit disparaître. La filiation
   est préservée, l'époque est détruite.
3. **Années permutées dans chaque langue** (G3) : même contrôle, surface préservée.
4. **Signatures permutées entre textes** : tous les contrastes doivent disparaître. C'est le
   contrôle « l'instrument lit-il vraiment quelque chose ? ».
5. **Colonnes d'atomes permutées** : le résultat ne doit pas survivre à la destruction de l'ordre
   des 14 atomes. Si `d_sig` est invariant par permutation des colonnes, la distance ne mesure rien
   de sémantique.
6. **Traductions/ doublons retirés** : les paires dont un texte est une traduction de l'autre sont
   déjà exclues par `meme_travail` ; on refait le test sans elles pour vérifier que le résultat ne
   tient pas à un doublon.
7. **Noyau déjà signé** : on ne teste **pas** les 27 paires déjà signées comme si elles étaient
   l'échantillon complet. Elles sont décrites, pas testées ; le test attend les 60.

### 5.6 La décision

- **α = 0,05**, Holm sur P1 et P2.
- **ROPE** : `|β standardisé| < 0,10` ou `ΔR² < 0,02` = effet **négligeable** ; 0,10–0,30 = petit ;
  > 0,30 = notable.
- **H0 rejetée** si un test principal survit à Holm **et** sort du ROPE. Si les deux sont dans le
  ROPE, on conclut « pas d'effet d'époque détectable », **pas** « H0 vraie ».
- **Incomplet** : si les 60 paires ne sont pas signées, le test est **incomplet**. On ne remplace
  pas les signatures manquantes, on ne réduit pas l'échantillon sans le déclarer. Le noyau est
  décrit, pas testé.

### 5.7 La puissance, dite avant

Avec 20 paires par groupe, le design ne détecte que des effets **standardisés** `|β|` de l'ordre de
**0,59** (α = 0,05, 80 %, régression simple) ; avec 40 paires (G2+G3), environ **0,43**. C'est
grossier : le design ne peut pas « prouver » un effet de 0,04 comme celui qui a survécu à Holm en
4A. Il peut **borner** les effets plus petits par l'IC et le ROPE, et c'est précisément ce qu'on lui
demande : **trancher le grossier**, pas le fin.

## 6. Le pré-enregistrement

Le pré-enregistrement est le JSON lui-même ([`protocole-date.json`](protocole-date.json)) ; cette
section en est la lecture.

| élément | valeur |
|---|---|
| date du gel | **2026-11-15** |
| graine | **20261115** |
| statut | **gelé avant toute lecture des 14 atomes des 26 textes non signés** |
| aveugle | la sélection n'utilise que `annee`, `tradition_label`, `language_original`, `author`, `title` ; jamais `d_sig`, `d_lex`, `cos` |
| source | `sources_manifest.json` + `sources_coverage.json` ; seules les sources `ok = true` |
| paires | **60** (20 G1, 20 G2, 20 G3), **59 textes**, paires uniques |
| exclusions | les 5 sources non acquises ; même texte/titre/travail ; paires déjà dans un autre groupe |
| arrêt | aucun arrêt anticipé, aucun ajout, aucun remplacement après lecture des résultats |
| déviations | toute déviation est écrite dans le JSON de résultats avec SHA-256 et date |
| instrument | `analytic_sigs_v1` **seul** ; les `v14_signature` du graphe v35 sont un autre instrument |
| calibration | re-extraire les 44 œuvres et exiger cos ≥ 0,99 (ou L2 ≤ 0,01) avant tout test |

**Ce que le gel interdit.** Il interdit de remplacer une paire G1 par une paire G2 parce que la
première n'a pas de signature, de réduire les 20 à celles qui sont signées, de changer les quotas
après avoir vu les `d_sig`, ou de mélanger les deux jeux de signatures pour « compléter ». Si les
26 textes ne sont pas signés, le test n'existe pas — et c'est un résultat de faisabilité, pas un
échec du protocole.

## 7. La commande que Panini peut rejouer

Le script est [`../tools/protocole_date.py`](../tools/protocole_date.py). Il lit les artefacts
§334 en lecture seule, vérifie leurs SHA-256, et **refuse d'écrire dans Panini**.

```bash
# 1. Vérifier le manifeste gelé (lecture seule)
python3 tools/protocole_date.py --verifier

# 2. Reconstruire le manifeste, si besoin (écrit reports/protocole-date.json)
python3 tools/protocole_date.py --construire --force \
  --sortie reports/protocole-date.json

# 3. Rejouer le test quand Panini a signé les 26 textes
python3 tools/protocole_date.py --rejouer \
  --signatures /tmp/v14.json \
  --sortie reports/protocole-date-resultats.json

# 3 bis. Variante depuis un autre checkout de Panini
python3 tools/protocole_date.py --rejouer \
  --panini /chemin/vers/Panini \
  --signatures /tmp/v14.json \
  --sortie /tmp/protocole-resultats.json
```

Le fichier de signatures attendu est un JSON de la forme :

```json
{
  "instrument": "V14 — extracteur du commit e10d695e (ou successeur compatible)",
  "commit": "…",
  "signatures": {
    "baudhayana_dharmasutra": {"ÊTRE": 0.12, "DIFFÉRENCE": 0.03, "...": 0.0},
    "...": {"...": 0.0}
  }
}
```

Les 14 clés doivent être exactement celles de la liste ; chaque signature doit sommer à 1 ± 10⁻⁶.
Le script calcule `d_sig`, décrit les 60 paires, puis exécute P1/P2 et le contrôle positif G1
**seulement si les 60 paires sont complètes**. Sinon il écrit `statut: incomplet`, la liste des
paires manquantes et les statistiques descriptives du noyau — sans p-value, pour ne pas faire croire
à un test sur un sous-ensemble choisi par la disponibilité.

**Ce que Panini doit faire, concrètement.** Signer les **26 textes** listés dans
`protocole-date.json` → `a_signer`, avec **le même** extracteur V14 que `analytic_sigs_v1.json`, et
fournir le JSON ci-dessus. Les 26 sources sont toutes acquises (`ok = true`) ; aucune ne demande une
nouvelle acquisition. La calibration sur les 44 œuvres existantes est le garde-fou : si l'extracteur
a dérivé, le test s'arrête.

## 8. Ce qui pourrait rendre ce protocole faux

1. **Les dates sont des estimations.** Le graphe ne porte pas d'incertitude ; les négatifs sont des
   siècles, les modernes vont de 1920 à 2013. Un décalage de 10 ans n'a pas le même sens à −400 et
   à 2000. G1 à ±10 ans est une convention, pas une vérité physique.
2. **La date est celle de la composition, pas de la traduction.** 24/44 œuvres sont anglaises, 19
   de langue inconnue ; les signatures sont calculées sur des traductions du XIXe–XXe siècle. Le
   test d'époque est **biaisé contre** un effet de la date de composition.
3. **L'instrument peut dériver.** Les 44 signatures de `analytic_sigs_v1` et les 57 du graphe v35
   diffèrent (cos 0,42–0,82). Si Panini re-signe avec une version différente, le test mesure la
   version, pas la théorie. La calibration sur les 44 est obligatoire.
4. **G1 n'a qu'une paire déjà signée.** Le contrôle positif de filiation est donc, lui aussi, en
   attente. Si Panini ne signe pas les 19 autres paires G1, on ne peut pas vérifier que
   l'instrument voit la filiation à date fixe — et P1/P2 perdent leur assise.
5. **G3 est surtout anglais.** 12/20 paires sont anglaises et inter-familles ; les 8 autres sont
   intra-famille. La strate « surface contrôlée » est donc surtout la strate anglaise, et la
   conclusion ne se transporte pas aux autres langues.
6. **Les paires ne sont pas indépendantes.** 60 paires, 59 textes, un texte jusqu'à 5 fois. Les
   permutations et le bootstrap sont par texte ; les IC restent fragiles.
7. **La puissance est faible.** Le design détecte |β| ≳ 0,59 (n = 20) ou ≳ 0,43 (n = 40). Un effet
   de 0,04 comme celui de 4A ne serait pas détecté ; il serait seulement **borné**.
8. **`d_topo` est une approximation.** Le plus court chemin non pondéré corrèle à r = 0,943 avec le
   `d_topo` publié ; ce n'est pas la même quantité. La filiation est donc contrôlée par une
   approximation, pas par la distance exacte de Panini.
9. **Le regroupement en familles est une décision de Drave.** `FAMILLES` fusionne les étiquettes qui
   séparent le même texte ou le même auteur ; c'est documenté et vérifiable, mais ce n'est pas la
   taxonomie de Panini. Un autre regroupement changerait les quotas.
10. **Le corpus reste petit et occidental.** 107 sources, 102 acquises, 48 textes dans les paires,
    44 signatures. G1 est surtout axial (Inde, Grèce, Chine, Abraham) ; les modernes sont peu
    nombreux. La conclusion vaudra pour ce corpus, pas pour « les langues ».

## 9. Fichiers et suite

| fichier | rôle |
|---|---|
| [`protocole-date.json`](protocole-date.json) | le manifeste gelé : 60 paires, 59 textes, 26 à signer, protocole, pré-enregistrement, SHA-256 |
| [`../tools/protocole_date.py`](../tools/protocole_date.py) | construit, vérifie et rejoue ; lecture seule de Panini |
| [`note-panini-334.md`](note-panini-334.md) | la note 4A, dont ce protocole est la suite |
| [`rapport-panini-334.md`](rapport-panini-334.md) | la fiche technique 4A (655 paires, 44 signatures, contrôles) |
| [`panini-334.json`](panini-334.json) | les chiffres 4A |
| `../Panini/research/nipada/falsification/pairs334_axes_v1.json` | les 655 paires (SHA-256 dans le JSON) |
| `../Panini/research/nipada/falsification/nipada_v334_graph_v35.json` | le graphe v35, dates, traditions, langues |
| `../Panini/research/nipada/falsification/analytic_sigs_v1.json` | les 44 signatures V14 (instrument de référence) |
| `../Panini/research/nipada/corpus/_cache/sources_manifest.json` | les 107 sources |
| `../Panini/research/nipada/corpus/_cache/sources_coverage.json` | les 102/107 acquisitions |

**La suite, en une phrase.** Envoyer à Panini le manifeste et la commande ; demander les **26
signatures** avec le même extracteur V14 ; rejouer ; puis reprendre la note 4A avec un résultat qui,
cette fois, sépare la date de la filiation et de la surface — ou qui dit, avec un IC et un ROPE, que
l'effet est trop petit pour ce corpus.
