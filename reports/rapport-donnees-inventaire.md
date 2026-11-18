# L'inventaire des données pour le palier 1 : 1,02 Go épinglés sur 3–6 Go demandés

> **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·
> **Verdict** : le dépôt porte **135,5 Go** de données apparentes (4 428 fichiers), dont **120,1 Go
> de Wikipédia en 10 langues**. Le français vraiment exploitable se réduit à **7,5 Go** — et le
> corpus épinglé (**1,017 Go**) en est un **sous-ensemble de contenu**. Il manque **1,98 Go** pour
> 3 Go et **4,98 Go** pour 6 Go, mais ces octets sont **déjà sur le disque**
> (`data/corpus_wiki_fr_texte/`, 7,50 Go) : l'écart de **volume** est fermable sans aucune collecte ;
> l'écart de **diversité** (≈ 0,1 Go de français hors Wikipédia) ne l'est pas.

Aucun fichier de `data/` n'a été modifié, aucun téléchargement n'a été fait. Les seules écritures
sont ce rapport et un fichier temporaire `/tmp/titres_wikibig.txt`.

## 1. Ce qui est mesuré, et comment

Mesures du **2026-11-18**, en lecture seule : `du -sb` et `find -type f` pour les octets et les
comptages, `stat` pour les tailles exactes, `wc -l` pour les lignes, `head -c` pour les échantillons,
`gzip -l` pour la taille décompressée des TMX (lue dans la queue gzip, sans décompresser). Le texte
n'est **jamais chargé pour être inspecté** : les gros fichiers ne sont traversés qu'en flux, pour
compter ou hacher, et seuls quelques kilo-octets sont lus.

Trois mesures ont été **faites ici** plutôt que reprises des manifestes :

1. **Langue** : échantillonnage de 300 blocs de 2 Ko (stopwords FR/EN) **et** comptage exact des
   occurrences de ` de ` et ` the ` sur tout le fichier ; calibration sur deux textes purs —
   `corpus_en.txt` (861 039 `the` pour 7 210 `de` sur 0,100 Go) et `corpus_wiki_fr_texte`
   (68 688 961 `de` pour 580 410 `the` sur 7,504 Go), soit un rapport **118:1** en faveur du
   français.
2. **Déduplication** : passe sur les **7,50 Go** du train avec des shingles de 96 octets (pas de 96 o,
   CRC32, 88 s) → **78 167 485 shingles, 2 290 786 déjà vus (2,93 %)**. Les collisions 32 bits
   attendues sur 78,2 M empreintes valent ≈ 711 000 (0,91 pp) : la duplication **réelle** est
   ≈ **2,0 %**.
3. **Recouvrement** : 200 titres tirés de `data/wiki_big/brut.txt` (un sur quatre) cherchés en
   **ligne entière exacte** dans `data/corpus_wiki_fr_texte/{train,val,test}.txt` → **200/200
   retrouvés** (182 dans le train, le reste dans val/test).

L'épingle du corpus n'a **pas** été refaite : les chiffres de `reports/corpus-epingle.json` sont
repris tels quels, et le `wc -l` du train redonne bien **2 480 766** lignes (cohérence, pas
re-épinglage).

## 2. Le total : 135,5 Go, dont 120 Go de Wikipédia

| famille | octets apparents | fichiers | part |
|---|---:|---:|---:|
| 10 langues — résumés (`data/corpus_wiki_<lang>/`) | 38,78 Go | 30 | 28,6 % |
| 10 langues — plein texte (`data/corpus_wiki_<lang>_texte/`) | 81,32 Go | 30 | 60,0 % |
| dérivés Wikipédia FR (`wiki_fr`, `wiki_big`, `wiki_mix`) | 5,76 Go | 19 | 4,3 % |
| `wiki_multi` (10 langues) | 0,86 Go | 25 | 0,6 % |
| corpus FR du dépôt + PDF/OCR | 1,30 Go | 40 | 1,0 % |
| parallèles FR-EN (TMX compressés) | 2,96 Go | 10 | 2,2 % |
| évaluation (`xnli`, `daccord`, `diabla`, `wikitext2`) | 2,38 Go | 65 | 1,8 % |
| le reste (artefacts `.npz` 0,56 Go, pidgin, adaptateurs, jw, ONU, UE, presse, SFT…) | ≈ 2,1 Go | 4 209 | 1,5 % |
| **total `data/`** | **135 523 369 596 o = 135,5 Go** | **4 428** | 100 % |

