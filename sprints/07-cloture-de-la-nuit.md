# Sprint 7 — Corriger le livelock du contexte (model.rs:1117) et consolider la nuit : handoff REPRISE/README, portes finales, revue de clôture

- **Début** : 05:39 · **Fin prévue** : 07:39 (boxing de 120 min)
- **Objectif** : Corriger le livelock du contexte (model.rs:1117) et consolider la nuit : handoff REPRISE/README, portes finales, revue de clôture
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.


## Revue — ce qui est livré, mesuré

Durée : 121 min (boxing 120 min). Commits : 7.

  - `e7db33b` DeepSeek-V4-Flash téléchargé (86,9 Go, 3 shards) : architecture et tokenizer lus depuis le shard 1, 784 tenseurs depuis le shard 2 — il manque le lien entre les deux
  - `beacdf9` DeepSeek-V4.1-Flash : pas de poids ouverts — c'est DeepSeek-V4-Flash qui est téléchargé, et le plan d'adaptation est écrit
  - `17282a7` Le résultat de la nuit : à k=256 le taux est le MÊME que l'attention complète (8/9), et les échecs sont sur d'autres fenêtres
  - `1b9808e` Le correctif du livelock finissait en SIGABRT : c'est corrigé, et vérifié par le code de sortie
  - `b3cba4c` README et REPRISE : prochaines étapes et compteur de lignes après la nuit
  - `c7fd7ea` REPRISE : le livelock corrigé, et le bilan des six résultats de la nuit
  - `32951e9` Le livelock du contexte est corrigé : troncature annoncée au lieu d'une boucle infinie

**Objectif du sprint** : « Corriger le livelock du contexte et consolider la nuit :
handoff REPRISE/README, portes finales, revue de clôture ». **Le livelock est
corrigé, avec un test qui aurait pendu avant.**

### 1. Le livelock : trouvé par accident, corrigé en quinze minutes

Une sonde d'aiguille a duré 23 minutes au lieu de 75 s. Cause : son invite faisait
**4 731 jetons** pour un `--ctx 4608`. Le moteur ne refusait pas la demande — il
**bouclait sans fin** : `KvCache::assurer` fait
`while cap < besoin { cap = (cap * 2).min(self.ctx) }` (`model.rs:1117`), et si
`besoin > ctx`, `cap` plafonne à `ctx` : la condition reste vraie pour toujours.
~1 700 % de CPU, indéfiniment.

Le même défaut avait été corrigé **côté GPU** au sprint 2 (`kv_assurer`, trouvé par
une relecture) ; le chemin CPU était resté. C'est exactement la classe de défaut que
le dépôt traque : un chemin oublié qui ne se manifeste que sur une entrée
particulière.

Correctif : la capacité est plafonnée au contexte déclaré, et `Model::generate`
**tronque l'invite en le disant** —

> `[contexte] invite de 4788 jetons > ctx 4608 : les 180 premiers sont ABANDONNÉS (troncature, pas de fenêtrage)`

⚠️ **Le premier correctif était faux, et la relecture de clôture l'a prouvé** : en
tronquant à `ctx` exactement, la boucle de décodage appelait `forward(pos = ctx)`,
dont l'assertion tombait — un **SIGABRT** (exit 134) là où j'ai écrit « rendu la main
en 312 s ». Mon script de vérification ne lisait ni le code de sortie ni le mot
« panicked » : il a pris un core dump pour une réussite. C'est la septième
artefact-trust error de la nuit, et la plus coûteuse — elle portait sur mon propre
correctif.

