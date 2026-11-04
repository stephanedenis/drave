# B13 — les passifs : la règle de position se trompe (5/5 faux)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **161/161 portes** : la règle de position (`agent` si avant le GV) se trompe sur les **cinq
> passifs** testés (`Le chat est mangé par le chien.` …) : le **GN sujet est un patient**, et le
> **GP en `par`** est l'agent. La règle naïve donne `agent` au sujet et `moyen` au `par` — deux
> erreurs par phrase. La couverture 0,8195 de T157 est donc **surévaluée**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-passifs.json`](pensee-passifs.json).

## 1. Les cinq passifs

| phrase | sujet | `par` | rôle attendu | rôle obtenu |
|---|---|---|---|---|
| `Le chat est mangé par le chien.` | chat = **patient** | chien = **agent** | patient/agent | **agent/moyen** |
| `La souris est chassée par le chat.` | souris = patient | chat = agent | patient/agent | agent/moyen |
| `Le livre est lu par Paul.` | livre = patient | Paul = agent | patient/agent | agent/moyen |
| `La lettre est écrite par Marie.` | lettre = patient | Marie = agent | patient/agent | agent/moyen |
| `Le gâteau est fait par le boulanger.` | gâteau = patient | boulanger = agent | patient/agent | agent/moyen |

**Ce que ça dit** :

- **La règle de position est fausse sur les passifs** : le sujet d'un passif est un **patient**,
  pas un agent ; le `par` + GN est l'**agent**, pas un « moyen ».
- **La couverture de T157 est surévaluée** : 0,8195 supposait la position suffisante ; sur les
  passifs, elle est fausse. La vraie couverture dépend de la part des passifs dans le gold.
- **Le correctif est simple** : détecter `être` + participe + `par` + GN → le GN sujet devient
  `patient`, le GN du `par` devient `agent`.
- **La négative est explicite** : 5/5 faux, pas 5/5 juste.

## 2. Ce que ce banc ne dit pas

- **La fréquence des passifs** dans le gold 432 : non mesurée ici.
- **Les passifs sans `par`** (`Le livre est lu.`) : le rôle du sujet reste patient, sans agent.
- **L'heuristique** ; le neuronal ne fait pas le rôle.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **cinq phrases** : un échantillon ;
- **la définition du rôle** : `moyen` pour `par` est défendable en sémantique, pas en syntaxe ;
- **le gold** : 432 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le correctif `être + participe + par`** : inverser les rôles sur les passifs.
2. **Les passifs dans le gold** : les compter.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les rôles du GN.
- [`autotest.py`](../tools/pensee/autotest.py) — T158, 161/161.
- [`pensee-passifs.json`](pensee-passifs.json) — les cinq.
