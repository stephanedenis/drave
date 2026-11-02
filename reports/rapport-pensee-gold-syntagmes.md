# B13 — les syntagmes neuronaux : BIO, tête 0,7606, et la politique de fusion

> **Ligne de roadmap** : **B13** (moteur de pensée) / **R0.7** (bloc linguistique) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **le tagger de syntagmes 7B local est qualifié** — exact **0,6173** (heuristique
> **0,1992**), **tête 0,7606** (heuristique **0,5614**), **0 refus**, **180 appels**. La cascade à
> **priorité confiance** rend **0,6168 / 0,7592** ; la cascade par défaut (priorité heuristique)
> reste à **0,2137 / 0,5670** : **la politique de fusion est le goulot**, pas le modèle.
>
> **Dispositif** : [`qualifier_syntagmes.py`](../tools/tests/linguistique/qualifier_syntagmes.py) ;
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`NeuronalLLMChunks`,
> `priorite_syntagme`) ; JSON [`pensee-gold-syntagmes.json`](pensee-gold-syntagmes.json).

## 1. Ce qui était mesuré

Le gold neuronal POS est qualifié : **0,8483** seul, **0,9440** en cascade, sans perte sur les
réelles ([`pensee-gold-neuronal`](rapport-pensee-gold-neuronal.md)). Le niveau suivant est le
**syntagme** : GN, GV, GP, REL, SUB. L'heuristique y est faible — exact **0,1992**, tête
**0,5614** sur les 180 — parce que ses découpes sont des **candidats** (confiance 0,4), pas des
segments appris.

## 2. Le dispositif

- **Modèle** : Qwen2.5-7B-Instruct Q4_K_M, deux shards (mêmes SHA-256 que le fait POS), servi
  par `llama-server` **b11017** en **CPU** (`-ngl 0`). Un chargement, 180 requêtes.
- **Tagger** : `NeuronalLLMChunks` tokenise avec `Heuristique._mots` (mots et nombres), demande
  une étiquette **BIO par token** — `O`, `B-GN`, `I-GN`, `B-GV`, `I-GV`, `B-GP`, `I-GP`,
  `B-REL`, `I-REL`, `B-SUB`, `I-SUB` — et **reconstruit les spans** sur les offsets des tokens.
  Une grammaire GBNF impose exactement une étiquette par token : le JSON ne peut pas dériver.
- **Prompt** : français, **cinq exemples hors gold** (GN avec déterminant, GP avec préposition,
  GV avec auxiliaire, SUB, et un token `O`). Sans exemples, le modèle met le déterminant hors
  du GN et l'auxiliaire hors du GV ; le few-shot est ce qui fait la différence.
- **Gold** : 180 phrases, **804 tokens**, **418 segments** — GN 170, GV 180, GP 34, SUB 17,
  REL 17. La tokenisation du bloc coïncide avec le gold sur **180/180**.
- **Limite structurelle** : **4 segments sont imbriqués** (un GP dans un GV). BIO est une
  séquence plate : ces 4 cas ne peuvent pas être rendus ensemble. L'exact est plafonné par là.
- **Confiance** : 0,6 pour le tagger (le seuil du POS) ; l'heuristique déclare 0,4 pour ses
  syntagmes. La politique `confiance` laisse donc le tagger passer devant ; la politique par
  défaut (`heuristique`) garde les spans de l'heuristique. Les deux sont mesurées.
- **Commande** :
  `python3 tools/tests/linguistique/qualifier_syntagmes.py --endpoint http://127.0.0.1:18082 --workers 1 --confiance 0.6`
  (le serveur 7B est lancé une fois ; `--workers 1` pour un run déterministe).

## 3. Les résultats

| lecture | 180 exact | 180 tête | 20 réelles exact | 20 réelles tête | 160 synth. exact | 160 synth. tête |
|---|---:|---:|---:|---:|---:|---:|
| **heuristique** | 0,1992 | 0,5614 | 0,4038 | 0,5800 | 0,1669 | 0,5583 |
| **neuronal seul** | **0,6173** | **0,7606** | **0,5138** | **0,6606** | **0,6331** | **0,7759** |
| **cascade (priorité heuristique)** | 0,2137 | 0,5670 | 0,4536 | 0,5979 | 0,1752 | 0,5620 |
| **cascade (priorité confiance)** | **0,6168** | **0,7592** | 0,5045 | 0,6667 | 0,6339 | 0,7732 |

- **Le neuronal seul gagne partout** : **+0,4181** exact et **+0,1992** tête sur les 180 ;
  **+0,1100 / +0,0806** sur les 20 réelles ; **+0,4662 / +0,2176** sur les 160 synthétiques.
- **La politique de fusion change tout** : la cascade par défaut ne prend que **+0,0145 /
  +0,0056** (elle ne peut ajouter que des spans non recouvrants) ; la cascade `confiance` prend
  **+0,4176 / +0,1978**. Le modèle était déjà bon : c'est la règle « le syntagme heuristique
  est prioritaire » qui le masquait.
- **La cascade `confiance` ≈ le neuronal seul** (exact 0,6168 contre 0,6173 ; tête 0,7592
  contre 0,7606) : les spans de l'heuristique qui ne recouvrent pas le modèle ajoutent
  quelques faux positifs et retirent quelques vrais. Elle garde en revanche les **unités
  sémantiques** de l'heuristique (fraction **0,6381**), que le tagger seul ne fournit pas.
