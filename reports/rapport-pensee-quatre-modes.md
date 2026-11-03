# L — la porte des quatre modes sur le gold 432 : le neuronal API domine (0,9309 / 0,8226 / 0,8784), la fusion dégrade (0,928 / 0,802 / 0,857)

> **Ligne de roadmap** : **L** (le bloc langue) · **Date** : 2026-11-03 · **Verdict** : ⚠️ **le neuronal
> seul est le meilleur sur les niveaux linguistiques** — POS **0,9309**, syntagmes **0,8226**, tête
> **0,8784** —, l'**heuristique** garde la **pragmatique** (acte **0,9954** contre **0,0**), et la
> **fusion** (parallèle et cascade) **régresse** : **0,928 / 0,802 / 0,857**. Un **refus** ; 858
> appels API, **254 341 tokens**, 13,3 min. La porte des quatre modes **révèle le problème de la
> fusion**, pas celui des blocs.

## 1. Le dispositif

- **Gold réel 432** (2 375 tokens), le même pour les quatre modes.
- **Neuronal** : `NeuronalLLMCompose` (POS + syntagmes) via l'**API DeepSeek** (`deepseek-chat`,
  `DEEPSEEK_KEY_FILE`), **aucun serveur local**, **aucun GPU** (règle 11).
- **Parallèle** : `Parallele([heuristique, neuronal], priorite_syntagme="confiance")`.
- **Cascade** : `Cascade(heuristique, neuronal, seuil=0,6, priorite_syntagme="confiance")`.
- **Mesures** : POS, syntagmes F1, tête F1, acte, fraction, refus ; **coût** : appels, tokens,
  latence, durée.

## 2. Les résultats

| mode | POS | syntagmes | tête | acte | fraction | durée |
|---|---:|---:|---:|---:|---:|---:|
| **heuristique** | 0,7394 | 0,2524 | 0,4516 | **0,9954** | 0,5165 | 0,3 s |
| **neuronal (API)** | **0,9309** | **0,8226** | **0,8784** | 0,0 | 0,0 | 795,8 s |
| **parallèle** | 0,9280 | 0,8020 | 0,8570 | 0,9954 | 0,5165 | 0,5 s |
| **cascade** | 0,9280 | 0,8020 | 0,8570 | 0,9954 | 0,5165 | 0,5 s |

- **Le neuronal gagne sur les niveaux linguistiques** : POS +0,19, syntagmes +0,57, tête +0,43
  par rapport à l'heuristique.
- **L'heuristique gagne sur la pragmatique** : acte 0,9954 contre 0,0 — le composite neuronal ne
  rend **pas** la pragmatique.
- **La fusion régresse** : parallèle et cascade sont **sous** le neuronal (0,928 < 0,9309 ;
  0,802 < 0,8226 ; 0,857 < 0,8784), alors qu'ils devraient au moins le valoir. La politique
  `confiance` fait gagner les étiquettes de l'heuristique (confiance 0,92 sur les classes fermées)
  sur celles du neuronal — c'est un **défaut de fusion**, pas un défaut des blocs.
- **Coût** : 858 appels API, 254 341 tokens, latence médiane 1,86 s, 797 s au total (le neuronal) ;
  l'heuristique et les fusions sont servies par le cache (0,5 s).

## 3. Les seuils de la porte

| seuil | valeur | passe |
|---|---|---:|
| `heuristique` | — | ✅ |
| `neuronal` | POS > 0 | ✅ |
| `parallele` | ≥ max(heuristique, neuronal) − 0,001 | ❌ (0,928 < 0,9299) |
| `cascade` | ≥ heuristique − 0,001 | ✅ |
| `aucun_refus` | 0 refus | ❌ (**1 refus**) |

**Verdict de la porte : 3/5** — et les deux échecs sont **informatifs** : la fusion qui dégrade et
le refus unique.

## 4. Le contrôle négatif

- **Le neuronal seul** : acte **0,0** et fraction **0,0** — il ne porte pas la pragmatique ; c'est
  bien l'heuristique qui la tient.
- **L'heuristique seule** : syntagmes **0,2524** — elle ne porte pas la structure ; c'est bien le
  neuronal qui la tient.
- **La fusion** : au lieu du **maximum** des deux (la promesse du contrat), elle rend **moins** que
  le neuronal sur ses niveaux. Le contrôle « la fusion ne doit pas dégrader » **échoue** — et c'est
  le fait.

## 5. Ce qui pourrait rendre ce résultat faux

- Le **refus unique** (1 phrase) : il faudrait le nommer ; il ne change pas les agrégats.
- 429 appels pour 432 phrases : effet de cache (3 phrases déjà annotées), comme sur la cascade.
- L'API DeepSeek peut varier ; la température est 0 et le cache est versionné (`data/deepseek/cache`).
- La politique de fusion (`priorite_syntagme="confiance"`) est **un choix** : le résultat dit qu'il
  est mauvais, pas que la fusion est impossible.

## 6. La suite de L

1. **Réparer la fusion** : donner au neuronal la priorité sur les niveaux qu'il tient, à
   l'heuristique ceux qu'elle tient (la pragmatique) — ou fusionner **par niveau**, pas par
   confiance globale.
2. **Nommer le refus** (la phrase, la raison) et le traiter.
3. **La pragmatique neuronale** : elle reste à 0,0 sur ce composite ; le contrat le dit.

## 7. Fichiers

- [`pensee-quatre-modes.json`](pensee-quatre-modes.json) — les mesures, le coût, les seuils.
- [`tools/tests/linguistique/qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) —
  le banc.
- [`docs/theorie/contrat-bloc-langue.md`](../docs/theorie/contrat-bloc-langue.md) — le contrat.
