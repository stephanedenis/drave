# Note — C9, latéralité : deux instances jumelles et leur corps calleux

> **2026-10-10 16:15 HAE** (heure lue sur la machine). Note de conception : `docs/` porte les
> hypothèses et les plans ; les mesures vivent dans `reports/`, une fiche par expérience. Ce qui est
> déjà mesuré est renvoyé aux fiches ; ce qui reste à faire est écrit comme une **porte à tenir**.

## 1. Ce que le plan demande (et ce qui existe déjà)

`docs/plan-cerveau-complet.md` § C9 — « Latéralité et corps calleux » :

- **cerveau** : deux hémisphères, ~2 × 10⁸ axones, connexions **homotopiques** (les régions
  symétriques se parlent) ;
- **conception** : deux **instances jumelles** du même modèle, un lien **homotopique par couche**
  (échange d'activations), avec **bande passante déclarée** ;
- **interface** : `--jumeau <hôte:port> --echange <couches|experts>` ;
- **invariant** : échange **désactivé** ⇒ chaque instance est **identique au modèle seul** ;
- **validation** : un gain (perplexité ou robustesse à une entrée dégradée) — **et si le gain est
  nul, le dire** (le plan écrit lui-même que c'est le cas le plus probable) ;
- **coût** : 1-2 semaines après C1. C1 est **fait** (graphe de régions, 0,00e0).

**Ce qui existe déjà et qu'il ne faut pas réinventer** :

| brique | où | ce qu'elle donne |
|---|---|---|
| découpage en régions et **relais** | `topologie.rs`, `--topologie`, porte `porte-topologie.sh` | deux instances **séparées** se parlent déjà, résultat identique au modèle entier (0,00e0) |
| **lien avec budgets** | `Lien { delai_ms, budget_octets, budget_ms, budget_paires }` | un lien peut **refuser** au-delà d'un budget (codes 6, 8, 9) |
| **bus de modulation** par socket | `--bus-serveur`, porte `porte-bus-socket.sh` | un canal de réglage atteint une autre machine |
| **trace** et **fusion** | `trace_globale.rs`, porte `porte-fusion.sh` | deux processus se relisent ensemble, dans un temps commun |

## 2. La conception minimale, mesurable tout de suite

La latéralité n'est **pas** un découpage : dans un découpage, les régions se **succèdent** ; dans
la latéralité, les deux instances traitent **les mêmes** couches et s'échangent leurs états **à
chaque couche**. Ce qui coûte, c'est donc **l'échange**, pas le calcul.

| élément | proposition | pourquoi |
|---|---|---|
| **jumelage** | `--jumeau <hôte:port>` : l'instance ouvre un lien vers une jumelle et lui envoie son état après chaque couche de la liste | le relais existe déjà ; ici il n'y a pas de « suite », seulement un **échange** |
| **échange** | `--echange couches:0,2,4` (ou `toutes`) : la liste des couches où l'état part | la bande passante se **déclare** couche par couche, comme le plan le demande |
| **mode** | `moyenne` (les deux états sont moyennés), `remplace` (la jumelle impose), `ajoute` | trois modes suffisent à mesurer si l'échange **aide**, **nuisance** ou **ne change rien** |
| **bande passante** | réutiliser `budget_octets` du lien : un échange qui dépasse **refuse** (code 6) | c'est déjà écrit, testé et documenté ; le plan demande de la **déclarer**, pas de l'inventer |
| **dégradation** | `--entree-bruit X` sur une instance : son entrée est bruitée, l'autre non | c'est la **validation du plan** : la robustesse, pas le gain de perplexité |

**Ce que la latéralité ne fera pas, et qu'il faut écrire d'avance** : si les deux instances sont
**identiques** et reçoivent **la même** entrée, l'échange ne peut rien apporter — elles calculent
déjà la même chose. Le plan le dit (« le gain est probablement nul ») ; la conception doit donc
prévoir **où** un gain est possible : (a) entrées **différentes** (une dégradée, une propre),
(b) **asymétrie** de calcul (une instance plus profonde), (c) **mémoire** partagée (l'une a vu un
épisode, l'autre non). Sans cela, la mesure sera nulle et n'aura rien appris.

## 3. Les portes à tenir (écrites AVANT le code)

1. **échange désactivé ⇒ identique au modèle seul**, au bit près (l'invariant du plan) ;
2. **échange activé avec des jumelles identiques et la même entrée ⇒ même résultat** : si l'échange
   change le chiffre dans ce cas, c'est un **bug**, pas un gain — la porte le dit ;
3. **le coût de l'échange est mesuré et déclaré** : octets par couche échangée, paires par décision,
   et **refus** (code 6) si la bande passante déclarée est dépassée ;
4. **le cas où un gain est possible est mesuré pour de vrai** : une instance reçoit une entrée
   **dégradée** (bruit sur `--entree`), l'autre non ; on publie l'écart **et** le verdict, même
   (surtout) s'il est nul ;
5. **le lien est homotopique et le dit** : la liste des couches échangées est **affichée**, et un
   échange sur une couche qui n'existe pas est **refusé** (code 2).

## 4. Ordre de travail proposé

1. `--jumeau` + `--echange` en mode `moyenne`, avec la porte § 3.1 et § 3.2 (déterminisme et
   non-effet quand tout est symétrique) — le socle ;
2. le coût (§ 3.3) : octets, paires, refus au-delà du budget ;
3. la validation § 3.4 (entrée dégradée d'un côté) — c'est **la** question du plan ;
4. alors seulement : `--echange experts` (échanger des **choix d'experts** plutôt que des états),
   qui est la variante la plus plausible pour un gain sur un modèle routé.
