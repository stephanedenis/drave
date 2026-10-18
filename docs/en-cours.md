# En ce moment

**Mis à jour : 2026-10-18, 17 h 07 HAE (heure locale, EDT).**

> Cette page dit l'**état courant**, pas l'histoire. Les résultats mesurés sont dans
> [`reports/`](../reports/), le récit daté dans [`journal/`](../journal/), la mission et l'ordre des priorités dans
> [`AGENTS.md`](../AGENTS.md).

## Les chantiers, et où ils en sont

| chantier | état | la fiche |
|---|---|---|
| **1. Couche entrée-sortie — corpus et généalogie** | **fait** : 448 langues UDHR, 13 222 articles, 55 familles Glottolog | [07](../reports/07-mesures-couche-commune.md) |
| **2. Couche entrée-sortie — traduction** | **mesuré** : 96 % (paires couvertes) · 16 % (100 langues) · suit la généalogie (30,7 / 22,0 / 15,2 %) | [07](../reports/07-mesures-couche-commune.md) |
| **3. Couche entrée-sortie — restitution** | **mesuré** : 85 % (1 langue) → 0,6 % (448) ; la courbe meurt entre 1 et 10 | [07](../reports/07-mesures-couche-commune.md) |
| **4. Couche entrée-sortie — styles et dialectes** | **mesuré** : dialectes 30-100 %, styles 6-24 % ; **confondant époque** à contrôler | [07](../reports/07-mesures-couche-commune.md) |
| **5. Couche entrée-sortie — qualité par domaine** | **ouvert** : juridique mesuré — le petit modèle **ne traduit pas** (2 paires sur 5 sous le plancher « ne rien traduire », chinois 0,8 chrF) ✗✗ | [07](../reports/07-mesures-couche-commune.md) |
| **6. Documentation et rangement** | **fait** : `AGENTS.md`, `docs/README.md`, mesures dans `reports/` | [AGENTS.md](../AGENTS.md) |
| **7. Module de pensée abstraite** | **en attente** : il ne commence pas avant que 1-5 soient fiables | [AGENTS.md](../AGENTS.md) |

## La priorité : la couche commune entrée-sortie

Drave Natif se construit couche par couche. La première est la **couche commune entrée-sortie** : lire et produire
**toutes les langues, dialectes et styles**, dans tous les registres, et être jugée sur sa **qualité de traducteur**
(restitution à l'identique, et traduction du sens d'une langue à l'autre). Le **module de pensée abstraite** attend
qu'elle soit fiable.

## Où en est cette couche (état au 18/10)

| ce qui est établi | le chiffre | la fiche |
|---|---|---|
| **la langue est lisible partout** dans l'état d'un modèle (pas de noyau neutre spontané) | 80-100 % dès la couche 1 (5 modèles d'octets, Qwen) | [07](../reports/07-mesures-couche-commune.md) |
| **le sens traverse les langues** — sur les paires bien couvertes | **96,4 %** (12 paires, dont fra↔cmn) · hasard 3,3 % | [07](../reports/07-mesures-couche-commune.md) |
| — mais sur un échantillon stratifié de 100 langues | **16,3 %** · 3,5× le hasard dans un vivier ouvert | [07](../reports/07-mesures-couche-commune.md) |
| **restitution exacte** : parfaite pour un modèle spécialisé, détruite par le partage | **85,1 %** (1 langue) → **0,6 %** (448 langues) | [07](../reports/07-mesures-couche-commune.md) |
| **généalogie** : l'alignement suit les familles (Glottolog, 55 familles) | **30,7 %** même branche · **22,0 %** même famille · **15,2 %** entre familles (hasard 3,3 %) | [07](../reports/07-mesures-couche-commune.md) |
| **dialectes** : lisibles, contenu retrouvé selon la couverture | 100 % lus · 30-100 % retrouvés | [07](../reports/07-mesures-couche-commune.md) |
| **styles** (traducteurs) : lisibles, contenu moins résistant | 87-100 % lus · 6-24 % retrouvés | [07](../reports/07-mesures-couche-commune.md) |
| **la langue est un petit paramètre de sortie** | 1,33 % des poids · 5 ms de bascule | [07](../reports/07-mesures-couche-commune.md) |

**Le corpus** : la Déclaration universelle des droits de l'homme, **448 langues**, 13 222 articles alignés, 43
écritures, 37 langues à variantes (`data/udhr/`, importeurs `tools/importer_udhr.py` et `tools/preparer_udhr.py`).

## Ce qui reste à faire, dans l'ordre

1. **qualité de traduction par domaine** (technique, juridique, littéraire, quotidien) et par **langue peu dotée** —
   c'est le juge de paix de la couche ;
2. **restitution exacte à l'échelle** : au-delà de 10 langues partagées, elle meurt ; modules par famille, ou modèle
   beaucoup plus grand ?
3. **le style** : lisible, mais le sens ne le traverse qu'à 24 % ;
4. **seulement ensuite** : le module de pensée abstraite, indépendant de la langue.

## La carte de la documentation

- [AGENTS.md](../AGENTS.md) — la mission et les règles (à lire avant d'agir) ;
- [docs/README.md](README.md) — la porte d'entrée, la carte de la documentation ;
- [docs/synthese/index.md](synthese/index.md) — la synthèse théorique (7 chapitres, 7 schémas) ;
- [docs/utilisation.md](utilisation.md) — utiliser le dépôt ;
- [`reports/`](../reports/) — les résultats mesurés ; [`journal/`](../journal/) — le récit daté.