Correctif du correctif : troncature à `ctx − n_new − 8` (la génération a sa place),
arrêt propre quand le contexte est plein, invariant `pos < ctx` gardé dans
`KvCache::ecrire` (au-delà, l'écriture partait dans le bloc de la tête KV suivante),
et bornes ajoutées à `--infer --topk` et `--ppl-reparti --ids`. **Re-vérifié en
lisant le code de sortie** : ctx 256 + invite de 306 jetons → troncature annoncée,
**exit 0** ; contexte plein → « génération arrêtée à 255 jetons », **exit 0**.

**Test de non-régression** renforcé : il exerce maintenant la BOUCLE de doublement
(4096 positions, `assurer(3000)`) puis le plafond, et l'invariant d'écriture.
**18 tests** au lieu de 17.

### 2. Le résultat scientifique de la nuit : le taux est le même

Neuf fenêtres contiguës, profondeur 0,5, 4 096 clés, mêmes invites pour les deux
chemins :

| fenêtre | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | trouvé |
|---|---|---|---|---|---|---|---|---|---|---|
| jetons du prompt | 4114 | 3996 | 4731 | 4664 | 4096 | 4046 | 4152 | 4013 | 4081 | |
| **attention complète** | oui | oui | **NON** | oui | oui | oui | oui | oui | oui | **8/9** |
| **k = 256** (6,25 %) | **NON** | oui | **oui** | oui | oui | oui | oui | oui | oui | **8/9** |

**Même taux, et les échecs ne sont pas les mêmes fenêtres** : l'attention complète
perd la plus longue (4 731 jetons) là où l'attention creuse la retrouve ; l'attention
creuse perd la première là où l'attention complète la retrouve. À 6 % des clés,
l'attention creuse **n'est donc pas moins fiable** que l'attention complète sur
cette tâche — ce qui décide du succès est la **divergence chaotique du décodage
greedy** (7e-4 nat suffisent à changer un jeton, et un code de huit caractères ne
pardonne pas un jeton).

Cela **corrige les conclusions des sprints 3 à 5** (« NON au milieu », « 0/3 à
k = 512 », « 1/3 à k = 256 ») : elles portaient toutes sur UNE fenêtre répétée. Elles
décrivaient fidèlement cette fenêtre et ne se généralisaient pas. C'est la troisième
conclusion de la nuit corrigée par une mesure plus large, et la leçon est toujours la
même : **un point n'est pas un taux, et une répétition n'est pas un tirage**.

### 3. Consolidation : ce que la prochaine session doit savoir

* `REPRISE.md` : une section « Sprint 7 » et un tableau des **six résultats de la
  nuit**, chacun avec sa source ;
* `README.md` : les « prochaines étapes » disent maintenant que le top-k déporté
  fonctionne (attention plate, croisement ~300 clés) mais **pas dans le
  préremplissage** (246 s par sonde au lieu de 75), et que la qualité de l'attention
  creuse se mesure en **taux** ;
* compteur de lignes Rust re-mesuré (13 758) dans les trois endroits qui le citent.

### 4. Portes de fin de nuit

| | valeur | référence |
|---|---|---|
| Qwen2.5-0.5B Q8_0 ctx 256 | **19,3885** | inchangée depuis le début de la nuit |
| gpt-oss-120b MXFP4 ctx 256 | **15,1757** | inchangée |
| `cargo test --release` | **18/18** | +1 (le test du livelock) |
| `--banc-topk` | vert de n = 1 à 1 000 000 | noyau fusionné inclus |
| `--banc-kv` | ×35,6 | inchangé |

## Introspection

- **Ce qui a marché** : le livelock a été trouvé parce qu'une sonde a duré anormalement
  longtemps et que j'ai fini par **mesurer les entrées** (compter les jetons de chaque
  fenêtre) au lieu de soupçonner la charge machine ou le GPU. La mesure qui tranche
  était à un `--tokenize` de distance.
- **Le motif de la nuit** : **six fois**, un artefact a promis ce qu'il ne faisait
  pas — un garde-fou jamais déclenché, un échantillon lu comme un accord global, un
  `grep` qui ne suit pas la chaîne d'appels, un décalage de fenêtre remis à zéro par
  un garde-fou mal calibré, une section annoncée dans un message de commit mais
  absente du rapport, et un moteur qui boucle au lieu de refuser. Les six ont été
  trouvés et corrigés dans le box où ils sont nés, et chacun a changé une conclusion.
  La règle qui les attrape tous : **vérifier l'instrument avant de croire la mesure**.