**126 Gio** au `du -sh` (127G) — l'écart est la différence Go/Gio. Le total **n'inclut pas**
`data/pidgin`, qui est un lien symbolique vers `/home/stephane/IA/drave-data/pidgin`
(328 747 430 o, compté une fois via `pidgin.old`).

Le français est le **4ᵉ** corpus des 10 langues (en 21 Gio, ru 11, de 10, **fr 7,8**, ja 6,9, es 6,4,
it 5,0, ar 3,4, pt 3,0, zh 2,5 — valeurs `du`).

**Hors `data/` (pour mémoire, non compté ici)** : `/home/stephane/Data13TB/stephane/data/wikipedia`
= **132 Gio** (bases sqlite + dumps), dont le dump FR `frwiki-…xml.bz2` = **7,13 Go** ;
`corpus/wiki_apparie` = **12 Gio** (6 084 fichiers, 10 langues, appariés par titre). Ce sont les
**sources** des corpus ci-dessus (même dump), pas du volume nouveau ; `wiki_apparie` recoupe les
extractions et doit être dédupliqué avant tout comptage.

## 3. Le corpus épinglé (référence, non refaite)

| fichier | octets | lignes | sha256 (préfixe) |
|---|---:|---:|---|
| `data/wiki_mix/propre/train.txt` | 1 017 487 092 | 2 480 766 | `0876b6089a…` |
| `data/wiki_mix/propre/val.txt` | 10 330 112 | 24 498 | `fbddef9181…` |
| `data/wiki_mix/propre/train.canal` | 1 017 487 092 | — | `04efed3039…` |
| `data/wiki_mix/propre/val.canal` | 10 330 112 | — | `f1abc5d1d6…` |
| **manifeste** | — | — | `fae5bb7389…` |

**La composition est exacte, au bit près** :
`wiki_fr/propre/train.txt` (186 089 472 o) + `wiki_big/propre/train.txt` (831 397 620 o)
= **1 017 487 092 o**, la taille du train de `wiki_mix`. Le `val.txt` du pin est
**le même fichier** que `wiki_fr/propre/val.txt` (même sha256 `fbddef…`) : 10,3 Mo, 24 498 lignes.

Conséquence : le train est dominé par `wiki_big` (**82 %** : 600 000 articles de page_id ≥ 1 M,
plein texte) alors que la **validation** vient de `wiki_fr` (résumés, 186 Mo). Train et val ne sont
pas du même domaine — c'est un candidat sérieux pour l'alerte de reproductibilité du 16/11
(`ppl_val` 2,40 annoncé, 17,3 à 22,6 retrouvés selon le morceau).

## 4. Le tableau des corpus

« Langue » : mesure par échantillonnage et/ou rapport `de`/`the` (§ 1). « Licence » : **déclarée**
dans un manifeste `reports/corpus-*.json` quand c'est indiqué, sinon « à vérifier » — aucune licence
n'a été vérifiée fichier par fichier.