- **Le français d'abord** : 20 réelles françaises **0,5679 / 0,7160** ; anglaises
  **0,3571 / 0,5000**. Le prompt est français ; l'anglais progresse quand même sur
  l'heuristique (**0,1379 / 0,3448**), mais reste le point faible.

## 4. Les contrôles négatifs

| contrôle | exact | tête |
|---|---:|---:|
| **vide** (tout `O`) | 0,0000 | 0,0000 |
| **BIO aléatoire** (graine 0) | 0,0419 | 0,1240 |
| **heuristique** (référence) | 0,1992 | 0,5614 |
| **neuronal** | **0,6173** | **0,7606** |

Le hasard tombe à **0,0419 / 0,1240**, très en dessous du modèle ; le contrôle « vide » est nul
par construction. Le score du modèle ne vient ni du déséquilibre des classes (418 segments sur
804 tokens, dont 180 GV), ni d'un artefact de span.

## 5. Le coût

- **180 appels**, **0 refus** ; latence CPU moyenne **4,004 s**, médiane **3,793 s** ; passe
  complète (serveur, hash, 180 phrases, quatre lectures, contrôles) **733,8 s** (~12 min).
- Le cache du tagger fait lire les quatre lectures (heuristique, neuronal, deux cascades) avec
  **180 appels HTTP**, pas 720.
- Pas de mesure GPU : les deux Quadro RTX 5000 sont réservées à N2.

## 6. Ce qui pourrait rendre ce résultat faux

- **Les 20 réelles ont servi au choix du prompt** (dev) ; les 160 synthétiques sont le test.
  Le test est propre, mais la grammaire synthétique partage les conventions du gold (GN avec
  déterminant, GV avec auxiliaire) : le modèle apprend la **convention**, pas seulement la
  langue. Les 20 réelles restent au-dessus de l'heuristique, ce qui limite le biais.
- **Le few-shot est français** : l'anglais est hors domaine (0,3571 / 0,5000) ; ne pas lire le
  0,7606 comme multilingue.
- **4 segments imbriqués** ne sont pas représentables en BIO ; l'exact est plafonné, pas la
  tête.
- **Le seuil 0,6 n'a pas été balayé** : il vient du POS (0,55 → 0,6). Un autre seuil change la
  part de l'heuristique et du modèle dans la cascade `confiance` ; la politique par défaut,
  elle, ne dépend pas du seuil.
- **Une seule passe** : température 0, grammaire, serveur unique ; pas de répétition
  multi-graines. La variance de batching du POS (un token) n'a pas été re-mesurée ici.
- **La tokenisation** : le gold et `Heuristique._mots` coïncident sur 180/180 ; si elle change,
  les spans changent.
- **La porte B13** est à **134/140** (six rouges de segmentation/anaphore corrélés au
  sous-module S `647205a`, hors tagger) ; la porte du bloc et les 14 tests du bloc sont verts.
  Le détail est dans [`pensee-gold-neuronal`](rapport-pensee-gold-neuronal.md) § 7.1.

## 7. Ce que la politique de fusion dit

Le code a maintenant deux politiques pour le syntagme :

- `priorite_syntagme="heuristique"` (défaut) : les spans de l'heuristique passent d'abord, le
  neuronal ne remplit que les trous. C'est la politique historique ; elle donne **0,2137 /
  0,5670** avec un tagger à 0,6173/0,7606 — le tagger est **inutilisé**.
- `priorite_syntagme="confiance"` : la plus confiante gagne (neuronal 0,6 contre heuristique
  0,4). Elle donne **0,6168 / 0,7592**.

C'est le résultat de **structure** : un tagger neuronal meilleur ne sert à rien si la règle de
fusion le muselle. La même leçon s'appliquera au POS et à la pragmatique : mesurer un bloc ne
suffit pas, il faut mesurer **la politique qui le branche**.

## 8. La suite

1. **Pragmatique** : acte, négation, modalité, double sens. L'heuristique est déjà à 1,0 sur
   l'acte dans le gold ; le tagger doit être mesuré, mais le gain attendu est faible — un
   négatif nommé est un résultat.
2. **Cascade complète** : POS (`NeuronalLLMPOS`) + syntagmes (`NeuronalLLMChunks`) +
   pragmatique, avec la politique `confiance` pour les spans ; mesurer la fraction sémantique
   et les quatre niveaux d'un coup.
3. **200+ phrases réelles** : l'anglais et les conventions non vues ; réduire le recouvrement
   dev/test.
4. **DRVM/native** : les poids GGUF et les deux taggers existent ; la parité native reste une
   mesure séparée (N0.3b).

## 9. Fichiers

- [`tools/tests/linguistique/qualifier_syntagmes.py`](../tools/tests/linguistique/qualifier_syntagmes.py) —
  le banc (serveur, 180 phrases, quatre lectures, contrôles, JSON).
- [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) — `NeuronalLLMChunks`,
  `grammaire_bio`, `ETIQUETTES_BIO`, `priorite_syntagme` dans `_supprimer_chevauchements`,
  `_fusion`, `Parallele`, `Cascade`.
- [`tools/tests/linguistique/test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py) —
  trois tests (BIO, refus, politique).
- [`pensee-gold-syntagmes.json`](pensee-gold-syntagmes.json) — les chiffres, les SHA-256, les
  seuils et les limites.
