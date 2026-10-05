# Note — les corpus de Panini-Research, et ce qu'ils permettent de mesurer

> Relevé du 06/10. Source : `/home/stephane/Data13TB/stephane/GitHub/Panini-Research`.

## 1. Où est le TEXTE (et où il n'est pas)

Deux familles de bases, et il faut les distinguer avant de compter :

| famille | contenu | verdict |
|---|---|---|
| `data/wikipedia_ingestion/backlog_<lang>.db` | **files d'URL** (`url_hash, url, status, byte_size, lang`) — 267 376 pour l'anglais, 99 565 pour le chinois, 11 langues | **pas du texte** : des listes de travail |
| `data/mass_ingestion/backlog_*.db` | `item_hash, source, lang, title, author, url, **raw_text**, v14_signature, word_count, ingested_at, status` | **le texte est là** |

## 2. Ce qu'il y a réellement

| corpus | documents | mots | texte |
|---|---:|---:|---:|
| gutenberg_en | 13 | 2 891 852 | 16,3 Mo |
| gutenberg_es | 10 | 1 559 905 | 9,2 Mo |
| gutenberg_de | 10 | 1 197 274 | 8,0 Mo |
| gutenberg_fr | 11 | 945 494 | 5,8 Mo |
| wikipedia_en | 20 935 | 2 080 862 | 13,0 Mo |
| wikipedia_de | 18 740 | 1 449 738 | 10,7 Mo |
| wikipedia_fr | 15 636 | 1 334 668 | 8,3 Mo |
| **total** | **55 380** | **11 464 573** | **~71 Mo** |

## 3. Les ŒUVRES PARALLÈLES — c'est le gisement qui compte

Trois œuvres existent en plusieurs langues **dans le corpus** :

| œuvre | langue A | langue B |
|---|---|---|
| Dumas, *Le comte de Monte-Cristo* | en, 460 989 mots | fr, 121 597 mots |
| Shakespeare, *Romeo and Juliet* | en, 25 976 mots | fr, 38 298 mots |
| Dostoïevski, *Crime and Punishment* | en, 206 549 mots | es, 176 258 mots |

**Même sens, forme de surface différente, texte littéraire entier.** C'est exactement
ce qu'il faut pour séparer, dans les premières couches, ce qui relève de la LANGUE
et ce qui relève du CONTENU.

## 4. Le plan que ces corpus permettent

**Étape 1 — les grappes linguistiques.** Commencer par *Romeo and Juliet* (le plus
court, et un dialogue : alignement par scène naturel) :

1. aligner des passages EN/FR ;
2. les faire passer par les couches 0-9 et **relever les activations par UNITÉ**
   (dimension, tête, neurone) ;
3. pour chaque unité, comparer deux corrélations : *même contenu, autre langue*
   contre *autre contenu, même langue*.

Une unité invariante à la langue porte du **contenu** ; une unité qui bascule avec
la langue porte de la **forme**. Le partage donne les grappes à isoler — mesuré,
pas supposé.

**Étape 2 — le vocabulaire de chaque œuvre et de chaque domaine.** Même méthode,
avec la variable « œuvre » puis « domaine » (Wikipedia en/de/fr) au lieu de
« langue ».

**Étape 3 — la rétroaction.** La carte langue/contenu dit quelle part des couches
0-9 la distillation doit reproduire : le contenu. Le reste est de la forme, et
c'est elle qu'un modèle récurrent peut porter à faible coût.

## 5. Ce qui existe déjà pour le faire

- `tools/invariance_semantique.py` — similarité inter-langue **par couche** (écrit
  ce soir, mesuré sur une paire de phrases : plateau à la couche 23 sur 48) ;
- `--trace-flux` / `--flux-forcer` — capture et rejeu **exact** du flux à l'entrée
  de chaque couche (nécessite **`--lot 1`** : le mode lot est dense, donc sans
  événements — mesuré) ;
- `analyse_flux.py` (lecteur DRVF v1/v2/v3), `profil_flux.py` (**périmé**, lit la
  v1 et plante sur la v3 — à réparer ou à retirer) ;
- `tools/approximabilite_bloc.py` — borne d'approximabilité d'un bloc (couches 0-9 :
  R² 0,19 après dix couches avec deux directions seulement, borne inférieure).

## 6. Ce qu'il reste à écrire

1. **un extracteur** `mass_ingestion` → texte brut, par œuvre et par langue
   (la colonne `raw_text` est là, le schéma est en §1) ;
2. **l'alignement** des passages parallèles (par scène pour Shakespeare, par
   chapitre pour Dumas) ;
3. **l'attribution par unité** — l'extension du §4-étape 1, qui est le cœur.
