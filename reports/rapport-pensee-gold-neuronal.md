# L — le gold neuronal : un tagger 7B local, la cascade POS à 0,944

> **Ligne de roadmap** : **B13** (moteur de pensée) / **R0.7** (bloc linguistique) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **le tagger 7B-Instruct local est qualifié** — POS seul **0,8483** (heuristique
> **0,7512**), **cascade à 0,6 : 0,9440** (20 réelles **0,9238**, 160 synthétiques **0,9471**),
> **0 refus**, **180 appels**. La cascade **garde** les classes fermées de l'heuristique (**0,9392**)
> et lui **prend** les ouvertes (**0,9474**) : c'est la complémentarité, pas le remplacement.
>
> **Dispositif** : [`qualifier_neuronal.py`](../tools/tests/linguistique/qualifier_neuronal.py) ;
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`NeuronalLLMPOS`) ; JSON
> [`pensee-gold-neuronal.json`](pensee-gold-neuronal.json).

## 1. Ce qui était bloqué

Le rapport du gold ([`pensee-gold`](rapport-pensee-gold-linguistique.md) § 4) disait : « le vrai
modèle neuronal est **refusé** (`llama-cli` local) ; la qualification neuronale reste à faire ».
Le refus était un **timeout** : `NeuronalLLM` lançait `llama-cli` sans `-st`, le binaire entrait
en mode conversation et attendait une entrée qui n'arrivait jamais. Deux autres pièces
manquaient : un **modèle local qui suive le format**, et un **tagger** qui rende des POS alignés
sur la tokenisation du bloc.

## 2. Le dispositif

- **Modèle** : Qwen2.5-7B-Instruct, GGUF **Q4_K_M**, deux shards (4 683 073 632 octets au total),
  téléchargés depuis `Qwen/Qwen2.5-7B-Instruct-GGUF`. SHA-256 dans le JSON :
  `dfce12e3…` (shard 1) et `539cf93f…` (shard 2). Licence Apache 2.0.
- **Runtime** : `llama-server` **b11017** (`aca5f933b`), **CPU seul** (`-ngl 0`, 40 threads) —
  les GPU de N2 ne sont pas touchés. Un chargement, 180 requêtes.
- **Tagger** : `NeuronalLLMPOS` tokenise avec `Heuristique._mots` (mots et nombres, sans
  ponctuation), envoie la **liste des tokens** et demande un objet `{"pos":[...]}` — **une
  classe par token, dans l'ordre**. Une **grammaire GBNF** (`grammaire_pos(n)`) impose le nombre
  exact de classes et le jeu `{DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM, INTJ,
  PUNCT}` : le JSON ne peut pas être tronqué, décalé ou hors jeu. Les spans sont ceux de la
  tokenisation, pas ceux que le modèle inventerait.
- **Prompt** : français, minimal — la liste des classes, la liste des tokens, `Réponse :`.
  Pas d'exemple few-shot : le prompt few-shot a été testé sur les 20 réelles mais n'a pas été
  retenu (il ajoutait des `INTJ` et des `AUX` parasites).
- **Gold** : 180 phrases, **804 tokens** — 20 réelles (`gold.json`) et 160 synthétiques
  (`gold_synthetique.json`). La tokenisation du bloc et celle du gold coïncident sur
  **180/180** phrases (vérifié avant la passe).
- **Confiance 0,6** : c'est le seuil de la cascade. L'heuristique déclare 0,92 pour les classes
  fermées, 0,72 pour les verbes connus, 0,55 pour l'ouvert et 0,30 pour l'inconnu. À 0,6, le
  tagger ne remplace donc **que** les tokens que l'heuristique déclare peu sûrs. Le seuil vient
  du `seuil_ouvert` de l'heuristique (0,55), pas d'un balayage sur le gold.
- **Commande** :
  `python3 tools/tests/linguistique/qualifier_neuronal.py --demarrer --port 18082 --workers 1 --confiance 0.6`
  (le serveur est lancé et arrêté par le script ; `--workers 1` pour un run déterministe).

## 3. Les résultats

