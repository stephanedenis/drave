# B13 — le bilan de l'anaphore : 27/30, CV 0,847, huit mesures

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **109/109 portes** : la ligne **coréférence** est consolidée en **huit mesures** — les quatre
> règles (27/23/24/23), l'hybride, la méta (25), la CV (0,847), l'accord (κ). Le **plafond 27/30**
> est atteint par la règle la plus simple ; la **CV** le confirme hors échantillon (0,85 ± 0,05).
> Le **vrai modèle neuronal reste bloqué** : c'est la limite de la ligne, pas un résultat.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-bilan.json`](pensee-anaphore-bilan.json).

## 1. Les huit mesures

| mesure | valeur | fiche |
|---|---:|---|
| règle « dernier nom » sur tout | **27/30** | `rapport-pensee-anaphore-limite.md` |
| rôle (segments) | 23/30 | `rapport-pensee-anaphore-roles.md` |
| hybride (sujet rôle + objet proximité) | 24/30 | `rapport-pensee-anaphore-hybride.md` |
| sémantique (verbes) | 23/30 | `rapport-pensee-anaphore-semantique.md` |
| méta (vote) | 25/30 | `rapport-pensee-anaphore-meta.md` |
| CV 5 plis | 0,833 | `rapport-pensee-anaphore-cv.md` |
| CV 20 graines | **0,847 ± 0,051** | `rapport-pensee-anaphore-cv-graines.md` |
| accord κ (role/sémantique) | **1,00** | `rapport-pensee-anaphore-kappa.md` |

**Ce que ça dit** :

- **Le plafond est 27/30** : aucune règle, aucun vote, aucun poids ne le dépasse ; les trois
  cas restants demandent une **annotation sémantique** que le gold ne porte pas.
- **La CV confirme** : 0,85 hors échantillon, min 22/30, max 27/30 — le plafond revient au
  meilleur tirage.
- **Le désaccord est structuré** : κ = 1,0 entre rôle et sémantique, −0,16 avec le dernier nom ;
  les règles sont **complémentaires**, pas redondantes.
- **La limite est le modèle neuronal** : la cascade mesurée reste la seule lecture.

## 2. Ce que ce banc ne dit pas

- **30 liens** ; 100 liens resserreraient la CV.
- **Les cas ambigus** ne sont pas arbitrés par deux annotateurs.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (30 liens) ;
- **les annotations** (les cas ambigus tranchés à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **100 liens** : la CV se resserre-t-elle ?
2. **Deux annotateurs** : mesurer l'accord humain (kappa) sur les cas ambigus.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — les huit mesures.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T106, 109/109.
- [`pensee-anaphore-bilan.json`](pensee-anaphore-bilan.json) — le bilan.
