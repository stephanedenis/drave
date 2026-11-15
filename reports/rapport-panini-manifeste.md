# W4 — Panini : le manifeste des 26 signatures V14 et le rejeu disponible

> **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **L** · **Tâche** : **W4** (J3 matin,
> la part du pilote) · **Date** : 2026-11-15 · **HEAD mesuré** : `be3f41ad` · **Verdict** :
> ✅ **le manifeste est prêt et envoyable** ; ❌ **le rejeu n'est pas un test** — **27/60** paires
> calculées, **33** manquantes, calibration **42/44**, **3** sources sous 300 mots, **5** groupes de
> doublons parmi les 26. **Aucune p-value de H0 n'est écrite.**
>
> **JSON** : [`panini-manifeste.json`](panini-manifeste.json) · **Commande Panini** :
> [`../tools/panini_signatures_26.py`](../tools/panini_signatures_26.py) · **Rejeu** :
> [`../tools/protocole_date.py`](../tools/protocole_date.py) · **Manifeste B1** :
> [`protocole-date.json`](protocole-date.json).

**En trois lignes.** (1) Les **26** textes du protocole B1 qui n'ont pas de signature
`analytic_sigs_v1` sont listés, avec leur fichier source, leur SHA-256, leurs mots et les paires
qu'ils servent ; la commande que Panini doit lancer et le format attendu sont ci-dessous. (2) Sur
les **60** paires, **27** ont leurs deux signatures (1 G1, 14 G2, 12 G3) : on les décrit, on ne
les teste pas ; les **33** autres sont nommées. (3) Le contrôle négatif des dates passe sur G2 mais
**sort du nul sur G3** (p_perm 0,001, tiré par une paire dont l'œuvre n'est pas calibrée), le
contrôle des signatures montre que l'instrument voit la **famille** sur G2 mais pas la date, et la
**calibration échoue sur 2 des 44 œuvres** : le test est **bloqué**, pas « non significatif ».

**Ce que cette fiche est, et n'est pas.**

- **Est** : le **manifeste** à envoyer (26 textes, commande, format, calibration), le **rejeu
  descriptif** de ce qui est signé, les **contrôles négatifs** exécutables, et ce qui bloque.
- **N'est pas** : une mesure de H0. Aucun `β_date`, aucun `p` de test, aucun `R²` de test n'est
  publié : les 27 paires sont un noyau **choisi par la disponibilité**, ce que le protocole B1
  interdit de traiter comme l'échantillon. Les `p_perm` des contrôles sont des **p de pipeline**,
  pas des p de H0.
- **Ne modifie rien chez Panini** : les sept artefacts §334 sont lus en lecture seule, leurs
  SHA-256 sont vérifiés (`python3 tools/protocole_date.py --verifier` → OK), et le script Panini
  refuse d'écrire dans son arborescence. Le statut `git` des dossiers lus est identique avant et
  après (`panini_lecture_seule.identique = true` dans le JSON).

## 1. Le manifeste : 26 textes, dont un seul vient des 655 paires

Le protocole B1 ([`rapport-protocole-date.md`](rapport-protocole-date.md)) porte sur **59 textes**
et **60 paires**. **33** textes ont déjà une signature dans `analytic_sigs_v1.json` ; **26** n'en
ont pas. C'est ce lot qui est demandé.

**Une précision qui évite un malentendu.** Les 26 ne sont pas « 26 œuvres du §334 sans signature »
au sens des 655 paires : un seul des 26, `zadeh_1965`, appartient aux **48 textes** des 655 paires.
Les 25 autres sont des textes du **manifeste des 60 paires** qui ne figurent pas dans les 655
paires. Les **3** autres textes des 655 paires sans signature (`an7_64_kodhana`,
`aristotle_de_anima`, `brahma_sutra_badarayana`) sont **hors des 60 paires** et leurs sources ne
sont **pas acquises** : le manifeste ne les demande pas. Compléter le §334 lui-même demanderait
d'abord ces acquisitions.

### 1.1 Les 26 textes à signer

`mots` = mots du fichier source ; `usage` = nombre de paires du protocole qui utilisent le texte ;
`note` = état particulier. Les 26 sources existent toutes, et sont toutes `ok = true` dans le
manifeste §334.

