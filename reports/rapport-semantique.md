# Le protocole sémantique natif — premier passage

> Campagne : **protocole sémantique natif** · expérience **1** (encodeur → décodeur, NVLink)
> Question : le modèle natif peut-il faire converger un `z` partagé sur 10 langues, puis
> restituer du sens en texte ? Verdict : **encodeur oui, décodeur non** — le rappel parallèle monte
> à **0,426** contre **0,167** de hasard et la sonde de langue tombe à **0,100** ; mais le chrF de
> traduction reste à **12,7** contre un plancher de **39,6**, et le diagnostic multilingue est
> **sous le plancher**.
> Date réelle : 2026-10-26 (HAE), base `route` 31,63 M, deux RTX 5000 par **NVLink**.

## 1. Le protocole

Le détail est dans [`docs/protocole-semantique.md`](../docs/protocole-semantique.md) ; le code dans
[`tools/semantique/`](../tools/semantique/). En bref :

1. **Rejouer** : chaque article UDHR (1–30) est lu dans **10 langues** (français, espagnol, allemand, italien,
   portugais, russe, arabe, chinois, hindi, swahili) ; le même article doit donner le même `z` (128 dims,
   normalisé), et chaque `z` doit se reconstruire.
2. **Converger** : une **contrastive InfoNCE** sur les articles (pas seulement l'alignement, qui collapse),
   un **adversaire de langue** (gradient inversé), le **mean pooling** des états cachés, et un découpage
   **par article** (train 1–24, val 25–30).
3. **Parler** : un décodeur (préfixes doux + jeton de langue cible) produit le texte ; on mesure la
   **reconstruction**, la **traduction** et le **plancher** `chrF(source, référence)`.
4. **Diagnostiquer** : plusieurs entrées (toutes les langues) → le même `z` → plusieurs sorties
   simultanées ; la matrice `chrF[source][cible]` et la **cohérence entre sources** disent où l'ambiguïté
   reste.

**Ce que le premier passage a corrigé dans le protocole** :

- l'**alignement seul collapse** : cosinus 0,98, rappel au hasard (0,18), sonde de langue 0,63 ;
- l'**all-gather détaché** était un bug : la contrastive ne touchait pas `z` ; le rendre **différentiable**
  (le gradient revient à la tranche locale) est ce qui a débloqué l'encodeur ;
- les **gradients du décodeur** écrasent l'encodeur : il faut **séparer les étages** — encodeur seul
  (contrastive + adversaire), puis décodeur **gelé** sur `z` ;
- le **décodeur partageait la base** de l'encodeur : il lui faut une **copie** (`base_decode`) et un
  préfixe plus long (16), sinon il n'a pas assez de capacité pour utiliser `z` ;
- les **articles du lot global** doivent être **distincts** : avec les mêmes articles sur les deux rangs,
  tous les positifs se confondent et la contrastive est morte.

## 2. Étage A — l'encodeur converge

Entraînement **encodeur seul** : deux rangs, `all_gather` des `z` par NVLink, contrastive globale
(articles distincts) + locale, adversaire 0,2, base lr 2e-4, tête lr 1e-3, seq 256, lot 8/rang,
30 articles, 10 langues, 300 pas. Le meilleur point est le **pas 250**.

| pas | rappel | rappel mélangé | sonde de langue | alignement |
|---:|---:|---:|---:|---:|
| 50 | 0,219 | 0,152 | 0,917 | 1,000 |
| 100 | 0,198 | 0,165 | 0,217 | 0,993 |
| 150 | 0,269 | 0,144 | 0,183 | 0,972 |
| 200 | 0,361 | 0,148 | 0,117 | 0,957 |
| **250** | **0,426** | **0,172** | **0,100** | **0,878** |
| 300 | 0,367 | 0,137 | 0,150 | 0,893 |

**Lecture** : le rappel parallèle passe de **0,167** (hasard, 1/6) à **0,426** ; le contrôle mélangé reste
à **0,172** ; la sonde de langue tombe à **0,100** (hasard 1/10). Le `z` est donc **discriminant** et
**neutre en langue** : l'étage sémantique est réel, sur 6 articles de validation. La courbe n'est pas
monotone (250 > 300) ; c'est une **fenêtre**, pas un équilibre — le même comportement que B9.

## 3. Étage B — le décodeur ne suit pas

À partir de l'état du pas 250, encodeur **gelé**, décodeur **séparé** (`base_decode`, 64,39 M au total),
préfixe 16, base_decode lr 2e-4, tête 1e-3, 500 pas demandés, arrêt à 200 (le critère d'arrêt a utilisé
le rappel, gelé — défaut de protocole à corriger : le critère de l'étage B doit être le chrF).

| pas | perte | chrF reconstruction | chrF traduction | plancher |
|---:|---:|---:|---:|---:|
| 50 | 12,39 | 12,2 | 5,6 | 39,6 |
| 100 | 7,45 | 12,2 | 7,8 | 39,6 |
| 150 | 3,03 | 12,5 | 7,5 | 39,6 |
| 200 | 1,56 | **12,7** | **5,3** | **39,6** |

La perte **s'effondre** (12,4 → 1,6) mais le chrF **ne bouge pas** (12,7) et reste **très en dessous du
plancher** (39,6). La génération ne suit pas la perte : le décodeur apprend la distribution locale, pas
la restitution conditionnée par `z`. **Négatif nommé** : l'étage B n'est pas tenu.

**Diagnostic multilingue simultané** — 5 langues (`fra`, `spa`, `deu`, `cmn`, `swh`), 2 articles de
validation, toutes les sources × toutes les cibles en un lot :

| mesure | valeur |
|---|---:|
| chrF diagonal (reconstruction) | **7,30** |
| chrF hors diagonale (traduction) | **6,26** |
| plancher source→référence | **12,57** |
| consensus entre sources (même cible) | **29,64** |
| sensibilité à la source | **0,704** |

Le décodeur est **sous le plancher** dans les deux sens ; le consensus de 29,6 entre sources est bas, et
la sensibilité à la source (0,704) est haute : les sorties dépendent encore de la langue d'entrée. C'est
exactement l'ambiguïté que le diagnostic devait révéler.

### Ablations : ni le préfixe ni la dimension ne débloquent

Trois variantes ont été testées après le premier passage.

| variante | ce qui change | résultat |
|---|---|---|
| **goulot 512** | `z` de 512 dims au lieu de 128, même étage A | rappel **0,278** (contre 0,426) ; 30 articles ; la dimension supplémentaire **dégrade** la séparation |
| **préfixe 64** | décodeur à 64 préfixes au lieu de 16, encodeur gelé | chrF **12,4 / 6,7** à 200 pas (contre 12,7 / 5,3) : pas de gain |
| **joint** | encodeur dégelé à lr 1e-5, contraste 5, adversaire 0,2 | rappel **0,437**, sonde **0,100**, chrF **12,9 / 8,4** : le `z` garde l'identité, le décodeur ne décolle pas |
| **ablation de `z`** | décoder avec `z` / `z=0` / `z` aléatoire | **5,84** / **2,52** / **2,56** : le décodeur **utilise** `z`, mais `z` ne porte pas le détail du texte |
| **8 unités** | tête linéaire 8 × 128 + diversité 0,2, moyenne pour le rappel | rappel **0,237** (contre 0,426) : la moyenne des unités **dilue** ; les unités ne sont pas encore des lecteurs distincts |

**Lecture** : un `z` unique de 128 dimensions est un **code d'identité** (il retrouve l'article, il ne le
reconstruit pas). Agrandir le vecteur ne rend pas le texte ; allonger le préfixe ne rend pas le texte ;
dégeler l'encodeur avec la reconstruction ne rend pas le texte. Le verrou est le **goulot** : une tête linéaire à 8 unités, moyennée pour le rappel, **dilue** (0,237) ;
il faut des unités qui **lisent des positions différentes** — une **attention de requêtes** sur les états,
ou une **attention croisée** du décodeur — pas une moyenne de projections.

## 4. Ressources et communication

- **NVLink** : `nvidia-smi topo -m` donne **NV1**, `nvidia-smi nvlink --status` **25,781 GB/s** ; NCCL
  **2.28.9** ; `NCCL_P2P_LEVEL=NVL`.
- **Deux rangs explicites** (torchrun/elastic n'a pas démarré sur cette machine) : un GPU par rang,
  `all_gather` différentiable des `z` et `all_reduce` des gradients par NVLink.
- **Étage A** : 31,97 M, seq 256, lot 8/rang, GPU 65–78 %, ~80 s pour 300 pas.
- **Étage B** : 64,39 M (deux bases), GPU ~61 %, ~160 s pour 200 pas.
- **CPU** : deux processus à ~100 % d'un fil chacun ; le reste du CPU est libre. Ce n'est plus le goulot :
  c'est le GPU et la boucle de décodage.

## 5. Ce qui pourrait rendre ce résultat faux

- **6 articles de validation** : le rappel 0,426 a un intervalle large ; il faut 20–30 articles.
- **Une seule graine** à chaque étage ; l'effet peut être une graine favorable.
- **Le critère d'arrêt de l'étage B** est le rappel (gelé), pas le chrF : l'arrêt à 200 n'est pas le bon.
- **Le décodeur** est un préfixe doux de 16 tokens sur une copie de la base ; un décodeur à attention
  croisée ou un entraînement plus long peut changer le verdict.
- **Le plancher** est calculé sur la surface source, pas sur un traducteur : c'est un plancher grossier.
- **La sonde de langue** est un centroïde, pas un classifieur entraîné ; elle sous-estime peut-être la langue.

## 6. Ce que le premier passage établit

1. **L'étage sémantique est possible** : un `z` de 128 dims, entraîné par contrastive + adversaire sur
   NVLink, sépare les articles et perd la langue (rappel 0,426, sonde 0,100).
2. **L'alignement seul ne suffit pas** : il collapse (0,98, rappel au hasard) ; la contrastive et
   l'adversaire sont nécessaires.
3. **L'ordre des étages compte** : les gradients du décodeur écrasent l'encodeur ; il faut entraîner
   l'encodeur d'abord, puis le décodeur sur `z` gelé.
4. **Le décodeur n'est pas réglé** : la perte baisse, le chrF non ; le diagnostic multilingue est sous le
   plancher. Les ablations montrent que **la dimension de `z` et la longueur du préfixe ne sont pas le
   levier** : un vecteur unique est un code d'identité, pas un code de contenu. Le raisonnement sur `z`
   gelé **n'est pas branché** — ce serait mesurer un décodeur, pas une pensée.

## 7. Prochaine action

- **Décodeur** : **unités sémantiques multiples** (une séquence de `z`, comme la RSN) ou **attention croisée**
  (z comme mémoire, pas comme préfixe) ; plus de données, décodage par recherche ; critère d'arrêt = chrF.
- **Validation** : 20–30 articles, 3 graines, split de langue (entraîner sans une langue, la tester).
- **Diagnostic** : matrice complète 10×10 sur 6 articles ; la sensibilité à la source doit baisser.
- **Raisonnement** : après un décodeur au-dessus du plancher seulement ; sinon, on ne mesure que la surface.

Les données et les historiques sont dans [`semantique-mesures.json`](semantique-mesures.json) ; le
protocole dans [`docs/protocole-semantique.md`](../docs/protocole-semantique.md) ; le code dans
[`tools/semantique/`](../tools/semantique/).
