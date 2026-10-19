# En ce moment

**Mis à jour : 2026-10-18, 17 h 07 HAE (heure locale, EDT).**

> Cette page dit l'**état courant**, pas l'histoire. Les résultats mesurés sont dans
> [`reports/`](../reports/), le récit daté dans [`journal/`](../journal/), la mission et l'ordre des priorités dans
> [`AGENTS.md`](../AGENTS.md).

## La synthèse (lire si on ne lit qu'une page)

**La couche entrée-sortie est mesurée, pas encore fiable.** Ce qui est établi : la langue est **lisible partout**
dans l'état (80-100 %), le **sens traverse les langues** sur les paires couvertes (96 %), l'alignement **suit la
généalogie** (37 / 28 / 11 % à écriture contrôlée), et la **restitution exacte** existe pour un modèle spécialisé
(85 %) mais **meurt dès qu'il partage 10 langues** (4 %). Ce qui manque : la **qualité de traducteur** — sur le
juridique, le petit modèle est **sous le plancher « ne rien traduire »** sur 2 paires sur 5 (mesure 50). *C'est ce
chiffre-là qu'il faut faire monter avant le module de pensée abstraite.*

## Le tableau de bord des chantiers

### Dépendances

```
C1 corpus/généalogie ──► C2 traduction ──► C5 qualité par domaine ──► C7 pensée abstraite
        │                     ▲                    ▲
        └──► C3 restitution ──┘                    │
        └──► C4 dialectes/styles ──────────────────┘
C6 documentation (transverse, ne bloque rien)
```

| chantier | dépend de | bloque | état |
|---|---|---|---|
| **C1** corpus et généalogie | — | C2, C3, C4 | **fait** |
| **C2** traduction (retrieval) | C1 | C5 | **mesuré** |
| **C3** restitution | C1 | — | **mesuré** |
| **C4** dialectes et styles | C1 | C5 (styles) | **mesuré**, époque à contrôler |
| **C5** qualité par domaine | C2, C4 | C7 | **ouvert** (juridique mesuré) |
| **C6** documentation et rangement | — | — | **fait** |
| **C7** pensée abstraite | C5 | — | **en attente** |

### Sous-chantiers : ce qui peut tourner en parallèle

| id | sous-chantier | indépendant ? | état | outil / fichier |
|---|---|---|---|---|
| **C5.1** | banc juridique (UDHR, chrF vs humain) | ✅ | **fait** (mesure 50 : le petit modèle ne traduit pas) | `tools/traduire_bench.py`, `reports/traduction-legal.json` |
| **C5.2** | banc **littéraire** (Verne, 2 références ; Alice) | ✅ **parallèle** | à faire | `tools/traduire_bench.py` (mode chapitres) |
| **C5.3** | banc **modèle plus grand** (gemma-3-1b, Qwen3) | ✅ **parallèle** | à lancer | `llama-cli` (GGUF en cache) |
| **C5.4** | corpus **technique** parallèle | ✅ **parallèle** | à construire | Gutenberg/`Panini` |
| **C5.5** | corpus **quotidien** parallèle | ✅ (avec C5.4) | à construire | Gutenberg (théâtre) |
| **C2.1** | répliquer la généalogie **par domaine** | dépend de C5.2-C5.5 | à faire | `retrieval_udhr.py --genealogie` |
| **C4.1** | styles **à époque contrôlée** (couples contemporains) | ✅ **parallèle** | à faire | `style_traducteur.py` + dates |
| **C3.1** | restitution **par famille** (modules spécialisés) | ✅ **parallèle** | à faire | `restitution_udhr.py` |
| **C1.1** | familles **manquantes** (11 langues sans Glottolog) | ✅ **parallèle** | à faire | `genealogie_udhr.py` |

**Règle de parallélisation** : on lance **en même temps** tous les sous-chantiers marqués ✅ dont les entrées
existent déjà ; un sous-chantier qui dépend d'un autre attend son **chiffre**, pas sa documentation.

## Questions en attente (consolidées ici, jamais bloquantes)

| question | qui peut y répondre | état |
|---|---|---|
| la qualité de traduction vient-elle avec la taille ? | **moi** (courbe 0,5 → 1,5 → 3 B en cours) | en cours |
| le plancher « ne rien traduire » est-il battu sur **chaque** direction ? | **moi** | non (fra→spa encore dessous) |
| quel domaine après le juridique ? | **moi** (littéraire via Verne, deux références) | à lancer |
| faut-il des modules par **famille** pour la restitution ? | **moi** (C3.1) | à lancer |
| les styles à **époque contrôlée** : quels couples contemporains ? | **moi** (chercher dans Gutenberg) | à lancer |
| la vision de la couche (ce qu'elle **doit** être) | **Stéphane** | en attente, ne bloque rien |

## La priorité : la couche commune entrée-sortie

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