| # | texte | année | langue | famille | mots | usage | paires | note |
|---:|---|---:|---|---|---:|---:|---|---|
| 01 | `apastamba_grhya_sutra` | -400 | san | INDIAN | 770 | 1 | `G1-05` | doublon de `hiranyakesi_grhya_sutra` |
| 02 | `baudhayana_dharmasutra` | -400 | san | INDIAN | 626 | 3 | `G1-01`, `G3-18`, `G3-19` | doublon de `vasistha_dharmasutra` |
| 03 | `brihadaranyaka_upanishad` | -700 | san | INDIAN | 596 | 3 | `G1-18`, `G2-16`, `G3-19` |  |
| 04 | `burnet_early_greek_philosophy` | 1930 | en | GRECO | 79972 | 1 | `G1-14` |  |
| 05 | `chandogya_upanishad` | -700 | san | INDIAN | 890 | 3 | `G1-17`, `G2-15`, `G3-18` | doublon de `isa_upanishad` |
| 06 | `daodejing` | -350 | lzh | CHINESE | 788 | 4 | `G1-07`, `G1-08`, `G2-20`, `G3-20` | signature via `qiwulun` |
| 07 | `epicurus_letters` | -300 | grc | GRECO | 84 | 2 | `G1-09`, `G1-10` | **84 mots** ; graphe v35 |
| 08 | `hiranyakesi_grhya_sutra` | -400 | san | INDIAN | 770 | 1 | `G1-03` | doublon de `apastamba_grhya_sutra` |
| 09 | `holbach_systeme_en` | 1770 | eng | EUROPE_MODERN | 123805 | 1 | `G3-06` | graphe v35 |
| 10 | `hume_dialogues_nhr` | 1779 | eng | EUROPE_MODERN | 39012 | 1 | `G3-07` | graphe v35 |
| 11 | `ingersoll_works` | 1879 | eng | EUROPE_MODERN | 98782 | 1 | `G1-16` | graphe v35 |
| 12 | `isa_upanishad` | -500 | san | INDIAN | 890 | 3 | `G2-15`, `G2-16`, `G2-17` | doublon de `chandogya_upanishad` |
| 13 | `liji` | -300 | lzh | CHINESE | 680 | 1 | `G2-20` |  |
| 14 | `lucretius_drn` | -55 | eng | GRECO | 1555 | 1 | `G3-06` | graphe v35 |
| 15 | `mandukya_upanishad` | -300 | san | INDIAN | 1343 | 4 | `G1-11`, `G1-12`, `G1-13`, `G2-17` |  |
| 16 | `miller_1956` | 1956 | eng | COGNITIVE_SCIENCE | 8883 | 1 | `G1-15` | graphe v35 |
| 17 | `paraskara_grhya_sutra` | -400 | san | INDIAN | 848 | 1 | `G1-04` | doublon de `sankhayana_grhya_sutra` |
| 18 | `plato_crito` | -399 | grc | GRECO | 5398 | 2 | `G1-01`, `G1-04` |  |
| 19 | `plato_euthyphro_jowett` | -399 | grc | GRECO | 12242 | 2 | `G1-02`, `G1-05` | graphe v35 |
| 20 | `sankhayana_grhya_sutra` | -400 | san | INDIAN | 848 | 1 | `G1-06` | doublon de `paraskara_grhya_sutra` |
| 21 | `sextus_pyrrho` | 190 | grc | GRECO | 42 | 3 | `G3-13`, `G3-14`, `G3-15` | **42 mots** ; graphe v35 |
| 22 | `vasistha_dharmasutra` | -400 | san | INDIAN | 626 | 1 | `G1-02` | doublon de `baudhayana_dharmasutra` |
| 23 | `xiaojing` | -300 | lzh | CHINESE | 908 | 2 | `G1-13`, `G2-19` |  |
| 24 | `yueji` | -200 | lzh | CHINESE | 1166 | 4 | `G1-19`, `G2-18`, `G2-19`, `G3-20` |  |
| 25 | `zadeh_1965` | 1965 | eng | FORMAL_LOGIC | 278 | 1 | `G1-15` | **278 mots** ; dans les 655 ; graphe v35 |
| 26 | `zhuangzi` | -300 | lzh | CHINESE | 788 | 1 | `G2-18` | signature via `qiwulun` |

