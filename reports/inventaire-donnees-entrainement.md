# L'inventaire local des données pour l'entraînement

> **Ligne de roadmap** : Données · **Date** : 2026-11-01 · **Verdict** : le disque porte
> **132 Go de Wikipédia** (10 langues), **12 Go d'articles Wikipédia en texte brut**, **6,6 Go de
> corpus déjà préparés** (dont 5,36 Mo de prose du dépôt unique), **~228 Go de documents à
> extraire** (dont 2 345 Kindle sous DRM, exclus), et **2,8 To de vidéos récupérées** qui ne sont
> pas des données d'entraînement. Le français « réel » hors Wikipédia reste **petit** : c'est le
> levier à construire, pas un stock à consommer.

## 1. Ce qui est mesuré, et comment

Tour du disque le 1er novembre 2026 : `df -hT`, `lsblk`, `du -sh` par répertoire (avec délais), et
`find -type f` pour les comptages et les extensions. Le `du` complet de `/home/stephane` (10,9 To)
a été **interrompu** : trop lent ; les chiffres sont des **mesures ciblées**, pas une somme
exhaustive. Le JSON joint porte les 59 entrées, leurs tailles, formats, rôles et états.

| volume | taille | utilisé | libre | ce qu'il porte |
|---|---:|---:|---:|---|
| `/home/stephane/Data13TB` (btrfs, 10,9 To) | 11 To | **8,9 To** | 2,0 To | archives 3,0 To (dont **2,8 To de vidéos récupérées**), Documents 159 Go, data 132 Go (Wikipédia), corpus 35 Go, Biblio_large 22 Go |
| `/home/stephane/IA` (ext4, RAID) | 938 Go | **895 Go (97 %)** | **34 Go** | DeepSeek 341 Go, artefacts 122 Go, cache 123 Go (dont HF 119 Go), modèles 77 Go |
| `/` (btrfs, NVMe) | 828 Go | 121 Go | 706 Go | système et logiciels |

**Le volume IA est presque plein** (34 Go libres) : c'est le point de vigilance avant tout nouveau
téléchargement de modèle.

## 2. Le texte déjà prêt (ou presque)

| source | taille | volume | état |
|---|---:|---|---|
| `data/wikipedia/` | **132 Go** | 10 langues : bases sqlite v14 (66 Go) + dumps `xml.bz2` (67 Go) ; **FR 7,25 Go + 7,13 Go** | **prêt** (bases) / à extraire (dumps) |
| `corpus/wiki_apparie/` | **12 Go** | 6 084 fichiers d'articles Wikipédia en texte brut (de_, en_, fr_, es_, it_…), appariés par titre | **prêt** (recoupe les dumps : dédoublonner) |
| `data/` (corpus du dépôt) | 6,6 Go | `corpus_en.txt` 15,5 M mots ; `corpus_multi` 18,7 M ; `corpus_fr_litterature` 2,76 M ; `corpus_fr` 0,79 M ; `corpus_repo` 1,01 M | **prêt** |
| `data/corpus_propre/`, `corpus_litt_propre/`, `corpus_repo_propre/` | 3,8 + 17 + 5,6 Mo | prose dédupliquée, splits train/val/test, **contamination 0/2 814** | **prêt** (fiches `corpus-*.json`) |
| `data/pidgin/` (symlink) | 314 Mo | bibles (KJV, WEB, récits) | à vérifier (licences) ; `pidgin.old` = doublon |
| `data/udhr/` + `corpus/udhr/udhr.zip` | 28 Mo + 2,2 Mo | traductions UDHR | **prêt** (domaine public) |
| `corpus/parallele_crime/` | 261 Mo | textes parallèles (Crime et Châtiment) | **prêt** |
| `data/multiun/`, `opensubtitles/`, `wikimatrix/`, `ted2020/`, `jrc/`, `eurlex/` | 1,2 Go + 1,2 Go + 326 Mo + 109 Mo + 48 Mo + 10 Mo | corpus de traduction (ONU, sous-titres, TED, UE) | **prêt** (licences à vérifier pour OpenSubtitles) |
| `data/consignes_train.jsonl`, `raisonnement/`, `deepseek/` | 98 Ko + 7,9 Mo + 13 Mo | 2 000 consignes FR, paires de raisonnement, distillations | **prêt** (SFT/distillation) |
| `docs/ + journal/ + reports/` | 6,39 Mo bruts | 1 308 documents, **5,36 Mo uniques** après dédup | **prêt** (N2.i) |

## 3. Ce qu'il faut extraire (et ce qu'il faut exclure)

| source | taille | contenu | décision |
|---|---:|---|---|
| `Biblio_large/` | **22 Go** | 2 345 Kindle **kfx-zip (DRM)**, 104 PDF, 87 xhtml, images | PDF/xhtml : extraire ; **Kindle : exclure** (DRM, base légale absente) |
| `archives/CEGEP/` | 11 Go | 2 711 PDF, 3 774 xlsx, 454 docx, 362 pptx, 109 epub | à extraire ; droits pédagogiques à vérifier ; PDF scannés → **OCR R4.4** |
| `archives/collections/` | 36 Go | 384 docx, 206 doc, 193 html, 1 250 jpg | à extraire, tri par droits |
| `Documents/` | **159 Go** | 42 832 txt, 9 005 html, 6 486 xml, 6 441 pdf, 3 629 azw | **personnel : exclu** sans tri explicite |
| `archives/Google-Takeout/` | 4,6 Go | export Google | personnel : exclu |
| `archives/recovery-raw/.../Videos/` | **2,8 To** | vidéos récupérées (PhotoRec) | **exclu** : pas du texte ; plus gros poste supprimable |
| `archives/recovery-raw/.../PhotoRec/` | 3,5 Go | 1 358 PDF récupérés (noms aléatoires), audio | à vérifier (doublons, PDF tronqués) |
| `archives/recup_dir_root/` | 27 Go | récupération brute | exclu |
| `archives/audio/` | 87 Go | audio | exclu (autre chantier) |
| `archives/opt/` | 5,4 Go | builds logiciels | exclu |
| `corpus/parallele_rj/`, `corpus/udhr/` (hors zip), `corpus/wiki_traces/` | 988 Mo + 21 Go + 1,8 Go | **traces DRVF v2**, pas du texte | exclu du pré-entraînement (21 Go de traces pour 2,2 Mo de texte UDHR) |

