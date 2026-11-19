# Le val tiers tranche : v1 gagne aussi sur wikitext2 (6,87 contre 7,09) — et la cause est la propreté, pas le volume

> **Ligne de roadmap** : N (le palier 1) · **Date** : 2026-11-19 · **Verdict** : ✅ mesuré — sur
> **wikitext2 français** (val tiers, 352 256 jetons, tout le fichier), le 142 M du corpus **v1** rend
> **PPL 6,8674**, celui du corpus **v2** **7,0930** (−3,2 % pour v1), le 73 M **7,3508**. Le
> classement de la nuit (v1 > v2) **tient hors du val v1-centré** — mais l'explication n'est pas
> « moins de données vaut mieux » : v2 est **plus sale** (`]]` **2 631** contre **5** par 20 Mo,
> `==` 48 contre 0), c'est du **plein texte brut dédupliqué**, pas du texte propre.
>
> **Dispositif** : `tools/ppl_ckpt.py` (l'architecture est lue dans le checkpoint, la PPL couvre
> **tout** le val — 43 lots de 8 × 1 024), checkpoints `v111`/`v211` (142 M, 110 000 pas) et `r5a`
> (73 M, 53 000 pas) · données [`ppl-wikitext2.json`](ppl-wikitext2.json).

## Les trois chiffres

| modèle | corpus | paramètres | pas | PPL wikitext2 |
|---|---|---:|---:|---:|
| `v111` | v1 (1,017 Go **propre**) | 141 935 400 | 110 000 | **6,8674** |
| `v211` | v2 (6,90 Go plein texte dédupliqué) | 141 935 400 | 110 000 | 7,0930 |
| `r5a` | v1 (73 M, référence d'échelle) | 73 366 568 | 53 000 | 7,3508 |

Sur le val de la nuit, v1 gagnait de 6,4 % ; sur wikitext2, de **3,2 %** — même sens, amplitude
plus faible. L'avantage de v1 n'est donc **pas** un pur artefact du val.

## Pourquoi v2 perd : la structure, pas les octets de balisage

Le balisage est un **marqueur**, pas la cause : `tools/nettoyer_corpus.py` (nouveau) retire le
balisage, les titres isolés et les lignes vides en double, et sur 30 Mo il n'enlève que **0,263 % des
octets** (30 000 000 → 29 921 269) — les `]]` pèsent quelques kilo-octets par 20 Mo. Ce n'est pas ça
qui coûte 3 %.

Ce qui diffère vraiment, c'est la **maille des lignes** :

| | v1 « propre » | v2 « dédupliqué » |
|---|---:|---:|
| octets par ligne | **410,2** | **108,8** |
| lignes | 2 480 766 | 63 438 199 |

v2 est **fragmenté** (titres, listes, paragraphes courts) : le modèle de bytes apprend une
distribution de sauts de ligne quatre fois plus dense, et c'est un autre problème que le texte long
de wikitext2. L'hypothèse à tester est donc **structurelle et de sélection** (v1 = résumés + « big »,
v2 = plein texte fragmenté), pas « du bruit dans les octets ».

## Les contrôles

- **Le même val pour les trois checkpoints**, tout le fichier (43 lots), même `seq`/`lot` : les
  chiffres sont comparables entre eux.
- **Le 73 M comme référence d'échelle** : il rend 7,35 — au-dessus des deux 142 M, l'échelle paie
  bien, ce qui rend le résultat v2 d'autant plus parlant.
- **Le sens est stable** entre deux vals de distributions différentes (v1-val et wikitext2) : v1
  gagne les deux fois.

## Ce qui pourrait le rendre faux

- **wikitext2 est aussi du Wikipédia** : les deux corpus partagent son domaine, et rien ne dit que
  les articles du *test* n'ont pas été vus (v2 couvre 2,15 M d'articles). Si v2 les avait vus, il
  aurait dû *gagner* : il perd, donc le biais joue au mieux contre lui.
- **La propreté est inférée d'un échantillon de 20 Mo**, pas d'un audit complet : les 2 631 `]]`
  sont un ordre de grandeur, pas un recensement.
- **Une graine, deux inits non bit-identiques** (noté dans la fiche de la nuit).
- **Le corpus v2 n'a pas de val propre** : c'est précisément le prochain dispositif à construire.

## Ce que ça change

Le palier 1 ne doit pas chercher **plus** de données : il doit **défragmenter** les 6,9 Go
(supprimer les titres isolés, recoller les paragraphes) — le nettoyage est écrit
(`tools/nettoyer_corpus.py`, autotest 7/7) et le test est en cours : un run de **30 000 pas** sur le
corpus nettoyé, comparé au checkpoint v2 de 30 000 pas (**wikitext2 7,4277**). Si la structure est la
cause, la PPL doit tomber ; sinon, c'est la sélection du contenu qu'il faut revoir.

## Voir aussi

- [la nuit du palier 1](rapport-150m-nuit.md) · [le corpus v2](rapport-corpus-v2.md) ·
  [le dédup par ligne](rapport-dedup-lignes.md) · [les données](ppl-wikitext2.json) ·
  [le plan natif](../docs/pilotage/natif-plan.md)
