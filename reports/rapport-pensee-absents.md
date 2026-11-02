# B13 — les absents : 0, les quatre étaient des faux

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **139/139 portes** : les **4 liens « absents »** du round précédent sont **0** après correction
> de la tokenisation : les mots étaient collés à la ponctuation (`dog;`, `letter;`), et le test
> les croyait hors du texte. Il n'y a **aucun antécédent absent** dans les 116 liens. La
> coréférence est **entièrement** résolue par la règle (51 intra + 65 inter).
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-absents.json`](pensee-absents.json).

## 1. Les classes corrigées

| classe | avant | **après** |
|---|---:|---:|
| intra-phrase | 50 | **51** |
| inter-phrase | 62 | **65** |
| **absents** | **4** | **0** |
| tout | 116 | 116 |

**Ce que ça dit** :

- **Les 4 absents étaient des faux** : `The cat sees the dog; it sleeps.` — le mot `dog;` (avec
  le point-virgule) n'était pas reconnu ; la tokenisation par `split()` était fautive.
- **La correction** : `re.findall(r"[a-zà-ÿ']+", texte.lower())` — les mots sont extraits sans
  ponctuation ; les 4 réapparaissent comme **inter-phrase** (l'antécédent est bien dans le texte).
- **Aucun antécédent absent** : dans ce gold, la règle résout **tous** les liens (51 + 65 = 116).
- **La leçon** : un « absent » peut être un **bug de mesure** ; il faut le nommer avant de le
  compter comme une limite.

## 2. Ce que ce banc ne dit pas

- **0 absent** ne veut pas dire que la règle est parfaite : elle a des erreurs (le plafond 86/103
  de la ligne anaphore), mais pas des antécédents manquants.
- **116 liens** : un échantillon.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 607** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la tokenisation** (les mots composés, les élisions) ;
- **le gold** ne contient pas de pronoms sans antécédent — c'est un biais du corpus ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les pronoms sans antécédent** : en ajouter au gold (le vrai absent) pour tester la limite.
2. **Le neuronal réel** : toujours bloqué.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `liens_absents`, tokenisation corrigée.
- [`autotest.py`](../tools/pensee/autotest.py) — T136, 139/139.
- [`pensee-absents.json`](pensee-absents.json) — les classes corrigées.