## 4. La quarantaine d'évaluation

À ne **jamais** mettre dans l'entraînement, et à contrôler par fenêtres avant chaque recette :

- `data/xnli/` (2,3 Go), `data/daccord/`, `data/diabla/`, `data/gqnli-fr` (cache HF), `data/wikitext2_test.txt` ;
- les splits **val/test** de `corpus_propre`, `corpus_litt_propre`, `corpus_repo_propre` ;
- les **questions** du banc R0.3 (`data/onu/`) et les PDF qui les portent ;
- les scans R4.4 (`work/r44/`) : corpus de mesure, pas d'entraînement ;
- `wiki-test-200k.txt` et `wikitext-2-raw/` (logits KLD) : évaluation de la distillation.

Les manifestes `reports/corpus-*.json` mesurent déjà **0 fenêtre contaminée** sur 2 814 (val) et
0/3 000 (repo) : c'est le contrôle à réappliquer à tout nouveau corpus.

## 5. Les enseignants, pas les données

| source | taille | rôle |
|---|---:|---|
| `IA/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf` | **341 Go** (365,7 Go) | professeur de distillation |
| `IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf` + ollama | 18,5 Go + 58 Go | professeur / inférence |
| `IA/cache/huggingface/hub/` | 119 Go | Qwen2.5 0,5B/1,5B/3B/7B (15 Go), Qwen3-0,6B, gemma-3-1b, whisper ; 14B/32B = configs seules |
| `archives/kld-logits-2026-09-24/` | 6,4 Go | logits de distillation (codestral 537 Mo, ds14b 2,49 Go, q32 1,25 Go, vl7b 2,49 Go) |
| `IA/artefacts/modeles-optimises/` | 116 Go | poids produits (qwen3-30b-8clusters, v4flash-*) — artefacts, pas données |
| `models/` (dépôt) | 2,5 Go | Qwen2.5-0,5B Q4/Q8 + vision |

## 6. Ce que ça dit pour l'entraînement

1. **Le levier français est Wikipédia, pas le dépôt.** La prose du dépôt ne fait que **5,36 Mo
   uniques** (N2.i) ; Wikipédia FR en offre **7,25 Go de base** ou **7,13 Go de dump**. C'est le
   seul stock local d'un autre ordre de grandeur — et il faut le dédupliquer, le filtrer et le
   séparer des évaluations.
2. **Les documents sont un gisement, pas un corpus.** ~228 Go de PDF/docx/xlsx (Biblio, CEGEP,
   collections, Documents) demandent extraction, tri de droits et, pour les scannés, la chaîne
   **R4.4** (90–97 % de parité, ~3 s/page) — c'est précisément ce pour quoi elle a été construite.
3. **Le DRM et le personnel ne sont pas des données.** 2 345 kfx-zip + 3 629 azw + 159 Go de
   Documents : exclus sans base légale et sans tri.
4. **L'espace est la contrainte immédiate** : IA à **97 %** (34 Go libres) ; 2,8 To de vidéos
   récupérées sont le plus gros poste supprimable ; Data13TB a 2,0 To libres.

## 7. Ce qui pourrait rendre cet inventaire faux

- **Le `du` de `/home/stephane` a été interrompu** : le volume affiche **8,9 To utilisés** pour
  ~3,5 To visibles ; des **snapshots btrfs / CoW** expliquent probablement l'écart — à vérifier
  avec `btrfs filesystem du`.
- Les tailles des répertoires profonds sont des mesures ciblées ; certains comptages de fichiers
  sont absents (`None` dans le JSON).
- Les **licences** ne sont pas vérifiées pièce par pièce : presse, JW, pidgin, OpenSubtitles,
  CEGEP/collections demandent un tri avant toute diffusion.
- Les **doublons** ne sont pas mesurés à l'échelle : `pidgin`/`pidgin.old`, `wiki_apparie` vs
  dumps Wikipédia, `DRM_Archive` vs `Biblio_large`, `Documents` vs `collections` — à dédupliquer
  avec `tools/corpus_propre.py` avant d'additionner des volumes.

## Fichiers

- JSON : [`inventaire-donnees-entrainement.json`](inventaire-donnees-entrainement.json) (59 entrées).
- Manifestes de corpus : [`corpus-propre.json`](corpus-propre.json), [`corpus-litt-propre.json`](corpus-litt-propre.json), [`corpus-repo-propre.json`](corpus-repo-propre.json).
- Dédup et splits : [`tools/corpus_propre.py`](../tools/corpus_propre.py).
- OCR pour les PDF scannés : [`rapport-r44-scans.md`](rapport-r44-scans.md) et [`tools/porte-ocr-scans.sh`](../tools/porte-ocr-scans.sh).
