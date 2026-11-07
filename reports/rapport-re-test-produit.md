# B13 — re-test produit : 50 textes libres, la vue linéaire supprime les chevauchements

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Ce que le produit fait sur les 50 textes de l'audit A26**, rejoués sur le code du 06/11 21 h :
> en vue **`alternative`** (défaut), 405 segments et **145 chevauchements** ; en vue **`filtrer`**,
> 297 segments et **0 chevauchement**. Les **5 textes sans syntagme** sont l'emoji, le texte vide,
> les espaces, `...` et un nombre nu — des entrées **non linguistiques**, pas des échecs.
>
> **Dispositif** : `tools/bloc_linguistique.py` (`Heuristique(partition=...)`), les 50 textes de
> [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json) ; JSON
> [`pensee-re-test-produit.json`](pensee-re-test-produit.json).

## 1. Les chiffres

| vue | segments | chevauchements | textes sans syntagme |
|---|---:|---:|---:|
| **`alternative`** (défaut) | 405 | **145** | 5 |
| **`filtrer`** (linéaire) | 297 | **0** | 5 |

**Ce que ça dit** :

- **La vue linéaire fait exactement ce qu'elle promet** : 0 chevauchement sur les textes libres.
- **Les 5 sans syntagme sont légitimes** : 🚀, `""`, `"   "`, `"..."`, `"1234567890"` — rien à
  segmenter.
- **Le défaut `alternative` documente** les 145 paires au lieu de les cacher (le client choisit).

## 2. Ce que ce banc ne dit pas

- **La justesse** : on compte des invariants (segments, chevauchements), pas la qualité
  linguistique des segments.
- **Le banc de l'audit** (107 paires) et le nôtre (145) ne comptent pas de la même façon : l'audit
  excluait des paires, et le code a gagné des verbes (morphologie) donc des GV.
- **Le temps** : 0,13 s pour les 50 textes.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition** du chevauchement (strict, ici) ;
- **le corpus** est écrit à la main ;
- **la comparaison** avec l'audit n'est pas à définition constante.

## 4. La suite

1. **Trancher le défaut produit** : `alternative` (fidèle) ou `filtrer` (linéaire).
2. ~~Un test de non-régression sur les 50 textes~~ — **fait** : `tools/tests/test_produit_libre.py` (4 tests, 10e contrôle de la porte).
3. **Le décompte** à définition constante avec l'audit.

## 5. Fichiers

- [`rapport-fiabilite-produit.md`](rapport-fiabilite-produit.md) — l'audit A26.
- [`pensee-re-test-produit.json`](pensee-re-test-produit.json).