### 1.2 Trois sources courtes, cinq doublons, vingt vecteurs nouveaux

- **3/26 sources sont sous le plancher de 300 mots** que `research/scripts/loi_analytique.py`
  applique pour produire `analytic_sigs_v1` : `epicurus_letters` (**84**), `sextus_pyrrho`
  (**42**), `zadeh_1965` (**278**). L'extracteur `sign_analytic` produit quand même un vecteur,
  mais ces trois signatures sont **hors du support des 44 références** : elles ne peuvent pas être
  calibrées. **6 des 33 paires manquantes** en dépendent : `G1-09`, `G1-10`, `G1-15`, `G3-13`,
  `G3-14`, `G3-15`.
- **5 groupes de sources byte-identiques parmi les 26** (10 textes) : `apastamba`/`hiranyakesi`,
  `baudhayana`/`vasistha`, `chandogya`/`isa`, `daodejing`/`zhuangzi`, `paraskara`/`sankhayana`.
  Signer les 26 donnera donc **21 vecteurs distincts**, pas 26. Mieux : `daodejing` et `zhuangzi`
  sont byte-identiques à `qiwulun`, **déjà signé** ; leur signature est donc déjà connue. Il reste
  **20 vecteurs nouveaux distincts** (dont 3 courts). Le manifeste demande quand même les 26 pour
  la traçabilité ; Panini peut les signer tous, le doublon sera vérifiable.
- **6 groupes de doublons parmi les 59 textes** : les 5 précédents plus `plato_gorgias` /
  `plato_gorgias_jowett` (déjà signés tous les deux, signature identique). Ce dernier touche
  **3 paires calculées** : `G2-01`, `G2-07`, `G3-16`.

## 2. La commande exacte et le format attendu

### 2.1 Ce que Panini lance

Le script est [`../tools/panini_signatures_26.py`](../tools/panini_signatures_26.py). Il fait deux
choses dans le **même** passage : (1) il re-extrait les **44** signatures de référence et vérifie
`cos ≥ 0,99` ou `L2 ≤ 0,01` ; (2) il signe les **26** textes et vérifie les 14 clés et la somme 1.
Il n'écrit **jamais** dans Panini : `--sortie` doit être hors de l'arborescence.

```bash
cd /chemin/vers/Panini/research
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  /chemin/vers/Qtrinet/tools/panini_signatures_26.py \
  --manifeste /chemin/vers/Qtrinet/reports/panini-manifeste.json \
  --sortie /tmp/panini-v14-26.json
```

- Le **venv de Panini** (`research/.venv`) est celui qui porte `nltk` et WordNet ; sans lui,
  l'extracteur ne démarre pas.
- La commande écrit `/tmp/panini-v14-26.json`. **C'est ce fichier que Panini renvoie** (ou dépose
  dans un dossier partagé) : il contient la calibration, les 26 signatures et les sources.
- Codes de sortie : **0** = calibration 44/44 et 26 signatures ; **2** = calibration incomplète
  (le test ne doit pas être lancé) ; **3** = source absente ou signature invalide.
- **Garde-fou de calibration.** Si la calibration n'est pas 44/44, le script met les 26 signatures
  dans `nouvelles` mais **ne les livre pas** dans `signatures` : le fichier ne contient alors que
  les 44 références, et le rejeu B1 reste `incomplet` (27/60) au lieu de tester sur un instrument
  non calibré. C'est volontaire.

### 2.2 Le format

Le fichier est un JSON UTF-8. Le rejeu B1 lit la clé `signatures` ; les autres clés sont le
diagnostic.

Exemple réel, avec une œuvre **déjà signée** (`2_esdras`, somme 1) ; les 26 doivent
suivre ce format :

