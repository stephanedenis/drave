# B13 — classement appris des candidats d'attachement : 142/145, mais la règle live est déjà à 137

> **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ❌ **ne pas intégrer le classement appris en l'état** ; le signal utile est le **vivier ordonné** (rang 0 : 139/145), à tester.
>
> **142/145 (0,9793)** hors-pli contre **137/145 (0,9448)** pour la règle live (empreinte `6e843018`, 13:51) : **+5**, McNemar 7/2, **p = 0,18**, IC 95 % bootstrap **[-0,7 ; +7,6] pts** → **non significatif**. Contre la référence committée (123/145, audit `e1171032`), le même modèle donne **+19** (McNemar 21/2, p = 6,6e-05) : la règle live a absorbé l'essentiel pendant la session. Le classement ne lit pas la cible choisie par la règle (seule la comparaison la lit) ; ses **142/145 ne bougent pas** quand la règle passe de 123 à 137.
>
> **Dispositif** : [`classement_cible.py`](../tools/tests/linguistique/classement_cible.py), JSON [`pensee-classement-appris.json`](pensee-classement-appris.json). [`bloc_linguistique.py`](../tools/bloc_linguistique.py) **non modifié** par ce prototype ; son empreinte est figée dans le JSON.

## 1. Protocole

- **Population** : les 145 segments gold qui portent une cible (`cibles`) **et** dont le span `(type, debut, fin)` est prédit par l'heuristique — exactement la population de la mesure d'attachement de `evaluer_gold.py` (GP 83, REL 26, SUB 36). Gold : **612 phrases** (20 `hand` + 432 `reel` + 160 synthétiques), inchangé pendant la session.
- **Vivier** : les tokens pleins de la phrase (POS ouverte ou `_est_verbe`), auxiliaires exclus. Construit sans le gold ; il contient la cible dans **144/145** cas (le cas manquant est `appelle` contre le token `appelle-moi`).
- **Features par candidat** : distance en tokens au segment, côté (gauche / droite / dedans), type du segment (GP/REL/SUB), préposition éventuelle (6 familles), longueur, nature `_est_verbe` et POS heuristique, rang dans la liste ordonnée **gauche → droite → dedans, puis distance**. S'y ajoutent des interactions lisibles (type × nature, génitif × nature) : 25 features au total.
- **Modèle** : régression logistique binaire (« ce candidat est-il la cible ? »), descente de gradient pleine bataille, L2 = 0,01, classes pondérées, arrêt sur convergence relative. Cible prédite = **argmax** du score.
- **Découpage** : phrases d'id **pair** → entraînement, ids **impairs** → test ; puis l'inverse. Exactitude = égalité exacte avec `cibles[0]`, la mesure de `evaluer_gold.py`. Le **regroupé hors-pli** prédit chaque segment par le modèle de l'autre moitié.
- **Empreinte** : les 123/145 sont l'état **committé** (audit `e1171032`) ; un autre agent a modifié `bloc_linguistique.py` pendant la session (129 puis 137/145 dans le worktree). Le JSON fige le fichier lu (`sha256[:16] = 6e843018`, 101 568 octets, mtime 13:51:26) ; les trois états sont rapportés ci-dessous.

## 2. Résultats par moitié

| sens (test) | modèle appris | règle live 137 (worktree) | règle committée 123 |
|---|---:|---:|---:|
| pairs → impairs (66 segments) | **66 (1,0000)** | 64 (0,9697) | 60 (0,9091) |
| impairs → pairs (79 segments) | **76 (0,9620)** | 73 (0,9241) | 63 (0,7975) |
| moyenne des sens | **0,9810** | 0,9469 | 0,8533 |
| regroupé hors-pli (145) | **142 (0,9793)** | 137 (0,9448) | 123 (0,8483) |

Par type (regroupé) : GP **81/83** contre 77/83 (live) et 69/83 (committée) ; REL **26/26** partout ; SUB **35/36** contre 34/36 et 28/36.

État intermédiaire mesuré pendant la session : à 129/145, le modèle donnait déjà 142, les deux sens 62/66 et 67/79. Les six cas réparés par la règle entre 123 et 129 sont les SUB synthétiques `s012`, `s030`, `s052`, `s097`, `s124`, `s139`.

## 3. Poids appris (et ce qu'ils disent)