| chemin | octets | lignes mesurées | langue | licence (source) | usage / note |
|---|---:|---:|---|---|---|
| `data/corpus_wiki_fr_texte/train.txt` | 7 504 078 589 | 88 114 432 | fr ≈ 99 % | CC-BY-SA 4.0 (déclarée) | **la réserve** : 2 149 330 articles, plein texte |
| `data/corpus_wiki_fr_texte/val.txt` | 419 555 119 | — | fr | CC-BY-SA 4.0 | évaluation (5 %) |
| `data/corpus_wiki_fr_texte/test.txt` | 415 302 543 | — | fr | CC-BY-SA 4.0 | évaluation (5 %) |
| `data/corpus_wiki_fr/train.txt` | 3 425 588 868 | 4 546 588 | fr ≈ 99 % | CC-BY-SA 4.0 | résumés, 2 273 294 articles — **redondant** |
| `data/wiki_fr/articles.txt` | 237 491 315 | 480 000 | fr | CC-BY-SA 4.0 | source de `wiki_fr/propre` |
| `data/wiki_fr/propre/train.txt` | 186 089 472 | — | fr | CC-BY-SA 4.0 | **dans le pin** |
| `data/wiki_big/brut.txt` | 1 047 525 530 | 2 400 000 | fr ≈ 99 % | CC-BY-SA 4.0 | source de `wiki_big/propre` |
| `data/wiki_big/propre/train.txt` | 831 397 620 | — | fr | CC-BY-SA 4.0 | **dans le pin** (82 %) |
| `data/wiki_multi/train.txt` | 275 467 919 | 440 000 | 10 langues | CC-BY-SA 4.0 | concaténation ; fr = 20,7 Mo |
| `data/corpus_fr_litterature.txt` | 17 031 747 | 350 641 | fr ≈ 98 % | à vérifier (DP probable) | littérature (Alice, Verne…) |
| `data/corpus_litt_propre/train.txt` | 15 332 926 | — | fr | à vérifier | littérature dédupliquée |
| `data/corpus_fr.txt` | 4 633 889 | 48 330 | fr | à vérifier | prose du snapshot |
| `data/corpus_propre/train.txt` | 3 244 858 | — | fr | à vérifier | dédup de `corpus_fr` |
| `data/corpus_repo.txt` | 6 394 114 | — | fr | dépôt | prose du dépôt (N2.i) |
| `data/corpus_repo_propre/train.txt` | 4 836 314 | — | fr | dépôt | 4,84 Mo uniques mesurés |
| `data/corpus_mixte*.txt` (5 fichiers) | 44 915 449 | — | fr/en | à vérifier | mélanges, 53,5 % fr |
| `data/corpus_multi.txt` | 121 523 142 | 1 465 777 | **71 langues** (UDHR) | domaine public revendiqué | français ≈ 9 734 o : **négligeable** |
| `data/corpus_en.txt` | 100 276 153 | 1 196 326 | en ≈ 98 % | CC-BY-SA (wiki) | anglais |
| `data/corpus_pdf/train.txt` | 295 760 347 | 8 306 610 | **en ≈ 70 %, fr ≈ 8 %** | livres : droits réservés | Biblio_large + CEGEP |
| `data/corpus_pdf_documents/train.txt` | 802 954 509 | 21 187 808 | **en ≈ 71 %, fr ≈ 6 %** | personnel, « à préciser » | **PII** (voir § 6) |
| `data/corpus_ocr*` (5 dossiers, tous splits) | 26 999 830 | — | fr | notes de cours, droits réservés | OCR CEGEP |
| `data/udhr/` | 28 858 709 | — | 71 langues | domaine public revendiqué | `_fra.txt` = 9 734 o |
| `data/structures/` | 122 454 | — | fr | dépôt | banque symbolique (6 fichiers) |
| `data/multiun/en-fr.tmx.gz` | 1 276 271 220 → **5 137 807 269** | — | fr-en | documents ONU, à vérifier | parallèle institutionnel |
| `data/opensubtitles/en-fr.tmx.gz` | 1 264 276 955 → **6 243 401 029** | — | fr-en | **non vérifiée** | parallèle oral |
| `data/wikimatrix/en-fr.tmx.gz` | 340 868 887 → **1 048 389 238** | — | fr-en | CC-BY-SA (dérivé wiki) | parallèle |
| `data/jrc/en-fr.tmx.gz` | 49 409 718 → **235 330 059** | — | fr-en | réutilisation UE, à vérifier | parallèle juridique |
| `data/ted2020/en-fr.tmx.gz` | 32 964 653 → **124 236 908** | — | fr-en | TED, à vérifier (NC-ND ?) | parallèle oral |
| `data/xnli/` | 2 380 057 696 | — | fr (traduit) | à vérifier | **évaluation seulement** |
| `data/pidgin.old/` | 328 747 430 | — | en/pidgin | KJV/WEB DP, autres à vérifier | = `data/pidgin` (symlink) |
| `data/jw/` | 36 851 670 | — | multilingue | droits réservés | usage local |
| `data/presse/` | 671 271 | — | fr | droits réservés | API presse |
| `data/onu/` | 10 176 222 | — | fr/multi | ONU | banc R0.3 / questions |
| `data/eurlex/` | 10 325 824 | — | fr/multi | UE | traduction |
| `data/deepseek/` (3 789 fichiers) | 13 375 971 | — | fr | API DeepSeek | distillation / SFT |
| `data/raisonnement/` | 8 175 404 | — | fr | généré | SFT |
| `data/adaptateurs/` | 177 390 271 | — | — | — | **poids LoRA, pas des données** |
| `data/wikitext2_test.txt` | 359 041 | — | en | — | évaluation |