```json
{
  "instrument": "V14 — sign_analytic (nipada.signing.analytical_projection), 10 000 premiers mots",
  "commit": "9b80c323…",
  "calibration": {"n": 44, "ok": 44, "fails": [], "seuil": {"cos": 0.99, "l2": 0.01}},
  "calibration_ok": true,
  "signatures": {
    "2_esdras": {
      "ÊTRE": 0.07446500282604852, "DIFFÉRENCE": 0.013816044014481109,
      "RAPPORT": 0.10099345547363615, "ORIENTATION": 0.005331763602619648,
      "SUJET": 0.14124697298283334, "TEMPS": 0.05189835957545314,
      "MODALITÉ": 0.02705634807902917, "NOMBRE": 0.14932406971800052,
      "ESPACE": 0.04847053574653187, "OPÉRATION": 0.06701372487945408,
      "FONCTION": 0.12163933372805281, "STRUCTURE": 0.14742169250272855,
      "SYMÉTRIE": 0.0006717195879862289, "ÉQUATION": 0.050650977283144785
    }
  },
  "nouvelles": {"…": "les 26 signatures, même format"},
  "sources": {"…": {"fichier": "nipada/corpus/_cache/sources/….txt", "sha256": "…", "mots": 770, "seuil_300": true}},
  "avertissements": []
}
```

Les contraintes sont celles de `tools/protocole_date.py` : **les 14 clés exactement**,
`ÊTRE, DIFFÉRENCE, RAPPORT, ORIENTATION, SUJET, TEMPS, MODALITÉ, NOMBRE, ESPACE, OPÉRATION,
FONCTION, STRUCTURE, SYMÉTRIE, ÉQUATION`, des flottants positifs, **somme = 1 ± 10⁻⁶**. Le
`signatures` du fichier complet contient les **59** signatures (44 de référence + 26 nouvelles) ;
les 26 seules sont aussi dans `nouvelles`. Ne jamais mélanger avec les `v14_signature` du graphe
v35 (instrument différent, cosinus 0,42–0,82 sur les 11 œuvres communes).

### 2.3 Le rejeu, côté pilote

Quand — et seulement quand — `calibration_ok` vaut `true`, le pilote lance :

```bash
python3 tools/protocole_date.py --rejouer \
  --signatures /tmp/panini-v14-26.json \
  --sortie reports/protocole-date-resultats.json
```

Le script B1 vérifie les SHA-256 des sept artefacts, calcule les 60 paires, puis P1/P2 et le
contrôle positif G1. Si le fichier ne contient que 44 signatures (calibration en échec), il écrit
`statut: incomplet` et **aucune p-value** — c'est le comportement voulu.

## 3. Le rejeu disponible : 27 paires, pas 60

Sur les 60 paires, **27** ont leurs deux signatures dans `analytic_sigs_v1` : **1 G1, 14 G2, 12 G3**.
Les **33** autres sont listées dans le JSON ; les voici par groupe :

- **G1** : `G1-01` à `G1-19` (19 paires) ; seule `G1-20` (`book_of_enoch` × `sibylline_oracles`) est calculable.
- **G2** : `G2-15` à `G2-20` (6 paires).
- **G3** : `G3-06`, `G3-07`, `G3-13`, `G3-14`, `G3-15`, `G3-18`, `G3-19`, `G3-20` (8 paires).

| groupe | paires | calculées | manquantes | `d_sig` moyenne | Δannée moyen | pente date (descriptif) |
|---|---:|---:|---:|---:|---:|---|
| **G1** | 20 | 1 | 19 | 0,0854 | 0 | — (n = 1) |
| **G2** | 20 | 14 | 6 | 0,0662 | 69,6 | **−0,426** (R² 0,251) |
| **G3** | 20 | 12 | 8 | 0,1134 | 1 521,3 | **−0,011** (R² 0,048) |
| **total** | **60** | **27** | **33** | **0,0879** | — | 0,015 (R² 0,088, n = 27) |

**Ce que le noyau disponible est vraiment.** Ce n'est pas un échantillon : c'est exactement ce que
la signature existante couvre. Les 14 paires G2 calculées sont **8 GRECO + 6 ABRAHAMIC** ; les 6
manquantes sont indiennes/chinoises. Les 12 paires G3 calculées sont **10 anglais + 2 grec** ; les
8 manquantes sont 2 anglais, 3 grecs, 2 sanskrits, 1 chinois. G1 n'a **qu'une** paire. Toute
lecture de ces 27 paires est donc une lecture du **biais de disponibilité** — précisément ce que le
protocole B1 interdit de traiter comme le test.

**Aucune p-value de H0.** Les pentes ci-dessus sont descriptives. Les `p_perm` de la section
suivante sont des **contrôles de pipeline** ; ils ne testent pas H0 et ne remplacent pas P1/P2.

## 4. Le contrôle négatif

