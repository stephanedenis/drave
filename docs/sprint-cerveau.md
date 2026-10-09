# Sprint « cerveau complet » — état d'avancement

> Lancé le 9 octobre à 17 h, **en autonomie jusqu'au 10 octobre 9 h (HAE)**.
> Plan de référence : `docs/plan-cerveau-complet.md` § 4 (premier sprint).
> Ce fichier est mis à jour **à chaque round** : il est la mémoire du sprint.

---

## Objectif du sprint

Trois capacités du plan, chacune avec sa **porte mesurée** :

| # | capacité | porte (invariant à vérifier) | état |
|---|---|---|---|
| **C1** | **graphe de régions** : descripteur de topologie, validateur, ordonnanceur par dépendances, pilote multi-nœuds | un graphe **linéaire** rend des logits identiques **au bit près** ; un découpage à **trois régions** égale le modèle d'un seul tenant | **C1a FAIT** · C1b à faire |
| **C12** | **trace globale horodatée + rejeu** | rejeu d'une exécution distribuée == exécution, **0,00e0** | à faire |
| **C5** | **bus de modulation multi-canaux** | canal nul ⇒ sortie **inchangée** | mécanique partielle (fichier), bus à faire |

**Contraintes non négociables** : les **23 portes** du dépôt et les tests restent
verts ; le profil `release` reste le **binaire de mesure** (toute promotion se paie
d'un passage des portes) ; le crate reste **std seul, sans dépendance**.

---

## C1a — descripteur de topologie (FAIT, 9 octobre 17 h 10)

**Livré** : `drave-core/src/topologie.rs` (module autonome, ~420 lignes dont 8 tests) :

- **format JSON minimal**, analysé **à la main** (le crate est std seul) : objets,
  tableaux, chaînes, entiers — et *rien d'autre* ;
- **validation stricte** : trou de couverture, recouvrement de couches, identifiant
  dupliqué, lien vers une région inconnue, lien réflexif, **cycle** (refusé tant que
  la récurrence C2 n'existe pas), clé inconnue, mode de lien inconnu — chacun avec un
  message et un **code de sortie** ;
- **ordre d'exécution** par tri topologique de Kahn, et détection « chaîne *vs*
  graphe » (le cas de non-régression) ;
- **`Topologie::chaine()`** : la topologie déduite de `--couches-locales`, c'est-à-dire
  le pont entre l'existant et le graphe.

**Commandes et résultats vérifiés** :

```bash
drave --topologie /tmp/topo_chaine.json   # CHAÎNE · 2 régions · plan en 2 étapes
drave --topologie /tmp/topo_y.json        # GRAPHE · 3 régions · délai déclaré affiché
drave --topologie /tmp/topo_trou.json     # refus : « couche 12 n'est portée par aucune région » (code 3)
```

**La topologie se lit sans modèle** : la commande passe avant le chemin du GGUF, parce
qu'un descripteur de régions ne décrit pas des poids.

**Tests** : 8 (chaîne lue et validée, trou, recouvrement, cycle, clé inconnue, mode
inconnu, graphe en Y, chaîne du moteur). Suite complète : **85 tests**.

---

## Prochaines étapes (dans l'ordre)

1. **C1b — pilote multi-régions** : `--topologie F --ppl-reparti` doit exécuter le
   graphe au lieu de la chaîne. Premier jalon : une topologie **linéaire** à trois
   régions sur deux instances doit rendre la **même perplexité** que le modèle entier,
   puis le cas à deux nœuds doit reproduire l'écart **0,00e0** d'aujourd'hui.
2. **C12 — trace globale** : chaque événement porte `(région, pas, lien, horodatage)`,
   et un mode `--rejouer-globale` doit rejouer l'exécution **à l'identique**.
3. **C5 — bus de modulation** : canaux (`recompense`, `nouveaute`, `incertitude`)
   diffusés à toutes les régions, y compris entre instances ; porte : canal nul ⇒
   aucune différence, bit à bit.

## Journal du sprint

| heure | fait |
|---|---|
| 9/10 17 h 10 | **C1a** : module `topologie.rs`, validation stricte, plan, 8 tests, suite à 85 tests. |
