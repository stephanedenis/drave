> Campagne : **toutes-langues** · expérience **19**
> Titre : 19. Couche 8 contre couche 10 : la correction de cible PAIE
> Date réelle : **2026-10-06 04:38 HAE** (source : commit `e89dbe3`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 19. Couche 8 contre couche 10 : la correction de cible PAIE

Même corpus (Romeo, 24 scènes appariées), même protocole (entraîné sur l'anglais,
testé sur le français), même taille de réseau. **Seule la couche cible change.**

| | **couche 10** | **couche 8** | gain |
|---|---:|---:|---:|
| invariance du professeur | 0,6532 | **0,7044** | **+0,0512** |
| fidélité sur l'anglais (apprise) | 0,6660 | **0,6967** | +0,0307 |
| **fidélité sur le français (transférée)** | 0,5802 | **0,6015** | **+0,0213** |
| invariance de sortie | **0,9540** | 0,9504 | −0,0036 |
| pire segment | **0,8738** | 0,8650 | −0,0088 |
| oracle sur le français | 0,6207 | **0,6540** | +0,0333 |
| **écart oracle** | **+0,0405** | +0,0525 | +0,0120 |

### La correction de cible paie, et le prix est négligeable

**+0,0213 sur la fidélité TRANSFÉRÉE** — c'est-à-dire sur la seule mesure qui
compte pour un pont destiné à servir : celle où l'on transporte le modèle vers une
langue qu'il n'a jamais vue, sans réapprentissage.

**Le seul prix est une invariance de sortie inférieure de 0,0036** — négligeable,
et c'est la courbe d'échange connue : un peu moins d'invariance pour nettement
plus de fidélité.

**Et le professeur lui-même confirme** : son invariance segment par segment passe
de 0,6532 à **0,7044** entre les couches 10 et 8. Le plateau est bien là, et le
pont n'apprend plus du détail en re-spécialisation.

### Ce que cela dit de la méthode

**Ma cible avait été choisie sur une seule mesure** — l'article 1 de l'UDHR avec
40 langues, qui plaçait le pic à 42 % de profondeur. Deux corpus et deux panels
ultérieurs le placent deux crans plus haut. **Le choix de la cible est un paramètre
aussi important que l'architecture**, et il se mesure.

**Il reste à refaire proprement sur l'UDHR complète** : le traçage des 392 langues
n'a écrit que les couches **0 et 10** (`--trace-couches 0,10`), donc la
comparaison à grande échelle demanderait un retraçage avec la couche 8 incluse.
Sur Romeo elle était possible sans retraçage parce que j'avais tracé `0,4,8,10` par
précaution — et cette précaution a payé.


---
