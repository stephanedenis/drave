# La sélection du contenu : `wiki_big` seul, `wiki_fr` seul, le mélange — à pas égal sur wikitext2

> **Ligne de roadmap** : N (le palier 1) · **Date** : 2026-11-19 · **Verdict** : ⚠️ **partiellement tranché** — la
> **sélection du contenu** est bien la variable : sur wikitext2, `wiki_big` **seul** rend **7,2237**,
> v1 **7,3987** et v2 **7,4277** : ces trois-là sont **au même niveau** (le rejeu de la nuit donne **7,3531**, soit ±1,8 % de run-à-run) ; `wiki_fr` seul, le
> meilleur sur le val de v1 (2,8973), est le **pire** sur le val tiers (**8,0876**). Les résumés
> sur-apprennent leur distribution ; le long-forme (**8,1943**) est du même ordre. Seuls ces deux-là sont nettement décrochés (+9-11 %).
>
> **Dispositif** : deux chaînes `entrainer_native.py` (GPU 0 = `wiki_big`, GPU 1 = `wiki_fr`),
> 3 tranches de 10 000 pas, même recette que les runs précédents (lr 1e-4, AMP, `d=896`, graine 1,
> val de v1 épinglé) · banc complet après chaque tranche.

## Les sources

| corpus | octets | lignes | octets/ligne | nature |
|---|---:|---:|---:|---|
| `data/wiki_big/propre/train.txt` | 831 397 620 | 2 040 058 | **407,5** | articles longs, texte propre |
| `data/wiki_fr/propre/train.txt` | 186 089 472 | 440 709 | **422,3** | résumés, texte propre |
| `data/wiki_mix_v2/train.txt` (plein texte) | 6 900 585 097 | 63 438 199 | 108,8 | plein texte fragmenté |

v1 = les deux premiers ; v2 = le troisième. Les deux sources sont **épinglées** pour la
reproductibilité : [`corpus-epingle-wikibig.json`](corpus-epingle-wikibig.json) (`11aa9b74…`) et
[`corpus-epingle-wikifr.json`](corpus-epingle-wikifr.json) (`d2804870…`). La question : l'avantage de
v1 (7,3987 contre 7,4277 à pas égal, 3,2 % à 110 000 pas) vient-il d'une **source** ou de leur
**mélange** ?

## Les résultats à 30 000 pas (wikitext2, 352 256 jetons)

| corpus | PPL wikitext2 | PPL val v1 |
|---|---:|---:|
| **`wiki_big` seul** (831 Mo) | **7,2237** | 3,1144 |
| v1 (wiki_big + wiki_fr) | 7,3987 | 3,0763 |
| v2 (plein texte) | 7,4277 | 3,1922 |
| `wiki_fr` seul (186 Mo) | 8,0876 | **2,8973** |

## La réplication de la nuit (19-20/11) — et le bruit du run-à-run

La nuit a **rejoué `wiki_big` seul** (même recette, même graine, même corpus) : le pas 1 est
**bit-identique** (perte 5,6191, PPL 185,706), mais à 30 000 pas le run rend **7,3531** contre
**7,2237** l'après-midi — **+1,8 %**. La PPL du val de v1, elle, reste stable (3,1196 contre 3,1144,
+0,17 %). La dispersion vient donc de l'**entraînement** (non-déterminisme GPU), pas de
l'initialisation — et elle porte sur le **val tiers**, celui qui juge la sélection.

**Conséquence** : les écarts fins (`wiki_big` **7,22-7,35**, v1 **7,3987**, v2 **7,4277**) sont
**dans le bruit** du run-à-run (±1,8 %) ; seuls le **long-forme** (**8,1943**) et `wiki_fr` seul
(**8,0876**), à +9-11 %, en sortent. Une comparaison fine demanderait **2-3 graines par corpus**.

## La lecture

1. **La source, pas la forme** : `wiki_big` seul bat le mélange et le plein texte sur le val tiers ;
   le nettoyage et le recollement du plein texte étaient déjà écartés (7,62 et 7,75).
2. **Les résumés (wiki_fr) sur-apprennent** : premier sur le val de v1 (2,8973), dernier sur
   wikitext2 (8,0876) — à pas égal, ils sont vus 1,6 fois (186 Mo) contre 0,35 fois pour `wiki_big`
   (831 Mo) : c'est une question d'**époques**, pas seulement de contenu.
3. **Le mélange v1 paie la présence de wiki_fr** : 7,3987 contre 7,2237 pour `wiki_big` seul, soit
   **2,4 %** — le mélange dilue la source qui généralise.
4. **Conséquence pour le palier 1** : la sélection doit être **explicite** (des articles longs, type
   `wiki_big`), pas un héritage de la préparation — et l'équilibrage des époques compte autant que
   le volume.

## Ce qui est déjà établi

- **La forme n'est pas la cause** : le nettoyage (7,6189) et le recollement (7,7476) du plein texte
  sont **pires** que le brut (7,4277) sur le val tiers — voir
  [le test à trois](rapport-nettoyage-corpus.md).
- **Le val tiers confirme le val de v1** : v1 bat v2 sur les deux (6,867 contre 7,093 à 110 000 pas).
- **Les deux sources de v1 sont « propres »** (407-422 o/ligne) ; le plein texte est fragmenté
  (108,8) — mais la fragmentation n'explique pas le déficit (test ci-dessus).

## Ce qui pourrait le rendre faux

- **Une graine, un point de mesure** (30 000 pas) : les écarts attendus sont de l'ordre de 0,3-3 %.
- **La taille des corpus diffère** (831 Mo, 186 Mo) : à pas égal, `wiki_big` voit 0,35 époque et
  `wiki_fr` 1,6 époque — « pas égal » n'est pas « époque égale ».
- **wikitext2 est du Wikipédia** : les trois corpus en viennent ; le val mesure un style
  d'extraction autant qu'un contenu.

## Voir aussi

- [le test à trois](rapport-nettoyage-corpus.md) · [le val tiers](rapport-val-tiers.md) ·
  [le corpus v2](rapport-corpus-v2.md) · [les données](ppl-wikitext2.json) ·
  [le plan natif](../docs/pilotage/natif-plan.md)
