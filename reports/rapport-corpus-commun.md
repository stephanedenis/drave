# Corpus commun Panini/NIPADA ↔ Drave — UDHR, article 1

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.2 · **Date** : 2026-11-07
> **Verdict** : ✅ **le corpus est construit et vérifié** — **21 textes** (20 langues stratifiées + le
> français pivot), **5 familles**, **10 écritures**, **42 phrases**, **3 603 caractères**. Les **21**
> paires Panini ↔ Drave sont **identiques après normalisation** ; **418 paires exactes** sur **438**
> appariables (**95,4 %**). **20 écarts de surface** sont **exclus, pas corrigés**. Les **8 contrôles**
> (**6 rejets** attendus + **2 témoins** d'acceptation) sont **conformes** (8/8).
> **Dispositif** : lecture seule de `../Panini/research/data/udhr_corpus.json` (HEAD du dépôt
> `e10d695`, 2026-10-25 ; fichier **non suivi par git**, SHA-256 `531bc75c…`, vérifié avant et
> après) ; `data/udhr/articles_propres.jsonl`, `langues.jsonl`, `genealogie.json` (HEAD
> `9c7f71dc`, 2026-11-07) ; outil `../tools/corpus_commun.py` ;
> JSON [`corpus-commun.json`](corpus-commun.json). Le corpus lui-même vit dans
> `work/corpus-commun/`, **non versionné** (`.gitignore` : `work/`).
> **Aucune écriture dans Panini** : le script vérifie l'empreinte de la source avant et après.
> Les artefacts du corpus versionnés sont cette fiche, son JSON et l'outil ; l'état, la roadmap et
> le journal sont mis à jour dans le même cycle.

## 1. La question, et ce que ce corpus est

J2.2 demande un **échantillon de 10 à 50 textes présent des deux côtés** (Panini/NIPADA et Drave),
normalisé en **UTF-8**, **une phrase par ligne**, avec des **métadonnées de langue et d'époque**.

Le seul corpus où les deux côtés ont **déjà le même texte**, et non deux traductions différentes,
est l'**article 1 de la Déclaration universelle des droits de l'homme** (DUDH, 1948) :

- Panini/NIPADA : `../Panini/research/data/udhr_corpus.json`, format `udhr-v2.0-xml`, **532 langues**,
  article 1, source déclarée `eric-muller/udhr` ;
- Drave : `data/udhr/articles_propres.jsonl`, **456 langues**, article 1, extrait du même fonds
  Unicode UDHR ; `langues.jsonl` et `genealogie.json` apportent le code ISO, l'écriture, la famille
  et la branche Glottolog.

**Ce que ce corpus est** : un **corpus d'intersection exacte**, contrôlé, reproductible, avec des
identifiants communs, des métadonnées de langue, de famille et d'époque, et une phrase par ligne.

**Ce que ce corpus n'est pas** :

- **pas un corpus de genres ni d'époques** : toutes les entrées sont des déclarations de 1948 ;
- **pas le corpus des 30 articles** : Panini ne publie que l'article 1 ; les 30 articles de Drave
  ne sont donc pas dans l'intersection ;
- **pas un échantillon aléatoire** : il est stratifié et choisi pour l'égalité exacte et la
  diversité des écritures ;
- **pas une preuve atome ↔ niveau** : il fournit le texte commun, pas la mesure ; le protocole de
  J2.1 exigera en plus des genres et des époques, donc un second corpus.

## 2. Sources et intersection — les chiffres

### 2.1 Les deux sources

| côté | fichier | format | langues | HEAD | date | SHA-256 |
|---|---|---|---|---|---|---|
| Panini/NIPADA | `../Panini/research/data/udhr_corpus.json` | JSON `udhr-v2.0-xml` | **532** | `e10d695` | 2026-10-25 | `531bc75c…` (fichier non suivi) |
| Drave | `data/udhr/articles_propres.jsonl` | JSONL | **456** | `9c7f71dc` | 2026-11-07 | `7ccac9c3…` |
| Drave | `data/udhr/langues.jsonl` | JSONL | 456 | `9c7f71dc` | 2026-11-07 | `12eee362…` |
| Drave | `data/udhr/genealogie.json` | JSON | 441 | `9c7f71dc` | 2026-11-07 | `3d907676…` |

Les **441** entrées de `genealogie.json` couvrent 441 des 456 fichiers Drave ; les **21** textes
retenus ont tous une branche Glottolog. Les **15** fichiers sans généalogie sont exactement les
**15** communs sans article 1.

**Le fichier Panini n'est pas suivi par git.** `git ls-files` le refuse, et une grande partie des
données de `Panini/research` est dans le même cas (le dépôt porte des centaines de milliers de
fichiers non suivis ; voir [`rapport-inventaire-panini.md`](rapport-inventaire-panini.md) § 1.2).
Le HEAD `e10d695` est donc celui du **dépôt**, pas une version du fichier :
le contrôle de non-modification est l'**empreinte SHA-256 avant/après** (`531bc75c…`), pas un
`git diff`. C'est le contrôle qui fait foi ici.

La source déclarée est la même des deux côtés (`eric-muller/udhr`). Elle **n'est pourtant pas
byte-identique** : après NFC et compression des espaces, **20 langues** gardent un écart de surface.
C'est un résultat en soi : les deux jeux ne sont pas deux copies du même fichier, mais deux
extractions ou deux révisions du même fonds.

### 2.2 Le recouvrement, étape par étape

| étape | n | taux | lecture |
|---|---:|---:|---|
| langues Panini | 532 | — | le fonds Panini |
| langues Drave | 456 | — | le fonds Drave |
| fichiers communs | **453** | **99,3 %** de Drave ; **85,2 %** de Panini | l'intersection des identifiants de fichier |
| article 1 côté Drave | 440 | 96,5 % de Drave | 16 fichiers Drave n'ont pas d'article 1 |
| appariables article 1 | **438** | 96,7 % de l'intersection | 15 communs sans article 1, 2 Drave hors Panini |
| **paires exactes** | **418** | **95,4 %** des appariables ; **78,6 %** de Panini | le corpus disponible |
| écarts de surface | 20 | 4,6 % des appariables | exclus, pas corrigés |
| sans article 1 (communs) | 15 | — | voir la liste ci-dessous |
| sans fichier Drave | 79 | — | le complément Panini |
| article 1 Drave hors Panini | 2 | — | `udhr_012.xml`, `udhr_prq.xml` |

**Les 20 écarts de surface exclus.** Ce ne sont pas des erreurs de lecture : ce sont des variantes
d'orthographe, de ponctuation ou de diacritiques. Cinq exemples :

| langue | Panini | Drave | nature |
|---|---|---|---|
| `ady` | `Цӏыф` | `ЦIыф` | palochka `ӏ` contre `I` latin |
| `cmn_hans` | `自由，在` | `自由,在` | virgule pleine largeur contre virgule ASCII |
| `hrv` | `rađaju` | `raćaju` | `đ` contre `ć` (variante orthographique) |
| `hau_NG` | `’yan-adam` | `‘yan-adam` | apostrophe courbe fermante contre ouvante |
| `yor` | `ẹ̀tọ́` | `è̩tó̩` | diacritiques combinants dans un ordre différent |

Les 20 identifiants sont dans le JSON (`intersection.listes.ecarts_surface`). **On ne les corrige
pas** : corriger une source pour la faire ressembler à l'autre serait fabriquer l'accord. Ils sont
exclus, et le biais qui en résulte est nommé au § 6.

**Les 15 communs sans article 1** : `bin`, `csw`, `iii`, `ike`, `kha`, `khk_mong`, `lia`, `lus`,
`nym`, `ojb`, `qxu`, `taj`, `tgl_tglg`, `tzm_tfng`, `umb`. **Les 2 Drave hors Panini** :
`udhr_012.xml`, `udhr_prq.xml`. **Les 79 sans fichier Drave** se répartissent en **40 variantes
numériques** (`udhr_021.xml` … `udhr_072.xml`) et **39 codes absents** (`udhr_aar.xml`,
`udhr_ayo.xml`, `udhr_cmn_hans_beijing.xml`, …) ; la liste complète est dans le JSON.

### 2.3 Les familles du pool exact

Le pool exact de **418** paires couvre **51 étiquettes de famille** (dont **10 `(inconnue)`**).
Les cinq familles retenues sont **parmi les six plus représentées** ; le **turcique** (17 paires)
est écarté malgré un compte supérieur à l'**afro-asiatique** (12), parce qu'il n'ajoute aucune
écriture nouvelle (cyrillique, arabe et latin sont déjà couverts) :

| famille | paires exactes | part du pool | textes retenus |
|---|---:|---:|---:|
| Indo-European | 120 | 28,7 % | 5 |
| Atlantic-Congo | 81 | 19,4 % | 4 |
| Austronesian | 37 | 8,9 % | 4 |
| Sino-Tibetan | 17 | 4,1 % | 4 |
| Turkic | 17 | 4,1 % | 0 (écarté : écritures déjà couvertes) |
| Afro-Asiatic | 12 | 2,9 % | 4 |
| 45 autres étiquettes | 134 | 32,1 % | 0 |
| **total** | **418** | **100 %** | **21** |

Les cinq familles retenues couvrent **267/418 = 63,9 %** du pool exact ; le turcique (**17**,
4,1 %) et les **45 autres** étiquettes (**134**, 32,1 %, dont les 10 `(inconnue)`) ne sont pas
représentés. Ce n'est donc **pas** un échantillon proportionnel : les trois petites familles
retenues sont **sur-représentées** (19,0 % chacune contre 8,9 % pour l'austronésien, 4,1 % pour le
sino-tibétain et 2,9 % pour l'afro-asiatique), l'**atlantic-congo** est à parité (19,0 % contre
19,4 %) et l'**indo-européen** est **sous-représenté** (23,8 % contre 28,7 %). C'est un choix
assumé pour la diversité des écritures, pas une estimation.

## 3. L'échantillon — 21 textes, 5 familles, 10 écritures

**Critères de sélection** :

1. présent des deux côtés, avec le **même identifiant** `udhr_<clé>` ↔ `udhr_<clé>.xml` ;
2. article 1 **identique** après NFC et compression des espaces — aucune correction manuelle ;
3. **5 familles** glottolog × **4 langues**, parmi les six plus représentées du pool exact, avec la
   diversité des écritures comme arbitrage (le turcique, 17 paires, est écarté) ;
4. **écritures distinctes** quand c'est possible (latin, devanagari, cyrillique, grec, adlam,
   arabe, birman, han, éthiopien, hébreu) ;
5. le **français** ajouté **hors strate** comme pivot de Drave (la langue de référence du dépôt).

| id | langue | écriture | famille | branche (feuille) | rôle | phrases | caractères |
|---|---|---|---|---:|---|---:|---:|
| `udhr_eng` | English | Latn | Indo-European | `macr1271` | strate | 2 | 170 |
| `udhr_hin` | Hindi | Deva | Indo-European | `hind1270` | strate | 2 | 189 |
| `udhr_bel` | Belarusan | Cyrl | Indo-European | `east1426` | strate | 2 | 154 |
| `udhr_ell_monotonic` | Greek (monotonic) | Grek | Indo-European | `nucl1783` | strate | 2 | 194 |
| `udhr_kin` | Rwanda | Latn | Atlantic-Congo | `rwan1241` | strate | 2 | 123 |
| `udhr_ewe` | Éwé | Latn | Atlantic-Congo | `ewei1234` | strate | 2 | 165 |
| `udhr_ibo` | Igbo | Latn | Atlantic-Congo | `cent2417` | strate | 2 | 157 |
| `udhr_fuf_adlm` | Pular (Adlam) | Adlm | Atlantic-Congo | `fula1264` | strate | 2 | 154 |
| `udhr_ind` | Indonesian | Latn | Austronesian | `stan1327` | strate | 2 | 181 |
| `udhr_tgl` | Tagalog | Latn | Austronesian | `taga1269` | strate | 2 | 192 |
| `udhr_mly_arab` | Malay (Arabic) | Arab | Austronesian | `sing1270` | strate | 2 | 161 |
| `udhr_jav` | Javanese (Latin) | Latn | Austronesian | `glob1245` | strate | 2 | 192 |
| `udhr_mya` | Burmese | Mymr | Sino-Tibetan | `nucl1811` | strate | 2 | 262 |
| `udhr_cmn_hant` | Chinese, Mandarin (Traditional) | Hant | Sino-Tibetan | `mand1471` | strate | 2 | 43 |
| `udhr_cnh` | Chin, Haka | Latn | Sino-Tibetan | `laic1236` | strate | 2 | 292 |
| `udhr_ctd` | Chin, Tedim | Latn | Sino-Tibetan | `thad1239` | strate | 2 | 221 |
| `udhr_arb` | Arabic, Standard | Arab | Afro-Asiatic | `arab1395` | strate | 2 | 116 |
| `udhr_amh` | Amharic | Ethi | Afro-Asiatic | `amha1244` | strate | 2 | 103 |
| `udhr_heb` | Hebrew | Hebr | Afro-Asiatic | `hebr1246` | strate | 2 | 126 |
| `udhr_hau_NE` | Hausa (Niger) | Latn | Afro-Asiatic | `west2718` | strate | 2 | 222 |
| `udhr_fra` | French | Latn | Indo-European | `glob1239` | pivot_fr | 2 | 186 |

**Répartition** : 20 strates (5 × 4) + 1 pivot ; **10 écritures** — latin 11 textes, arabe 2,
adlam 1, cyrillique 1, devanagari 1, éthiopien 1, grec 1, han 1, hébreu 1, birman 1. Les **42
phrases** viennent de l'article 1 : **2 phrases par texte** dans les 21 cas. Total : **3 603
caractères**, **566 tokens séparés par des espaces** (dont 2 pour le chinois et 2 pour l'amharique,
qui ne séparent pas les mots par des espaces — voir § 6).

## 4. Normalisation — ce qui est fait, et ce qui ne l'est pas

**Fait** :

- **UTF-8 sans BOM**, fins de ligne **LF**, une **phrase par ligne**, **aucune ligne vide** ;
- **NFC** (Unicode), compression de toute suite d'espaces en une espace ;
- remplacement de la séquence éthiopienne `U+1362 U+1361` (`።፡`) par `U+1362` + espace, pour que
  la deuxième phrase d'un texte amharique ne commence pas par un espace-mot ;
- segmentation après `. ! ? … । ။ ؟ ۔ ። ፧` suivi d'une espace, et après `。！？` même sans espace.

**Non fait** (et c'est volontaire) :

- pas de **casse** (pas de `lower()`), pas de suppression des **diacritiques**, pas de
  translittération, pas de normalisation de la ponctuation (hors l'espace-mot éthiopien ci-dessus) ;
- pas de **traduction** : les deux côtés lisent le même texte, pas deux traductions ;
- pas de **correction** des 20 écarts de surface : ils sont exclus ;
- pas de **tokenisation** : `nb_mots_ws` est un comptage sur les espaces, pas un découpage
  linguistique.

**Exemple** (`udhr_eng.txt`) :

```text
All human beings are born free and equal in dignity and rights.
They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.
```

**Exemple de script sans espace** (`udhr_cmn_hant.txt`, deux lignes, `。` final) :

```text
人人生而自由，在尊嚴和權利上一律平等。
他們賦有理性和良心，並應以兄弟關係的精神相對待。
```

### 4.1 Les fichiers produits

| fichier local (non versionné) | contenu |
|---|---|
| `textes/<id>.txt` | le texte, une phrase par ligne, UTF-8, LF |
| `corpus.jsonl` | une phrase par ligne + `id`, `iso3`, `langue`, `script`, `famille`, `genre`, `epoque`, `role`, `phrase_index`, `sha256_phrase` |
| `metadata.tsv` | une ligne par texte : `id`, `iso3`, `langue`, `script`, `famille`, `branche_feuille`, `genre`, `epoque`, `role`, `nb_phrases`, `nb_mots_ws`, `nb_caracteres`, `sha256_fichier` |
| `index.json` | manifeste : sources, sélection, normalisation, contrôles, textes |
| `sources.sha256` | empreintes des trois sources Drave + de la source Panini + de l'outil |
| `controle-negatif.json` | les huit tests de contrôle (6 rejets + 2 témoins) |

Le corpus est régénérable par `python3 tools/corpus_commun.py --tout`. `--verifier` reconstruit
dans un dossier temporaire et compare **octet par octet** ; `--controle-negatif` rejoue les tests.

## 5. Contrôles — ce qui a été vérifié, et comment

| contrôle | attendu | obtenu |
|---|---|---|
| égalité exacte Panini ↔ Drave, 21 textes | 21/21 | **21/21** |
| familles attendues (5) | 5/5 | **5/5** |
| UTF-8 strict, sans BOM, LF | 21/21 | **21/21** |
| une phrase par ligne, aucune ligne vide | 21/21 | **21/21** |
| reconstruction `textes/*.txt` == `corpus.jsonl` | 21/21 | **21/21** |
| déterminisme (`--verifier`, reconstruction octet par octet) | identique | **identique** |
| source Panini inchangée (SHA-256 avant/après) | `531bc75c…` | **`531bc75c…`** |
| contrôles (6 rejets + 2 témoins) | 8/8 conformes | **8/8** |

### 5.1 Les contrôles, test par test

| test | attendu | obtenu | ce qu'il vérifie |
|---|---|---|---|
| `temoin_paire_correcte` | acceptation | ✅ acceptation | la paire correcte passe |
| `panini_altere` | rejet | ✅ rejet | un caractère changé côté Panini casse l'égalité |
| `drave_altere` | rejet | ✅ rejet | un caractère changé côté Drave casse l'égalité |
| `appariement_croise` | rejet | ✅ rejet | l'anglais contre le français est refusé |
| `phrase_supprimee` | rejet | ✅ rejet | 1 phrase au lieu de 2 : refus |
| `ligne_vide` | rejet | ✅ rejet | 3 lignes dont une vide : refus |
| `empreinte_fausse` | rejet | ✅ rejet | une empreinte qui n'est pas celle du fichier est refusée |
| `pivot_francais_coherent` | acceptation | ✅ acceptation | le pivot est bien `Indo-European` et `pivot_fr` |

Le dispositif n'est donc pas un simple « relancer le script » : il **altère** le texte, **croise**
les langues, **supprime** une phrase, **vide** une ligne et **falsifie** une empreinte — six rejets
attendus — plus deux témoins qui doivent **accepter** (la paire correcte et la cohérence du pivot).
Les huit tests sont dans `work/corpus-commun/controle-negatif.json`.

### 5.2 Ce qui pourrait rendre ce corpus faux

- **Le filtre d'égalité exacte** exclut 20 langues qui diffèrent par une apostrophe, une cédille,
  une virgule ou une lettre. Si ces variantes sont systématiques dans une famille ou une écriture, l'échantillon
  est biaisé vers les orthographes « propres ». C'est le premier risque, et il est mesurable :
  comparer les 20 exclus aux 418 retenus (famille, écriture, longueur) est un contrôle à faire.
- **La sélection n'est pas aléatoire** : 5 familles sur 51, 10 écritures sur plusieurs dizaines,
  21 textes sur 418 paires exactes. Toute conclusion sur « les langues » ou « les familles » doit
  être stratifiée, pas généralisée.
- **L'article 1 est court** : 42 phrases, 3 603 caractères. Un taux de retrieval ou une corrélation
  au niveau du texte aura une variance élevée ; le split-half de J2.1 (10 textes / 10) est
  probablement trop petit ici.
- **Une seule époque, un seul genre** : `epoque = 1948` est la date d'adoption, pas la date de
  chaque traduction ; le genre est `declaration` pour les 21. Aucun contrôle de l'époque n'est
  possible dans ce corpus.
- **`nb_mots_ws` n'est pas une tokenisation** : 1 par phrase pour le chinois et l'amharique, alors
  que la phrase contient plusieurs mots. Pour ces deux langues, utiliser `nb_caracteres` ou un
  tokeniseur dédié.
- **La segmentation est une règle de ponctuation**, pas un modèle : pas de gestion des abréviations,
  pas de désambiguïsation des points. L'article 1 n'a pas d'abréviation, mais un autre corpus
  pourrait produire des phrases fausses. Le tibétain a été écarté pour cette raison.
- **La source Panini peut bouger** : le corpus est lié à `udhr_corpus.json` (HEAD du dépôt
  `e10d695`, fichier non suivi). Une mise à jour du fichier change son SHA-256 ; il faut régénérer
  et re-vérifier.

## 6. Limites, nommées

1. **Un seul genre, une seule époque.** Le corpus ne permet ni le contrôle de l'époque (β +0,138
   chez Panini) ni celui du genre. Il ne suffit pas, à lui seul, au protocole atome ↔ niveau de
   J2.1 ; il fournit la **base commune** et le **contrôle d'identité**.
2. **Article 1 seulement.** Panini ne publie que l'article 1 ; les 30 articles de Drave ne sont pas
   dans l'intersection. Le corpus est donc **parallèle** mais **court**.
3. **Sélection stratifiée, non proportionnelle.** 5 familles sur 51, 10 écritures, 21 textes sur
   418 paires exactes. Les petites familles sont sur-représentées ; l'indo-européen est
   sous-représenté. Ce n'est pas une estimation de la diversité de l'UDHR.
4. **20 écarts de surface exclus.** Ce sont des variantes réelles (apostrophes, cédilles, virgules,
   ordre des diacritiques), pas du bruit. Les exclure évite de fabriquer l'accord, mais biaise
   l'échantillon vers les orthographes sans variante.
5. **Comptage des mots.** `nb_mots_ws` est un comptage sur les espaces ; il vaut 1 par phrase pour
   le chinois et l'amharique. Ce n'est pas une tokenisation.
6. **Segmentation.** Règles de ponctuation forte, sans modèle statistique ; le tibétain a été
   écarté. Un autre corpus (genres, époques) demandera un segmenteur plus robuste.
7. **Le corpus local n'est pas versionné.** `work/` est ignoré par git ; la fiche et le JSON sont
   les artefacts durables. La reproduction exige le chemin `../Panini/research`.

## 7. La suite — J3.1 et J3.2

- **J3.1 — retrieval à époque contrôlée.** Ce corpus permet le contrôle de **surface** (écriture,
  famille, branche) et le contrôle **négatif** (permuter les langues, croiser les familles). Il ne
  permet **pas** le contrôle de l'**époque** : il faudra un second corpus multi-époques (les 44
  œuvres de Panini, ou un corpus Gutenberg daté côté Drave), ou traiter l'époque comme un facteur
  non contrôlé et le dire.
- **J3.2 — généalogie à deux faces.** Les 21 langues ont une **branche Glottolog** (Drave) et une
  **famille Panini** ; la confrontation des deux représentations est possible sur ces 21 lignes,
  avec la limite que les 21 textes ne couvrent que 5 familles, qui totalisent 267/418 paires exactes.
- **Contrôle à ajouter** : comparer les 20 exclus aux 418 retenus (famille, écriture, longueur)
  pour mesurer le biais d'orthographe ; et rejouer le corpus sur un segmenteur différent pour
  vérifier que les 42 phrases ne sont pas un artefact de la règle.
- **Ne pas conclure** de ce corpus une propriété des langues ou des familles : il est stratifié,
  court, et mono-époque. Il est un **dispositif de contrôle**, pas un échantillon représentatif.

## 8. Fichiers

- **corpus local (non versionné)** : `work/corpus-commun/` — `textes/` (21 fichiers), `corpus.jsonl`
  (42 lignes), `metadata.tsv` (21 lignes + en-tête), `index.json`, `sources.sha256`,
  `controle-negatif.json`, `README.md` ;
- **outil** : [`../tools/corpus_commun.py`](../tools/corpus_commun.py) — construction, vérification,
  contrôle négatif ;
- **JSON versionné** : [`corpus-commun.json`](corpus-commun.json) — sources, intersection, sélection,
  normalisation, contrôles, 21 textes, limites, prochaine étape ;
- **sources Panini (lecture seule)** : `../Panini/research/data/udhr_corpus.json` (HEAD `e10d695`,
  2026-10-25) ;
- **sources Drave** : `../data/udhr/articles_propres.jsonl`, `../data/udhr/langues.jsonl`,
  `../data/udhr/genealogie.json` (HEAD `9c7f71dc`, 2026-11-07) ;
- **source externe** : `eric-muller/udhr` — <https://github.com/eric-muller/udhr> ; DUDH,
  <https://www.un.org/en/about-us/universal-declaration-of-human-rights>.