| lecture | 180 | 20 réelles | 160 synthétiques | fermé | ouvert |
|---|---:|---:|---:|---:|---:|
| **heuristique** | 0,7512 | **0,9238** | 0,7253 | **0,9392** | 0,6211 |
| **neuronal seul** | 0,8483 | 0,8286 | 0,8512 | 0,7660 | 0,9053 |
| **cascade à 0,6** | **0,9440** | **0,9238** | **0,9471** | **0,9392** | **0,9474** |

- **Le neuronal seul** : **+0,0971** sur l'heuristique (0,8483 contre 0,7512), mais il **perd**
  sur les 20 réelles (0,8286 contre 0,9238). Il n'est pas un remplaçant.
- **La cascade** : **+0,1928** sur l'heuristique, **+0,2218** sur les synthétiques, **0** perte
  sur les réelles. Elle ajoute **+0,0957** au neuronal seul.
- **La complémentarité est nette** : le neuronal est faible sur le fermé (0,7660) et fort sur
  l'ouvert (0,9053) ; l'heuristique est l'inverse (0,9392 / 0,6211). La cascade prend le fermé
  à l'heuristique (0,9392, inchangé) et l'ouvert au neuronal (0,9474). C'est le résultat de
  **structure** : un 7B local utilisé sur le **résidu** fait mieux que le 7B entier et que
  l'heuristique seule.
- **Ce que le modèle confond** (seul) : `ADV→AUX` (21), `PRON→CONJ` (12), `VERB→AUX` (11),
  `ADV→PUNCT` (11), `VERB→NOUN` (10). Ce sont les classes fermées et les frontières ADV/PUNCT.
- **Ce que la cascade confond encore** : `CONJ→PRON` (16), `NOUN→PRON` (8), `VERB→NOUN` (7) —
  les erreurs de l'heuristique sur le fermé, que la cascade ne corrige pas (c'est le prix de
  la politique « le fermé reste à l'heuristique »).

## 4. Le choix du modèle (les 20 réelles, dev)

| modèle | condition | POS |
|---|---|---:|
| Qwen2.5-0.5B (base) | prompt du contrat, `llama-cli -st` | **refusé** : recopie le schéma, ne rend pas de POS |
| Qwen2.5-3B-Instruct Q4_K_M | prompt minimal + grammaire | 0,6667 (70/105) |
| **Qwen2.5-7B-Instruct Q4_K_M** | prompt minimal + grammaire | **0,8286** (87/105) |

Les 20 réelles ont servi de **jeu de développement** (choix du modèle et du prompt) ; les 160
synthétiques sont le **jeu de test**. Le 3B est dominé ; le 0.5B de base ne suit pas le format.
Le 7B est le plus petit modèle local testé qui qualifie le contrat.

## 5. Les contrôles négatifs

| contrôle | ce qu'il fait | exactitude |
|---|---|---:|
| **majoritaire** | toujours `NOUN` | **0,2289** |
| **uniforme** | tirage uniforme sur les 12 classes | **0,0833** |
| **permutation** | les POS prédits sont permutés entre tokens (graine 0) | **0,1729** |
| **sans régression** | cascade réelles = heuristique réelles | **0,9238** (égal) |

Les trois contrôles restent **sous 0,40** ; le neuronal (0,8483) et la cascade (0,9440) sont
loin au-dessus. La permutation teste le **métrique** (le score ne vient pas du déséquilibre des
classes) ; le contrôle « sans régression » teste la **politique** (la cascade ne dégrade pas les
réelles).

## 6. Le coût

- **180 appels HTTP**, **0 refus** ; latence CPU moyenne **3,043 s**, médiane **2,886 s**, p95
  **5,012 s**. La passe complète (serveur, hash, 180 phrases, heuristique et cascade) dure
  **548 s** (~9 min).
- Le serveur charge le modèle **une fois** ; le cache du tagger évite de répéter les 180 appels
  quand la cascade relit les mêmes phrases. Sans cache, la cascade doublerait les appels.
- Pas de mesure GPU : les deux Quadro RTX 5000 sont réservées à N2.

## 7. Ce qui pourrait rendre ce résultat faux

