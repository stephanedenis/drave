# B13 — DRVF `thought` : la trace se relit, la corruption se voit

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **9/9 portes** : le flux `thought` fait **23 597 octets** pour **93 événements**, se relit,
> se rejoue **à l'identique** (`diff = None`), et **refuse** un score modifié (`diff = 0`).
> La trace n'est plus un objet en mémoire : c'est un **fichier** qui prouve.
>
> **Dispositif** : [`trace.py`](../tools/pensee/trace.py), [`autotest.py`](../tools/pensee/autotest.py),
> contrat [`moteur-de-pensee.md`](../docs/implantation/moteur-de-pensee.md) §6.

## 1. Le format

```
en-tête   "DRVF"                4 octets
          version     u16 = 1
          profil      u16 = 1 (thought)
          longueur    u32
charge    JSON canonique {probleme, racine, evenements}
```

La racine porte l'**état** complet (ses candidats), pour que le rejeu n'ait pas besoin du store
d'origine ; chaque événement porte `parent`, `enfant`, `operateur`, `params`, `score`, `cout`,
`strategie`, `pas`. Le **corps** n'est pas recopié à chaque pas : l'empreinte suffit, et le rejeu
**recalcule** l'enfant avec l'opérateur du problème.

## 2. Le rejeu

| étape | résultat |
|---|---|
| encoder (cruches, BFS, 200 nœuds) | **23 597 octets**, 93 événements |
| décoder | racine + 93 événements, profils/version/longueur vérifiés |
| rejouer | 93 enfants **recalculés**, mêmes empreintes, mêmes scores |
| `diff(trace, rejeu)` | **None** |
| score du premier événement +1 | **`ValueError`** — le rejeu refuse |
| `diff_fichiers(original, corrompu)` | **0** — le premier événement divergent est localisé |

## 3. La porte

`python3 -m tools.pensee.autotest` → **9/9** :

- T0 store canonique, T1 rejeu, T1 graine, **T1 DRVF thought**, T2 stratégies, T3 anytime,
  T4 justification, T5 AC-3, T6 alpha-bêta ;
- le contrôle négatif du DRVF est explicite : **un score corrompu ne se rejoue pas**.

## 4. Ce que cette fiche ne dit pas

- **Le payload est JSON** dans une enveloppe DRVF, pas le format binaire des activations : c'est
  un flux de **trace**, pas un flux de neurones ; le profil `thought` est distinct.
- **Le rejeu exige le problème** (les opérateurs) : le fichier transporte la trace et la racine,
  pas le code des opérateurs ; c'est une **preuve relative au problème**.
- **AC-3 et alpha-bêta n'ont pas encore leur trace DRVF** : le codec est testé sur la boucle
  mono-agent (cruches, BFS) ; les étendre est un pas séparé.
- **Le diff compare les événements**, pas les décisions de stratégie internes (la file d'AC-3,
  les coupes d'alpha-bêta) : la stratégie est un champ, pas un état.
- **Le banc anytime** (AUC, regret) n'est pas encore mesuré ; c'est la prochaine action B13.

## 5. Ce qui pourrait rendre cette fiche fausse

- une racine dont l'**état** ne correspond pas à l'empreinte (le codec le vérifie) ;
- un opérateur **non déterministe** (le rejeu recalculerait autre chose) ;
- un score **flottant** qui ne se compare pas exactement (le codec tolère 1e-9) ;
- un JSON **non canonique** qui change l'ordre des clés (le codec trie) ;
- un flux **tronqué** (la longueur u32 le refuse).

## 6. Fichiers

- [`tools/pensee/trace.py`](../tools/pensee/trace.py) — enveloppe, rejeu, diff.
- [`tools/pensee/autotest.py`](../tools/pensee/autotest.py) — 9/9.
- [`moteur-de-pensee.md`](../docs/implantation/moteur-de-pensee.md) — §6, le profil.
- [`rapport-pensee-ac3-alphabeta.md`](rapport-pensee-ac3-alphabeta.md) — AC-3/alpha-bêta, 8/8.
