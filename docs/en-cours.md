# En ce moment

**Mis à jour : 2026-10-19, 16 h 55 HAE (heure locale, EDT).**

> Cette page dit l'**état courant**, pas l'histoire. Les résultats mesurés sont dans
> [`reports/`](../reports/), le récit daté dans [`journal/`](../journal/), la mission et l'ordre des priorités dans
> [`AGENTS.md`](../AGENTS.md).

## La synthèse (lire si on ne lit qu'une page)

**L'étage entrée-sortie est mesuré, pas encore fiable.** Ce qui est établi : la langue est **lisible partout**
dans l'état (80-100 %), le **sens traverse les langues** sur les paires couvertes (96 %), l'alignement **suit la
généalogie** (37 / 28 / 11 % à écriture contrôlée), et la **restitution exacte** existe pour un modèle spécialisé
(85 %) mais **meurt dès qu'il partage 10 langues** (4 %). Ce qui manque : la **qualité de traducteur**. Le banc
juridique de l'UDHR était **contaminé** (mesure 61 : le 7 B **récite** l'article 1 mot pour mot au lieu de
traduire) ; sur un **règlement européen de 2025**, non mémorisable, la qualité réelle est **54,7-76,6 de chrF**
(0,5-14 B, 4 paires, mesures 62-63-66) — **au-dessus du plancher de +30 à +40**, mais **loin de 100**. La **courbe
propre** est **lisse et monotone** (54,7 → 73,3 en eng→fra, 63,1 → 76,6 en fra→eng, du 0,5 au 14 B, mesures 63 et
66) : *le « coude à 3 B » de l'UDHR était un artefact ; le premier aplatissement est à 7 B en fra→eng (+0,9)*. Et le **littéraire**, enfin aligné (93,2 % d'ancres à ±2,
mesure 64), est le **plus dur** : **47,7-49,8**, où la taille n'aide presque pas (+2,1). Et l'entrée sait
**signaler** son bruit (seuil à 3,23 bits/token : fautes et langues mêlées détectées à 100 %, AUC 1,00) mais
**pas le corriger** : la correction automatique **empire** le texte 8 fois sur 9 (mesure 65). La qualité se
**réplique** sur un second règlement (+1,1 à +2,5 points, mesure 67). *C'est la qualité de traducteur qu'il faut
faire monter avant le module de pensée abstraite.*

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
| **C5.1b** | banc juridique **post-cutoff** (EUR-Lex 2025) | ✅ **parallèle** | **fait** (mesure 62) et **répliqué** sur un 2ᵉ règlement (mesure 67 : +1,1 à +2,5) | `tools/corpus_eurlex.py`, `data/eurlex/`, `reports/traduction-eurlex*.json` |
| **C2.2** | **seuil de bruit** et correction de l'entrée | ✅ **parallèle** | **fait** (mesure 65 : détection AUC 1,00 ; correction 8/9 empirent) | `tools/seuil_bruit.py`, `reports/seuil-bruit-3b.json` |
| **C5.2** | banc **littéraire** (Verne) | ✅ **parallèle** | **fait** (mesure 64 : alignement validé 93,2 %, littéraire 47,7-49,8) | `tools/aligneur_litteraire.py`, `tools/traduire_bench.py --corpus verne_align` |
| **C5.3** | banc **modèle plus grand** (Qwen2.5 0,5 · 1,5 · 3 · 7 · 14 B) | ✅ **parallèle** | **fait** de 0,5 à 14 B (mesures 63 et 66) : le coude apparaît à 7 B en fra→eng (+0,9) | `tools/traduire_bench.py` |
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
| la qualité de traduction vient-elle avec la taille ? | **moi** (mesure 62) | **oui, mais de moins en moins** : +1,7 à +6,3 du 3 au 7 B, et +0,9 à +3,8 du 7 au 14 B |
| le plancher « ne rien traduire » est-il battu sur **chaque** direction ? | **moi** (mesure 62) | **oui** : +30 à +40 points sur les 4 paires |
| l'UDHR est-elle utilisable comme juge ? | **moi** (mesure 61) | **non** : le modèle la récite — banc de mémoire |
| peut-on **corriger** automatiquement l'entrée abîmée ? | **moi** (mesure 65) | **non** : 8/9 des corrections empirent ; seule la restauration des accents gagne |
| quel domaine après le juridique ? | **moi** (mesure 64) | **littéraire mesuré** : 47,7-49,8, le plus dur |
| le banc propre tient-il sur un **autre document** ? | **moi** (mesure 67) | **oui** : +1,1 à +2,5 points sur le règlement 2025/2509 (jouets) |
| faut-il des modules par **famille** pour la restitution ? | **moi** (C3.1) | à lancer |
| les styles à **époque contrôlée** : quels couples contemporains ? | **moi** (chercher dans Gutenberg) | à lancer |
| la vision de l'étage (ce qu'il **doit** être) | **Stéphane** | en attente, ne bloque rien |

## La priorité : l'étage entrée-sortie

Drave Natif se construit **étage par étage**. Le premier est l'**étage entrée-sortie** : lire et produire
**toutes les langues, dialectes et styles**, dans tous les registres, et être jugée sur sa **qualité de traducteur**
(restitution à l'identique, et traduction du sens d'une langue à l'autre). Le **module de pensée abstraite** attend
qu'elle soit fiable.

## Où en est cet étage (état au 19/10)

| ce qui est établi | le chiffre | la fiche |
|---|---|---|
| **la qualité de traducteur, sur texte non mémorisable** (règlements UE 2025) | **54,7 → 73,3** (eng→fra) et **63,1 → 76,6** (fra→eng) du 0,5 au 14 B · **répliqué** sur un 2ᵉ règlement (+1,1 à +2,5) | [07](../reports/07-mesures-couche-commune.md) |
| **le littéraire** (Verne, alignement validé) | **47,7-49,8** (3 B/7 B) · +24 à +26 sur le plancher · la taille n'aide presque pas (+2,1) | [07](../reports/07-mesures-couche-commune.md) · [alignement](../reports/alignement-verne.md) |
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
   est **mesuré** (mesure 64 : 47,7-49,8, le plus dur) ; il reste le **technique**, le **quotidien**, et les
   **langues peu dotées** — chaque domaine avec un corpus **post-cutoff**, sinon on mesure la mémoire (mesure 61) ;
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
