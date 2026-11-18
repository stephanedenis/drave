# Session da0f2984 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `da0f2984-32d0-459d-a761-d3faf6a10b8a` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 09:15 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 51 |
| Appels d'outils | 70 |
| Fichiers touchés | 1 |
| Commandes | 50 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français). La machine est dédiée.  TÂCHE : l'INVENTAIRE des données disponibles pour le palier 1 du modèle natif (100-150 M, 3-6 Go de français propre). Tu ne télécharges RIEN et tu ne modifies AUCUNE donnée : tu mesures ce qui est là et tu chiffres l'écart.  À faire : 1. `du -sh data/*` et les sous-dossi … [2012 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français). La machine est  … [2292 caractères tronqués]

*70 appels d'outils.* Actions notables :

- bash — Mesure la taille de data et ses sous-dossiers
- bash — Liste le contenu de data
- bash — Liste la fin du contenu de data
- bash — Compte les fichiers et tailles par dossier
- bash — Inspecte la structure des dossiers wiki et corpus
- bash — Lit l'épingle du corpus et cherche rapports liés
- bash — Liste tous les rapports
- bash — Liste les sous-dossiers propre
- read
- bash — Lit le recensement français
- bash — Lit les manifestes de corpus principaux
- bash — Trouve les fichiers qui mentionnent wiki_mix
- bash — Aperçu des premiers octets de trois corpus
- bash — Inspecte les dossiers secondaires
- … et 50 autres

**Synthèse produite :**

⏵ Clôture : synthèse des quatre chiffres demandés

**Inventaire terminé** — `data/` n'a pas été modifié, aucun téléchargement, aucun commit. Le rapport est écrit : `reports/rapport-donnees-inventaire.md` (296 lignes, 21 Ko).

\## 1. Total des données

**135,5 Go apparents** (135 523 369 596 o, **4 428 fichiers**) ; **126 Gio** au `du -sh` (127G). Dont **120,1 Go de Wikipédia en 10 langues** (38,78 Go de résumés + 81,32 Go de plein texte), 5,76 Go de dérivés Wikipédia FR, 2,96 Go de parallèles FR-EN compressés (12,79 Go décompressés), 2,38 Go d'évaluation, 1,30 Go de corpus FR/PDF/OCR. À noter : 0,74 Go ne sont pas des données (.npz, adaptateurs LoRA) et les PDF sont **majoritairement anglais** (~70 % EN, 6–8 % FR).

\## 2. Écart au palier 1 (3–6 Go)

| | Go | part de la cible |
|---|---:|---:|
| corpus épinglé | **1,017** | 33,9 % (3 Go) / 17,0 % (6 Go) |
| **manque pour 3 Go** | **1,98** | 66,1 % |
| **manque pour 6 Go** | **4,98** | 83,0 % |

Mais **ces octets sont déjà sur le disque** : `data/corpus_wiki_fr_texte/train.txt` = **7,50 Go** (fr ≈ 99 %, CC-BY-SA), qui donne **6,2–6,3 Go nets** après déduplication (~2,0 % mesuré) et retrait du recouvrement avec le pin — soit 1,25× les 4,98 Go manquants. **L'écart de volume est fermable sans collecte ; l'écart de diversité (~0,1 Go hors Wikipédia) ne l'est pas.**

\## 3. Les 3 sources les plus prometteuses déjà présentes

1. **`data/corpus_wiki_fr_texte/`** — 7,50 Go, 2,15 M articles, fr ≈ 99 %, CC-BY-SA : ferme l'écart de volume à elle seule, mais même encyclopédie que le pin (les 200 titres testés de `wiki_big` y sont tous, 182/200 dans le train = part train attendue de 90 %).
2. **Les parallèles FR-EN** — 12,79 Go décompressés (multiun, opensubtitles, wikimatrix, jrc, ted), ≈ 4,5 Go de français estimés, genres réellement nouveaux ; licences hétérogènes à trier.
3. **La prose FR hors Wikipédia déjà nettoyée** — ≈ 0,10 Go (littérature 15,3 Mo, corpus_fr 3,2 Mo, dépôt 4,8 Mo, ~72 Mo de FR dans les PDF) : volume négligeable mais seule diversité immédiate ; les PDF personnels contiennent des **PII** (NAS partiel, adresse) et sont à exclure.

\## Prochaine action de collecte (non faite)