## 5. L'écart au palier 1

Le plan natif demande **3–6 Go de français propre** pour un **100–150 M**
([`natif-plan.md`](../docs/pilotage/natif-plan.md), § 2).

| | Go | part de la cible | octets/paramètre |
|---|---:|---:|---:|
| cible basse | 3,00 | 100 % | 20 (à 150 M) |
| **corpus épinglé** | **1,017** | **33,9 %** | **6,8 (150 M) / 10,2 (100 M)** |
| cible haute | 6,00 | 100 % | 60 (à 100 M) |
| **manque pour 3 Go** | **1,983** | 66,1 % | — |
| **manque pour 6 Go** | **4,983** | 83,0 % | — |

Même à 100 M, le corpus actuel donne **10,2 octets/paramètre**, la moitié de Chinchilla (20) ; la
cible basse du palier 1 est exactement Chinchilla pour 150 M.

**L'écart de volume est déjà comblé sur le disque.** `data/corpus_wiki_fr_texte/train.txt` fait
**7,50 Go** ; après déduplication (≈ 2,0 %, § 1) il reste **≈ 7,2–7,35 Go**, dont **1,02 Go
recouvre le pin** (contenu, pas octets) → **≈ 6,2–6,3 Go nets ajoutables**. La réserve vaut donc
**2,4×** la cible basse (3 Go) et **1,2×** la cible haute (6 Go), et les octets **nets** valent
encore **1,25×** les 4,98 Go qui manquent pour 6 Go.

**Ce qui manque vraiment n'est pas du volume, c'est du non-Wikipédia.** Le français hors Wikipédia
déjà présent et déjà propre représente ≈ **0,10 Go** : littérature 15,3 Mo, `corpus_fr` 3,2 Mo,
dépôt 4,8 Mo, ~72 Mo de français noyés dans les PDF (mesuré : 6–8 % de 1,10 Go). Même en
l'ajoutant, le corpus du palier 1 resterait **≈ 98 % Wikipédia**.

### Les 3 sources les plus prometteuses déjà présentes

1. **`data/corpus_wiki_fr_texte/` — 7,50 Go, 88,1 M lignes, 2,15 M articles, fr ≈ 99 %,
   CC-BY-SA.** La seule source qui ferme l'écart de volume à elle seule (**+6,2 à 6,3 Go nets**).
   Limite : c'est **la même encyclopédie** que le pin — même domaine, même registre, même style.
   Elle apporte des octets, pas un nouveau savoir (leçon de [`rapport-n2-corpus-1go`](rapport-n2-corpus-1go.md) :
   à compute constant, 5,6× plus de corpus fait apprendre **autre chose**, pas plus).
2. **Les parallèles FR-EN — 12,79 Go décompressés** (multiun 5,14 + opensubtitles 6,24 +
   wikimatrix 1,05 + jrc 0,24 + ted 0,12), soit ≈ **4,5 Go de français** (estimation : ~35 % du
   TMX après balisage). Genres réellement nouveaux : ONU institutionnel, sous-titres oraux, TED,
   droit de l'UE, Wikipédia traduit. Limites : licences hétérogènes (OpenSubtitles **non
   vérifiée**, TED possiblement NC-ND), alignement phrase à phrase (ce n'est pas de la prose
   longue), et il faudra un corpus de phrases, pas de documents.
3. **La prose française hors Wikipédia déjà nettoyée — ≈ 0,10 Go** : littérature 15,3 Mo (DP
   probable), `corpus_fr` 3,2 Mo, dépôt 4,8 Mo, + les ~72 Mo de français des PDF. Volume
   négligeable, mais c'est la **seule diversité de domaine immédiatement disponible** ; les PDF
   personnels sont à exclure (PII), les autres licences à vérifier.

`data/corpus_wiki_fr/` (3,43 Go) **n'est pas dans ce trio** : ce sont les résumés de la **même**
encyclopédie, déjà couverts par la source 1 — de la redondance, pas une réserve.

## 6. Doublons et risques

**Sommes exactes (prouvées, pas estimées)** — elles montrent que plusieurs fichiers sont des
décompositions l'un de l'autre, et qu'il ne faut pas les additionner :

- `wiki_mix/propre/train.txt` = `wiki_fr/propre/train.txt` + `wiki_big/propre/train.txt`
  (186 089 472 + 831 397 620 = 1 017 487 092) ;
