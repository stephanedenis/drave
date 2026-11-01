# N2.j — Du vrai français : 186 Mo de Wikipédia, et ce que vaut le filtre « non ambigu »

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : entraîné sur **186 Mo** de
> Wikipédia français, le bloc linguistique vaut **7,42** sur la littérature et **12,41** en anglais,
> contre **12,29** et **32,90** pour la base du dépôt (×1,7 à ×2,6) — mais **6,72** sur le dépôt
> (décalage de domaine). Le filtre « phrases non ambiguës », lui, **ne paie pas** : il garde 29,8 %
> des phrases du dépôt (les **courtes**, 55 contre 153 caractères) et, à taille égale, il transfère
> **moins bien** que le hasard (11,81 contre 10,11 sur la validation du dépôt).

## La question

N2.i a montré que le corpus du dépôt (5,36 Mo uniques) **généralise** (littérature −22 %, anglais
−40 %) sans relever le domaine ; le recensement du 01/11 concluait : « il faut un corpus d'un autre
ordre ». L'inventaire local en donne un : **132 Go de Wikipédia** (10 langues), dont la base FR de
7,25 Go. Deux questions :

1. que vaut le **bloc linguistique** entraîné sur du vrai français, à recette identique ?
2. le filtre « **phrases non ambiguës** » — un générateur de candidats ne trouve qu'une lecture —
   aide-t-il, ou retire-t-il du signal ?

## Le dispositif

- **Corpus** : 120 000 articles FR (`n_chars` 800–40 000), **237,5 Mo** bruts ; déduplication par
  shingles de 96 octets → **206,7 Mo** uniques (−13,0 %, 56 506 runs) ; split par chunks de 8 Ko →
  **train 186,1 Mo**, val 10,3, test 10,3 ; **0 / 100** fenêtres de validation dans l'entraînement.
- **Base** : 11,47 M, 20 000 pas × 8 × 128 (20,5 Mo vus, 11 % du corpus), lr 3e-4, graine 1 —
  exactement la recette de N2.h.
- **Évaluation** : val/test du corpus, littérature, anglais, wikitext2, courbe 129→512,
  décomposition ; plus la **validation du dépôt** (transfert croisé).

## Ce qui est mesuré

| base | val (son corpus) | val du dépôt | littérature | anglais | wikitext2 | 256 octets |
|---|---:|---:|---:|---:|---:|---:|
| **dépôt (3,24 Mo)** | 3,2402 | 3,2402 | 12,29 | 32,90 | 33,29 | 11,72 |
| **wiki (186 Mo)** | 4,0284 | 6,7194 | 7,42 | 12,41 | 13,91 | 9,28 |
| **wiki + non ambigu** | 4,0494 | 6,7843 | 7,57 | 13,05 | 14,41 | 9,60 |

## Le filtre « non ambigu »

Le générateur de candidats ([`tools/structures`](../tools/structures/)) rend une structure, ou
plusieurs quand un segment (GP, relative) peut se rattacher à deux cibles. « Non ambigu » = une
seule structure trouvée.

| corpus | phrases | non ambiguës | octets | longueur moyenne |
|---|---:|---:|---:|---:|
| dépôt (train) | 20 239 | **29,8 %** | 345 Ko | 55,1 (contre 153,0) |
| Wikipédia (échantillon de 200 000) | 200 000 | **15,4 %** | ~1,7 Mo | courte aussi |

Deux bases de **345 Ko** (même budget, même recette) :

| base | val du dépôt | littérature | anglais |
|---|---:|---:|---:|
| **témoin** (phrases au hasard) | **10,1055** | 72,62 | 463,33 |
| **non ambigu** | 11,8054 | 75,98 | 477,84 |
| base pleine (3,24 Mo) | 3,2402 | 12,29 | 32,90 |

Le filtre **sélectionne les phrases courtes** (55 caractères contre 153) et, à taille égale, il
**transfère moins bien** que le hasard. À 345 Ko, les deux bases sont de toute façon très loin de la
base pleine : **le volume domine**.

### Le curriculum

Démarrer sur le non ambigu puis continuer sur le corpus complet est la seule façon d'utiliser le
filtre sans perdre de données : 2 000 pas sur les 1,7 Mo non ambigus, puis 18 000 pas sur les
186 Mo du wiki, contre 20 000 pas sur le wiki seul.

Inscrire **2 000 pas** sur les 1,7 Mo non ambigus avant les 18 000 pas sur le wiki **dégrade** légèrement tout : **4,0494** contre **4,0284** sur la val du wiki, **7,57** contre **7,42** en littérature, **13,05** contre **12,41** en anglais, **6,7843** contre **6,7194** sur le dépôt. L'effet est petit mais **cohérent sur les cinq mesures** : commencer par des phrases simples ne donne pas un meilleur bloc linguistique — les 10 % de pas passés sur une distribution étroite (phrases courtes, 55 caractères) coûtent plus qu'ils n'apportent.

## Ce que ça change pour N2

Le levier du bloc linguistique est le **corpus réel** : +186 Mo de français donnent ×1,7 à ×2,6 hors domaine, à recette et budget identiques. Le filtre non ambigu n'est pas un levier — ni en remplacement (à taille égale, il transfère moins bien qu'un témoin aléatoire), ni en préambule (le curriculum dégrade). Si la structure doit aider, elle doit être **ajoutée** au texte — un canal d'annotation — et non **retirée** du texte.

## Ce qui pourrait le rendre faux

- **Le texte wiki est du wikitexte nettoyé** : les titres de section sont collés au texte
  (« Biographie Enfance et formation… ») ; la PPL n'est pas comparable à celle du dépôt, et le
  « vrai français » y est encyclopédique, pas littéraire.
- **20 000 pas = 11 % du corpus** : la base n'est pas convergée ; un entraînement plus long dirait
  autre chose.
- **Le filtre est heuristique** : toute préposition déclenche une ambiguïté ; un détecteur plus fin
  doublerait peut-être la part non ambiguë, et le verdict changerait.
- **Licences** : Wikipédia est sous CC-BY-SA ; les textes ne sont **pas versionnés** (`data/` hors
  dépôt), seul le manifeste porte l'empreinte.
- **Un seul corpus, une seule graine** pour la base : les écarts OOD sont grands, mais l'intervalle
  n'est pas mesuré.

## Fichiers

- Extraction : `work/n2j/` (script d'extraction sqlite) ; corpus : `data/wiki_fr/`, manifeste
  [`corpus-wiki-propre.json`](corpus-wiki-propre.json).
- Filtre : `work/n2j/filtre_wiki.py` ; générateur : [`tools/structures/generateur.py`](../tools/structures/generateur.py).
- Points de contrôle : `work/n2j/base-wiki.pt`, `base-unamb.pt`, `base-curriculum.pt`.
- Mesures : `work/n2j/eval.json`, `work/n2j/eval-repo.json`.
