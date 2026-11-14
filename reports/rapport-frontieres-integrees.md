# B13 — les frontières de phrase : 32/40 textes faux → 0, et le gold ne bouge pas

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Le P0-4 est fermé** : sur **40 textes libres** (URL, courriels, chemins, décimaux, dates,
> abréviations, ellipses, listes, code inline), les frontières passent de **32/40 faux** à
> **0/40** ; **102 → 59 phrases** ; les **actes faux** de **63/102** à **0/59** ; plus aucune
> coupure (47), fusion (4), chevauchement (9), fausse question (5) ni espace de tête (31). Le
> **gold est inchangé** : POS 0,8496, F1 0,6474, attachement **235/236**, **183/183** portes.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`decouper_phrases`,
> `_phrases`), fiche A28 [`rapport-frontieres-phrase.md`](rapport-frontieres-phrase.md) ; JSON
> [`pensee-frontieres-integrees.json`](pensee-frontieres-integrees.json).

## 1. La règle

Un balayage **unique** du texte, avec des **zones protégées** où la ponctuation n'est jamais une
frontière :

| zone | exemple |
|---|---|
| décimaux | `12.5`, `12.03.2024` |
| URL, courriels, domaines | `https://exemple.fr/a.b`, `nom@ex.fr` |
| chemins et extensions | `src/app.py`, `C:\data\fichier.csv` |
| abréviations | `M.`, `Dr.`, `cf.`, `p. ex.`, `etc.` |
| ponctuation répétée | `...`, `?!`, `!?` |
| code inline et blocs | `` `x.y` ``, ``` ```…``` ``` |

Après un **titre** (`M.`), un mot qui ouvre presque sûrement une phrase (`Il`, `Elle`, `Mais`…)
coupe ; sinon non. Un **saut de ligne structurel** coupe ; un espace de tête ne crée pas de
phrase vide.

## 2. Avant / après (40 textes)

| défaut | avant | **après** |
|---|---:|---:|
| textes à frontières fausses | 32/40 | **0/40** |
| phrases | 102 | **59** |
| coupures | 47 | **0** |
| fusions | 4 | **0** |
| chevauchements | 9 | **0** |
| fausses questions | 5 | **0** |
| espaces de tête | 31 | **0** |
| actes faux | 63/102 | **0/59** |

## 3. Le gold

**Delta 0** sur POS, F1, attachement et tokens : le gold ne contient **aucun** des cas traités
(pas de décimal, d'URL, d'abréviation). C'est un **contrôle de non-régression**, pas un gain de
mesure — le gain est sur les textes libres. Deux spans de phrase sont corrigés (`r308`, `r318` :
espace de tête).

## 4. Ce que ce banc ne dit pas

- **Le gold ne teste pas ces cas** : le gain n'est pas mesuré sur le gold, et c'est normal.
- **Les 40 textes** sont écrits par l'auditeur (pas un tirage aléatoire).
- **La tokenisation** (patch B, optionnel) n'est pas intégrée : elle change les tokens
  (477 → 362) sans toucher au gold.

## 5. Ce qui pourrait rendre cette fiche fausse

- **une abréviation inconnue** (`St.`, `Ste.`) peut encore couper ;
- **les regex** sont un choix : un cas non prévu passera à travers ;
- **le `_MARQUEUR`** (lignes de liste) dépend du format markdown.

## 6. La suite

1. **La tokenisation** (patch B) : à mesurer avant d'intégrer.
2. **Les abréviations rares** : une liste ouverte.
3. **Les faux positifs** : `n.` peut être un nom.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `decouper_phrases`.
- [`rapport-frontieres-phrase.md`](rapport-frontieres-phrase.md) — la fiche A28.
- [`pensee-frontieres-integrees.json`](pensee-frontieres-integrees.json).