- `corpus_fr.txt` = `corpus_fr_train.txt` + `corpus_fr_val.txt` (4 402 195 + 231 694 = 4 633 889) ;
- `corpus_multi.txt` = `corpus_multi_train.txt` + `corpus_multi_val.txt`
  (115 446 985 + 6 076 157 = 121 523 142) ;
- `corpus_mixte_propre.txt` = 10 × `corpus_mixte_dev.txt` (6 144 000 / 614 400) ;
- `wiki_multi/train.txt` = concaténation exacte des 10 `<lang>_train.txt`.

**Recouvrement Wikipédia (le risque principal).** Trois extractions du **même dump** FR cohabitent :
`corpus_wiki_fr_texte` (plein texte, 7,50 Go), `corpus_wiki_fr` (résumés, 3,43 Go) et
`wiki_fr`/`wiki_big` (186 + 831 Mo, déjà dans le pin). Le test des 200 titres rend **200/200**
retrouvés dans le plein texte (182 dans le train — cohérent avec la part train de 90,0 % —, le
reste dans val/test) : la partie **`wiki_big` du pin (82 %)** est donc un **sous-ensemble de
contenu** de `corpus_wiki_fr_texte`. La partie `wiki_fr` (résumés, 18 %) vient des **mêmes
articles** (même dump, mêmes page_id) — recouvrement d'articles certain, recouvrement d'octets non
mesuré. Additionner les deux corpus compte deux fois la même encyclopédie.

**Autres doublons** :

- `data/pidgin` (symlink) et `data/pidgin.old` : **328 747 430 o chacun**, mêmes noms de fichiers,
  même taille — doublon intégral.
- Les `.canal` ont exactement la taille de leur `.txt` (`wiki_fr/propre`, `wiki_big/propre`,
  `corpus_propre`) : ce sont des transformations, pas du texte — ne pas compter 2×.
- `corpus_fr_litterature.txt` → `corpus_litt_propre` ; `corpus_repo.txt` → `corpus_repo_propre` ;
  `corpus_fr.txt` → `corpus_propre` ; `wiki_fr/articles.txt` → `wiki_fr/propre` ;
  `wiki_big/brut.txt` → `wiki_big/propre` : chaque paire est source + dérivé.
- `corpus_ocr_cegep`, `_micro`, `_avant_micro`, `_pilote-2pages` : quatre versions successives du
  même matériel (0,35 à 4,5 Mo).
- `data/wiki_big/propre/train.canal` a la taille de `train.txt` et `wiki_fr/propre/train.canal-placebo`
  aussi : artefacts d'expérience, pas des corpus.

**Risques de qualité et de droits** :

- **PII** : `corpus_pdf_documents` contient des documents **personnels** — l'échantillon lu au
  hasard porte un avis de cotisation avec adresse et un numéro d'assurance sociale partiellement
  masqué. À **exclure** du pré-entraînement sans caviardage, malgré ses 803 Mo.
- **Licences non vérifiées** : OpenSubtitles, TED, JW, presse, PDF Biblio/CEGEP, `pidgin`. Wikipédia
  est la seule licence déclarée à la fois **homogène et permissive** (CC-BY-SA 4.0) : les autres
  sont déclarées **restrictives** (« droits réservés », « personnel ») ou **absentes**. Toute
  diffusion du modèle doit créditer Wikipédia et partager à l'identique.
- **Domaine de validation** : le `val` du pin vient des **résumés** quand le train vient du **plein
  texte** — la PPL du palier 1 mesurerait un décalage de domaine (cf. l'alerte de reproductibilité).
- **Le français des PDF est minoritaire** : 8 % et 6 % mesurés ; compter `corpus_pdf` +
  `corpus_pdf_documents` comme du français (1,10 Go) est faux d'un facteur ≈ 15 (1,10 Go
  comptés pour ≈ 72 Mo réels).
- **45,8 % des lignes du plein texte font moins de 80 caractères** (titres de sections, listes,
  ébauches) : c'est de la matière Wikipédia, pas de la prose continue — un filtre de longueur sera
  à appliquer avant d'épingler une v2.

## 7. La prochaine action de collecte (à faire plus tard, pas ici)

**Le volume est déjà là : la prochaine collecte doit viser la diversité, pas les octets.** Par
ordre de valeur :

