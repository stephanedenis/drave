# R05 — le balayage : 0,984 de rappel@10 sur le lexical, 0,702 sur les paraphrases

> **Ligne de roadmap** : R0.4 (deuxième tête) · **Date** : 2026-10-29 · **Verdict** : ✅ **la
> porte 1 est franchie sur le lexical** (rappel@10 **0,984** ≥ 0,95) à **0,1 ms par requête** ;
> ⚠️ **0,702 sur les paraphrases**, là où une tête serait utile — et où R0.4 a montré qu'elle
> ne paie pas.
>
> **Dispositif** : `tools/index_spans.py` (spans de nombres et de dates, offsets dans le flux,
> classement par BM25 du passage porteur) ; porte `tools/porte-balayage.sh` (6 contrôles) ;
> JSON brut [`r05-balayage.json`](r05-balayage.json) ; spec
> [`tete-balayage.md`](../docs/implantation/tete-balayage.md).

## La question

La fiche R05 demande un **balayage classique d'abord** : retrouver les spans (nombres, dates)
qui répondent à une requête, avec des offsets exacts, avant d'ajouter une tête. La porte 1 :
**rappel@10 ≥ 0,95 sur les nombres et les dates**.

## Ce qui est mesuré

| banc | n | rappel@10 | temps |
|---|---:|---:|---:|
| lexical (249 questions) | 249 | **0,984** | 0,1 ms |
| paraphrases (84 questions) | 84 | **0,702** | 0,1 ms |

**Le chemin classique suffit sur le lexical** : quand la question partage ses mots avec le
document, le span qui porte la valeur est dans les dix premiers, en 0,1 ms. **Il ne suffit pas
sur les paraphrases** (0,702) — et c'est exactement là qu'une tête serait nécessaire.

## Les contrôles

| contrôle | résultat |
|---|---|
| offsets exacts (223 spans de `format-flux.md`) | ✅ tous dans le flux |
| rejeu (deux indexations) | ✅ identiques |
| recherche exacte « 3 663 » | ✅ offset 8036 |
| balayage de la question de référence | ✅ valeur dans les dix premiers |
| terme absent (« zorglub 42 ») | ✅ rien |
| **terme d'un autre document** (« drave », « billots ») | ✅ rien |

## Ce que ça dit

1. **Le balayage classique est acquis** : offsets exacts, rejeu, 0,1 ms. Il peut devenir une
   action du contrôleur — le branchement dans le pipeline reste à faire.
2. **La tête de balayage n'est pas ajoutée** : la porte 2 (« la tête bat BM25 sur les
   paraphrases ») est le même mur que R0.4 (0,575 contre 0,745) — elle est nommée, pas franchie.
3. **Le rappel@10 du lexical hérite du contrôleur** : le span index classe par le BM25 du
   passage ; il ne fait pas mieux que lui, il fait autre chose (des valeurs au lieu de phrases).

## Ce qui pourrait le rendre faux

- **le terme de la question est dans le span gold par construction** : sur le banc lexical, le
  rappel mesure surtout que BM25 retrouve la phrase ;
- **le classement est celui du passage** : deux spans d'une même phrase partagent leur score ;
- **les paraphrases** (0,702) : non résolues, et la tête qui devait les résoudre échoue ;
- **la tokenisation** : offsets en octets du **flux**, pas du fichier source.

## Fichiers

- `tools/index_spans.py` — l'index, la recherche exacte, le balayage, la mesure.
- `tools/porte-balayage.sh` — la porte à 6 contrôles.
- `docs/implantation/tete-balayage.md` — la spec.
- `reports/r05-balayage.json` — les mesures.
