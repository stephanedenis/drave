2026-10-24

# En ce moment

**Mis à jour : 2026-10-24, 17 h 00 HAE (heure locale, EDT).**

> Cette page dit **où l'on va, ce qui est en cours, où l'on en est, et ce qu'il reste** aux trois horizons. Les
> détails — chaque chiffre, chaque fiche — sont dans [`reports/`](../reports/), la théorie dans
> [`synthese/`](synthese/index.md), le plan dans [`roadmap.md`](roadmap.md). **Ici, on ne garde que l'actualité.**

## Où l'on va (l'objectif final)

**Démontrer que la structure bat la taille, et construire le moteur qui rend cette structure observable,
décomposable, répartissable et rejouable.**

Deux programmes : le **moteur** (les flux, les cinq axes) et l'**intelligence** (l'entrée-sortie linguistique, puis
la pensée abstraite jugée sur des **opérations** — l'étage 2 ne se bâtit pas sur une entrée-sortie qui n'est pas
fiable). La thèse n'est plus une hypothèse : **la sonde est plate dès le 1,5 B** (0,7256 / 0,7269 / 0,7189), **le
pont plafonne à 0,87**, et à profondeur fixe le 14 B est **dernier** (0,4833) — dix fois la taille pour +0,001.
Voir [`vision.md`](vision.md) et [`mission.md`](agent/mission.md).

## Ce qui est en cours (l'actualité du 24/10)

**La nouvelle phase**, après la révision de la raison d'être, de la stratégie et du plan :

1. **A7 la grappe déportée** : la couche exécutée ailleurs rend **le même chiffre** (`porte-topologie`, 92 s,
   42.5477) et le flux coûte **1 608 octets/flux** ; reste la **grappe intra-couche** (A7.3).
2. **B4 les opérateurs abstraits** : la carte de l'étage 2 est faite ; **B4.1 a rendu un négatif net** (la négation
   n'est pas portée par l'état : flip 0,4148, garde 0,5852) — B4.2 est l'**opérateur appris**, à entraîner dans l'état.
3. **A8 l'ordonnanceur place et perte** : le terme de perte est **codé et testé** (`choisir_avec_perte`, 3 tests) ;
   reste à le brancher dans `model.rs`.

**Ce que la journée a établi** : la **carte du raisonnement naturel** est close (trois courbes complètes, les pics
tardifs, la sonde qui sature dès le 1,5 B) ; la **passe complète** est **45/47** (les deux structurels connus,
**aucun rouge nouveau**, la 47ᵉ porte verte en 18 s) ; **DiaBLa** au 3 B (+38,1/+41,3) ; le **14 B l24** était déjà
mesuré (0,6305/0,8153 — le meilleur point à 50 %).

## Où l'on en est (les chiffres qui comptent)

| | |
|---|---:|
| mesures de la fiche principale | **173** |
| portes (passe complète) | **47** — 45 vertes, 2 structurels |
| fiches / JSON de résultats | 156 / 228 |
| la sonde, au pic du 1,5 B | **0,810** (DACCORD l22) · **0,7256** (XNLI) |
| le pont, au pic du 14 B | **0,8715** (l36) — il plafonne à 0,87 |
| le KV int8 tardif / le 4 bits de la tête | **+0,03 %** / **+10 %** (reverté) |

Le détail de la carte du raisonnement : [05](synthese/05-la-pensee-sans-verbaliser.md) et sa
[synthèse](../reports/rapport-carte-raisonnement-naturel.md).

## Les sept chantiers, en une ligne chacun

| chantier | état |
|---|---|
| **C1** corpus et généalogie | ✅ fait (UDHR 448 langues, Glottolog) |
| **C2** traduction | ✅ mesuré (le juge post-cutoff, le plancher, la marge) |
| **C3** restitution | ✅ mesuré (85 % pour un modèle spécialisé, détruite à 10 langues) |
| **C4** dialectes et styles | ✅ mesuré (lisibles ; l'époque reste à contrôler) |
| **C5** qualité par domaine | ✅ les **six registres** + le **dialogue spontané** (DiaBLa) |
| **C6** documentation | ✅ fait (l'inventaire, la revue, les portes) |
| **C7** pensée abstraite | 🔬 **la carte est faite** (l'état porte le raisonnement, le pont l'aligne à 0,87, le plan résiste) ; les **opérateurs** restent (B4) |

## Ce qui reste, aux trois horizons

**Court terme — les prochaines lignes (toutes mesurables sans ressource extérieure)**
1. **B4.2** — l'opérateur **appris** (B4.1 a rendu un négatif : la sonde ne lit pas la négation) ;
2. **A7.3** — la grappe intra-couche (la frontière de couche est déjà déportée) ;
3. **A8.3** — brancher `choisir_avec_perte` dans `model.rs` (le KV et la tête).

**Moyen terme**
- **B4.2** les opérateurs composés ; la **grappe** neuronale complète (A7.3) ; l'**ordonnanceur** qui applique la
  règle (A8.3).
- **B1.5 la prose scientifique** : bloquée, pas de corpus parallèle humain.
- Le **FPGA** (A5.4, le matériel), la **démonstration distante** (A3.4, le compte Colab), le **MoE** (A6.2, pas de
  modèle local).

**Objectif final**
- **L'intelligence** : une entrée-sortie **fiable** (étage 1, tenu : six registres, 24 langues, le dialogue) puis une
  **pensée abstraite indépendante de la langue**, jugée sur des **opérations** (étage 2 : la carte est faite, les
  opérateurs restent).
- **Le moteur** : un modèle **décomposable** (la grappe), **répartissable** (le relais, fait), **observable** (la
  trace, le diff) et **rejouable** — la vision, tenue par ses mesures.

## Les questions ouvertes (consolidées ici, jamais bloquantes)

- **Bloquées par une ressource** : **B1.5** (le corpus d'articles humain), **A3.4** (le compte Colab), **A5.4** (la
  carte Stratix V), **A6.2** (un MoE local).
- **Ouvertes sans blocage** : les **styles à époque contrôlée** (les couples contemporains), les **modules par
  famille** pour la restitution, le **pic du 32 B** (10-20 h en 4 bits, nommé, non forcé).

## La carte de la documentation

[`AGENTS.md`](../AGENTS.md) — la mission et les règles ; [`docs/README.md`](README.md) — l'inventaire ;
[`roadmap.md`](roadmap.md) — le plan et la file « jamais en attente » ; [`synthese/index.md`](synthese/index.md) — la
théorie ; [`reports/`](../reports/) et [`journal/`](../journal/) — les résultats et le récit.
