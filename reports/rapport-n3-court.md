# N3.10 — `court` : le premier profil qui change le coût

> **Ligne de roadmap** : N3 · **Date** : 2026-11-17 · **Verdict** : ✅ **N3.10 tenu** — `court`
> (fenêtre d'attention divisée par quatre) est **bit-exact** en deçà de sa fenêtre, **non
> substituable** au-delà (**3,633e-02**), et **0,694×** le temps sur une charge dominée par
> l'attention. Sur le modèle entraîné de 34 M, la perplexité **ne monte pas** (23,7480 → **23,5824**
> sur 2 048 octets en distribution) et le temps gagne **~5 %** : la fenêtre déclarée de 1 024
> n'est pas utilisée au-delà de 256 sur ce modèle.
>
> **Dispositif** : [`tools/porte-n3-court.sh`](../tools/porte-n3-court.sh) · petit `drave-n0`
> (**132 720 paramètres**, `d_model` 32, 2 blocs, `window` 256, graine 7) exporté `defaut` et
> `court` ; sur le modèle entraîné, `work/n2ac/mix1024-60k.drvm` (384 dimensions, 6 blocs,
> `window` 1 024, 137 Mo) réécrit avec `impl: "court"`, perplexité native sur
> `data/corpus_mixte.txt` (in distribution, 1 024 et 2 048 octets) et sur deux textes du dépôt
> (hors distribution).

## Ce qui est mesuré

| contrôle | résultat |
|---|---|
| 32 octets (< 64 = fenêtre courte) : `defaut` vs `court` | **bit-exact** |
| 1 024 octets : `defaut` vs `court` | **3,633e-02** ≠ 0 → non substituable |
| coût, 1 024 octets, médiane de 11 passes alternées | **0,694×** (80,8 → 56,0 ms, CV 3–6 %) |
| modèle entraîné, perplexité 1 024 octets (in distribution) | 22,9458 → **22,9083** |
| modèle entraîné, perplexité 2 048 octets (in distribution) | 23,7480 → **23,5824** |
| modèle entraîné, temps de la passe 2 048 octets | 73,9 s → **70,0 s** (~5 %) |
| modèle entraîné, deux textes hors distribution (~520 o) | directions **opposées** (38,08→36,94 ; 27,68→28,52) → bruit |
| moteur numpy | `court` **exécuté** (parité Rust **2,980e-07**), fenêtre appliquée |

## Ce que la porte établit

1. **La seule différence est la fenêtre** : en deçà de la fenêtre courte, les logits sont
   bit-exacts — le profil ne « gagne » pas en changeant autre chose.
2. **Au-delà, la fonction change** : 3,633e-02 d'écart sur les logits, donc `court` n'est pas une
   substitution mais un **candidat au routage**.
3. **Le coût baisse là où l'attention pèse** : 0,694× sur une charge où l'attention représente
   ~50 % des opérations.
4. **Sur ce modèle entraîné, la fenêtre longue ne sert pas** : couper de 1 024 à 256 ne dégrade pas
   la perplexité en distribution (elle baisse même légèrement) et rend la passe ~5 % plus rapide.
   C'est une propriété du modèle **et** du corpus, pas du profil.

## Ce que la porte ne prouve PAS — et c'est écrit

- **Le gain dépend de la part de l'attention** : sur le 34 M, le FFN domine (~5,5 M des ~6,3 M
  d'opérations par position), l'attention ne pèse que ~14 % — d'où ~5 % de temps et non 30 %.
- **Un modèle, un corpus, un découpage** : 2 048 octets du début de `corpus_mixte.txt`, une passe,
  perplexité par octet. Cela ne dit pas que la fenêtre longue est inutile *en général* ; cela dit
  qu'elle ne sert pas ici.
- **Les textes hors distribution ne concluent pas** : deux directions opposées à ~520 octets —
  c'est du bruit, et c'est écrit plutôt que moyenné.
- **Le temps inclut le démarrage du processus** (~5 ms) et la lecture du modèle (137 Mo) : sur
  1 024 octets le premier pèse peu, le second non.
- **Le modèle synthétique est non entraîné** : il prouve la sémantique et le coût, pas la qualité.

## Ce que ça change

Le catalogue de profils cesse d'être homogène en coût : `defaut` et `bloque` sont **substituables**
(contrat), `flou` et `court` sont **routables** (autres fonctions), et `court` est le premier qui
**paie en temps sans coût de qualité mesuré sur ce modèle**. Un routage a donc, pour la première
fois, quelque chose à arbitrer — mais l'arbitrage exige un coût de qualité sur un corpus de
validation et des contextes où la fenêtre longue sert vraiment. La politique reste une question
ouverte (R0.5/R06 : un seuil global ne transfère pas).

## Voir aussi

- [la porte](../tools/porte-n3-court.sh) · [le format](../tools/drvm.py) ·
  [le moteur natif](../drave-core/src/native.rs) · [les variantes](rapport-n3-variante.md) ·
  [les routes](rapport-n3-route.md)
