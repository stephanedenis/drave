# R06 v2 — la cascade des lecteurs : +1,2 point, pour 9 appels de modèle

> **Ligne de roadmap** : R06 (relecture) · **Date** : 2026-10-29 · **Verdict** : ✅ **la
> cascade est le seul dispositif de relecture qui gagne** — **0,325** contre 0,313 (auto) sur
> les paraphrases, **0,976** sur le lexical, **0,450** au pilote — ⚠️ mais le gain des
> paraphrases coûte **9 appels de modèle** (18 s) pour **une question**.
>
> **Dispositif** : `lecture.py --lecteur cascade` (étage 1 : span ou extractif selon la forme ;
> étage 2 : le modèle si l'étage 1 refuse) ; trois jeux ; JSON
> [`r06-cascade.json`](r06-cascade.json) ; spec
> [`pipeline-lecture.md`](../docs/implantation/pipeline-lecture.md).

## Pourquoi une cascade

R06 a montré que « relire plus » ne change **jamais** la réponse extractive (0/249, 0/84) : la
relecture n'est pas un second passage, c'est un **changement de modalité**. La cascade est ce
changement, écrit : on essaie le lecteur le moins cher (span, extractif), et on ne paie le
modèle que si l'étage 1 refuse — c'est-à-dire quand le document ne partage rien avec la
question.

## Ce qui est mesuré

| jeu | cascade | auto (sans modèle) | appels modèle |
|---|---:|---:|---:|
| lexical (248) | **0,976** | 0,976 | **0** |
| paraphrases (83) | **0,325** | 0,313 | **9** |
| pilote (20) | 0,450 | 0,450 | **0** |

**Le gain est réel mais mince** : +1,2 point sur les paraphrases, +1 question sur 83, pour
9 appels de modèle et ~18 s. Ailleurs, la cascade ne coûte rien (0 appel) et ne change rien.

**Et le lexical progresse** : la voie auto sur le corpus gelé monte à **0,976** (contre 0,878
pour l'extractif seul) — le span et l'extractif se complètent mieux qu'avant la re-mesure.

## Ce que ça dit

1. **La cascade est correcte** : elle ne dégrade jamais (≥ l'auto partout) et paie le modèle
   seulement quand il peut servir. C'est le seul dispositif de relecture qui passe ce test.
2. **Son économie est mauvaise** : 9 appels pour 1 question. Le déclencheur (le refus à 1,0)
   est trop rare pour couvrir les cas où le modèle aiderait (R06 : il en manquait 15).
3. **Le problème n'est pas la cascade, c'est le déclencheur** — et les trois tentatives de
   seuil (R0.5, R06, cette cascade) montrent que la confiance lexicale ne le fournit pas.

## Ce qui pourrait le rendre faux

- **9 appels** : une question d'écart, du bruit à cette échelle ;
- **le seuil 1,0** : c'est lui qui décide quand le modèle s'appelle ; un seuil plus haut
  appellerait plus souvent, mais R0.5/R06 ont montré qu'il ne transfère pas ;
- **le corpus** : 83 paraphrases, un modèle de 0,5 B ; un plus grand modèle renverserait
  l'économie (le modèle seul ferait mieux, la cascade deviendrait inutile) ;
- **le coût** : 1,9 s par appel, non modélisé dans la décision.

## Ce que ça change

1. **Le pipeline a une politique complète** : extractif par défaut, `--auto` pour un corpus de
   valeurs, `--cascade` quand on accepte de payer le modèle sur les refus.
2. **La fiche R06 est réécrite** : la relecture = cascade, et son verrou est le déclencheur.
3. **La prochaine action est claire** : un déclencheur qui ne soit pas une échelle de scores
   (un accord entre lecteurs, une dispersion, une couverture) — ou l'acceptation du modèle seul
   sur les corpus de paraphrases.

## Fichiers

- `tools/lecture.py` — `--lecteur cascade` (étage 1 auto, étage 2 modèle).
- `reports/r06-cascade.json` — les mesures des trois jeux.
