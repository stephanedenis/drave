# La RSN — la fondation est posée et mesurée

> **Ce que ce document est.** La **première implémentation** de la représentation sémantique neutre :
> le module [`tools/rsn.py`](../tools/rsn.py), le chemin **surface → RSN**, les invariants, la
> couverture mesurée et ce qui manque encore. Le contrat complet est dans
> [`moteur-de-pensee.md`](../docs/implantation/moteur-de-pensee.md) ; la théorie dans
> [`pensee-iterative.md`](../docs/theorie/pensee-iterative.md).

## 1. Ce qui est construit

| brique | fichier | état |
|---|---|---|
| **le candidat** (`corps`, `annotation`, `statut`, `provenance`, `cout`, `score`) | `tools/rsn.py` | fait |
| **l'état** (`id`, `parent`, `profondeur`, `candidats`, `budget`, `empreinte`) | `tools/rsn.py` | fait |
| **la canonicalisation** (clés triées, UTF-8, aucun flottant dans `corps`) | `tools/rsn.py` | fait |
| **l'empreinte Merkle** (les candidats triés → une empreinte stable) | `tools/rsn.py` | fait |
| **surface → RSN** (l'`Annotation` → les faits et les prédications) | `tools/rsn.py` | fait |
| **le test des invariants** (5 contrôles) | `tools/tests/test_rsn.py` | 5/5 |

**La prédication** : un syntagme qui porte un **rôle** (`agent`, `prédicat`, `lieu`, `patient`,
`theme`, `possession`, `but`) et une **cible** devient un candidat `predication` — c'est la brique
du sens, celle que la pensée manipulera.

## 2. La mesure (20 phrases du gold, le 21/11)

| mesure | valeur | contrôle |
|---|---:|---|
| **la couverture** (phrases avec ≥ 1 prédication) | **19/20 = 95,0 %** | une phrase sans syntagme n'en a pas |
| **les candidats** | **34,5 / phrase** (689 au total) | le texte vide en a 0 |
| **le déterminisme** | la même empreinte sur deux analyses | `e98f3b8a…` |
| **l'ordre des candidats** | l'empreinte ne change pas | Merkle trié |
| **le contrôle négatif** (texte vide) | **0 candidat**, `refus = "vide"` | — |

**Les rôles trouvés** (les plus fréquents) : `agent` 16, `predicat` 5, `groupe nominal` 5,
`patient` 3, `lieu` 3, `but` 3, `theme` 2, `possession` 2.

## 3. Ce que ça permet, et ce que ça ne permet pas

**Ce que ça permet** : le moteur de pensée a **enfin** sa matière — un état de candidats avec un
statut, un score, une provenance et une empreinte rejouable. On peut **compter** les candidats,
**comparer** deux analyses (l'empreinte), **rejouer** (le même texte redonne le même état) et
**filtrer** (les `retenus`).

**Ce que ça ne permet pas encore** :
- **La désambiguïsation** : tous les candidats sont des hypothèses ; le premier tri (les prédications
  de confiance ≥ 0,7) n'en retient aucun sur la phrase de test (la confiance des syntagmes est
  souvent 0,40) — c'est un **seuil arbitraire**, à remplacer par un score appris.
- **La composition** : la RSN ne compose pas encore deux phrases (la référence, la coréférence, la
  temporalité).
- **Le sens** : la RSN est **structurée**, pas **interprétée** — elle ne dit pas *qui fait quoi* au
  sens profond ; elle donne les **prédications candidates**, ce qui est la bonne unité pour la suite.

## 4. Ce qui vient après (le chemin)

1. **Le score appris** : remplacer le seuil 0,7 par un modèle qui apprend quelles prédications
   retenir (la donnée : les annotations humaines du gold).
2. **La composition** : les liens entre prédications (le même agent dans deux phrases, la
   coréférence).
3. **Le state store** : les opérations `put`/`get`/`children`/`frontier`/`replay` du contrat
   (`moteur-de-pensee.md` § 2) — aujourd'hui l'état est en mémoire.
4. **Le gold de pensée** : les trajectoires humaines, sans lesquelles on ne peut ni entraîner ni
   mesurer un pas de pensée.

## 5. Les limites

- **20 phrases** n'est pas un banc : la couverture 95 % est un **démarrage**, pas une preuve. Le
  test sur les 612 phrases est à faire.
- **Le contrôle négatif** (le texte vide) est le seul ; il faut aussi un contrôle **positif**
  (une phrase connue → une prédication attendue) et un contrôle **adversarial** (une phrase
  ambiguë → deux candidats concurrents).
- **La RSN n'est pas versionnée comme un format public** : le schéma `drave.rsn` v1 est posé, il
  n'est pas encore dans `tools/schemas/` ni dans la roue.