1. **Des livres français en domaine public** — dump **Wikisource FR** et catalogue **Gutenberg FR**
   (quelques centaines de Mo compressés, taille exacte à mesurer), extraction, filtre de longueur,
   déduplication contre les 7,5 Go Wikipédia, puis épinglage. Objectif : **+0,5 à 1 Go de prose
   longue**, un registre que Wikipédia ne donne pas. C'est exactement ce que le plan appelle
   « des livres, des articles ».
2. **Un extrait de français contemporain sous licence claire** (presse ou web filtré) — plus lourd :
   droits à trier, qualité à filtrer, PII à retirer. À ne lancer qu'après le point 1.
3. **Ne pas collecter de Wikipédia** : 7,5 Go sont déjà sur le disque, un téléchargement de plus
   n'ajoute **aucun savoir nouveau**.

**Le prérequis n'est pas la collecte, c'est l'outillage.** `tools/corpus_propre.py` garde tous les
shingles en mémoire (≈ 80 Go par Go de texte, cf. [`rapport-n2-corpus-1go`](rapport-n2-corpus-1go.md)) :
dédupliquer les 7,50 Go en une passe demanderait ~600 Go de RAM pour 125 Go installés. Il faut une
**passe par blocs** avec un état de chevauchement avant de construire le corpus v2 — et **une
nouvelle épingle** (`corpus-epingle-v2`), la v1 restant la référence des campagnes passées.

## 8. Contrôle négatif et ce qui pourrait rendre ce rapport faux

**Contrôles négatifs** (des tests qui **pouvaient** échouer) :

- le détecteur de langue appliqué à `corpus_en.txt` donne **1,6 % de français** et 861 039 `the` :
  il ne classe pas tout en français ;
- la somme `wiki_fr/propre/train + wiki_big/propre/train` retombe **à l'octet près** sur
  `wiki_mix/propre/train` (1 017 487 092) : une composition inventée ne tomberait pas juste ;
- le test des 200 titres pouvait donner ~0 si `wiki_big` venait d'un autre dump ; il donne 200/200 ;
- le `wc -l` du train épinglé redonne **2 480 766**, la valeur du manifeste.

**Ce qui pourrait rendre ce rapport faux** :

- la déduplication est mesurée par **échantillonnage de shingles** (pas de 96 o, CRC32) et non avec
  l'outil du dépôt ; le taux réel peut différer de quelques dixièmes de point, et il est mesuré sur
  le **train seul** ;
- la part de langue est **échantillonnée** (300 blocs, et un rapport `de`/`the` global), pas un
  recensement ; elle ne distingue pas le français québécois, l'ancien français ou le français
  fautif ;
- le recouvrement d'articles est prouvé sur **200 titres sur 600 000** ; un article de `wiki_big`
  absent du plein texte serait passé inaperçu s'il ne figurait pas dans l'échantillon ;
- les **licences** ne sont pas vérifiées pièce par pièce : « déclarée » signifie « écrite dans un
  manifeste », pas « auditée » ;
- les 7,50 Go incluent des **listes, tableaux et ébauches** (45,8 % de lignes courtes) : le volume
  « propre » après filtrage de prose sera inférieur au volume brut ;
- les tailles des dossiers sont **apparentes** (`du -sb`), pas la consommation disque réelle (blocs,
  CoW btrfs) ; le total en Gio est donné à part.

## 9. Fichiers

- l'épingle : [`corpus-epingle.json`](corpus-epingle.json) et [`rapport-corpus-epingle.md`](rapport-corpus-epingle.md) ;
- les manifestes des corpus : [`corpus-wiki-fr-texte.json`](corpus-wiki-fr-texte.json),
  [`corpus-wiki-fr.json`](corpus-wiki-fr.json), [`corpus-wiki-big-propre.json`](corpus-wiki-big-propre.json),
  [`corpus-wiki-propre.json`](corpus-wiki-propre.json), [`corpus-pdf.json`](corpus-pdf.json),
  [`corpus-pdf-documents.json`](corpus-pdf-documents.json), [`corpus-propre.json`](corpus-propre.json),
  [`corpus-litt-propre.json`](corpus-litt-propre.json) ;
- le plan : [`natif-plan.md`](../docs/pilotage/natif-plan.md) ;
- l'inventaire disque antérieur (autre périmètre, 2026-11-01) :
  [`inventaire-donnees-entrainement.md`](inventaire-donnees-entrainement.md).
