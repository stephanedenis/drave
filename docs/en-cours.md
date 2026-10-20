# En ce moment

**Mis à jour : 2026-10-20, 12 h 55 HAE (heure locale, EDT).**

> Cette page dit l'**état courant**, pas l'histoire. Les résultats mesurés sont dans
> [`reports/`](../reports/), le récit daté dans [`journal/`](../journal/), la mission et l'ordre des priorités dans
> [`AGENTS.md`](../AGENTS.md).

## La synthèse (lire si on ne lit qu'une page)

**La cible.** Un **étage entrée-sortie** qui lit et produit **toutes les langues, dialectes et styles**, dans tous
les registres, et qu'on juge en **qualité de traducteur** — restitution à l'identique et traduction du sens. Quand il
sera **fiable**, l'**étage 2** (pensée abstraite, indépendante de la langue) pourra commencer : on n'y passe pas
avant ([AGENTS.md](../AGENTS.md) § 1).

**Les résultats du moment (20 octobre).**

- **Le juge a changé** : le banc UDHR était **contaminé** (le 7 B **récite** l'article 1 au lieu de traduire,
  mesure 61). Le juge est désormais un **texte neuf** : un règlement européen de 2025, 139 unités alignées par
  structure, traductions humaines.
- **La qualité réelle** y est de **55-76 de chrF** (0,5-14 B, mesures 62-63-66) — **+30 à +40** au-dessus du
  plancher, **loin de 100**. Elle **se réplique** sur un second règlement (+1,1 à +2,5, mesure 67).
- **La taille aide, mais de moins en moins** : 54,7 → 73,3 (eng→fra) du 0,5 au 14 B ; le gain par doublement tombe
  à **+0,9** (7 → 14 B, fra→eng) — mesures 63 et 66. *Le levier n'est pas la taille seule.*
- **Trois registres mesurés** : juridique (+35,3 de marge), **presse** (+38,6), **littéraire** (+25,9) — le
  littéraire est le plus dur, mais **pas par le contenu** : **96 %** des noms, **0,5 %** d'omissions ; l'écart est
  de **style** (mesures 64 et 68).
- **La couverture des langues est le facteur** : sur les **24 langues officielles de l'UE**, **+35,8** de marge sur
  le hasard pour les **13 langues annoncées** par le modèle, **+21,5** pour les **10 autres** ; les trous sont
  l'**irlandais (+8,0)** et le **maltais (+10,8)** (mesure 71). *L'écart brut entre langues est surtout la
  distance* (mesure 69), et le plancher **dépend de l'écriture** (28ᵉ piège). **La taille ne comble pas cet écart** :
  il passe de 15,6 (3 B) à 14,2 (7 B), soit −1,4 (mesure 72).
- **L'entrée sait signaler son bruit** (fautes et langues mêlées : **AUC 1,00**), **pas le corriger** : 8/9 des
  corrections empirent, et la plus fluide est la plus fausse (mesure 65).
- **Ce qui tient déjà** : la langue est **lisible partout** (80-100 %), le **sens traverse les langues** (96 % sur
  les paires couvertes), l'alignement **suit la généalogie** (37/28/11 %), et la **restitution exacte** existe pour
  un modèle spécialisé (85 %) mais **meurt à 10 langues** (4 %).

**Le plan de match, en relation avec la cible.**

1. **Compléter les registres** : juridique ✅, presse ✅, littéraire ✅ ; reste le **quotidien parlé** (dialogue,
   conversation) et le **technique** — chacun avec un corpus **post-cutoff** et un **contrôle de mémoire**.
2. **Compléter les langues** : 24 langues UE mesurées ; reste les **langues peu dotées hors UE** (UDHR, avec
   contrôle de contamination) et la **direction inverse** (X→eng).
