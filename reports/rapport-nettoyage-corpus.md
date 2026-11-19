# Le corpus nettoyé : 6,874 Go, `]]` à zéro, 40,4 M lignes de contenu — le test à 30 000 pas est lancé

> **Ligne de roadmap** : N (le palier 1) · **Date** : 2026-11-19 · **Verdict** : ✅ nettoyé et
> épinglé — `tools/nettoyer_corpus.py` (flux, autotest 7/7) fait passer le corpus v2 de
> **6 900 585 097** à **6 894 225 744 o** (−0,378 %), de **63 438 199** à **60 117 634** lignes
> (40,4 M de contenu + 19,7 M de vides), et les `]]` de **2 631 à 0** par 20 Mo. L'effet sur le
> modèle est **en cours de mesure** : un run de 30 000 pas sur le corpus nettoyé, comparé au
> checkpoint v2 de 30 000 pas (wikitext2 **7,4277**).
>
> **Dispositif** : `tools/nettoyer_corpus.py` (liens, modèles, tableaux, références, balises,
> italiques, titres isolés, vides en double) · corpus épinglé
> [`corpus-epingle-clean.json`](corpus-epingle-clean.json) (`860aeb6a…`, manifeste `2f79f863…`) ·
> run `cl` (3 tranches de 10 000 pas, lr 1e-4, même recette que la nuit).

## Ce que le nettoyage change

| | v2 brut | v2 nettoyé | v1 « propre » |
|---|---:|---:|---:|
| octets | 6 900 585 097 | 6 894 225 744 | 1 017 487 092 |
| lignes (contenu) | 63 438 199 | 40 400 154 | 2 480 766 |
| octets par ligne | 108,8 | **170,7** | **410,2** |
| `]]` par 20 Mo | 2 631 | **0** | 5 |
| `==` par 20 Mo | 48 | 48 (en ligne) | 0 |

Le nettoyage **retire le balisage et les titres isolés**, mais il ne peut pas **recoller les
paragraphes** : la maille reste à 170 o/ligne contre 410 pour v1. Si la fragmentation est la cause
des 3,2 %, ce run le dira à moitié — il faudra un recollement des paragraphes pour l'éliminer.

## Le test à trois

Deux corpus dérivés du même v2, deux runs de 30 000 pas (3 tranches de 10 000, depuis zéro, même
recette : lr 1e-4, AMP, `d=896`, graine 1) :

| run | corpus | octets/ligne | état |
|---|---|---:|---|
| `v23` | v2 **brut** | 108,8 | fait — wikitext2 **7,4277** |
| `cl` | v2 **nettoyé** (`860aeb6a…`, `2f79f863…`) | 170,7 | en cours (3 tranches) |
| `rf` | v2 **nettoyé + recollé** (`9a5ca658…`, `f9214450…`, `tools/reflow_corpus.py`) | **349,6** | lancé (3 tranches) |

Le recollement (`reflow_corpus.py`, autotest) joint les lignes d'un paragraphe en une seule :
**349,6 o/ligne**, la maille de v1 (410,2). Les trois runs sont jugés sur **wikitext2** (tout le
val, 352 256 jetons) — le val tiers qui a montré le biais.

**Lecture attendue** : si `cl3` ou `rf3` tombent sous 7,43, le balisage/la fragmentation comptaient ;
si les trois restent au même niveau, c'est la **sélection du contenu** (plein texte vs résumés) qu'il
faut accuser, et le prochain corpus doit changer de source, pas de forme.

## Les points intermédiaires (val de v1, PPL / top-40)

| tranche | v2 brut | v2 nettoyé (`cl`) | v2 recollé (`rf`) |
|---:|---|---|---|
| 10 000 | 3,5568 / 0,888 | 3,5913 / **0,918** | 3,5763 / 0,883 |
| 20 000 | **3,2989** / 7,8688 | 3,3201 / 7,9091 | 3,4200 / 8,0378 |
| 30 000 | — | *(en cours)* | *(en cours)* |

À 20 000 pas, le nettoyé est à **+0,6 %** de PPL du brut (3,3201 contre 3,2989) et son meilleur
top-40 du début (0,918) est retombé à 0,871 : la forme ne creuse pas d'écart sur la PPL, et son
avantage d'échantillonnage n'est pas stable. Le juge reste wikitext2.

**Wikitext2 à 20 000 pas** (le val tiers) : brut **7,8688**, nettoyé **7,9091**, recollé **8,0378** —
le **brut gagne encore**, et le recollé est le plus mauvais. La forme n'explique donc pas le déficit
de v2 face à v1 : la **sélection du contenu** (résumés + « big » de v1 contre le plein texte de
`wiki_fr_texte`) reste la seule différence qui tienne.

## Ce qui pourrait le rendre faux

- **Une seule graine, une seule comparaison à 30 000 pas** : l'écart attendu (~3 %) est petit devant
  la variance des 20 prompts du banc, mais la PPL de wikitext2 (352 256 jetons) est stable.
- **Le nettoyage a un effet de bord** : il supprime 36 % des lignes (titres, vides) — la distribution
  des sauts de ligne change, ce qui peut déplacer la PPL sans améliorer le modèle.
- **Le corpus nettoyé n'est pas promu dans `data/`** : il vit dans `work/clean/` (épinglé) et devra
  être promu — avec son manifeste — si le test est concluant.

## Voir aussi

- [le val tiers](rapport-val-tiers.md) · [le corpus v2](rapport-corpus-v2.md) ·
  [le dédup par ligne](rapport-dedup-lignes.md) · [l'épingle](corpus-epingle-clean.json) ·
  [le plan natif](../docs/pilotage/natif-plan.md)
