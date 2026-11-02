# B13 — l'audit des mesures « seule » : 15/15 cohérentes, et un transfert qui manque

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **31/31 portes** : après le bug du round 31, les trois mesures (`seule`, `seule_sto`,
> `seule_minute`) rendent désormais leur **état final** et leur **chemin**. L'audit vérifie
> `but == (final == P_BUT)` et `pas == len(chemin)` sur **5 politiques × 3 mondes = 15/15**.
> Il révèle un **transfert manquant** : la politique entraînée sur la porte **minute** échoue
> sur la porte **stochastique** (état `open` jamais vu), là où la politique **stable** réussit.
>
> **Dispositif** : [`audit.py`](../tools/pensee/audit.py), [`courbe.py`](../tools/pensee/courbe.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-audit.json`](pensee-audit.json).

## 1. L'audit

Les trois mesures sont refactorées : `trace_seule`, `trace_seule_sto`, `trace_seule_minute`
rendent `(but, pas, état final, chemin)` ; les fonctions publiques n'en gardent que
`(but, pas)`. L'audit rejoue les 15 combinaisons et vérifie la cohérence.

| politique | stable | minute | stochastique |
|---|---|---|---|
| **stable** (T16) | but/8 | échec/200 | **but/9 (2 essais)** |
| **minute** (T21) | but/8 | **but/8** | **échec/200** |
| **complete** (T25) | but/8 | but/8 | **échec/200** |
| **reseau** | échec/200 | échec/200 | échec/200 |
| **mlp** | échec/200 | échec/200 | échec/200 |

**Ce que ça dit** :

- **La correction du round 31 est confirmée** : la politique minute atteint le but en 8 pas
  sur la porte minute ; la stable échoue (contrôle négatif).
- **Le transfert a un trou** : la politique entraînée sur la porte **minute** ne sait pas gérer
  l'état `open=True` (la porte stochastique ouverte) ; elle tourne (final `[3,0]`). La politique
  entraînée sur la porte **stable** voit ces états et réussit (9 pas, 2 essais).
- **Les réseaux échouent partout** : l'imitation des Q-tables ne conduit pas (T23/T24).
- **15/15 cohérentes** : la mesure ne ment plus ; le bug de comparaison est mort.

## 2. Ce que ce banc ne dit pas

- **5 politiques** seulement ; un curriculum complet sur les états `open` comblerait le trou.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **La porte stochastique** est indépendante (80 % à chaque essai) ; une porte qui apprend
  serait autre.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (les 5 politiques sont mesurées sur les 3 mondes) ;
- un **audit complice** de la mesure (non : `but` et `final` viennent du même chemin) ;
- un **A* caché** (non : les traces n'appellent que la Q-table) ;
- un **audit qui ne teste que la cohérence** et pas la **vérité** du but (le but est `P_BUT`,
  vérifié par la coordonnée finale).

## 4. La suite

1. **Curriculum des états `open`** : entraîner la politique minute sur la porte stochastique.
2. **Porte mobile** : la porte change de case ; mesurer la robustesse.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`audit.py`](../tools/pensee/audit.py) — l'audit, 15 combinaisons.
- [`courbe.py`](../tools/pensee/courbe.py) — les traces.
- [`autotest.py`](../tools/pensee/autotest.py) — T28, 31/31.
- [`pensee-audit.json`](pensee-audit.json) — les 15 lignes.