3. **Choisir le levier** : la taille donne des rendements décroissants et **ne comble pas la couverture**
   (mesure 72) ; le prochain levier est la **couverture** — et un **découpage de surface** par langue/famille
   (MoE d'adaptateurs, C5.6), pas un noyau séparé —
   (données par langue et par domaine) et la **représentation** — la **RSN multi-niveaux**, en **unités de sens**,
   jamais en jetons.
4. **Seulement ensuite** : l'**étage 2**, la pensée abstraite.

**Ce qui bloque encore le passage à l'étage 2** : la qualité sur les **langues peu dotées**, le **registre parlé**,
et une mesure du **sens** qui ne soit pas de surface (le chrF est un **plancher**, pas une note absolue).

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
| **C5** qualité par domaine | C2, C4 | C7 | **ouvert** (juridique **propre** mesuré) |
| **C6** documentation et rangement | — | — | **fait** |
| **C7** pensée abstraite | C5 | — | **en attente** |

### Sous-chantiers : ce qui peut tourner en parallèle

| id | sous-chantier | indépendant ? | état | outil / fichier |
|---|---|---|---|---|
| **C5.1** | banc juridique **UDHR** | ✅ | **contaminé** (mesure 61 : le modèle récite l'UDHR) — banc de **mémoire**, plus juge | `tools/test_contamination.py`, `reports/contamination-*.json` |
| **C5.1b** | banc juridique **post-cutoff** (EUR-Lex 2025) | ✅ **parallèle** | **fait** (mesure 62), **répliqué** (67), **8 langues** (69) et **carte 24 langues** (71) | `tools/corpus_eurlex.py`, `tools/carte_langues.py`, `data/eurlex/`, `reports/traduction-*.json` |
| **C2.2** | **seuil de bruit** et correction de l'entrée | ✅ **parallèle** | **fait** (mesure 65 : détection AUC 1,00 ; correction 8/9 empirent) | `tools/seuil_bruit.py`, `reports/seuil-bruit-3b.json` |
| **C5.2** | banc **littéraire** (Verne) | ✅ **parallèle** | **fait** (mesure 64 : 47,7-49,8) ; **noms 96 %** (mesure 68 : le chrF bas est stylistique) | `tools/aligneur_litteraire.py`, `tools/analyse_litteraire.py` |
| **C5.3** | banc **modèle plus grand** (Qwen2.5 0,5 · 1,5 · 3 · 7 · 14 B) | ✅ **parallèle** | **fait** de 0,5 à 14 B (mesures 63 et 66) : le coude apparaît à 7 B en fra→eng (+0,9) | `tools/traduire_bench.py` |
| **C5.4** | corpus **technique** parallèle | ✅ **parallèle** | à construire | Gutenberg/`Panini` |
| **C5.5** | corpus **presse / actualité** parallèle | ✅ **parallèle** | **fait** (mesure 70 : marge +36 à +39) ; le **quotidien parlé** reste à construire | `tools/corpus_presse.py`, `data/presse/` |
| **C5.6** | **modules par langue / famille** (MoE de surface : adaptateurs, tête, routeur) | ✅ **parallèle** | **à mesurer** — il faut d'abord un **corpus d'entraînement par langue** (les 139 unités du banc sont pour l'évaluation) | `tools/adaptateur_langue.py`, banc 24 langues |
| **C2.1** | répliquer la généalogie **par domaine** | dépend de C5.2-C5.5 | à faire | `retrieval_udhr.py --genealogie` |
| **C4.1** | styles **à époque contrôlée** (couples contemporains) | ✅ **parallèle** | à faire | `style_traducteur.py` + dates |
| **C3.1** | restitution **par famille** (modules spécialisés) | ✅ **parallèle** | à faire | `restitution_udhr.py` |
| **C1.1** | familles **manquantes** (11 langues sans Glottolog) | ✅ **parallèle** | à faire | `genealogie_udhr.py` |

**Règle de parallélisation** : on lance **en même temps** tous les sous-chantiers marqués ✅ dont les entrées
existent déjà ; un sous-chantier qui dépend d'un autre attend son **chiffre**, pas sa documentation.

## Questions en attente (consolidées ici, jamais bloquantes)

| question | qui peut y répondre | état |
|---|---|---|
| la qualité de traduction vient-elle avec la taille ? | **moi** (mesure 62) | **oui, mais de moins en moins** : +1,7 à +6,3 du 3 au 7 B, et +0,9 à +3,8 du 7 au 14 B |
| le plancher « ne rien traduire » est-il battu sur **chaque** direction ? | **moi** (mesure 62) | **oui** : +30 à +40 points sur les 4 paires |
| l'UDHR est-elle utilisable comme juge ? | **moi** (mesure 61) | **non** : le modèle la récite — banc de mémoire |
| peut-on **corriger** automatiquement l'entrée abîmée ? | **moi** (mesure 65) | **non** : 8/9 des corrections empirent ; seule la restauration des accents gagne |
| quelle **unité de mesure** à l'entrée et à la sortie ? | **moi** (RSN en unités de sens ; jeton = technique) | en cours : la RSN est en unités de sens ; les métriques par jeton sont des diagnostics |
| quel domaine après le juridique ? | **moi** (mesures 64 et 70) | **presse mesurée** (au niveau du juridique) ; le **littéraire** reste 10 points en dessous ; le **quotidien parlé** reste à construire |
| la qualité dépend-elle de la **langue** ? | **moi** (mesures 69, 71) | la **couverture** du modèle : +35,8 (annoncées) contre +21,5 (non annoncées) ; trous irlandais/maltais |
| peut-on **découper par langue** (MoE) pour alléger ? | **moi** (C5.6 ; synthèse 07) | **oui en surface**, non en noyau : adaptateurs/têtes par langue, routage par segment, 1,33 % de poids et 5 ms de bascule |
| le littéraire perd-il le **contenu** (noms, omissions) ? | **moi** (mesure 68) | **non** : 96,2 % des noms, 0,5 % d'omissions — l'écart est **stylistique** |
| le banc propre tient-il sur un **autre document** ? | **moi** (mesure 67) | **oui** : +1,1 à +2,5 points sur le règlement 2025/2509 (jouets) |
| faut-il des modules par **famille** pour la restitution ? | **moi** (C3.1) | à lancer |
| les styles à **époque contrôlée** : quels couples contemporains ? | **moi** (chercher dans Gutenberg) | à lancer |
| la vision de l'étage (ce qu'il **doit** être) | **Stéphane** | en attente, ne bloque rien |

## La priorité : l'étage entrée-sortie

Drave Natif se construit **étage par étage**. Le premier est l'**étage entrée-sortie** : lire et produire
**toutes les langues, dialectes et styles**, dans tous les registres, et être **jugé** sur sa **qualité de
traducteur** (restitution à l'identique, et traduction du sens d'une langue à l'autre). Entre le module
pré-linguistique et le module post-linguistique circule une **représentation sémantique neutre (RSN)** : une
structure multi-niveaux, faite d'**unités de sens** — **jamais de jetons** (le jeton est l'unité technique du
tokeniseur, pas l'unité du sens). Le **module de pensée abstraite** attend que cet étage soit fiable.

## Où en est cet étage (état au 19/10)

| ce qui est établi | le chiffre | la fiche |
|---|---|---|
| **la qualité de traducteur, sur texte non mémorisable** (règlements UE 2025) | **54,7 → 73,3** (eng→fra) et **63,1 → 76,6** (fra→eng) du 0,5 au 14 B · **répliqué** sur un 2ᵉ règlement (+1,1 à +2,5) | [07](../reports/07-mesures-couche-commune.md) |
| **le littéraire** (Verne, alignement validé) | **47,7-49,8** (3 B/7 B) · **noms 96 %**, 0,5 % d'omissions : le chrF bas est un écart de **style** (mesure 68) | [07](../reports/07-mesures-couche-commune.md) · [alignement](../reports/alignement-verne.md) |
| **la qualité par langue** (8 langues, mêmes 80 sources) | **45-71** de chrF brut mais **marge 33-40** sur le plancher ; le 7 B **comble le polonais** (+10,1) — l'écart brut est surtout la **distance** (mesure 69) | [07](../reports/07-mesures-couche-commune.md) |
| **la carte des registres** (marge sur le plancher, 7 B) | **juridique +35,3** · **presse +38,6** · **littéraire +25,9** : l'institutionnel et la presse se valent, le littéraire est 10 points en dessous (mesures 62, 68, 70) | [07](../reports/07-mesures-couche-commune.md) |
| **la carte des 24 langues** (marge sur le hasard) | **13 annoncées +35,8** · **10 non annoncées +21,5** (écart +14,2) · trous : **irlandais +8,0**, **maltais +10,8** · **la taille ne comble pas l'écart** : 15,6 (3 B) → 14,2 (7 B), −1,4 (mesures 71-72) | [07](../reports/07-mesures-couche-commune.md) |
| **le bruit d'entrée est signalable** (seuil 3,23 bits/token) | fautes et langues mêlées : **100 %** détectées, AUC **1,00** · accents : **25 %**, AUC 0,69 | [07](../reports/07-mesures-couche-commune.md) |
| **le banc UDHR est contaminé** — le modèle récite, il ne traduit pas | article 1 reproduit **mot pour mot** (7 B) | [07](../reports/07-mesures-couche-commune.md) |
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

1. **qualité de traduction par domaine** : le **juridique** a un banc **propre** (mesure 62) et le **littéraire**
   est **mesuré** (mesure 64 : 47,7-49,8, le plus dur) ; il reste le **technique** et le **quotidien parlé** (la presse est faite), et les **langues peu dotées** — chaque
domaine avec un corpus **post-cutoff**, sinon on mesure la mémoire (mesure 61) ;
2. **l'unité de mesure de l'entrée et de la sortie** : passer des métriques par **jeton** (techniques, dépendantes
   du tokeniseur) aux **unités grammaticales multi-niveaux** (morphème, mot, syntagme, proposition, énoncé), à
   mesure que les modules s'approchent de **grammaires formelles** représentant les entrées et sorties en
   **compréhension totale** ; les métriques par jeton restent des **diagnostics d'instrument** ;
3. **restitution exacte à l'échelle** : au-delà de 10 langues partagées, elle meurt ; modules par famille, ou modèle
   beaucoup plus grand ?
4. **le style** : lisible, mais le sens ne le traverse qu'à 24 % ;
5. **seulement ensuite** : le module de pensée abstraite, indépendant de la langue.

## La carte de la documentation

- [AGENTS.md](../AGENTS.md) — la mission et les règles (à lire avant d'agir) ;
- [docs/README.md](README.md) — la porte d'entrée, la carte de la documentation ;
- [docs/synthese/index.md](synthese/index.md) — la synthèse théorique (7 chapitres, 7 schémas) ;
- [docs/utilisation.md](utilisation.md) — utiliser le dépôt ;
- [`reports/`](../reports/) — les résultats mesurés ; [`journal/`](../journal/) — le récit daté.
