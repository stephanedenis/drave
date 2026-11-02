# B13 — la porte stochastique : 80 % d'ouverture, la politique réessaie

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **18/18 portes** : la porte ne s'ouvre plus qu'à **80 %** ; la `PolitiqueApprise` entraînée
> sur la porte déterministe affronte le bruit. L'A* + la sonde atteignent le but en **30 nœuds**
> (sonde 7, coût 68) : la politique **réessaie** quand la porte résiste.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-stochastique.json`](pensee-stochastique.json).

## 1. La porte stochastique

Même labyrinthe que T11, mais `sonde_p_sto` ouvre la porte avec **80 %** de probabilité ; en cas
d'échec, l'état **reste** (la politique doit réessayer). La politique est celle de T12
(200 épisodes, graine 0), entraînée sur la porte **déterministe**.

| essai | nœuds | sonde | coût | but |
|---|---:|---:|---:|---|
| **apprise + A*** | **30** | **7** | **68** | **oui** |

**Ce que ça dit** :

- **Le bruit ne bloque pas** : l'A* explore et la sonde réessaie ; le but est atteint en 30 nœuds,
  comme sur la porte déterministe.
- **La politique apprise transfère** : elle n'a pas été entraînée sur le bruit, mais elle vise
  toujours la porte ; le moteur gère les échecs.
- **Le coût est identique** (68) : les 7 appels de sonde incluent les essais.
- **Le vrai test serait la politique seule** sur le bruit : elle peut tourner si la porte
  résiste ; c'est la prochaine mesure.

## 2. Ce que ce banc ne dit pas

- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le bruit est indépendant** (80 % à chaque essai) ; une porte qui **apprend** ou se **corrompt**
  serait plus dure.
- **L'A* masque encore** la politique ; la politique seule sur le bruit n'est pas mesurée ici.
- **Le coût 5** de la sonde est déclaré.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (la porte s'ouvre au premier essai) ;
- un **A* trop fort** qui contournerait la porte (les murs l'en empêchent) ;
- un budget **trop grand** ;
- une confusion **politique / moteur** : la politique vise, le moteur réessaie.

## 4. La suite

1. **La politique seule sur le bruit** : combien de fois tourne-t-elle avant d'ouvrir ?
2. **Porte qui se referme** : après un pas, la porte se referme ; le moteur doit repasser.
3. **Porte apprise avec le bruit** : entraîner sur la porte stochastique.
4. **Politique DRVM/native** : un vrai modèle quand les poids seront là.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `LABYRINTHE_PORTE_STO`, `REGISTRE_PSTO`,
  `sonde_p_sto`.
- [`autotest.py`](../tools/pensee/autotest.py) — T15, 18/18.
- [`pensee-stochastique.json`](pensee-stochastique.json) — le bilan.
