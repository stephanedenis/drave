# B13 — la réponse dirigée : 19/19, la première réponse juste

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **129/129 portes** : la **réponse dirigée** (pour une question fermée, `non` si la phrase nie,
> sinon `oui` ; dans la langue de la question) fait **19/19** — la première réponse **juste**
> mesurée par le juge. Le chemin : 17/19, puis 19/19 après avoir corrigé la **langue** (les deux
> questions anglaises répondaient « oui » au lieu de « yes »).
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`juge.py`](../tools/tests/linguistique/juge.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-reponse-dirigee.json`](pensee-reponse-dirigee.json).

## 1. Le chemin

| étape | justes | taux |
|---|---:|---:|
| bloc (réponse au contenu) | 0/19 | 0,0000 |
| extraction (GN) | 0/19 | 0,0000 |
| **dirigée (négation, langue de la question)** | **19/19** | **1,0000** |
| — avant la correction de langue | 17/19 | 0,8947 |

**Ce que ça dit** :

- **La négation suffit** pour ces 19 questions fermées : la réponse est `oui`/`yes` sauf si la
  phrase porte une négation — 19/19.
- **Le bug de langue était réel** : les deux questions anglaises répondaient « oui » ; la
  correction (la langue de l'annotation) donne 19/19. C'est le **contrôle négatif** du round :
  sans la langue, 17/19.
- **Ce n'est pas de la compréhension** : la réponse ne dépend que de la **surface** (la
  négation) ; une question ouverte, une question piège ou un contenu inversé la feraient
  échouer.
- **Le juge est enfin utilisé** : la référence (T124) sert, le bloc est mesuré, la réponse
  dirigée passe — la chaîne miroir → juge → mesure est complète.

## 2. Ce que ce banc ne dit pas

- **Les questions ouvertes** (le contenu libre) ne sont pas couvertes.
- **19 questions fermées** : un plafond facile.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la référence** est `oui`/`yes` pour toutes les questions : la réponse dirigée la retrouve
  par construction (la négation est rare) ;
- **le juge** compare des chaînes : « oui » et « yes » ne sont pas égaux ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les questions négatives** : ajouter des questions qui nient (`Ne viens-tu pas ?`) et voir
  si la réponse dirigée s'inverse correctement.
2. **Le neuronal réel** : toujours bloqué ; c'est lui qui répondrait aux questions ouvertes.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `repondre_dirigee`, `fidelite_dirigee`.
- [`juge.py`](../tools/tests/linguistique/juge.py) — `juge`, `couverture`.
- [`autotest.py`](../tools/pensee/autotest.py) — T126, 129/129.
- [`pensee-reponse-dirigee.json`](pensee-reponse-dirigee.json) — le chemin.