- **Ce que je dois changer** : deux conclusions de feuille de route ont été écrites
  puis corrigées dans la nuit (« un index est nécessaire » sur trois sondes du même
  texte ; « l'échec est systématique à k ≤ 512 » sur trois répétitions déterministes).
  Une conclusion sur un taux demande un taux, et un taux demande des tirages
  INDÉPENDANTS — pas des répétitions.
- **Doute laissé ouvert** : le taux creux (1 fenêtre mesurée sur trois chemins) et la
  courbe k(contexte) (deux points, une fenêtre chacun) ne sont pas établis. Le
  chemin par lots est le verrou : sans lui, chaque sonde creuse coûte 246 s.
- **Doute** : le livelock corrigé au point d'entrée `generate` — reste-t-il un chemin
  (mode réparti, `--ppl` avec `--limit` > `--ctx`, préremplissage par lots) qui puisse
  encore demander plus que le contexte ? La revue de clôture est justement chargée de
  le dire.

### 5. Demande de l'utilisateur en fin de nuit : DeepSeek-V4.1-Flash

L'utilisateur a demandé d'« adapter les tests de contexte à DeepSeek-V4.1-Flash »,
puis de « télécharger DeepSeek-V4.1-Flash ». Vérification faite :

* **DeepSeek-V4.1-Flash est un modèle d'API** ([api-docs](https://api-docs.deepseek.com/news/news260910/)) —
  **aucun poids ouvert**, donc rien à télécharger ;
* **DeepSeek-V4-Flash** est la base à poids ouverts ([unsloth GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF)),
  et c'est **elle** qui est téléchargée : quantification UD-IQ1_M (la plus petite,
  86,9 Go en 3 shards ; le dépôt complet pèse 1,67 To), dans
  `/home/stephane/FastNVMe/models/DeepSeek-V4-Flash-UD-IQ1_M/` (~25 Mo/s, ~1 h).

Deux obstacles mesurés, et documentés dans `docs/plan-deepseek-v4-flash.md` :
le **GGUF est découpé en shards** (le shard 1 ne contient aucun tenseur, le moteur
ouvre UN fichier) et **l'architecture `deepseek4` n'est pas implémentée** (le moteur
en lit la configuration — 43 couches, 256 experts top-6 — mais n'a pas son
attention ni son routage). Le plan en cinq étapes est écrit, avec la question qui
compte pour la mission : **le taux de récupération tient-il quand k/contexte
décroît, sur un modèle à 1 M de contexte ?**

## Planning — prochaine session

| # | chantier | critère de succès |
|---|---|---|
| 1 | **Le top-k dans le chemin par lots** (le verrou mesuré : 246 s par sonde creuse) | une sonde creuse à 4 096 clés sous 100 s, préremplissage élagué de perplexité égale |
| 2 | **Élargir le taux** : 20 fenêtres × {dense, k = 256, k = 1 024} (l'outil produit 20 fenêtres contiguës) | trois taux avec leur intervalle de confiance, et la question « les échecs sont-ils corrélés au texte ? » |
| 3 | **La courbe k(contexte)** : 8 192 et 16 384, deux fenêtres, k = 1 024 / 2 048 / 4 096 | deux points de plus, et une réponse à « le rapport k/contexte décroît-il ? » |
| 4 | **Le routage des experts** : comparer les routages CPU/GPU de gpt-oss | l'hypothèse du décalage de perplexité est confirmée ou réfutée |
| 5 | Les chemins qui peuvent encore dépasser le contexte (le livelock est corrigé, la relecture a listé les autres) | plus aucun dépassement silencieux, et c'est testé |

**Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