Livres français en domaine public (**Wikisource FR + Gutenberg FR**) pour la diversité, pas pour le volume — et **pas de Wikipédia** (7,5 Go déjà là, zéro savoir nouveau). Prérequis technique avant une épingle v2 : une passe de déduplication **par blocs** (l'outil actuel demande ~80 Go de RAM par Go de texte, soit ~600 Go pour 7,5 G
… [3 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md` | 1 | 9 |

### Commandes exécutées (échantillon)

- **T1** Mesure la taille de data et ses sous-dossiers
- **T1** Liste le contenu de data
- **T1** Liste la fin du contenu de data
- **T1** Compte les fichiers et tailles par dossier
- **T1** Inspecte la structure des dossiers wiki et corpus
- **T1** Lit l'épingle du corpus et cherche rapports liés
- **T1** Liste tous les rapports
- **T1** Liste les sous-dossiers propre
- **T1** Lit le recensement français
- **T1** Lit les manifestes de corpus principaux
- **T1** Trouve les fichiers qui mentionnent wiki_mix
- **T1** Aperçu des premiers octets de trois corpus
- **T1** Inspecte les dossiers secondaires
- **T1** Vérifie le dossier corpus hors data
- **T1** Cherche la composition de wiki_mix dans les rapports
- **T1** Cherche wiki_mix dans les outils et liste wiki_multi
- **T1** Compte les lignes des corpus texte
- **T1** Vérifie les données externes au dépôt
- **T1** Cherche fichiers de licence et champs licence
- **T1** Échantillonne les corpus multi et anglais
- **T1** Inspecte les dumps Wikipédia externes
- **T1** Lit les fiches du corpus 1 Go et élargi
- **T1** Total octets, nombre de fichiers par dossier
- **T1** Taille décompressée des corpus parallèles TMX
- **T1** Échantillonne la langue des corpus (stopwords)
- **T1** Lit les rapports de contamination PDF et wiki
- **T1** Compte de/the pour trancher la langue
- **T1** Mesure la densité d'accents des corpus PDF
- **T1** Compare la structure des trois extractions Wikipédia
- **T1** Analyse la structure des lignes du corpus wiki texte
- **T1** Vérifie la RAM disponible et l'approche du déduplicateur
- **T1** Mesure le taux de duplication locale sur 150 Mo
- **T1** Mesure la duplication sur tout le corpus wiki texte
- **T1** Liste les manifestes avec licence et cherche la cible du palier 1
- **T1** Lit la définition du palier 1 et la suite de l'épingle
- **T1** Lit le bilan natif sur le pas suivant
- **T1** Vérifie les sommes exactes et le doublon pidgin
- **T1** Calibre les densités de/the en anglais pur
- **T1** Somme par famille de corpus
- **T1** Compte les titres de wiki_big retrouvés dans le plein texte
- … et 10 autres

## 4. Mesures et résultats marquants

- **T1** `"split": "hash salé (graine 1) de page_id : 5% val, 5% test"`
- **T1** `"split": "hash salé (graine 1) de page_id : 5% val, 5% test, le reste train ; un article n'est que dans un split",`
- **T1** `"split": "hash salé du chemin : 5% val, 5% test"`
- **T1** `reports/rapport-n2-200k.md-26-  de `data/wiki_fr/propre` (186 Mo) et `data/wiki_big/propre` (831 Mo) ; canal concaténé ; le`
- **T1** `reports/rapport-n2-200k.md-27-  découpage interne réserve les 5 % finaux à la validation d'entraînement.`
- **T1** `reports/rapport-n2-200k.md-30-  lieu de 60 000 (×3,33). GPU 0, **11 410 s** (3 h 10), ~57 ms/pas.`
- **T1** `reports/rapport-n2-200k.md-32-  dans des chunks de 8 192, 8 lots × 16 fenêtres. Le témoin 60 k (`work/n2w/mix-60k.pt`), repassé`
- **T1** `# N2.aa — Le corpus de 831 Mo à compute constant : un autre domaine, pas plus de savoir`
- **T1** `> étages de 20 000 pas, canal), le corpus de **831 Mo** (600 000 articles, offset 1 M, **0 fuite**)`
- **T1** `> propre domaine** (écart ~0,2) : à 40 Mo vus, un corpus 5,6× plus grand ne fait pas apprendre plus`
- **T1** `200 000) ; brut **1 048 Mo** → dédupliqué **924 Mo (88,2 %)** → train **831 Mo**, val 46 Mo, test`
- **T1** `46 Mo ; **0 fuite** sur 4 000 fenêtres (`reports/corpus-wiki-big-propre.json`).`
- **T1** `- **Modèle** : 34,3 M (`384/512`), deux étages de 20 000 pas × 8 × 128, positions [0, 384], canal de`
- **T1** `| modèle | val N2.z (186 Mo) | val grand (831 Mo) |`
- **T1** `| **N2.z** (186 Mo, canal) | **3,5250** | 3,7107 |`
- **T1** `| **grand** (831 Mo, canal) | 3,7025 | **3,4604** |`
- **T1** `**Le corpus ne paie pas à compute constant.** Les deux modèles ont vu **40 Mo** de texte (2 × 20 000`
- **T1** `pas × 8 × 128) ; le grand en a vu 5 % et le petit 21 %. Le grand ne peut donc pas « savoir plus » :`
- **T1** `**La bonne question n'est donc pas « plus de données ? » mais « plus de pas ? ».** À 40 Mo vus, le`
- **T1** `(le contrôle : 200 000 pas sur 186 Mo, puis sur 831 Mo).`
- **T1** `- **40 Mo vus** : c'est le point le plus limitant ; à 200 000 pas, la conclusion pourrait s'inverser.`
- **T1** `# N2.i — Le corpus élargi : 4,84 Mo uniques au lieu de 3,24`
- **T1** `> courant (**+49 %** de texte unique, autres registres) ne fait pas baisser la PPL en domaine`
- **T1** `N2.h a laissé une question chiffrée : le corpus propre fait **3,24 Mo** d'entraînement, alors que`
- **T1** `le dépôt courant en contient bien plus (recensement du 01/11 : 27,7 Mo avec les transcripts, mais`
- **T1** `du dépôt, dédupliqué, est-il plus grand que celui du snapshot ?** Oui — 6,39 Mo bruts pour`
- **T1** `docs+journal+rapports, 5,36 Mo uniques. Est-ce que cela fait baisser la PPL honnête ?`
- **T1** `- **corpus** : `docs/` + `journal/` (hors `sessions/`) + `reports/`, 1 308 documents, 6,39 Mo`
- **T1** `bruts ; dédupliqué par les mêmes shingles de 96 octets (−16,2 %, 2 008 runs), split par chunks`
- **T1** `de 8 Ko → **4 836 314** octets d'entraînement, 262 144 de validation, 262 144 de test ;`
- **T1** `(20 000 pas supervisés), distillation 20 000 pas × 16 × 128, lr 1e-4 puis 3e-5, **3 graines** ;`
- **T1** `C'est **1,49×** le texte unique de N2.h (3,24 Mo), à genre constant.`
- **T1** `| **N2.h — 3,24 Mo** | 3,0904 | 3,0904 | 3,1960 | 16,70 | 57,58 | 56,88 | 14,11 |`
- **T1** `| **N2.i — 4,84 Mo** | 3,1278 | 3,6996 | 3,2714 | 12,93 | 33,83 | 35,53 | 14,28 |`
- **T1** `En domaine, **3,1278** sur son propre jeu et **3,6996** sur l'ancien, contre **3,0904** : l'élargissement ne fait pas mieux sur la prose du snapshot, et le corpus courant contient d'autres registres (`
- **T1** `Le levier « plus de texte du dépôt » n'est pas un levier de domaine : il **dilue la prose** (3,70 sur l'ancienne validation contre 3,09) parce qu'il ajoute des registres — et il **généralise** (littér`
- **T1** `- **+49 % de texte unique, pas 10×** : le recensement à 27,7 Mo comptait les transcripts de`
- **T1** `sessions (méta-texte, code, JSON) ; la prose du dépôt ne fait que 5,36 Mo uniques.`
- **T1** `data/corpus_wiki_fr_texte/train.txt           FR~ 96.3%  (7.504 Go)`
- **T1** `data/corpus_wiki_fr/train.txt                 FR~ 95.8%  (3.426 Go)`
- **T1** `data/wiki_big/brut.txt                        FR~ 95.5%  (1.048 Go)`
- **T1** `data/corpus_pdf/train.txt                     FR~ 16.5%  (0.296 Go)`
- **T1** `data/corpus_pdf_documents/train.txt           FR~ 14.7%  (0.803 Go)`
- **T1** `data/corpus_en.txt                            FR~  1.6%  (0.100 Go)`
- **T1** `data/corpus_mixte.txt                         FR~ 53.5%  (0.011 Go)`
- **T1** `data/wiki_multi/train.txt                     FR~ 41.3%  (0.275 Go)`
- **T1** `data/corpus_multi.txt                         FR~ 17.4%  (0.122 Go)`
- **T1** `data/corpus_fr_litterature.txt                FR~ 97.5%  (0.017 Go)`
- **T1** `data/wiki_mix/propre/train.txt                FR~ 95.3%  (1.017 Go)`
- **T1** `[still running after 60000ms; moved to background job bash-468]`
- **T1** `data/corpus_pdf/train.txt accentués 0.29%`
- **T1** `data/corpus_pdf_documents/train.txt accentués 0.33%`
- **T1** `échantillon 150 Mo, fenêtre 96 o, pas 16 o`
- **T1** `shingles 9374994, dupliqués 67770 (0.72 %)`
- **T1** `(`porte-indice`, `porte-melange`) + `porte-bloc-code` **transitoire** (×2,40 pour ×4 pendant la`
- **T1** `vides 247759 (24.8%), courts<80 458311 (45.8%)`

