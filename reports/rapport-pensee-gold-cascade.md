# B13 — la cascade complète : POS 0,9415, syntagmes 0,7539, acte 1,0

> **Ligne de roadmap** : **B13** (moteur de pensée) / **R0.7** (bloc linguistique) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **la cascade complète est mesurée** — POS **0,9415**, syntagmes exacts **0,6088**,
> **tête 0,7539**, acte **1,0**, fraction **0,6381**, **0 refus**, **180 + 180 appels**. Les
> **ablations sont exactes** : la cascade complète vaut la cascade POS (0,9415) **et** la cascade
> syntagmes (0,6088 / 0,7539) ; les parties s'additionnent sans perte. La politique de fusion
> reste le levier : **0,5670** avec la priorité heuristique contre **0,7539** avec `confiance`.
>
> **Dispositif** : [`qualifier_cascade.py`](../tools/tests/linguistique/qualifier_cascade.py) ;
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`NeuronalLLMCompose`) ; JSON
> [`pensee-gold-cascade.json`](pensee-gold-cascade.json).

## 1. Ce qui était mesuré

Les deux taggers étaient qualifiés séparément : POS **0,8483** seul / cascade **0,9440**
([`pensee-gold-neuronal`](rapport-pensee-gold-neuronal.md)) ; syntagmes **0,6173** exact /
**0,7606** tête, cascade `confiance` **0,7592**
([`pensee-gold-syntagmes`](rapport-pensee-gold-syntagmes.md)). Il restait à mesurer **le bloc
complet** — les deux taggers dans une seule annotation, la pragmatique de l'heuristique — et à
vérifier que les parties **s'additionnent** sans se détruire.

## 2. Le dispositif

- **Bloc** : `NeuronalLLMCompose(pos, chunks)` — `NeuronalLLMPOS` + `NeuronalLLMChunks`,
  appelés une fois par phrase, réunis en une `Annotation` `source = neuronal`. Un refus d'un
  des deux n'efface pas l'autre (annotation partielle).
- **Modèle** : Qwen2.5-7B-Instruct Q4_K_M, deux shards (SHA-256 dans le JSON), `llama-server`
  **b11017** en **CPU** (`-ngl 0`). **2 appels HTTP par phrase** (POS + syntagmes).
- **Cascade** : `Cascade(heuristique, compose, priorite_syntagme="confiance")` ; la
  pragmatique reste à l'heuristique (acte 1,0 sur le gold). La politique `confiance` est
  comparée à la politique par défaut (`heuristique`).
- **Gold** : 180 phrases, 804 tokens (20 réelles + 160 synthétiques), la même tokenisation que
  le bloc (180/180).
- **Ablations** : cascade POS seule (sans syntagmes), cascade syntagmes seule (sans POS),
  cascade complète, cascade complète avec la priorité par défaut. Les quatre lectures relisent
  les mêmes annotations (le cache évite 720 appels).
- **Commande** :
  `python3 tools/tests/linguistique/qualifier_cascade.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-gold-cascade.json`.

## 3. Les résultats

| lecture | POS 180 | synt. exact | synt. tête | acte | fraction |
|---|---:|---:|---:|---:|---:|
| **heuristique** | 0,7512 | 0,1992 | 0,5614 | 1,0000 | 0,6381 |
| **neuronal (composite)** | 0,8495 | 0,6090 | 0,7552 | 0,0000 | 0,0000 |
| **cascade POS seule** | **0,9415** | 0,2114 | 0,5657 | 1,0000 | 0,6381 |
| **cascade syntagmes seule** | 0,7512 | **0,6088** | **0,7539** | 1,0000 | 0,6381 |
| **cascade complète (confiance)** | **0,9415** | **0,6088** | **0,7539** | **1,0000** | **0,6381** |
| **cascade complète (défaut)** | 0,9415 | 0,2137 | 0,5670 | 1,0000 | 0,6381 |

- **La complète = POS seule ∪ syntagmes seuls**, exactement : POS 0,9415, syntagmes
  0,6088/0,7539, acte 1,0. Les deux taggers touchent des niveaux différents ; la fusion ne les
  mélange pas.
- **Le composite seul** : POS 0,8495, syntagmes 0,6090/0,7552 ; il ne rend pas la pragmatique
  (acte 0,0) et n'a pas d'unités sémantiques (fraction 0,0). C'est la cascade, pas le composite,
  qui est le bloc de production.
- **Les 20 réelles** : POS 0,9238, syntagmes 0,5000/0,6607, acte 1,0, fraction 0,4690.
  **Les 160 synthétiques** : POS 0,9442, syntagmes 0,6255/0,7682, acte 1,0, fraction 0,6592.
- **Le fermé/ouvert** : la cascade garde le fermé de l'heuristique (0,9392) et prend l'ouvert
  au modèle (0,9432) ; le composite seul est à 0,7751/0,9011.

## 4. Les ablations et la politique

