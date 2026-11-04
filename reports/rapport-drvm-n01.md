# N0.1 — DRVM se lit-il ? Oui, et le payload est enfin vérifié

> **Ligne de roadmap** : **N (le natif)** · **Date** : 2026-11-04 · **Verdict** : ✅ **149/149
> portes** : la porte **N0.1** du modèle natif est re-jouée sur un **mini-conteneur** : écriture,
> lecture, `mmap`, hash, **refus de version** et **refus de corruption** — **6/6**. La corruption
> du payload n'était **pas** refusée : le lecteur vérifiait le hash du manifeste mais pas celui
> du **payload**. C'est corrigé (`read_drvm(verifier=True)`).
>
> **Dispositif** : [`drvm.py`](../tools/drvm.py), [`autotest.py`](../tools/pensee/autotest.py),
> JSON [`pensee-drvm-n01.json`](pensee-drvm-n01.json).

## 1. Les six contrôles

| # | contrôle | résultat |
|---:|---|---|
| 1 | écriture (SHA-256, 476 octets) | ✅ |
| 2 | lecture (manifeste, tenseurs) | ✅ |
| 3 | `mmap` (taille = fichier) | ✅ |
| 4 | hash du fichier | ✅ |
| 5 | refus de version (2) | ✅ `version non supportée : 2` |
| 6 | **refus de corruption** | ✅ `hash du payload invalide` (avant : **accepté**) |

**Ce que ça dit** :

- **Le format tient** : DRVM v0 écrit, lit, mappe et hashe un conteneur valide.
- **Le bug était réel** : `read_drvm` vérifiait le manifeste (`msha`) mais **pas le payload**
  (`psha`) — une corruption du dernier octet passait. La porte N0.1 l'a attrapé.
- **Le correctif** : `read_drvm(verifier=True)` hashe le payload via `mmap` ; `verifier=False`
  garde le chemin rapide (le coût est un SHA-256 de 34 Mo pour un vrai modèle, ~30 ms).
- **La négative est explicite** : sans `verifier`, la corruption est acceptée (assumé).

## 2. Ce que ce banc ne dit pas

- **Le modèle réel** (Qwen GGUF) est absent : le test porte sur un mini-conteneur, pas sur un
  DRVM de 34 M paramètres.
- **Le coût du hash** sur un vrai payload n'est pas mesuré ici.
- **Le DRVM v0** : la version 0 est un brouillon de format.
- **La porte N0.1 du corpus** (`qualifier_porte_drvm.py`) attend le GGUF.

## 3. Ce qui pourrait rendre cette fiche fausse

- **un mini-conteneur** : 476 octets, pas 34 Mo ;
- **le SHA-256** : la corruption testée est un octet, pas un scénario adversarial ;
- **le `verifier=False`** : il reste un chemin non vérifié, documenté ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le GGUF** (Qwen 7B) : la porte N0.1 complète quand le modèle sera là.
2. **Le coût du hash** : mesurer sur un payload de 100 Mo.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`drvm.py`](../tools/drvm.py) — `read_drvm(verifier=True)`.
- [`autotest.py`](../tools/pensee/autotest.py) — T146, 149/149.
- [`pensee-drvm-n01.json`](pensee-drvm-n01.json) — les six contrôles.
