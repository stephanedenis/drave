# B13 — le juge contre le bloc : 0/19, la première mesure de correction

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **128/128 portes** : le juge, désormais muni de **19 références**, mesure le **bloc** et
> l'**extraction** : **0/19** pour les deux. C'est la première mesure de **correction** (et non
> de présence) : le bloc ne répond pas (il rend `None`), l'extraction rend le GN (« le chat »),
> qui n'est jamais la réponse (« oui »).
>
> **Dispositif** : [`juge.py`](../tools/tests/linguistique/juge.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-juge-bloc.json`](pensee-juge-bloc.json).

## 1. Le juge contre le bloc

| candidat | questions | justes | **taux** |
|---|---:|---:|---:|
| bloc (réponse au contenu) | 19 | 0 | **0,0000** |
| extraction (GN) | 19 | 0 | **0,0000** |
| référence (le juge lui-même) | 19 | 19 | 1,0000 |

**Ce que ça dit** :

- **La correction est mesurée** : 0/19 n'est plus « pas de référence » (T123), c'est « le bloc
  et l'extraction ne répondent pas juste ». La différence est le **juge**.
- **Deux zéros, deux raisons** : le bloc rend `None` (il ne répond pas) ; l'extraction rend le
  sujet (« le chat »), qui ne peut pas être « oui ».
- **Le juge est calibré** : la référence fait 19/19 ; le bloc 0/19 — l'écart est la marge de
  progression, et elle est **totale**.
- **La négative est explicite** : un candidat qui rend la référence ferait 19/19 ; aucun ne le fait.

## 2. Ce que ce banc ne dit pas

- **Les 19 questions sont fermées** ; une réponse ouverte n'est pas jugée.
- **Le juge compare des chaînes** : « oui » et « Oui » sont égaux (normalisation), « oui » et
  « oui, demain » ne le sont pas.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de la référence** (une chaîne, pas le sens) ;
- **19 questions** : un échantillon ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Répondre par extraction dirigée** : chercher la réponse dans le texte (le GN qui suit le
   verbe), pas le premier GN — puis re-juger.
2. **Le neuronal réel** : toujours bloqué ; c'est lui qui répondrait.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`juge.py`](../tools/tests/linguistique/juge.py) — `juge_bloc`, `juge_extraction`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — les 19 références.
- [`autotest.py`](../tools/pensee/autotest.py) — T125, 128/128.
- [`pensee-juge-bloc.json`](pensee-juge-bloc.json) — les taux.