- **Le jeu de test n'est pas totalement aveugle** : les 20 réelles ont servi au choix du modèle
  et du prompt ; les 160 synthétiques sont générées par la grammaire du bloc, avec les mêmes
  catégories que le prompt. Un gold réel plus large (200+ phrases) est la prochaine mesure.
- **Contamination possible** : Qwen2.5-7B-Instruct a été pré-entraîné sur un grand corpus ; les
  160 phrases synthétiques sont générées, mais des constructions proches ont pu être vues. Aucun
  fine-tuning sur le gold n'a été fait.
- **POS seulement** : le tagger ne rend ni syntagmes, ni pragmatique. Le gain de 0,1928 est un
  gain **POS** ; il ne dit rien de la cascade complète (syntagmes, attachement, acte).
- **Le seuil 0,6 est lié à l'échelle de confiance de l'heuristique** : une autre heuristique, ou
  un autre seuil, change la part du fermé et de l'ouvert. Le seuil a été fixé a priori (0,55 →
  0,6), mais la valeur 0,6 reste un choix de politique.
- **La variance de batching** : un run à 4 requêtes parallèles a donné 0,8495 (neuronal seul)
  contre 0,8483 en séquentiel — un token d'écart. Le chiffre committé est le run séquentiel.
- **Le modèle est externe** : les deux shards GGUF ne sont pas dans le dépôt ; le JSON porte
  leur SHA-256. Une autre quantisation (Q8, Q4_0) peut changer le score.
- **La tokenisation** : le gold et `Heuristique._mots` coïncident sur 180/180 ; si la
  tokenisation du bloc change, les spans et la comparaison changent.
- **Une seule passe** : le run est déterministe (température 0, grammaire), mais une seule
  graine de serveur ; pas de répétition multi-graines.

### 7.1 La porte B13 (hors tagger)

La porte `tools/pensee/autotest.py` rend **134/140** au moment de ce fait (T111, T113–T115,
T132–T133). Ces six tests comparent des F1 **exacts** de segmentation et d'anaphore ; ils ont
dérivé après la mise à jour du sous-module S (`647205a`, commit `13f4e131`), qui change
l'analyseur. La corrélation est **nommée** ; la cause n'est pas isolée par un contrôle (le
worktree HEAD sans sous-module donne un autre jeu de rouges). Le tagger n'y touche pas : la
porte `porte-bloc-linguistique.sh` est verte. La porte B13 était **140/140** au dernier cycle
committé (15 h 57) ; la régression est **nommée** et attend la mise à jour des valeurs par S
(ou un retour du sous-module).

## 8. La suite

1. **Syntagmes et pragmatique** : la même boucle (prompt + grammaire) pour GN/GV/GP/REL/SUB et
   pour l'acte ; ensuite la cascade **complète** avec le vrai modèle, pas avec le mock.
2. **DRVM/native** : les poids GGUF et le tagger existent maintenant ; la conversion et la
   parité natives sont une mesure séparée (N0.3b), pas un résultat de ce gold.
3. **200+ phrases réelles** : réduire le recouvrement dev/test et mesurer les classes ouvertes
   sur du texte non synthétique.
4. **Coût GPU** : si une carte se libère, mesurer le même tagger sur GPU ; ne pas toucher aux
   GPU de N2.

## 9. Fichiers

- [`tools/tests/linguistique/qualifier_neuronal.py`](../tools/tests/linguistique/qualifier_neuronal.py) —
  le banc (serveur, 180 phrases, heuristique, cascade, contrôles, JSON).
- [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) — `NeuronalLLMPOS`,
  `grammaire_pos`, `CLASSES_POS`.
- [`tools/tests/linguistique/test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py) —
  deux tests de contrat (transport factice, refus).
- [`pensee-gold-neuronal.json`](pensee-gold-neuronal.json) — les chiffres, les SHA-256, les
  seuils et les limites.
- Modèle : `Qwen/Qwen2.5-7B-Instruct-GGUF`, `qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf` et
  `-00002-of-00002.gguf` (4,68 Go, Apache 2.0) ; non versionné (`models/` est ignoré).