| feature | pairs→impairs | impairs→pairs | moyenne |
|---|---:|---:|---:|
| rang | -3,112 | -3,380 | **-3,246** |
| cote_gauche | +0,760 | +1,526 | **+1,143** |
| cote_dedans | -1,054 | -0,580 | **-0,817** |
| nat_verbe (`_est_verbe`) | +1,172 | +0,735 | **+0,953** |
| GP × verbe | +1,018 | +0,873 | **+0,946** |
| distance | -0,401 | -0,756 | **-0,578** |
| type_GP | -0,496 | -0,636 | **-0,566** |
| pos_verbe | +0,026 | +0,633 | +0,329 |
| GP × pos_verbe | -0,006 | +0,579 | +0,287 |
| SUB × verbe | +0,246 | +0,225 | +0,235 |
| REL × verbe | -0,093 | -0,363 | -0,228 |
| prep_loc | -0,232 | -0,355 | -0,294 |
| type_REL | +0,029 | +0,238 | +0,134 |

Les autres poids sont petits (|moyenne| < 0,11) : `prep_gen`, `prep_dat`, `prep_but`, `prep_moy`, `prep_autre`, `pos_nom`, `GEN_x_verbe`, `GEN_x_posV`, `longueur` ; les signes de `longueur`, `prep_dat`, `GP × pos_verbe` et `GEN × …` changent d'un pli à l'autre (bruit, pas signal).

Lecture : **le rang porte tout** (prendre le premier de la liste), la gauche vaut mieux que le dedans, un verbe vaut mieux qu'un nom — surtout pour un GP —, et le type GP est pénalisé à rang égal. Le modèle apprend donc surtout le **prior de liste**, pas une grammaire.

## 4. Contrôle négatif et ablations

| contrôle | justes | taux |
|---|---:|---:|
| règle live 137 (empreinte 6e843018) | 137/145 | 0,9448 |
| règle committée (123) | 123/145 | 0,8483 |
| hasard uniforme dans le vivier (attendu) | — | 0,3876 |
| hasard uniforme, tirages (pairs / impairs) | — | 0,3485 / 0,3671 |
| hasard parmi les 103 cibles distinctes | — | 0,0097 |
| **rang 0 seul** (premier de la liste, sans apprentissage) | **139/145** | **0,9586** |
| modèle sans `rang` | 139/145 | 0,9586 |
| modèle sans tout le prior de position | 95/145 | 0,6552 |
| modèle sans interactions | 141/145 | 0,9724 |
| modèle sans nature | 139/145 | 0,9586 |

- **Modèle contre règle live** : 7 justes / 2 fausses, McNemar exact **p = 0,1797** ; bootstrap **+3,45 pts [-0,69 ; +7,59]** (2 000 tirages). Non significatif.
- **Modèle contre rang 0** : 3 justes / 0 fausse (g003, g014, g016), **p = 0,25**. Le « appris » ajoute +3 au prior, pas davantage.
- **Modèle contre 123** : 21 justes / 2 fausses, **p = 6,6e-05** ; bootstrap **+13,1 pts [+6,9 ; +20,0]**. Significatif, mais c'est la comparaison à une règle que la règle live a déjà dépassée.
- **Stabilité** : 10 découpages aléatoires de phrases → modèle **0,9848 ± 0,0116**, règle **0,9476 ± 0,0207** (gain +0,0372). **Sensibilité** : 141 à 142/145 pour (L2, époques) ∈ {0,001, 0,01, 0,1} × {500, 6000}.
- **Hors 5 segments à vivier unique** (mesure automatique) : 137/140 (0,9786) contre 133/140 (0,95) pour la règle live.
- **Sur-apprentissage** : exactitude d'entraînement 0,9931 contre 0,9793 hors-pli ; l'écart est faible, mais 25 poids pour 66–79 segments d'entraînement restent beaucoup.

## 5. Ce que ça dit

