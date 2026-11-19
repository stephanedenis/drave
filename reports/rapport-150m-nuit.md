# Le palier 1 : deux 142 M, deux corpus, 110 000 pas — v1 garde la PPL, v2 gagne l'échantillonnage

> **Ligne de roadmap** : N (le palier 1) · **Date** : 18-19/11 · **Verdict** : ✅ mesuré — à **pas
> égal** (110 000 pas, 11 tranches de 10 000, lr 1e-4, même architecture, même val épinglé), le
> corpus **v1** (1,017 Go) converge à **PPL 2,844** et le corpus **v2** (6,90 Go dédupliqué) à
> **3,038** : **v1 est 6,4 % meilleur sur la PPL**, mais **v2 gagne le top-20 final** (0,948 contre
> 0,900) et les deux courbes **plafonnent** après ~60 000 pas.
>
> **Dispositif** : deux chaînes `entrainer_native.py` (GPU 0 = v2, GPU 1 = v1), 11 × 10 000 pas
> chacune (~0,42 s/pas), `--dim 896 --expert-hidden 896` (**141 935 400 paramètres**), AMP, graine 1,
> val **`data/wiki_mix/propre/val.txt`** (épinglé `fbddef91…`) · banc complet
> ([`checkpoint_bench.sh`](../bench/checkpoint_bench.sh), 20 prompts, 128 octets) après chaque
> tranche · données [`courbe-150m.json`](courbe-150m.json) · lr choisie par
> [la sonde](rapport-150m-lr.md).

## La courbe

| tranche | pas | PPL v1 | PPL v2 | top-40 v1 / v2 | top-20 v1 / v2 | précision v1 / v2 |
|---:|---:|---:|---:|---|---|---|
| 1 | 10 000 | 3,5088 | 3,5568 | 0,877 / 0,888 | 0,929 / 0,959 | 0,6305 / 0,6296 |
| 2 | 20 000 | 3,2186 | 3,2989 | 0,837 / **0,896** | 0,939 / 0,907 | 0,6531 / 0,6491 |
| 3 | 30 000 | 3,0763 | 3,1922 | 0,829 / **0,883** | 0,920 / **0,932** | 0,6664 / 0,6572 |
| 4 | 40 000 | 3,0007 | 3,1224 | 0,888 / 0,888 | 0,932 / 0,887 | 0,6750 / 0,6632 |
| 5 | 50 000 | 2,9583 | 3,0913 | 0,888 / 0,883 | 0,910 / **0,938** | 0,6768 / 0,6679 |
| 6 | 60 000 | 2,9141 | 3,0554 | 0,842 / **0,869** | 0,926 / **0,940** | 0,6823 / 0,6718 |
| 7 | 70 000 | 2,8919 | 3,0420 | 0,882 / **0,898** | 0,935 / 0,915 | 0,6839 / 0,6729 |
| 8 | 80 000 | 2,8731 | 3,0361 | 0,893 / **0,897** | 0,895 / **0,947** | 0,6868 / 0,6718 |
| 9 | 90 000 | 2,8590 | 3,0363 | 0,891 / **0,897** | 0,906 / **0,931** | 0,6868 / 0,6740 |
| 10 | 100 000 | 2,8452 | 3,0276 | 0,899 / 0,878 | 0,880 / 0,924 | 0,6883 / 0,6754 |
| **11** | **110 000** | **2,8440** | **3,0381** | 0,871 / 0,849 | 0,900 / **0,948** | **0,6878** / 0,6768 |

## Lecture

1. **Les deux courbes plafonnent** : v1 passe de 3,51 à 2,844 (−19 %) puis ne gagne plus que 0,1 %
   par tranche après 90 000 pas ; v2 de 3,56 à 3,038 (−15 %) et **stagne** dès la 6ᵉ tranche
   (3,0361 → 3,0363 entre 80 000 et 90 000, puis 3,0381 à 110 000 — dans le bruit). À 110 000 pas, le
   rendement est nul.
2. **La PPL favorise v1 de 6 %** — mais c'est **le val qui parle** : il vient de la famille de v1
   (résumés `wiki_fr`, une part de son train) ; v2 est du **plein texte** `wiki_fr_texte`, une
   autre extraction. Une PPL n'est comparable qu'à distribution de validation égale — ici elle
   mesure aussi le corpus, pas seulement le modèle.
3. **L'échantillonnage est un wash, avec un avantage v2 au top-20** : à la dernière tranche, top-40
   0,871 (v1) contre 0,849 (v2) mais top-20 **0,900 contre 0,948** ; sur les tranches 2 à 9, v2 gagne
   7 fois le top-20. L'écart est faible, dans la variance de 20 prompts.
4. **Le greedy est instable** : 9-14 de répétition, avec une pointe à **36** à la 6ᵉ tranche de v2 —
   un unique régime de 20 prompts suffit à produire une boucle extrême. Le décodage top-40/T=0,5
   reste le régime de production ([fiche](rapport-decodage-r1.md)).

## Les contrôles

- **Même recette, même architecture, même graine** : les deux chaînes partent du même code et du
  même init à 0,1 % près (perte au pas 1 : **5,6109** v1, **5,6184** v2 — pas bit-identique, noté).
- **Le banc après chaque tranche** (20 prompts, 128 octets, contrôle aléatoire n=128) : les métriques
  de génération sont comparables entre tranches et entre chaînes.
- **Le val est épinglé** (`fbddef91…`) et le corpus v2 l'est aussi (`9861fb39…`) : chaque chiffre
  nomme sa donnée.
- **La recette est justifiée** : lr 1e-4 (3e-4 ne casse pas le palier — [fiche](rapport-150m-lr.md)),
  et la percée a lieu vers 1 550 pas sur les deux chaînes.

## Ce qui pourrait le rendre faux

- **Le val est v1-centré** : le verdict « v1 meilleur » peut être un artefact de distribution. Un
  val tiré de **v2** (et tenu à l'écart de son train) est la prochaine mesure à faire.
- **Une graine, deux inits non bit-identiques** : l'écart de 6 % en PPL est bien au-dessus du bruit
  attendu, l'écart d'échantillonnage (0,5-2,5 points) non.
- **20 prompts, 128 octets** : le greedy à 36 de répétition montre la variance du banc.
- **110 000 pas = 0,9 milliard de jetons** : v1 a vu ~0,9 époque de son Go, v2 ~13 % de ses 6,9 Go —
  « pas égal » n'est pas « époque égale ».

## Ce que ça change

1. **Le palier 1 a sa recette** (142 M, lr 1e-4, AMP, ~0,42 s/pas, 110 000 pas en 13 h sur un GPU).
2. **La donnée ne paie pas encore** : à budget de pas égal, 6,9 Go ne battent pas 1 Go sur cette
   validation — mais le val est v1-centré. La prochaine expérience est un **val v2** et un run à
   **époque égale** (pas à pas égal), pas un run plus long.
3. **L'échantillonnage est la métrique qui bouge** : c'est elle qu'il faut suivre pour le palier 1,
   avec le décodage top-40/T=0,5.

## Voir aussi

- [la sonde de lr](rapport-150m-lr.md) · [le corpus v2](rapport-corpus-v2.md) ·
  [la courbe des 73 M](rapport-courbe-r1-r3.md) · [le décodage](rapport-decodage-r1.md) ·
  [les données](courbe-150m.json) · [le plan natif](../docs/pilotage/natif-plan.md)