Le protocole B1 prévoit des contrôles négatifs ; on exécute ceux qui ont un sens sur les 27 paires
disponibles. Les permutations sont **2 000**, graine **20261115**.

| contrôle | n | observé | nul / seuil | lecture |
|---|---:|---|---|---|
| **N2** années permutées **dans chaque famille** (G2) | 14 | β = −0,426 | 95 % [−0,521 ; 0,149] ; `p_perm` 0,252 | la pente observée est **dans** le nul : pas d'effet date détectable sur ce sous-ensemble |
| **N3** années permutées **dans chaque langue** (G3) | 12 | β = −0,0113 | 95 % [−0,0088 ; 0,0292] ; `p_perm` **0,001** | **hors du nul** : signal de sous-ensemble, pas un résultat — voir ci-dessous |
| **N4** signatures permutées (G2) | 14 | `d_sig` 0,0662 | nul 0,1205 ± 0,0138 ; `p_perm` 0,001 | les paires de même famille sont **plus proches** que le hasard : l'instrument voit la famille (positif) ; la pente de date, elle, disparaît (`p_perm` 0,255) |
| **N4** signatures permutées (G3) | 12 | `d_sig` 0,1134 | nul 0,1209 ± 0,0167 ; `p_perm` 0,654 | pas de structure de distance ; pente de date `p_perm` 0,577 |
| **N4** signatures permutées (tout) | 27 | `d_sig` 0,0879 | nul 0,1208 ± 0,0093 ; `p_perm` 0,001 | le noyau est plus proche que le hasard, mais la pente de date ne survit pas (`p_perm` 0,312) |
| **N5** colonnes d'atomes permutées | — | — | — | **contrôle vide** : une permutation commune des 14 colonnes laisse `‖s_a − s_b‖₂` invariante ; il ne peut rien détruire. À remplacer par une permutation des étiquettes par signature, ou par N4 |
| **N6** doublons de sources exclus | 3 paires | G2 β = −0,330 (n = 12) ; G3 β = −0,027 (n = 11) | — | `G2-01`, `G2-07`, `G3-16` utilisent `plato_gorgias`, byte-identique à `plato_gorgias_jowett` (même signature) ; le signe ne change pas |
| **positif G1** | 1 | `d_sig` 0,0854 | — | **non exécutable** : une seule paire G1 signée ; le contrôle positif de filiation manque |
| **calibration 44** | 44 | **42 OK** | cos ≥ 0,99 **ou** L2 ≤ 0,01 | **échec** : `bengio_2003` (cos 0,9678 ; L2 0,1053), `mengzi` (cos 0,9891 ; L2 0,0500) |

**Le point G3.** Le contrôle N3 sort du nul parce que la paire `G3-08`
(`miller_evidence_prophecy` × `bengio_2003`, Δ = 167 ans, `d_sig` = 0,2306) est à la fois la plus
grande distance et le plus petit écart de date des **10 paires anglaises** du sous-ensemble. C'est
aussi une paire qui utilise `bengio_2003`, **l'une des deux œuvres qui échouent à la calibration**.
Sans elle, la pente devient positive (+0,012) et le `p_perm` reste 0,011 (n = 11) : le signal ne
tient pas à une seule paire, mais il **change de signe** avec une paire et il tient à un
sous-ensemble de 12 paires dont une œuvre n'est pas calibrée. Ce n'est pas un résultat d'époque ;
c'est la démonstration que **le noyau disponible ne doit pas être testé**.

**Le point N5.** Le contrôle « colonnes d'atomes permutées » du protocole B1 est **mathématiquement
vide** pour la distance L2 : si `P` est une permutation des 14 colonnes, `‖P s_a − P s_b‖₂ =
‖s_a − s_b‖₂`. Il ne peut pas départager une distance sémantique d'une distance quelconque. Le
remplacer par une permutation **indépendante par signature** (ce qui détruit la correspondance des
atomes) ou par N4.

**Le point calibration.** C'est le blocage le plus dur. Le protocole B1 exige que les 44 œuvres
soient reproduites avant tout test. Dans notre copie de Panini (`HEAD 9b80c323`, venv
`research/.venv`), **42/44** passent ; `bengio_2003` et `mengzi` échouent. Le test ne peut donc pas
être lancé même si les 26 signatures arrivent : il faudrait que Panini fournisse une calibration
**44/44** (ou explique l'écart : version de l'extracteur, WordNet, source). C'est une question à
poser dans le message, pas un détail.