1. **Le levier est le vivier, pas les poids** : le simple « premier candidat plein de la liste gauche → droite → dedans » fait **139/145** (95,9 %), déjà au-dessus de la règle live (137). Les 25 poids n'ajoutent que **+3** (g003, g014, g016 : préférer le verbe gouvernant au nom objet à distance 1), non significatif.
2. **La règle live a rattrapé le prototype** : en ajoutant les verbes anglais au lexique, la logique REL/SUB par segment précédent et les têtes de candidats S, elle est passée de 123 à 137. Il ne reste au modèle que +5, et il paie 2 régressions.
3. **Les 3 erreurs du modèle** : `r048` (« lettre à sa sœur » → il choisit `lettre` au lieu de `écrit`) et `r068` (même chose en anglais) — la POS étiquette le verbe comme nom, le modèle ne peut pas trancher ; `r230` (`appelle` contre `appelle-moi`) — découpage du gold, hors d'atteinte.
4. **Les 8 erreurs de la règle live** : `g002` et `s041` (cible vide sur le doublon d'union), `g012` / `r018` (« à manger » → `manger` au lieu de `prêt` / `prête`), `s108` / `s122` (nom à gauche du GP au lieu du verbe), `r309` (« Peut-être qu'il viendra » → `Peut-être` au lieu de `viendra`), `r230`. Le modèle en répare 7, mais introduit `r048` / `r068`.

## 6. Limites (dont la petite taille)

- **145 segments, dont 26 REL et 5 à vivier unique** ; 2 000 tirages bootstrap ne créent pas de données. Les écarts de 3 à 5 unités ne sont pas interprétables seuls — d'où le test apparié et l'IC joints.
- **Le dessin des features et l'ordre de la liste ont été choisis après une passe exploratoire sur les 145** : le découpage valide les **poids**, pas le dessin. Les 142/145 sont donc optimistes pour un corpus neuf ; c'est la limite principale.
- **La règle live bouge** : la fiche est une photo du worktree à l'empreinte `6e843018` (137/145) ; 123 est l'état committé. Si `bloc_linguistique.py` change encore, relancer le script ; les 142/145 du modèle ne dépendent que du vivier, de la POS et de `_est_verbe` (donc du lexique), pas de la cible choisie.
- **Le vivier, la POS et la segmentation viennent de l'heuristique** : une erreur de tokenisation est invisible au classement (`r230`), une erreur de POS coûte `r048` / `r068`.
- **Paraphrases** : aucun texte exact n'est partagé entre les deux moitiés, mais les paraphrases du gold (mêmes phrases à quelques mots près) restent des deux côtés ; les taux absolus sont optimistes, le gain l'est moins.
- **La convention du gold** (verbe gouverneur ou nom antécédent) n'est pas documentée ; le modèle apprend la convention observée.
- **Les 94 segments au span non prédit ne sont pas mesurés** : une intégration changerait leur attachement sans évaluation.
- **Le hasard est haut** (0,3876) parce que le vivier est petit (2,86 candidats en moyenne, 5 segments à un seul) : le bon contrôle est le rang 0 et la règle live, pas 1/103.

## 7. Recommandation

**Ne pas intégrer le classement appris en l'état.** À 137/145, le gain de +5 n'est pas significatif (p = 0,18, IC incluant 0), le modèle introduit 2 régressions, et 25 poids pour +3 sur le prior de rang ne se justifient pas — d'autant que les features ont été dessinées sur le corpus.

**Ce qu'il faut garder du prototype**, par ordre de coût :

1. **Le vivier ordonné** (premier token plein, gauche d'abord) : 139/145, +2 sur la règle live, non significatif mais gratuit. À tester comme règle déterministe, pas comme modèle.
2. **Le fallback quand la cible est vide** (g002, s041) : +2 sans risque, indépendant du reste.
3. **La préférence verbe contre nom proche** (g012, r018, s108, s122) : +4, mais elle casse r048 / r068 si elle n'est pas gardée par le lexique — à traiter seulement si le lexique verbal tient.
4. **`r309`** : accepter un candidat intérieur quand le segment est une complétive en tête de phrase.

Si l'objectif est le chiffre maximal sur ce gold, le modèle à **142/145** est le meilleur trouvé ; mais il n'est pas validé au-delà de ces 145 segments. Une validation propre demanderait de figer le dessin sur un dev et de tester sur un gold tenu à l'écart — pas disponible ici.

## 8. Fichiers

- [`classement_cible.py`](../tools/tests/linguistique/classement_cible.py) — prototype autonome, aucune dépendance nouvelle ; n'écrit que le JSON.
- [`pensee-classement-appris.json`](pensee-classement-appris.json) — résultats, poids par pli, 145 prédictions auditées, empreinte du bloc.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — **non modifié** ; empreinte `6e843018` dans le JSON.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger()` et la mesure d'exactitude, réutilisés tels quels.
