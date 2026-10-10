> Campagne : **toutes-langues** · expérience **52**
> Titre : 52. Un processus ORPHELIN volait la moitié de la machine — et mon propre outil de nettoyage l'avait laissé passer
> Date réelle : **2026-10-06 17:22 HAE** (source : commit `0b9599c`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 52. Un processus ORPHELIN volait la moitié de la machine — et mon propre outil de nettoyage l'avait laissé passer

### 52.1 Le symptôme

Le traçage du corpus Wikipedia apparié tournait **quatre fois trop lentement** :
**60 s par trace** au lieu des 16 s mesurés à vide. À ce rythme, 2 892 traces
demandaient **48 heures** — au-delà de toute fenêtre.

### 52.2 La cause

Deux processus `drave` tournaient **en parallèle** alors que le script de traçage est
**séquentiel** : il n'en lance qu'un à la fois. Le second avait pour parent
`systemd --user` (PID 1 du utilisateur) — c'était un **orphelin**, survivant d'un
lancement antérieur dont j'avais tué le script mais **pas l'enfant**.

Un processus dont le parent meurt est **ré-adopté par `systemd`** et continue de
tourner. Il consommait **18 cœurs sur 40**, et écrivait dans
`parallele_crime/traces/en_05.drvf` — un fichier **partiel**, tronqué en pleine
écriture, que le script aurait ensuite **sauté** (`[ -s fichier ] && continue`) en le
croyant complet.

### 52.3 Pourquoi mon outil de nettoyage ne l'a pas vu

Mon tueur en Python cherche un motif dans la ligne de commande des processus :

```python
if 'trace_crime' in cl or ('ctx 8192' in cl and 'drave' in cl):
```

Or la ligne de commande du **script** contient `trace_crime`, mais celle de son
**enfant `drave`** ne la contient pas — elle contient `drave … --trace-flux …`. Tuer
le script laisse donc l'enfant vivant, ré-adopté, invisible au motif suivant.

**La règle qui manquait** : quand on tue un script qui lance des enfants, il faut tuer
**par arbre de processus**, pas par motif de ligne de commande. Et vérifier ensuite
qu'aucun orphelin n'a `systemd` pour parent.

### 52.4 Le résultat après nettoyage

| | avant | après |
|---|---:|---:|
| durée d'une trace Wikipedia | **60 s** | **16-17 s** |
| charge moyenne | 45 | **28** |
| durée estimée des 2 892 traces | 48 h | **~13 h** |

**Un seul orphelin coûtait 2,5× sur tout le corpus.** Et le fichier partiel a été
supprimé : il aurait produit un segment manquant **silencieusement**, exactement le
genre de faute que ce rapport traque ailleurs.

### 52.5 Une décision prise au passage

Le traçage du corpus **Crime et Châtiment** a été **arrêté** : 774 s par trace
(13 minutes !) pour 48 traces, en concurrence avec les 2 892 traces Wikipedia qui
demandent 17 s chacune. Le rapport de valeur était manifestement défavorable.
**4 segments sur 24 sont tracés** et conservés ; le corpus est écrit et pourra être
traité plus tard, hors concurrence.


---