## 5. Ce qui bloque, et ce qui pourrait rendre faux

1. **Les 26 signatures manquent.** C'est le blocage nominal : 33 paires sur 60 n'ont pas leurs deux
   signatures. Le manifeste et la commande sont le livrable ; le test attend.
2. **La calibration échoue sur 2/44.** `bengio_2003` et `mengzi` ne sont pas reproduits au seuil
   B1. Tant que ce n'est pas résolu, `calibration_ok = false` et le rejeu reste `incomplet`.
3. **3 sources sont sous 300 mots.** `epicurus_letters` (84), `sextus_pyrrho` (42), `zadeh_1965`
   (278) : 6 paires manquantes en dépendent. L'extracteur produira un vecteur, mais hors du support
   des 44 références ; la signature de ces textes est à traiter comme **non calibrée**.
4. **5 groupes de doublons parmi les 26** (10 textes), dont `daodejing`/`zhuangzi` déjà identiques à
   `qiwulun` : 21 vecteurs distincts au mieux, 20 nouveaux. La paire `G2-15` (`chandogya` ×
   `isa_upanishad`) est un couple de jumeaux : elle aura `d_sig = 0`, ce n'est pas une mesure
   d'écart sémantique.
5. **G1 n'a qu'une paire signée.** Le contrôle positif de filiation n'est pas exécutable ; sans lui,
   P1/P2 n'ont pas d'assise. Le protocole l'écrit déjà ; le rejeu le confirme.
6. **Le noyau disponible est biaisé.** 14 G2 = 8 GRECO + 6 ABRAHAMIC ; 12 G3 = 10 anglais + 2 grec ;
   1 G1. Les 33 manquantes sont surtout indiennes, chinoises et grecques. Toute conclusion sur ce
   noyau serait une conclusion sur la disponibilité, pas sur la date.
7. **Le contrôle N5 est vide** tel qu'écrit ; le corriger avant le test final, sinon il donnera
   faussement « le résultat survit » (il sera invariant par construction).
8. **Les dates et les traductions restent les limites de B1** : dates de composition estimées,
   signatures calculées sur des traductions majoritairement anglaises, corpus petit. Le test ne
   pourra rien dire de plus que ce que B1 a déjà écrit.

## 6. Fichiers et suite

| fichier | rôle |
|---|---|
| [`panini-manifeste.json`](panini-manifeste.json) | le manifeste complet : 26 textes, 44 références, commande, format, rejeu, contrôles, calibration |
| [`rapport-panini-manifeste.md`](rapport-panini-manifeste.md) | cette fiche |
| [`../tools/panini_signatures_26.py`](../tools/panini_signatures_26.py) | le script **côté Panini** : calibration 44 + 26 signatures, sortie hors Panini |
| [`../tools/panini_manifeste.py`](../tools/panini_manifeste.py) | construit et vérifie ce JSON, rejoue les contrôles |
| [`../tools/protocole_date.py`](../tools/protocole_date.py) | le rejeu B1 : 60 paires, P1/P2, contrôle positif |
| [`protocole-date.json`](protocole-date.json) | le manifeste gelé B1 (60 paires, 59 textes, 26 à signer) |
| [`rapport-protocole-date.md`](rapport-protocole-date.md) | la fiche B1, dont ce manifeste est la suite |
| [`note-panini-334.md`](note-panini-334.md) · [`rapport-panini-334.md`](rapport-panini-334.md) | la note 4A et la fiche technique du §334 |

**La suite, en une phrase.** Envoyer à Panini le JSON et la commande ; demander le retour de
`/tmp/panini-v14-26.json` avec une calibration **44/44** ; si elle est là, lancer le rejeu B1 sur
les 60 paires ; sinon, publier la calibration en échec et ne pas conclure — le test n'existe pas.

**Ce que W4 laisse à W5/W6.** W5 (restitution v3) ne dépend pas de Panini. W6 (clôture) lira ce
manifeste comme la part « Panini » de la semaine : le livrable est le **manifeste**, pas un
résultat d'époque. La ligne R0.7 / L reste ouverte sur les 26 signatures et sur la calibration.
