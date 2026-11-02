# B13 — la mesure corrigée : `seule_minute` rendait de faux échecs

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **30/30 portes** : un **bug de mesure** dans `seule_minute` comparait un triplet `(x, y, open)`
> à `P_BUT` (un couple) : la comparaison était **toujours fausse**, donc la fonction rendait
> « échec » même quand la politique atteignait le but. Corrigé, **quatre politiques atteignent
> le but en 8 pas** ; les fiches T21, T22, T25, T26 sont **invalidées** et corrigées ; le
> contrôle (la politique entraînée sur la porte stable) échoue toujours.
>
> **Dispositif** : [`courbe.py`](../tools/pensee/courbe.py), [`autotest.py`](../tools/pensee/autotest.py),
> JSON [`pensee-correction.json`](pensee-correction.json).

## 1. Le bug

`seule_minute` (dans `courbe.py`) faisait :

```python
cle, pas = (0, 0), 0
...
if cle == P_BUT:          # (4, 4) contre (4, 4, False) : toujours faux
    return True, pas
cle, _ = p._pas((cle[0], cle[1], False), a, True)   # rend un triplet
```

Le triplet ne peut jamais égaler `P_BUT` ; la fonction rendait `False` après 8 pas (le `propose`
renvoie `None` au but) ou après 200 pas (la politique sans `None`). **Quatre fiches** ont conclu
« la politique seule échoue » sur cette base.

## 2. La mesure corrigée

| politique | avant (bug) | après (corrigé) |
|---|---|---|
| minute entraînée (T21) | échec/8 | **but/8** |
| shaping (T22) | échec/8 | **but/8** |
| professeur complet (T25) | échec/8 | **but/8** |
| sans None (T26) | échec/200 | **but/8** |
| stable entraînée (T20, contrôle) | échec/200 | **échec/200** |
| réseau linéaire (T23) | échec/200 | **échec/200** |
| MLP (T24) | échec/200 | **échec/200** |

**Ce que ça dit** :

- **Le bug était dans la mesure, pas dans le modèle** : les quatre politiques entraînées sur la
  porte minute **atteignent le but en 8 pas**, le chemin optimal.
- **Le contrôle tient** : la politique entraînée sur la porte **stable** échoue sur la minute
  (200 pas) ; le réseau et le MLP échouent aussi. La correction ne rend pas tout vrai.
- **La discipline a payé** : la porte T27 (positive + négative) est née de la correction ;
  elle vérifie que la minute réussit **et** que la stable échoue.
- **Quatre fiches corrigées** : T21, T22, T25, T26 portent désormais un avertissement en tête
  et leurs chiffres sont remplacés par les vrais.

## 3. Ce que ça change pour la thèse

- **La Q-table tabulaire suffit** sur ce jouet : la politique seule atteint le but en 8 pas ;
  l'A* n'était nécessaire que pour les politiques **non entraînées sur la bonne transition**
  (la stable, le réseau, le MLP).
- **Le « professeur incomplet »** (T25) était un artefact : la politique complète existe ; ce
  sont les imitateurs (T23/T24) qui échouent, pas le professeur.
- **La leçon de méthode** : un retour `False` sans trace ne prouve rien ; la comparaison de
  structures doit être testée (T27 le fait).

## 4. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (les quatre politiques sont mesurées sur 8 pas, pas 200) ;
- un **A* caché** (non : `seule_minute` n'appelle que la Q-table) ;
- une **correction qui masque** un autre bug (T20/T23/T24 restent des contrôles négatifs) ;
- un **chemin** qui ne serait pas le plus court (8 = Manhattan, vérifié).

## 5. La suite

1. **Étendre la correction** : vérifier les autres mesures (`seule_sto`, `seule`) par un test
   de structure.
2. **Curriculum** : maintenant que la politique complète existe, mesurer sa **robustesse**
   (portes mobile, bruit).
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 6. Fichiers

- [`courbe.py`](../tools/pensee/courbe.py) — `seule_minute` corrigé.
- [`autotest.py`](../tools/pensee/autotest.py) — T21/T22/T25/T26 corrigées, T27 ajoutée, 30/30.
- [`pensee-correction.json`](pensee-correction.json) — les mesures avant/après.
