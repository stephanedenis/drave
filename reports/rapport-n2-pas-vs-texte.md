# N2.ab — Plus de pas paie ; plus de texte paie en largeur, pas en français

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : à 60 000 pas, le corpus de
> **186 Mo** vaut **3,4365** sur sa validation (N2.z à 40 000 pas : 3,5250) et le corpus de
> **831 Mo** vaut **3,3301** sur la sienne (3,4604 à 40 000 pas) : **plus de pas paie sur les deux**
> (+0,09 à +0,13). Mais le corpus de 831 Mo **gagne en largeur** — anglais **8,32** contre 9,52,
> wikitext2 **9,16** contre 10,71 — et **perd en français** : littérature 6,14 contre 6,00,
> validation fr 3,59 contre 3,44. **Le corpus est un échange, pas un gain.**

## Le dispositif

- Deux corpus : 186 Mo (N2.j) et 831 Mo (N2.aa) ; la même recette : 34,3 M, 60 000 pas × 8 × 128,
  positions [0, 384], canal de structure.
- Évaluation croisée (les deux validations) + hors domaine avec le canal : littérature
  (`data/corpus_fr_litterature.txt`), anglais (`data/corpus_en.txt`), wikitext2.

## Ce qui est mesuré

| modèle | pas | val fr | val grand | littérature | anglais | wikitext2 |
|---|---:|---:|---:|---:|---:|---:|
| N2.z (186 Mo, 2 étages) | 40 k | **3,5250** | 3,7107 | — | — | — |
| grand (831 Mo, 2 étages) | 40 k | 3,7025 | **3,4604** | — | — | — |
| **fr-60k** (186 Mo) | 60 k | **3,4365** | 3,7237 | **6,0011** | 9,5185 | 10,7138 |
| **big-60k** (831 Mo) | 60 k | 3,5877 | **3,3301** | 6,1381 | **8,3173** | **9,1609** |

## Lecture

**Le compute paie, et c'est le levier le plus sûr.** Les deux modèles gagnent ~0,1 en passant de
40 k à 60 k pas sur leur propre validation — un seul étage de 60 k bat même les deux étages de
N2.z (40 k) en français (3,4365 contre 3,5250).

**Le corpus paie en largeur.** Le modèle de 831 Mo est **1,20 PPL meilleur en anglais** et **1,55
meilleur sur wikitext2** : les 600 000 articles (offset 1 M) contiennent plus de monde, et le
modèle l'utilise. C'est le premier gain OOD net de la ligne N depuis N2.j.

**Mais il perd en français proche.** Sur la littérature (Verne), 6,14 contre 6,00 ; sur la
validation du corpus de 186 Mo, 3,59 contre 3,44. Le corpus de 186 Mo est **plus proche** de ces
textes.

**La validation n'est pas neutre.** Comparer des corpus sur la validation de l'un d'eux, c'est
comparer des domaines. Les mesures **hors domaine** (anglais, wikitext2, littérature) sont les
seules qui disent la **largeur** ; la validation dit la **proximité**.

## Ce que ça change pour N2

- **Deux corpus, deux usages** : le 186 Mo pour le français de production (le plus proche), le
  831 Mo pour la largeur (anglais, monde) — ou un mélange à tester.
- **Le levier testable** est le **compute** : 60 k pas donnent 3,44 en français ; 200 k pas
  devraient donner ~3,3 sans changer de corpus.
- La **littérature** et l'**anglais** deviennent les mesures de choix pour comparer les corpus ;
  la validation fr garde son rôle de proximité.

## Ce qui pourrait le rendre faux

- **Une graine par point**, deux corpus, trois jeux OOD : les écarts (0,1 à 1,5) sont nets, mais
  l'intervalle n'est pas mesuré.
- **60 k pas** : ni l'un ni l'autre n'est convergé ; à 200 k, l'écart de largeur pourrait grandir.
- **Le canal** est fourni aux deux ; les OOD sont évalués avec un canal recalculé sur leur texte
  (pas d'asymétrie).
- **La tranche 1 M–1,6 M est plus récente** que 200 k–320 k : une part de l'écart est temporelle.

## Fichiers

- Modèles : `work/n2w/fr-60k.pt`, `big-60k.pt` ; mesures : `work/n2w/eval-*.json`, `ood-*.json` ;
  outils : `work/n2w/{eval_croise,eval_ood_canal}.py`.
- Corpus : `data/wiki_big/` ; manifeste : `reports/corpus-wiki-big-propre.json`.
