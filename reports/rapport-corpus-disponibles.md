# Les corpus disponibles — l'inventaire (le 22/11)

> **Ce que ce document est.** L'**inventaire** des corpus présents dans `data/` (137 Go), avec leurs
> volumes et ce qu'ils permettent. Il répond à la question « où est la donnée pour le palier
> 100–150 M sur 3–6 Go ? » — et la réponse est : **elle est déjà là**.

## 1. Le volume total

**`data/` : 137 Go.** Les corpus de texte (wiki par langue) :

| corpus | volume |
|---|---:|
| `corpus_wiki_en_texte/` | 21 Go |
| `corpus_wiki_ru_texte/` | 11 Go |
| `corpus_wiki_de_texte/` | 10 Go |
| `corpus_wiki_en/` | 9,3 Go |
| `corpus_wiki_fr_texte/` | 7,8 Go |
| `corpus_wiki_ja_texte/` | 6,9 Go |
| `wiki_mix_v2/` | 6,5 Go |
| `corpus_wiki_es_texte/` | 6,4 Go |
| `corpus_wiki_it_texte/` | 5,0 Go |
| `corpus_wiki_ru/` | 4,9 Go |
| `corpus_wiki_de/` | 4,5 Go |
| `corpus_wiki_ja/` | 4,2 Go |
| **`corpus_wiki_fr_palier1/`** | **3,6 Go** |
| `corpus_wiki_fr/` | 3,6 Go |
| les autres (ar, pt, es, zh, xnli, udhr…) | ~20 Go |

## 2. Le palier 1 existe déjà

**`data/corpus_wiki_fr_palier1/`** : `train.txt` **3,44 Go** + `val.txt` 73 Mo + `test.txt` 37 Mo.

**C'est exactement le « 3–6 Go » du diagnostic du 16/11.** Le corpus du 100 M actuel
(`wiki_mix/propre`, 1,017 Go) en est le **tiers**. Le palier 100–150 M sur 3–6 Go n'est donc
**pas bloqué par la donnée** : il est bloqué par **le temps de préparation** (le corpus doit être
nettoyé, dédupliqué, et le run doit être lancé).

## 3. Ce que ça change

Le diagnostic du 16/11 disait : « le premier pas utile est un 100–150 M sur 3–6 Go ». **La donnée
est là** ; le vrai coût est :

- **le nettoyage** : le corpus wiki contient du bruit (les titres, les liens, les articles courts) ;
- **la déduplication** : le wiki a des doublons (les redirections, les articles proches) ;
- **le temps GPU** : le 100 M à 0,29 s/pas ferait **30 000 pas en 2,4 h** sur 3,44 Go
  (≈ 27 tokens/paramètre — le bon ratio, contre 30 au 30 k sur 1 Go).

**La prédiction, à écrire d'avance** : sur 3,44 Go (27 tokens/paramètre), le 100 M devrait donner
**mots > 0,85, répétition ≤ 5, non-UTF-8 ≈ 0, PPL < 2,5** — et **ne pas sur-apprendre** au 30 k.

## 4. Ce qui manque

- **La licence du wiki** : Wikipédia est sous CC BY-SA 4.0 — l'usage est libre avec attribution ;
  **le corpus dérivé doit porter la licence**, et c'est à vérifier avant publication.
- **La qualité** : le wiki est **encyclopédique**, pas littéraire — la diversité (livres, presse,
  dialogues) manque. C'est le point du « ~98 % Wikipédia » déjà noté.
- **Le dédoublonnage** : non fait — c'est le premier chantier du palier.

## 5. La limite

**137 Go est un inventaire, pas un corpus.** Le tri, le nettoyage, la dédup et le mélange
(la recette de `wiki_mix_v2`) restent à faire — c'est **des heures de CPU**, pas des jours de GPU.
