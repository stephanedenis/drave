# R0.2 — le contrôleur de lecture : 100 % de récupération à 30 % du budget

> **Ligne de roadmap** : R0.2 (et première tranche de R0.3) · **Date** : 2026-10-29 ·
> **Verdict** : ✅ le contrôleur **préserve la lecture intégrale** à **30 %** du budget sur
> les **5 types** — et le plafond n'est pas le contrôleur, c'est le **lecteur**.
>
> **Dispositif** : 20 questions, 5 types, 5 documents ; `tools/lecteur_controleur.py` +
> `tools/banc_lecture.py` ; porte `tools/porte-lecteur.sh` ; JSON brut
> [`r02-banc-lecture.json`](r02-banc-lecture.json) ; spécifications
> [`lecteur-controleur.md`](../docs/implantation/lecteur-controleur.md) et
> [`banc-lecture.md`](../docs/implantation/banc-lecture.md).

## La question

À **30 %** du budget, un contrôleur **classique** (survol, BM25, balayage, relecture,
arrêt) retrouve-t-il la réponse de la lecture intégrale — sur au moins **3 types** de
documents ? Et si oui, est-ce que cela suffit à lire ?

## Le dispositif

- **5 types, 1 document par type, 4 questions par type = 20 questions.** Technique, prose,
  tableau, juridique (un PDF réel), code.
- Chaque question porte un **indice** qui localise le passage gold (le harnais échoue si
  l'indice est absent) et une **valeur** courte qui doit se retrouver dans la réponse.
- **Le même lecteur** pour toutes les lectures : un extractif qui rend le passage le mieux
  scoré **avec sa citation**. Son index est celui du document entier : lire moins ne change
  pas son modèle de la question, seulement ce qu'il peut choisir.
- **Le budget est en octets lus.** Intégrale = 100 % ; contrôlée = 10 %, 30 %, 50 %.
- **Contrôles** : passages aléatoires au même budget (graine fixe), passages mélangés,
  question vide (« sans but »), closed-book.

## Ce qui est mesuré

| type | récup. à 30 % | valeur à 30 % | valeur à 100 % | coût à 30 % | aléatoire à 30 % |
|---|---:|---:|---:|---:|---:|
| technique | **1,000** | 0,750 | 0,750 | 2 567 o (**24,2 %**) | 0,500 |
| prose | **1,000** | 0,500 | 0,500 | 487 o (**6,9 %**) | 0,000 |
| tableau | **1,000** | 0,750 | 0,750 | 3 359 o (**17,3 %**) | 0,000 |
| juridique | **1,000** | 0,250 | 0,250 | 837 o (**22,5 %**) | 0,250 |
| code | **1,000** | 0,500 | 0,500 | 1 244 o (**20,5 %**) | 0,000 |

**Deux lectures de ce tableau, et il faut les deux.**

1. **Le contrôleur ne perd rien.** À 30 % du budget, il lit le passage gold dans **100 %**
   des cas sur les cinq types, et le taux de réponse est **exactement** celui de la lecture
   intégrale (0,25 à 0,75 selon le type). Le coût réel est de **7 à 24 %** du document,
   pour un plafond de 30 % : le critère d'arrêt s'arrête avant le budget.
2. **Le lecteur plafonne.** Même en lisant **tout**, le lecteur extractif ne trouve la
   valeur que dans **25 à 75 %** des cas. Le goulot n'est donc pas la sélection, c'est la
   lecture : un extractif lexical ne répond pas à une question dont la formulation ne
   partage pas les mots du passage.

C'est la réponse à la question de la roadmap, avec sa nuance : la **sélection** est un
problème de contrôleur (et il est résolu) ; la **compréhension** reste un problème de
modèle — et c'est R0.3, avec un modèle externe, qui doit le dire.

## Les contrôles négatifs

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **passages aléatoires** au même budget | récupération nettement plus basse | ✅ 0,000 à 0,500 contre **1,000** |
| **sans but** | ne pas répondre | ✅ valeur 0, F1 0 sur les cinq types |
| **closed-book** | aucune réponse | ✅ 0 réponse, F1 0 |
| **passages mélangés** | ne pas s'effondrer (l'ordre ne doit pas aider) | ✅ récupération 1,000 : le contrôleur ne dépend pas de l'ordre |

## Ce qui pourrait le rendre faux

- **Petit N** : quatre questions par type ; un cas vaut 0,25, et 1,000 sur quatre cas n'est
  pas un taux. Les chiffres disent « sur ce pilote », pas « en général ».
- **Contrôleur et lecteur partagent BM25** : « le choix du lecteur est toujours lu » est en
  partie structurel. Le chiffre **non circulaire** est la récupération du **gold** (1,000).
- **Les questions sont lexicales** : le banc ne dit rien des paraphrases. C'est assumé et
  écrit : les poser mesurerait le lecteur, pas le contrôleur.
- **Le corpus est choisi par l'auteur du banc** : cinq documents du dépôt, pas un
  échantillon. Le banc complet (30 documents, 300 questions) est R0.3.
- **Le gold est localisé par un indice** : l'indice prouve qu'un passage existe, pas qu'il
  est le meilleur gold.
- **Pas de temps** : le coût est en octets, pas en secondes. Un modèle lent changerait la
  conclusion sur le débit.

## Ce que ça change

R0.2 est **mesuré** : le lecteur a une politique qui ne perd rien à 30 %. La prochaine
action est **R0.3** : porter le banc à 30 documents et 300 questions, et **brancher un
modèle** pour savoir si le plafond de 25–75 % est celui du lecteur extractif ou celui du
document. Le contrôleur, lui, n'a plus besoin d'être amélioré pour passer la porte : il
faut maintenant lui donner un lecteur qui comprenne.

## Fichiers

- `tools/lecteur_controleur.py` — passages, BM25, cinq actions, budget, trace.
- `tools/banc_lecture.py` — les modes, les métriques, les contrôles.
- `tools/porte-lecteur.sh` — la porte.
- `docs/implantation/lecteur-controleur.md`, `docs/implantation/banc-lecture.md` — les specs.
- `tools/tests/documents/bench-pilote.json` — les 20 questions et leurs golds.
- `reports/r02-banc-lecture.json` — les mesures brutes.