| contrôle | POS | synt. exact | synt. tête | acte |
|---|---:|---:|---:|---:|
| cascade complète (confiance) | 0,9415 | 0,6088 | **0,7539** | 1,0 |
| cascade complète (défaut) | 0,9415 | 0,2137 | **0,5670** | 1,0 |
| cascade POS seule | 0,9415 | 0,2114 | 0,5657 | 1,0 |
| cascade syntagmes seule | 0,7512 | 0,6088 | 0,7539 | 1,0 |

- **La politique `confiance` vaut +0,1869 de tête** sur le défaut (0,7539 contre 0,5670) à POS
  et acte égaux. C'est la même leçon que la fiche des syntagmes : la règle de fusion est le
  goulot.
- **L'ablation POS** : sans le tagger POS, le syntagme ne gagne pas le POS (0,7512) ; sans le
  tagger de syntagmes, le POS ne gagne pas le syntagme (0,2114). Les deux sont nécessaires.
- **La pragmatique est préservée** : acte 1,0, négation 1,0, modalité 0,9944, double sens 0,8889
  — exactement l'heuristique. Le composite ne la dégrade pas parce qu'il n'y touche pas.

## 5. Les contrôles négatifs

- **Heuristique seule** : POS 0,7512, syntagmes 0,1992/0,5614, acte 1,0 — la référence.
- **Composite seul** : POS 0,8495, syntagmes 0,6090/0,7552, acte 0,0 — sans la pragmatique.
- **Cascade par défaut** : 0,9415 / 0,2137 / 0,5670 / 1,0 — la politique qui muselle.
- **Variance de run** : les fiches individuelles donnaient POS **0,9440** et syntagmes
  **0,6168/0,7592** ; la complète donne **0,9415** et **0,6088/0,7539**. L'écart (2 tokens de
  POS, ~6 de syntagmes) est la **variance de batching** du serveur, déjà observée (0,8483 vs
  0,8495) ; les ablations internes, elles, sont **exactement** égales. La composition n'ajoute
  pas d'erreur ; la bande de run est d'environ 0,005.
- **Les contrôles des deux fiches** (vide, BIO aléatoire 0,0419/0,1240, POS uniforme) restent
  valables : le composite utilise les mêmes taggers, avec les mêmes prompts et la même
  grammaire.

## 6. Le coût

- **180 appels POS + 180 appels syntagmes**, **0 refus** ; latence CPU moyenne **7,122 s**,
  médiane **6,761 s** (deux appels par phrase). La passe complète (six lectures, ablations,
  contrôles) dure **1 295,3 s** (~21,6 min).
- Le cache des taggers fait lire les six lectures avec **360 appels HTTP**, pas 2 160.
- Pas de mesure GPU : les deux Quadro RTX 5000 sont réservées à N2.

## 7. Ce qui pourrait rendre ce résultat faux

- **La bande de run** : les chiffres absolus varient de ~0,005 entre deux runs (batching) ;
  les écarts entre lectures (politique, ablations) sont mesurés dans le même run, donc plus
  fiables que les comparaisons entre fiches.
- **La pragmatique n'est pas neuronale** : acte 1,0 est l'heuristique ; le composite ne rend
  que POS et syntagmes. Un tagger de pragmatique reste à mesurer — et l'heuristique est déjà
  à 1,0 sur l'acte, donc le gain attendu est faible.
- **4 segments imbriqués** restent hors de portée du BIO ; l'exact est plafonné.
- **L'anglais** est hors domaine (20 réelles : 6 anglaises) ; la fiche des syntagmes le nomme.
- **Les 20 réelles ont servi au choix des prompts** ; les 160 synthétiques sont le test.
- **Une seule graine de serveur**, température 0, grammaire ; pas de répétition multi-graines.
- **La porte B13** est à 134/140 (six rouges de segmentation/anaphore corrélés au sous-module S
  `647205a`, hors tagger) ; la porte du bloc et les 15 tests sont verts.

## 8. La suite

1. **DRVM/native** : la politique du moteur de pensée reçoit un **vrai modèle** (`PolitiqueLLM`,
   préparée) ; mesurer le cadenas, le labyrinthe et la porte avec l'oracle, l'aveugle, le hasard
   et le LLM ; le coût réel (latence) à côté du coût symbolique.
2. **Pragmatique neuronale** : mesurer un tagger d'acte/négation/modalité ; si l'heuristique
   reste à 1,0, le résultat est un négatif nommé.
3. **200+ phrases réelles** : l'anglais et les conventions non vues.
4. **Production** : le composite est le bloc à brancher ; le coût est de deux appels par phrase.

## 9. Fichiers

- [`tools/tests/linguistique/qualifier_cascade.py`](../tools/tests/linguistique/qualifier_cascade.py) —
  le banc (six lectures, ablations, contrôles, JSON).
- [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) — `NeuronalLLMCompose`.
- [`tools/tests/linguistique/test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py) —
  le test du composite (15 tests au total).
- [`pensee-gold-cascade.json`](pensee-gold-cascade.json) — les chiffres, les seuils, les limites.
