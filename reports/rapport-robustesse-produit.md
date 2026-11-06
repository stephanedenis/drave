# B13 — la robustesse du produit : un surrogate ne plante plus, une entrée non-str est refusée

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅ **deux bugs
> produit fermés** — un **surrogate isolé** faisait planter `analyser` (`UnicodeEncodeError` sur
> `len(texte.encode())`) et une entrée **non-str** (`bytes`, `int`, `list`) levait
> `AttributeError`. Désormais : l'encodage utilise `errors="replace"` et une entrée non textuelle
> rend `refus="non_texte"` (0 étiquette, pas d'exception). **Huit tests** produit passent.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`analyser`,
> encodages), [`test_produit.py`](../tools/tests/test_produit.py) (`TestRobustesse`) ; audit
> amont [`rapport-produit-bloc-l.md`](rapport-produit-bloc-l.md) (A24 : 50 phrases libres, 18
> correctifs) ; JSON [`pensee-robustesse-produit.json`](pensee-robustesse-produit.json).

## 1. Les deux bugs

| entrée | avant | après |
|---|---|---|
| `"Le chat \ud800 dort."` | `UnicodeEncodeError` | analyse normale (21 étiquettes) |
| `b"octets"`, `42`, `["liste"]` | `AttributeError` | `refus="non_texte"`, 0 étiquette |
| `None` | `refus="vide"` (silencieux) | `refus="non_texte"` (explicite) |

## 2. L'audit de fiabilité (A24) en trois chiffres

- **0 plantage** sur 50 phrases libres, **0 refus**, **0 sortie vide**, **0 span hors texte**.
- **132 paires** de syntagmes qui se chevauchent (31/50 textes, **51,9 % des étiquettes**) : le
  générateur S + l'union, pas le chunker (0 chevauchement seul). **Ne pas dédupliquer en
  silence** : la déduplication donne F1 0,5849 → 0,6141 mais **222 → 208** attachements exacts.
- **Temps** : 1,08 / 4,60 / 19,43 ms à 10/50/200 mots (923/218/51,5 phrases/s) ; démarrage à
  froid 99–113 ms ; RSS 30,7 Mio, delta 0 après 100 analyses.

## 3. Les correctifs produit qui restent (P0)

1. **Expliciter les alternatives de syntagmes** (132 paires) — sans dédupliquer.
2. **Frontières de phrase** : décimaux, dates, URL/emails, abréviations (`M.` duplique la phrase),
   et les types `url`/`emoji` jamais émis.
3. **Compositions** : propager `refus` et `contexte` ; `MockNeuronal` invente 4 étiquettes sur
   `"... !!! ???"`.
4. **Cascade sélective** : 50/50 appels, 1 676/1 676 sur le gold.
5. **Langue** : `fr`/`fra` selon le mode ; 39/50 avec profils contre 50/50 en défaut.

## 4. Ce que ce banc ne dit pas

- **La justesse en liberté** : l'audit mesure des invariants (spans, contrats), pas la justesse.
- **Les 50 phrases** : écrites à la main, pas un tirage aléatoire.
- **La cascade** : la rouge `cascade_pos` est éteinte par un **plancher 0,70** ; la fusion dégrade
  encore le POS de 1,16 pt (à corriger côté comportement).

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — encodage et garde non-str.
- [`test_produit.py`](../tools/tests/test_produit.py) — 8 tests, dont 2 de robustesse.
- [`rapport-produit-bloc-l.md`](rapport-produit-bloc-l.md) — l'audit A24.
- [`pensee-robustesse-produit.json`](pensee-robustesse-produit.json).
