# Rapport — découpage des MoE en clusters, pour notre mode d'opération

**En une ligne** : sur Qwen3-30B-A3B (128 experts, 8 par jeton), regrouper les
experts par **fréquence d'usage** suffit à diviser par ~1,8 la ventilation d'un
jeton (3,08 nœuds au lieu de 5,32 au hasard, à 8 clusters) — et la co-activation,
qui devait faire mieux, donne **exactement la même partition** (accord 1,000). Le
découpage n'a donc pas besoin d'un algorithme de graphes : il a besoin d'un
**ordre**, et d'un format qui le respecte.

## Pourquoi cette question

Notre mode d'opération est événementiel et réparti : un jeton ne lit que les
experts qu'il allume, et si les experts sont sur des nœuds différents, il faut
autant d'allers-retours que de nœuds concernés. Les compteurs d'usage existants
disaient quels experts sont **chauds** ; ils ne disaient pas lesquels sont chauds
**ensemble**. C'est cette seconde information qui décide du placement.

## La chaîne de mesure

1. **Trace de routage dans le moteur** — `DRAVE_TRACE_EXPERTS=<chemin>` écrit une
   ligne par (couche, jeton) : les indices des experts retenus. Ajouté aux DEUX
   chemins (jeton par jeton et par lots), parce que le préremplissage passe par le
   second et que c'est lui qui voit le plus de jetons.
2. **`tools/clusters_moe.py`** — construit la co-activation par couche, découpe en
   `G` clusters **équilibrés** (glouton : experts du plus fréquent au plus rare,
   chacun rejoint le cluster qui a de la place et maximise la co-activation
   moyenne ; puis recherche locale), et mesure trois choses :
   * **couverture** : part des k experts d'un jeton qui tiennent dans son meilleur
     cluster (1,0 = un seul nœud suffirait) ;
   * **ventilation** : nombre de clusters nécessaires pour couvrir 90 % des experts
     d'un jeton (1,0 = le meilleur cas possible) ;
   * **équilibre** : taille des clusters.
3. **Deux témoins**, sans lesquels les chiffres ne veulent rien dire : le même
   découpage **au hasard** (mêmes tailles) et le même découpage **groupé par
   fréquence** (sans co-activation).

## Résultats — Qwen3-30B-A3B, ~1 600 jetons, 48 couches

| clusters | couverture | ventilation | couverture (hasard) | ventilation (hasard) | gain |
|---|---|---|---|---|---|
| 4 | **0,799** | **1,94** | 0,440 | 3,59 | ×1,8 |
| 8 | **0,607** | **3,08** | 0,319 | 5,32 | ×1,9 |
| 16 | **0,442** | **4,46** | 0,250 | 6,55 | ×1,8 |

**Le résultat négatif est le plus utile** : la partition apprise par co-activation
et celle qui se contente de **trier les experts par fréquence** sont **identiques**
— accord de 1,000 sur les paires, pour les trois valeurs de G et sur toute la
trace. Autrement dit : sur ce modèle, les experts qui s'allument ensemble sont
simplement les experts fréquents. La co-activation n'ajoute rien que la fréquence
ne donne déjà.

Conséquence pour le format : pas besoin d'un partitionneur de graphe ni d'un
index sophistiqué. Il faut un **ordre** (experts chauds d'abord) et une
**disposition contiguë** qui permette à un nœud de ne lire que sa tranche.

## Ce que cela implique pour le mode d'opération

* **8 nœuds, 8 clusters** : un jeton interroge **3,08** nœuds en moyenne au lieu de
  5,32 — la ventilation est divisée par 1,7, donc la latence et le trafic aussi.
* **4 nœuds** : 1,94 nœud par jeton — un jeton sur deux tient dans un seul nœud.
* Ce gain ne vient pas d'une organisation « intelligente » mais du **déséquilibre
  d'usage** des experts : quelques experts servent presque tous les jetons. Le
  corollaire est une mise en garde : un découpage **équilibré par taille** (ce que
  fait ce prototype) n'est pas optimal en charge ; il faudrait équilibrer par
  *usage*, ce qui est un autre problème (et une autre mesure).

## Le format proposé (esquisse, à confronter aux gros modèles)

1. **Un manifeste multi-fichiers** (`MANIFEST.json` à côté du GGUF) : pour chaque
   shard, les tenseurs, leurs offsets et leurs longueurs. Indispensable de toute
   façon : les modèles lourds sont livrés en 3 à 8 shards et le moteur n'ouvre
   qu'un fichier aujourd'hui.
2. **Un index MoE** (`*.moe.json`) : par couche, l'ordre des experts par fréquence
   et l'affectation aux clusters. Un nœud lit sa tranche d'experts en mmap, sans
   parcourir le fichier.
3. **Une disposition contiguë par cluster** : les tenseurs d'un même cluster
   regroupés dans le fichier. Un nœud qui héberge le cluster *c* n'a alors qu'une
   plage à lire, ce qui rend le streaming NVMe→RAM→VRAM séquentiel au lieu
   d'aléatoire.
4. **Compatibilité** : tout ceci est optionnel. Un GGUF sans index se comporte
   comme aujourd'hui ; l'index est un accélérateur, pas une dépendance.

## Ce que ce rapport ne dit pas

* **un seul modèle** (Qwen3-30B-A3B, 8 experts sur 128) et **un seul corpus**
  (Wikitext-2, ~1 600 jetons). gpt-oss (4 experts sur 128) est en cours de mesure ;
  DeepSeek-V4.1-Flash, Kimi-K2.7 et GLM-5.3 (256 experts ou plus, jusqu'à 1 M de
  contexte) sont en téléchargement — c'est là que le découpage compte vraiment, et
  c'est la première chose à refaire avec eux.
* **l'usage pondéré** : la trace ne contient que les indices, pas les poids. Or un
  jeton est dominé par son premier expert ; une couverture pondérée serait plus
  parlante (le moteur peut écrire les poids, c'est une ligne).
* **le coût du déséquilibre** : les clusters sont équilibrés en NOMBRE d'experts,
  pas en charge. Un nœud qui reçoit les experts chauds travaillera plus que les
  autres — mesuré nulle part ici.
* **la longue traîne** : 1 600 jetons ne suffisent pas à couvrir les experts rares
  (certains n'apparaissent qu'une fois). La trace de 2 048 jetons en cours et les
  traces longues sur les gros modèles trancheront.

## Reproduire

```bash
# 1. la trace
DRAVE_TRACE_EXPERTS=/tmp/routage.txt ./drave-core/target/release/drave <modele> \
    --ppl /tmp/ids_qwen_long.txt --ctx 2048 --limit 2048 --lot 64 --threads 16
# 2. le découpage
python3 tools/clusters_moe.py /tmp/routage.txt --clusters 8 --json /tmp/clusters.json
```
