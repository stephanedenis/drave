# B13 — les nombres ont une POS : 45 tokens réparés, zéro perte

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Le P1-6 de l'audit produit** : les **nombres** n'avaient aucun POS (`typ == "nombre"` n'entrait
> pas dans la boucle POS). Ils sont désormais **NUM** (confiance 0,90) ; le gold est **inchangé**
> (POS 0,85 ; F1 0,6482 ; attachement 235/236 ; **183/183**).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_pos` : règle
> `\d+([.,]\d+)*` ; la boucle POS accepte `typ == "nombre"`) ; JSON
> [`pensee-pos-nombres.json`](pensee-pos-nombres.json).

## 1. Ce que ça répare

| avant | après |
|---|---|
| `12`, `2024` : aucun POS | **NUM** (0,90) |
| l'audit : **45 nombres** sans POS sur 1 068 tokens | 0 (hors ponctuation) |

**Ce que ça ne répare pas** : `12.5` est encore **tokenisé** `12` `.` `5` (la frontière de phrase
est protégée, pas le token) — c'est le patch B de la fiche des frontières, non intégré.

## 2. Ce que ce banc ne dit pas

- **Le gold n'a que 2 NUM** : le gain n'est pas mesuré sur le gold, il est **produit**.
- **`a`** reste PREP dans « il y a 12.5 euros » (l'ambiguïté avoir/préposition n'est pas tranchée).
- **La ponctuation** (257 tokens) n'a toujours pas de POS : aucune classe du schéma.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le format** des nombres (décimal, milliers, siècles) n'est pas couvert ;
- **NUM** n'est pas dans `POS_FERME` : il est produit par la règle, pas par le lexique.

## 4. La suite

1. **Tokenizer `12.5`** comme un seul nombre (patch B).
2. **POS de la ponctuation** : une classe `PONCT` ou rien (à trancher).
3. **L'ambiguïté `a`** (avoir/préposition) par la position.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — la règle NUM.
- [`pensee-pos-nombres.json`](pensee-pos-nombres.json).
