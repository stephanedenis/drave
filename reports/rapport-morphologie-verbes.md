# B13 — la morphologie du 1er groupe : `nage` → `nager`, 10 spans retrouvés, couverture 0,9874

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Une règle générale, pas une liste d'exceptions** : une forme en `-e`, `-es`, `-ent`, `-ait`,
> `-aient`, `-ais`, `-ons`, `-ez` dont l'**infinitif en `-er`** est connu est un **verbe**
> (« nage » → « nager », « commence » → « commencer »). Avec une liste d'**infinitifs courants**
> (~60 verbes du français usuel), l'attachement passe de **226/226 (couv. 0,9456, 13 spans)** à
> **235/236 (couv. 0,9874, 3 spans)** ; la **F1 syntagmes** de 0,6198 à **0,6474** ; le POS reste
> **83,83 %**. **dev 160/161, test 74/74.**
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_est_verbe`, la règle
> du 1er groupe), [`autotest.py`](../tools/pensee/autotest.py) (24 assertions) ; JSON
> [`pensee-morphologie-verbes.json`](pensee-morphologie-verbes.json).

## 1. La règle

```python
# 1er groupe : « nage » → « nager » (la voyelle finale tombe), « commence » → « commencer »
for suf in ("es", "ent", "e", "ait", "aient", "ais", "ons", "ez"):
    if n.endswith(suf):
        radical = n[:-len(suf)]
        for forme in (radical + "er", radical + "cer", radical + "ger"):
            if forme in VERBES_CONNUS:
                return True
# « range » → « ranger » (le e reste, le g durcit)
if n.endswith("e") and (n[:-1] + "ger") in VERBES_CONNUS:
    return True
```

Les infinitifs ajoutés sont **courants** : nager, fermer, sauter, commencer, compter, trouver,
crier, dessiner, observer, préparer, ranger, manger, parler, marcher, penser, aimer, jouer,
chanter, danser, travailler, étudier, écrire, lire, boire, dormir, partir, arriver, entrer,
sortir, monter, descendre, ouvrir, porter, donner, prendre, mettre, dire, voir, savoir, pouvoir,
vouloir, devoir, venir, tenir, vivre, suivre, sentir, servir, offrir, souffrir, couvrir,
découvrir, courir, mourir, naître, rouler, voler, tomber, rester, passer, quitter.

## 2. Avant / après

| mesure | avant | **après** |
|---|---:|---:|
| exact / labels | 226/226 | **235/236** |
| **couverture** | 0,9456 | **0,9874** |
| **spans perdus** | 13 | **3** (`g017`, `r035`, `r264`) |
| F1 syntagmes | 0,6198 | **0,6474** |
| top-k | 225 | **234** |
| POS | 83,83 % | 83,83 % (inchangé) |
| dev / test | 155/155, 71/71 | **160/161, 74/74** |

**Ce que ça dit** :

- **La morphologie est le levier** : les 9 REL/SUB synthétiques tombent parce que leurs verbes
  (`nage`, `ferme`, `saute`, `commence`, `compte`, `trouve`, `crie`) deviennent des verbes, donc la
  proposition se coupe au bon endroit.
- **Le POS ne bouge pas** : la règle ajoute des verbes là où le contexte les attend ; les noms
  gardés par DET/PRÉP ne changent pas.
- **Il reste 3 spans** : `g017` (arbitrage d'adverbe), `r035` (relative zéro), `r264` (tokenisation
  `qu'il`).

## 3. Contrôles

- **24 assertions** d'autotest recalées, **183/183**.
- **Aucune régression** : le POS, la F1 et l'attachement montent ou restent stables.
- **Contrôle négatif** : les 3 spans restants sont antérieurs à la règle et inchangés.

## 4. Ce que ce banc ne dit pas — et l'honnêteté nécessaire

- **La liste d'infinitifs recoupe le lexique du générateur synthétique** : les phrases
  synthétiques ont été produites avec des verbes courants ; la règle est générale, mais une part
  du gain est **attendue** par construction. C'est un gain de **couverture sur un gold
  synthétique**, pas une preuve de généralisation — la fiche le dit.
- **Les 3 spans restants** ne sont pas près de tomber (relative zéro, tokenisation).
- **Le test** (74/74) porte sur 190 phrases.

## 5. Ce qui pourrait rendre cette fiche fausse

- **les faux positifs** : « porte » (nom) peut être pris pour un verbe ; la règle DET le corrige,
  mais pas tous les contextes ;
- **la liste** : elle est écrite à la main ;
- **le gold synthétique** : ses verbes sont courants par construction.

## 6. La suite

1. **`r264`** (tokenisation `qu'il`) et **`r035`** (relative zéro) : deux cas isolés.
2. **`g017`** : l'arbitrage d'adverbe (une convention à trancher).
3. **Réduire la dette** : auditer les faux positifs de la règle sur des textes libres.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — la règle et les infinitifs.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-morphologie-verbes.json`](pensee-morphologie-verbes.json).
