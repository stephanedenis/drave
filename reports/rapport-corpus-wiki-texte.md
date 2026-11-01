# Le texte intégral de Wikipédia — le pilote FR

> **Verdict.** Le débaliseur `tools/corpus_wikipedia_texte.py` fonctionne : **100 000 articles**
> en **1,082 Go** (10,45 Ko par article), **1,045 G caractères**, **168,6 M mots** estimés, résidus
> **1 / 20 000 lignes** (`{{`), **0 / 6 661** fenêtres de 8 Ko de la validation retrouvées dans
> l'entraînement, **0 / 40** fenêtres des jeux d'évaluation. Le run complet (2,5 M) est lancé.
>
> **Date** : 2026-11-01. **Ligne** : Données (D/R/A). **Machine** : CPU seul.

## 1. La source

Les corpus `data/corpus_wiki_<langue>/` sont les **résumés** (`summary`) de la base v14,
**tronqués à 8 000 caractères**. Le dump `frwiki-latest-pages-articles-multistream.xml.bz2`
(**7,13 Go** compressés) porte les **articles entiers**. Le pilote mesure ce que le texte intégral
ajoute : **10,45 Ko par article** contre **1,46 Ko** de résumé en moyenne — la prose entière, les
sections, les listes, les paragraphes.

## 2. La méthode

`tools/corpus_wikipedia_texte.py` :

1. lit le dump en flux (`bz2` + `ElementTree.iterparse`) ;
2. garde l'espace de noms 0, sans redirection ; filtre `< 300` caractères ;
3. **débalise** : commentaires, `<ref>`, tableaux `{| … |}`, modèles `{{ … }}` (30 itérations),
   fichiers et catégories retirés, **liens remplacés par leur libellé**, titres de sections
   conservés, listes décapitées, entités HTML décodées, `&nbsp;` normalisé ;
4. **déduplique** les articles (BLAKE2b) ; les tronçons sont dédupliqués dans l'entraînement ;
5. **sépare** par article (hash salé du `page_id`, 5 % val, 5 % test) ;
6. écrit `train/val/test.txt` (les tronçons de 8 192 caractères, coupés aux mots), le **SHA-256**
   des trois fichiers et le **manifeste** JSON.

## 3. Le pilote (100 000 articles)

| grandeur | valeur |
|---|---:|
| pages lues | 146 250 |
| articles gardés | **100 000** |
| redirections écartées | 31 998 |
| articles trop courts (< 300 car.) | 3 574 |
| doublons d'articles | 0 |
| caractères gardés | **1 045 085 924** |
| mots estimés (car. / 6,2) | **168 562 245** |
| train / val / test | 972,6 Mo / 56,3 Mo / 52,7 Mo |
| articles train / val / test | 89 914 / 5 105 / 4 981 |
| résidus (`{{` / `[[` / `<`) sur 20 000 lignes | **1 / 0 / 3** |

**Aucune fuite entre splits.** Le contrôle standard (`verifie_contamination.py`, unité = ligne)
signale 3,66 % et 3,49 % de lignes dupliquées entre les splits — ce sont les **titres de sections
répétés** (« Biographie », « Notes et références »…), pas de la prose. Au **niveau du tronçon réel
(8 Ko)**, le contrôle refait à la main donne **0 / 6 661** (validation) et **0 / 6 228** (test) :
le corpus est propre à l'unité d'entraînement. Les **jeux d'évaluation** (XNLI fr, UDHR, jeux
locaux) donnent **0 / 40** fenêtres retrouvées.

**Ce que le débaliseur perd** : les **infobox** et les dates de modèles, les **formules `<math>`**,
les **tableaux** ; les liens deviennent des libellés, les titres de sections restent. La fiche
l'écrit : le texte est de la **prose encyclopédique**, pas l'article complet mis en forme.

## 4. La projection et le run complet

À 10,45 Ko par article, les 2,5 M d'articles donnent **~26 Go** de texte (contre 3,68 Go de
résumés pour le français). Le run complet est lancé :

```bash
python3 tools/corpus_wikipedia_texte.py \
  --sortie data/corpus_wiki_fr_texte --manifeste reports/corpus-wiki-fr-texte.json
```

Il écrit le corpus et son manifeste ; le prochain checkpoint commite le manifeste, refait la
contamination sur le corpus complet et met à jour l'état. Les neuf autres langues suivent le même
outil (`--langue de`, etc.).

## 5. Ce qui pourrait être faux

- **Le pilote n'est pas un échantillon aléatoire** : les 100 000 premiers `page_id` sont les
  articles les plus anciens ; le run complet donnera le volume réel (probablement plus de 26 Go).
- **Le débaliseur est regex** : les modèles non fermés, les tableaux imbriqués et les liens de
  légende peuvent laisser des résidus au-delà des 20 000 lignes mesurées.
- **La déduplication est exacte** : les quasi-doublons (traductions, copies) restent.
- **La licence** : CC-BY-SA 4.0 (et GFDL) — le corpus reste local, l'attribution et le partage à
  l'identique s'appliquent à toute diffusion.
- **Le contrôle 8 Ko est ad hoc** : il mérite d'entrer dans `verifie_contamination.py` comme
  option de taille de tronçon.

## Fichiers

- `tools/corpus_wikipedia_texte.py` — l'outil (dump → texte intégral).
- `reports/corpus-wiki-fr-texte-pilote.json` — le manifeste du pilote (SHA-256 des trois fichiers).
- `reports/corpus-wiki-fr-texte-pilote-contamination.json` — le contrôle du pilote.
- `data/corpus_wiki_fr_texte/` — le corpus complet (en cours d'écriture).
- `reports/corpus-wiki-fr-texte.json` — le manifeste du run complet (à venir).
