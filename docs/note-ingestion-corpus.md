# Note — l'ingestion des corpus, dans l'ordre demandé

> 06/10. Ordre fixé par Stéphane : **l'UDHR d'abord**, puis **Wikipedia**, puis
> **la littérature multilingue de Gutenberg**, en commençant par les œuvres au
> plus grand nombre de traductions.

## 1. UDHR — fait, et c'est le bon premier corpus

`/home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml/` — **456 langues**,
2,2 Mo, téléchargé depuis l'Internet Archive (le chemin `unicode.org/udhr/…` du
projet « UDHR in Unicode » renvoie **404** aujourd'hui ; l'archive le sert
encore).

| propriété | valeur |
|---|---|
| langues | **456** |
| **articles par langue** | **30 — dans TOUTES** |
| paragraphes de préambule | 58 à 67, variable selon la traduction |
| unité d'alignement stable | **l'ARTICLE** |

**13 680 unités sémantiques alignées par construction** — même texte, 456
langues, sans aligneur donc sans décalage possible. Format :
`<udhr iso639-3='eng' xml:lang='en' n='English'>` → `<preamble><para>` et
`<article>`.

## 2. Wikipedia — trouvé en local, rien à télécharger

`/home/stephane/Data13TB/stephane/nipada/wikipedia_decompressed/` — **81 Go**,
six langues :

| langue | fichiers | | langue | fichiers |
|---|---:|---|---|---:|
| en | 28 126 | | fr | 9 386 |
| de | 11 632 | | ru | 7 401 |
| es | 7 074 | | it | 1 970 |

Morceaux JSON de 150 articles, avec `title` et `page_id` — donc **appariables
entre langues par l'entité**. C'est la source des grappes de DOMAINE.

Et à ne pas confondre : `Panini-Research/data/wikipedia_ingestion/backlog_*.db`
porte des **files d'URL** (267 376 pour l'anglais), **pas du texte**.

## 3. Gutenberg — les œuvres parallèles, déjà repérées

`Panini-Research/data/mass_ingestion/backlog_gutenberg_*.db`, colonne `raw_text` :

| œuvre | langue A | langue B |
|---|---|---|
| Dumas, *Le comte de Monte-Cristo* | en, 460 989 mots | fr, 121 597 |
| Shakespeare, *Romeo and Juliet* | en, 25 976 | fr, 38 298 |
| Dostoïevski, *Crime and Punishment* | en, 206 549 | es, 176 258 |

« Le plus grand nombre de traductions » : ces trois-là d'abord, puis étendre par
téléchargement (Project Gutenberg a des traductions multiples de nombreux
classiques).

## 4. La méthode demandée, et ce qu'elle exige

> « grouper les œuvres multilingues en petits lots de paragraphes potentiellement
> identiques d'une langue à l'autre, et étiqueter correctement les grappes de
> connexions en fonction des langues. À cette étape-ci on s'intéresse plus à la
> traduction de petit contenu symétrique qu'au sens porté par l'ensemble d'un
> paragraphe. »

Traduction en étapes mesurables :

1. **Découper en petites unités alignées** — pour l'UDHR c'est déjà fait par
   construction (l'article, et ses paragraphes) ; c'est le corpus qui demande le
   moins de travail d'alignement et le moins de risque ;
2. **Faire passer chaque unité par les couches 0-9** et relever les activations
   **par unité de connexion** (dimension, tête, neurone) ;
3. **Étiqueter** : pour chaque connexion, deux mesures contradictoires —
   *invariante entre les 456 langues du même article* (elle porte le contenu) et
   *dépendante de la langue* (elle porte la forme) ;
4. **La grappe est l'ensemble des connexions qui basculent ensemble** avec la
   langue. C'est ce regroupement-là qu'il faut isoler, et il se **mesure** — il
   ne se postule pas.

**Ce que le « petit contenu symétrique » change** : on ne cherche pas à comparer
le sens d'un paragraphe entier, mais à apparier des unités courtes dont on sait
qu'elles disent **la même chose** dans deux langues. L'article 1 de l'UDHR est
cinq fois le même énoncé ; c'est le matériau le plus propre qu'on puisse avoir.

## 5. Ce qui existe, ce qui manque

**Existe** : `tools/invariance_semantique.py` (similarité inter-langue par
couche), `--trace-flux` / `--flux-forcer` (capture et rejeu exact, exige
`--lot 1`), `analyse_flux.py` (lecteur DRVF v1/v2/v3), `approximabilite_bloc.py`.

**Manque, dans l'ordre** :
1. un **extracteur UDHR** → `(langue, article, paragraphe) → texte`, qui rend les
   13 680 unités alignées ;
2. un **extracteur Wikipedia** → par entité et par langue, depuis les morceaux
   JSON locaux ;
3. l'**attribution par unité de connexion** (étape 3 ci-dessus) — le cœur, et
   l'extension de ce que `invariance_semantique.py` fait déjà par couche ;
4. **`profil_flux.py` est périmé** (lit la v1, plante sur la v3) : à réparer ou à
   retirer avant de s'en servir.
