# Le coût du professeur : ce qu'on calcule pour rien

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

Constat de départ : nos traces contiennent **toutes** les couches du professeur.
La mission s'arrête au premier niveau abstrait — couche 10 sur 24 pour Qwen2.5-0.5B,
couche 17 sur 48 pour Qwen3-30B-A3B. Tout ce qui suit est calculé, écrit, stocké,
et jamais lu.

## 1. Le gaspillage, mesuré sur les traces existantes

| trace | professeur | couches stockées | profondeur utile | **gaspillé** |
|---|---|---|---|---|
| `vaste/eng.drvf` | Qwen2.5-0.5B | 0..23 + 1000..1023 | 0..10 | **77,4 %** |
| `langues30b/deu.drvf` | Qwen3-30B-A3B | 0..47 + 1000..1047 | 0..17 | **82,6 %** |

Les couches `1000+k` sont les sous-couches de la couche `k` : le traçage enregistre
les deux, donc 48 entrées de couche pour un modèle de 24.

## 2. Ce que `--couches a:b` rattrape

Texte complet de l'UDHR en anglais (42 unités, 10 412 caractères), `--lot 1` :

| | couches tracées | enregistrements | taille | temps |
|---|---:|---:|---:|---:|
| sans `--couches` | 48 (0..23 + sous-couches) | 24 192 | 60,6 Mo | **25,52 s** |
| `--couches 0:11` | 22 (0..10 + sous-couches) | 11 088 | 27,7 Mo | **16,63 s** |

**−35 % de temps, −54 % de disque**, et le fichier contient exactement la profondeur
utile. Sur le professeur 30B (48 couches, utile jusqu'à 17), `--couches 0:18` coupe
**62 % du calcul**.

## 3. Le piège : `a:b` EXCLUT `b`

`--couches 0:10` rend les couches **0 à 9**. Pour inclure la couche 10 il faut
`--couches 0:11`. Vérifié sur les en-têtes : `COUCHES STOCKÉES = [0..9, 1000..1009]`.

## 4. La coupe n'est PAS transparente — et le témoin le prouve

Le moteur **est** déterministe : deux exécutions identiques rendent 5 544/5 544
positions bit-à-bit égales. Et `--couches 0:24` (plage complète explicite) est
**exactement** égal à l'absence du drapeau. Le drapeau lui-même ne change donc rien.

Mais `--couches 0:11` **altère les couches qu'il conserve** :

| comparaison | positions identiques | écart max (i16) |
|---|---|---|
| A vs A (même commande) | 5 544 / 5 544 | 0 |
| A vs C (`--couches 0:24`) | 5 544 / 5 544 | 0 |
| **A vs B (`--couches 0:11`)** | **5 192 / 5 544** | **188** |

Ce n'est pas un simple facteur d'échelle (une norme finale ferait cos = 1 et un
rapport constant) :

| couche | cos(A, B) | \|A\|/\|B\| | écart-type |
|---|---:|---:|---:|
| 0 | **1,000000** | 1,000000 | 0 |
| 5 | 0,995591 | 0,999527 | 7,3e-03 |
| 10 | 0,997972 | 1,000356 | 7,7e-03 |

La couche 0 est **exacte**, la divergence naît ensuite et plafonne autour de
**0,2–0,4 % d'angle**. C'est une déviation numérique, pas sémantique — mais elle
existe, et elle déplace la *cible* qu'on demande au pont d'atteindre.

**Cause dans le code** : `couche_fin < n_layer` fait rendre au moteur le **flux
brut** au lieu du flux normalisé (`model.rs:5740`), sémantique voulue pour un nœud
de grappe (« ce qu'un nœud doit expédier »), et le commentaire de `model.rs:2559`
documente déjà le danger de la double norme. `--couches` est un outil de
**répartition**, pas un arrêt anticipé d'inférence.

## 5. La règle

- **Traçage du professeur** : `--couches` est acceptable — 0,3 % d'angle est très
  en dessous des effets mesurés (±3 points de fidélité), à condition de le **dire**.
- **Un vrai arrêt anticipé** (garder la sémantique du modèle entier, ne pas calculer
  les couches suivantes) reste à écrire : c'est la seule version sans réserve.
- **Ne jamais** mettre `--trace-couches` en croyant borner le calcul : il ne filtre
  que l'**écriture**. Seul `--couches a:b` borne l'exécution.

## 6. Second gaspillage : `--couches` borne l'EXÉCUTION, pas le CHARGEMENT

Mesuré sur la trace en cours (Qwen2.5-0.5B, `--couches 0:11`) :

```
[modele] 24 couches chargées en 8.514 s — listes 1.04 Go , 20 threads
```

**24 couches chargées pour 11 exécutées.** Dans `load_partiel`, la construction des
couches est une boucle `for l in 0..cfg.n_layer` (`model.rs:4001`) ; la plage
`couches` n'est consommée qu'**après**, en `couche_debut`/`couche_fin`
(`model.rs:4368-4369`). Le lyrisme des commentaires (« exécution bornée ») est exact
mais partiel : on charge tout, on n'exécute qu'une partie.

Sur le 0.5B (491 Mo) c'est sans conséquence. Sur **Qwen3-30B-A3B**, professeur dont
on n'utilise que les couches 0..17 sur 48, cela veut dire **lire 18 Go sur un disque
rotatif pour en calculer 37 %**. Le correctif est court — passer `couches` à la
boucle de construction et sauter les indices hors plage — et n'a pas été fait ici.

## 7. Le coût d'une longue invite : l'attention est quadratique

Tentative de tracer les **42 unités** de l'UDHR (10 424 caractères en anglais,
20 703 en abkhaze) à `--ctx 4096`. Après **plus de cinq minutes**, l'abkhaze était
toujours en cours et le fichier atteignait **156 Mo** — contre 16,6 s et 27,7 Mo
pour l'anglais à `--ctx 512`. Passage de 512 à 4 096 jetons = **64× plus de travail
d'attention**. Job arrêté.

**Leçon** : pour multiplier la donnée, il faut multiplier les **passes courtes**,
pas allonger les passes. Retenu : **10 unités par langue** (~130 jetons en anglais,
~350 en abkhaze) à `--ctx 1024`, soit ~5× la donnée actuelle pour ~12 s par langue.
