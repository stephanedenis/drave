# Campagne 24 h — où Drave est à son meilleur, tâche par tâche

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

> 08/10, 21 h. Le matériel suivant n'est pas encore là ; cette campagne occupe
> la machine à mesurer ce que l'architecture par listes vaut **pour chaque
> famille de tâches**, au lieu du seul couple (Qwen2.5-0.5B, perplexité) sur
> lequel le dépôt a le plus mesuré.
>
> File d'exécution : `tools/campagne-benefices.sh` (relançable étape par étape).
> Journaux et sorties brutes : `/tmp/campagne24/`. Entraînements en parallèle sur
> les deux GPU (`/tmp/campagne24/tr_*.log`).

---

## 1. Le piège trouvé avant de commencer

`data/wikitext2_test.txt.ids` **vient d'un autre tokenizer** que Qwen2.5 : il
commence par `201,438,10498…` là où Qwen2.5 produit `198,284,8397…`. Le donner au
0,5 B ne mesure pas le modèle, il mesure la perplexité d'un texte découpé par
quelqu'un d'autre :

| identifiants utilisés | perplexité (256 jetons, ctx 512) |
|---|---:|
| ceux du dépôt (`data/wikitext2_test.txt.ids`) | **7 710,72** |
| tokenisés **par le modèle** | **17,43** |

Toute la campagne serait partie de là. La règle est donc inscrite dans le script :
**chaque modèle tokenise son propre corpus** (`ids_pour`), et aucune mesure n'est
prise sur un fichier d'identifiants d'origine inconnue.

---

## 2. Les familles de tâches, et ce qui est mesurable aujourd'hui

| famille | support dans Drave | ce que la campagne mesure |
|---|---|---|
| **langage** (perplexité) | oui | grille de modèles 0,5 B → 120 B |
| **génération / latence** | oui | tok/s, et le coût par jeton |
| **contexte long** | oui | ctx 512 → 8 192, mémoire et débit |
| **préremplissage par lots** | oui | `--lot` 1 → 64 : le seul levier qui multiplie un débit de disque |
| **code** | oui (modèles) | codestral-22B et gpt-oss dans la grille |
| **raisonnement** | oui (modèles) | r1-distill-1.5B et 14B dans la grille |
| **MoE / routage** | oui | Qwen3-30B-A3B : experts réveillés, volume de routage |
| **parcimonie événementielle** | oui | seuil et k-WTA, dense contre listes |
| **multilingue / sémantique** | oui (outils) | traces UDHR : la bande 10-15 survit-elle à la correction d'échelle ? |
| **répartition** | oui | deux nœuds, et la carte de latence |
| **embeddings / recherche** | **NON** | `bge-m3` est lisible en en-tête mais **inexécutable** : le moteur exige `blk.0.attn_norm.weight` et une attention causale. C'est un manque, pas un résultat |
| **décodage spéculatif** | **NON** | `eagle3-gpt-oss-120b` est sur le disque, le moteur n'a aucune notion de brouillon (`grep eagle\|brouillon\|specul` = 0) |

---

## 3. La file

| étape | ce qu'elle produit | durée typique |
|---|---|---|
| `grille` | 6 modèles : PPL, RSS, octets lus, débit (0,5 B → 120 B, HDD et NVMe) | 1 à 3 h |
| `parcimonie` | 12 réglages × {dense, listes} : PPL, événements, tok/s | ~1 h |
| `contexte` | ctx 512 → 8 192 : PPL, cache KV choisi, RSS | ~20 min |
| `lot` | `--lot` 1 → 64 sur 512 jetons | ~15 min |
| `routage` | MoE 30B : experts par jeton, volume | ~20 min |
| `semantique` | traces UDHR avec et sans l'échelle par enregistrement | ~30 min |
| `noyau` | bande passante mémoire, push/pull par densité | ~5 min |
| `repartition` | `porte-flux.sh` + la porte du modèle entraîné | ~20 min |
| `portes` | les portes de non-régression | ~10 min |

**Et cinq batches enchaînés automatiquement après la file** (chacun attend le
marqueur de fin du précédent — un `pgrep` sur un script pas encore lancé rend la
main tout de suite, et deux gros modèles se retrouveraient lus en même temps) :

| batch | question | mesure |
|---|---|---|
| **2** | le bénéfice événementiel dépend-il de la **tâche** ? | même modèle sur prose, français, code, multilingue : densité, PPL, débit en dense et en listes |
| **3** | la mémoire **tient-elle** ? | aiguille dans la botte de foin, 512 → 4 096 jetons, 3 profondeurs |
| **4** | que vaut la **génération** ? | TTFT et débit par modèle, quatre tâches (code, traduction, arithmétique, résumé) verbatim, conversation à trois tours |
| **5** | le **lot** paie-t-il sur un modèle qui ne tient pas en cache ? | Qwen3-30B-A3B depuis le NVMe, `--lot` 1 → 64 |
| **6** | le **cas extrême** | DeepSeek-V4.1-Flash Q2, **365,7 Go sur 125 Go de RAM** : octets lus, RSS, temps |

### Les entraînements lancés en parallèle

Deux paires **à lecture égale** (le jumeau dense lit exactement ce que le routé
lit par jeton), pour voir si l'avantage du routage tient à l'échelle :

| GPU | paire | paramètres | lectures/jeton/couche |
|---|---|---|---|
| 0 | dense dim 256 (ff 768) **vs** routé 8 experts, top-2, 384 | 3,2 M vs ~10 M | 0,85 M |
| 1 | dense dim 384 (ff 1152) **vs** routé 16 experts, top-2, 576 | 7,2 M vs ~40 M | 1,92 M |

40 000 pas chacune, corpus de 100 Mo, initialisation à 0,08 et évaluation
alignée (les deux corrections du 08/10). À l'arrivée : export GGUF, porte
d'exécution, mesure des paires et des événements par jeton dans le moteur, puis
répartition à deux nœuds.

---

## 5. Ce qui est déjà acquis avant la campagne (pour ne pas le refaire)

- **La parcimonie s'entraîne** : R̂ = 0,17 atteint par l'entraînement, réglable
  jusqu'à 0,03 — là où la parcimonie imposée après coup plafonnait à 85 % de
  densité (`reports/rapport-parcimonie-entrainee.md`).
- **Un événement n'est pas un MAC** : le pull dense est au mur mémoire (14,0 Go/s,
  67 % du repère), et un événement coûte 2,9× (valué) à 4,3× (signé) un poids
  dense. D'où la cible : quelques pour cent de densité, pas 15 %.
- **Le modèle produit ici tourne dans Drave et se découpe** : porte d'exécution
  tenue (corrélation des logits min 0,99, top-1 95,7 %) et répartition à deux
  nœuds à **0,0000 % d'écart** (`reports/rapport-modele-moteur.md`).
