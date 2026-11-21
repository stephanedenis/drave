# D — La diversité n'est plus bloquée : Wikisource par les Pages, 4 livres, 3,48 Mo

> **Ligne de roadmap** : D (les données) · **Date** : 2026-11-20 (nuit) · **Verdict** : la collecte
> par les **portails** échouait (1 241 octets pour 40 pages : ce ne sont que des transclusions) ;
> la voie **Page:** (espace 104) rend le texte corrigé. **4 livres du domaine public** collectés et
> épinglés — Madame Bovary (1,09 Mo), Le Rouge et le Noir (1,04 Mo), Vingt mille lieues sous les
> mers (0,91 Mo), Le Tour du monde en quatre-vingts jours (0,43 Mo) — **3 480 645 octets** au total,
> manifeste `d29009d7…`. Gutenberg répond toujours **503**.
>
> **Dispositif** : [`collecter_wikisource_v2.py`](../tools/collecter_wikisource_v2.py) — l'index
> `Livre:` donne le fichier, les `Page:<fichier>/<n>` sont listées (allpages, ns 104), lues par lots
> de 50 (prop=revisions), nettoyées (noinclude, modèles, liens, références, balises) et ordonnées ;
> 1 s entre les appels et cinq essais sur 429 (la première passe a été limitée en débit).

## Le tableau

| livre | octets | pages |
|---|---:|---:|
| Flaubert — Madame Bovary (Conard, 1910) | 1 094 096 | ~520 |
| Stendhal — Le Rouge et le Noir | 1 040 202 | ~500 |
| Verne — Vingt mille lieues sous les mers | 911 802 | 452 |
| Verne — Le Tour du monde en quatre-vingts jours | 434 545 | 224 |
| **total** | **3 480 645** | |

*(Candide est écarté : son index ne porte que 2 pages, le texte est transclus d'un autre scan.)*

## Ce qui pourrait le rendre faux

- **Quatre livres, un registre** : roman français du XIXᵉ — ce n'est pas de la diversité de genre,
  ni de langue, ni d'époque.
- **Le nettoyage laisse des traces** : en-têtes de page, filets, fragments de modèles coupés par le
  découpage (`100px`, `center|…`) — un post-nettoyage les retire, mais un contrôle à l'œil reste
  nécessaire avant tout entraînement.
- **Pas de dédoublonnage** avec les autres corpus du dépôt (le corpus littérature existait déjà).
- **Pas encore utilisé** : ni entraînement, ni val — c'est une brique de collecte, pas un résultat
  de modèle.

## La suite

Étendre (20-50 livres → 30-80 Mo), dédupliquer contre le corpus littérature, et s'en servir comme
**val d'un autre registre** — le contraste Wikipédia/littérature manque à toutes les mesures de la
semaine.

## Voir aussi

- [l'inventaire des données](rapport-donnees-inventaire.md) · [la sélection du contenu](rapport-selection-contenu.md) ·
  [le corpus du palier 1](rapport-corpus-palier1.md)
