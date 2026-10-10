> Campagne : **campagne-benefices** · expérience **00**
> Titre : 0. Le piège qui a failli tout fausser
> Date réelle : **2026-10-08 21:32 HAE** (source : commit `89ae2c3`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 0. Le piège qui a failli tout fausser

`data/wikitext2_test.txt.ids` **vient d'un autre tokenizer** que Qwen2.5 :
`201,438,10498…` là où le modèle produit `198,284,8397…`. Sur les mêmes octets :

| identifiants | perplexité (256 jetons, ctx 512) |
|---|---:|
| ceux du dépôt | **7 710,72** |
| tokenisés par le modèle | **17,43** |

Un facteur 442. La règle est désormais dans le script : **chaque modèle tokenise
son propre corpus**. C'est aussi la première chose à vérifier avant de croire une
perplexité publiée quelque part.

---
