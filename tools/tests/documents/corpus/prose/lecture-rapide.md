# La lecture rapide — ce que Drave doit construire pour lire comme un humain

> **Ce que ce document est.** L'analyse des **techniques de lecture rapide** humaines et de ce qui manque à Drave
> pour les rendre utilisables sur les différents types de documents. Ce n'est **pas** une fiche de résultat : les
> chiffres cités sont ceux des fiches [`reports/`](../../reports/) ; le plan qui en découle est le **programme R**
> de [`roadmap.md`](../pilotage/roadmap.md) ; les fiches de fonctionnalité sont dans
> [`backlog/index.md`](../pilotage/backlog/index.md). **Chargement** : à lire quand la question est « que veut dire
> lire vite pour Drave ? » — pas pour l'état courant.

## En trois idées

1. **La lecture rapide humaine n'est pas une vitesse, c'est une allocation** : survoler, balayer, lire
   sélectivement, revenir — selon le but et le type de document, avec une perte de compréhension contrôlée.
2. **Drave a l'économie de cette allocation, pas sa sémantique** : le calcul suit l'activité (FFN creux, sortie
   précoce), mais rien ne décide **quoi** lire, **dans quel ordre**, **à quelle profondeur**, **pour quel but**.
3. **Il manque un lecteur, pas une technique** : un graphe de document, une politique de lecture, une fenêtre
   hiérarchique, une mémoire de travail, une restitution — et un banc qui mesure la compréhension **par unité de
   calcul**, avec un contrôle négatif.

---

## 1. Ce que la lecture rapide humaine est vraiment

La revue de Rayner et al. (2016) est le point de repère : les promesses de **1 000 mots/minute avec compréhension
pleine** ne tiennent pas. Les **saccades** ne sont pas un défaut à supprimer — elles servent à revenir sur ce qui
n'a pas été compris ; la **vision périphérique** est floue ; les programmes de lecture rapide entraînent surtout à
**écrémer** ([APS, *So Much to Read, So Little Time*](https://www.psychologicalscience.org/publications/speed_reading.html)).
Le levier réel est donc :

- **le but** : on ne lit pas un roman, un contrat et un tableau de bord avec la même attention ;
- **la structure** : titres, tableaux, figures, références, code — le document n'est pas un flux linéaire ;
- **l'allocation** : décider de survoler, balayer, lire, relire, arrêter ;
- **la mémoire** : garder le gist, les entités, les faits, et savoir **où** revenir ;
- **la restitution** : répondre, résumer, extraire, citer — sinon « lire » n'est pas prouvé.

La bonne métrique n'est donc **pas le débit** mais **la compréhension par unité de calcul** : une courbe
vitesse-compréhension, avec un **contrôle négatif** (ce qu'on perd quand on saute). Un lecteur rapide qui ne sait
pas dire ce qu'il a sauté n'est pas un lecteur, c'est un filtre.

## 2. L'échelle du lecteur

| niveau | ce que c'est | état de Drave |
|---|---|---|
| **L0 — flux** | octets, perplexité, génération | ✅ acquis |
| **L1 — saut de calcul** | sortie précoce, parcimonie, chemin court | ✅ mesuré |
| **L2 — document** | régions typées, structure, layout, provenance | ❌ absent |
| **L3 — politique** | survol, écrémage, balayage, sélectif, relecture | ❌ absent |
| **L4 — mémoire** | gist, entités, faits, épisodique | ❌ négatif (N5) |
| **L5 — restitution** | réponse, résumé, extraction, citation | ❌ absent |
| **L6 — banc** | courbe vitesse-compréhension par type | ❌ absent |

**Drave est à L1. La lecture rapide humaine est un pilotage L2–L4, prouvé par un banc L5–L6.** C'est pourquoi
ajouter une « tête d'écrémage » au modèle actuel ne composerait pas : il n'y a ni document à survoler, ni politique
pour choisir, ni sortie pour prouver la compréhension.

## 3. Les chiffres qui bornent le diagnostic

Tous sont mesurés et cités dans les fiches ; ils disent où le lecteur se bloque.

| contrainte | mesure | conséquence |
|---|---|---|
| **Contexte natif** | 129 octets, PPL **2,6998** ; 130 → **2,7149** ; 2 000 octets → PPL **54,04** | ~25 mots ; une page est 23× trop longue ; 130/136/160/256 sont **négatifs** |
| **Long contexte** | 18/18 aiguilles à 12 288 jetons | c'est **Qwen2.5-0.5B**, pas `drave-n0` — ne pas s'en prévaloir pour le natif |
| **Tokenisation** | octets, pas de BPE | séquences 3–4× plus longues ; l'empan utile fond encore |
| **Sortie précoce** | 4 blocs **5,978 ms** vs 6 blocs **7,871 ms** (−24,05 %), coût **−1,61 point** | c'est un saut de **calcul**, pas un saut de **contenu** : la décision est la confiance du prochain octet, pas la pertinence |
| **Têtes précoces** | **57,6 / 61,6 / 62,1 %** vs **62,7 %** ; témoin **0,39 %** | ce sont des lectures rapides de jetons, pas des stratégies |
| **Mémoire** | signal courant R² **0,992** ; à 8 pas **−0,681** ; l'entraînement l'aggrave (**−1,091 → −2,773**) | pas de gist, pas de relecture, pas de cohérence multi-sections |
| **Sémantique** | `z` : rappel **0,426** vs hasard **0,167** ; chrF reconstruction **12,7**, plancher **39,6** | le sens est au-dessus du hasard, mais **ne se restitue pas** |
| **Usage** | SFT **24/24 vus, 0/4 tenus** ; génération cohérente **12 octets** | pas d'assistant, pas de résumé, pas d'extraction |
| **Encodeurs** | `bge-m3` lisible, **inexécutable** (M4) | pas de recherche par similarité, pas de balayage neuronal |
| **Architecture** | le plan des douze capacités n'est pas réalisé ; des briques isolées existent (délai, récurrence, périphérie signal) | les briques existent, pas le lecteur |

À l'inverse, ce qui existe déjà et qui est rare : **prélecture/tampons** (6,22 Go lus, 3,40 s contre 9,52 Go /
5,97 s à la demande), **cache KV 19,25×**, **codec classique 100 %**, **trace et rejeu exacts**. Ce sont les bons
matériaux ; il manque le plan.

## 4. Les 14 techniques et leur état

| # | technique humaine | ce qu'elle exige | état | manque |
|---|---|---|---|---|
| 1 | **Survol** (TOC, titres, figures, conclusion) | structure, passe globale, gist | ❌ | graphe de document + état de résumé |
| 2 | **Écrémage** (gist, sauter les détails) | saillance, saut au niveau du passage | 🟡 sortie précoce au jeton | politique de saut conditionnée par la pertinence |
| 3 | **Balayage** (chercher un nom, un chiffre) | requête, index/pattern | 🟡 regex/BM25 possibles ; pas d'encodeur | bloc de recherche + requête |
| 4 | **Lecture sélective** (ne lire que l'utile) | but, pertinence, connaissance préalable | ❌ | conditionnement au but + scoreur |
| 5 | **Empan / chunking** | unités mots/phrases, spans larges | 🟡 octets, pas de BPE, 129 octets | tokeniseur + attention multi-échelle |
| 6 | **Guidage / méta** (rythme, moins de régressions) | politique de fixation | ❌ | contrôleur d'actions |
| 7 | **Relecture / régression** | retour arrière, mémoire épisodique | ❌ N5 négatif | tampon épisodique + déclencheur |
| 8 | **Vision périphérique** | prélecture parafovéale | 🟡 prélecture I/O, pas modèle | tête de prévisualisation |
| 9 | **Subvocalisation** | contourner le décodage sériel | 🟡 calcul parallèle, génération sérielle | métrique de temps de lecture (faux manque) |
| 10 | **Lecture active** (SQ3R, annoter, résumer) | question, restitution, auto-test | ❌ pas de SFT | boucle de restitution |
| 11 | **Lecture structurelle** (tableaux, code, maths) | 2D, AST, symbolique | ❌ | parseurs classiques + blocs |
| 12 | **Lecture croisée** (comparer, citer) | retrieval, provenance, agent | ❌ M4, pas d'agent | index + provenance + boucle d'outils |
| 13 | **Multilingue** (glose, traduction) | traduction, cognats | 🟡 `z` 0,426 ; chrF sous le plancher | qualité du décodeur |
| 14 | **Multimodal** (scans, figures, layout) | OCR, vision, layout | ❌ | encodeur visuel |

**Lecture de la matrice** : 0 technique opérationnelle au niveau document ; 6 ont un **substrat** mesuré (2, 3, 5,
8, 9, 13) ; 8 sont **absentes**. Le substrat est bon ; c'est l'assemblage qui manque.

## 5. Les cinq couches manquantes

### 5.1 Le document (L2)

- **Bloque** : le modèle ne voit qu'un flux d'octets. Aucun moyen de dire « lis le titre, saute la section 3,
  compare les colonnes 2 et 4 ». Les parseurs existent (DOCX/HTML pour les corpus, découpage en chapitres de
  [`aligneur_litteraire.py`](../../tools/aligneur_litteraire.py)) mais **hors bus**, ad hoc, sans modèle commun.
- **Bloc minimal** : un bloc classique `document` qui émet des **régions typées** (titre, section, paragraphe,
  tableau, code, maths, figure) avec offsets et provenance. Parseurs PDF/HTML/DOCX/Markdown/EPUB ; tables en
  lignes/colonnes/cellules ; code en AST ; maths en LaTeX/MathML. **Aucun entraînement.**
- **Débloque** : survol, balayage, sélectif, structurel, croisé.
- **Porte** : un document de 50 pages se découpe en régions avec provenance exacte ; « où est le tableau X » se
  résout sans modèle ; le rejeu de la découpe est identique.

### 5.2 La fenêtre et la hiérarchie (L2)

- **Bloque** : 129 octets. Les tentatives 130/136/160/256 sont toutes négatives ; à 2 000 octets la PPL est
  **54**, donc le modèle ne généralise pas, il **surapprend sa longueur**. Le test 18/18 à 12 288 jetons est un
  modèle externe.
- **Bloc minimal** : deux voies, à mesurer : (a) entraînement sur séquences longues avec curriculum et états de
  résumé ; (b) lecteur par morceaux avec un **état de section** (span → paragraphe → section → document), qui
  n'exige pas que l'attention voie tout. BPE si N4.1 le justifie.
- **Débloque** : survol, écrémage, cohérence de section.
- **Porte** : PPL à 1 000 octets dans un facteur 1,5 de celle à 129 ; aiguille **native** ≥ 15/18 à 4 000 octets ;
  sinon la hiérarchie doit compenser, et c'est elle qu'on mesure.

### 5.3 La politique de lecture (L3) — le cœur du sujet

- **Bloque** : la sortie précoce accélère de 24 % en perdant 1,61 point, mais elle décide **quand le prochain octet
  est facile**, pas **ce qui vaut la peine d'être lu**. Il n'y a ni saccade, ni budget, ni arrêt, ni relecture.
  C'est la différence entre **sauter du calcul** et **sauter du contenu**.
- **Bloc minimal** : un bloc `lecteur` (classique d'abord) avec trois actions — `survol` (titres + premières/
  dernières phrases), `balayage` (BM25/regex sur les régions), `lecture` (région) —, une **politique de budget**
  (événements/paires) et un **critère d'arrêt**. Puis trois têtes légères, greffées sur le mécanisme des têtes
  précoces : `survol` (pertinence d'une région depuis son début), `balayage` (appariement requête/span),
  `relecture` (confiance ou contradiction).
- **Débloque** : écrémage, balayage, sélectif, guidage, relecture.
- **Porte** : à 30 % du budget, le contrôleur retrouve ≥ 90 % de la réponse de la lecture intégrale sur **trois
  types de documents** ; contrôles : régions aléatoires au même budget, sections mélangées.

### 5.4 La mémoire de travail et épisodique (L4)

- **Bloque** : N5 est net — le signal courant est lisible (R² 0,992), celui d'il y a 8 pas ne l'est pas (−0,681),
  et l'entraînement **aggrave**. Le tampon gelé lit +0,879, mais le réseau ne s'en sert pas. Sans gist, pas de
  compréhension multi-sections ; sans store de régions, pas de relecture.
- **Bloc minimal** : un **état de résumé par section** + une **table d'entités/faits** + un **store de régions**
  (offsets) pour la relecture ; KV cache avec éviction ; tampon en entrée.
- **Débloque** : cohérence, relecture, citation, réponse à une question dont l'indice est loin.
- **Porte** : répondre à une question dont la réponse est en section 2 après avoir lu la section 5, **avec
  citation** ; contrôle : la même question sans le document (closed-book) doit échouer.

### 5.5 La restitution et le banc (L5–L6)

- **Bloque** : le modèle natif est mesuré en **perplexité** — une mesure de fluidité, pas de fidélité. La règle du
  miroir du dépôt le dit : toute mesure d'entrée se double d'une mesure de sortie. Ici, la sortie n'existe pas :
  24/24 vus, **0/4 tenus**, 12 octets cohérents. « Rapide » n'est pas défini sans une tâche et un critère de
  compréhension.
- **Bloc minimal** : un banc par type de document (prose, technique, tableau, code, juridique, presse), 20–50
  questions/résumés/extractions avec **spans gold** ; modes intégral / écrémage / balayage / sélectif ; mesures :
  exactitude, citation, événements, octets, temps ; contrôles : closed-book, régions aléatoires, sections
  mélangées, fuite des titres.
- **Débloque** : tout le reste ; sans lui, on ne saura pas si une technique marche.
- **Porte** : une **courbe vitesse-compréhension** par type, avec un point « écrémage à 30 % du coût, ≥ 90 % de
  l'exactitude » et un contrôle négatif qui échoue.

## 6. Par type de document

| type | technique clé | premier bloqueur | bloc minimal |
|---|---|---|---|
| **Prose / récit** | écrémage, relecture, mémoire des entités | 129 octets, pas d'épisodique | contexte hiérarchique + gist |
| **Exposé / technique** | survol, structurel, résumé | pas de graphe de document | parseur de sections + état de section |
| **Tableaux** | balayage, comparaison, extraction | pas de modèle de table | parseur 2D + opérations classiques (SQL) |
| **Code** | lecture structurelle, exécution | pas d'AST ni d'exécuteur | parseur AST + interpréteur bloc |
| **Maths** | notation, définitions, preuve | pas de parseur symbolique | LaTeX/MathML + CAS bloc |
| **Juridique / admin** | sélectif, références croisées, exactitude | pas d'index ni de retrieval | index + graphe de citations |
| **Presse** | pyramide inversée, saillance | pas de graphe de document | structure + scoreur de saillance |
| **Formulaires** | extraction de champs | pas de sortie structurée | schéma + IE + SFT |
| **Hypertexte** | navigation, pertinence des liens | pas d'agent/outil | graphe de liens + boucle d'outils |
| **Multilingue** | glose, traduction | décodeur sous le plancher | qualité du décodeur (chrF > 39,6) |
| **Scanné / figures** | OCR, layout, figures | pas de vision | encodeur visuel |

## 7. Le banc qui manque (et qui peut démarrer sans entraîner)

C'est le point le plus actionnable : **on peut mesurer la lecture rapide au niveau système dès aujourd'hui**, avec
le moteur existant et un modèle externe, sans toucher à `drave-n0`.

**Dispositif proposé** : 30 documents, 6 par type (prose, technique, tableau, code, juridique), 10 questions chacun
avec spans gold. Graphe de document classique ; contrôleur à quatre modes (intégral, écrémage, balayage, sélectif) ;
même modèle ; trace rejouée.

**Mesures** : exactitude (exact/F1), exactitude de citation (le span cité est-il le bon ?), événements/paires,
octets lus, secondes ; ratio à la lecture intégrale.

**Contrôles négatifs** : régions aléatoires au même budget ; sections mélangées ; questions dont la réponse est dans le
titre seul (fuite) ; **closed-book** (le modèle répond sans le document) ; lecture intégrale sans graphe.

**Ce qui pourrait rendre le résultat faux** : spans gold dans les titres ; contrôleur réglé sur le test ; modèle
qui répond de mémoire ; petit N ; temps mesuré à chaud. La fiche doit les nommer avant le code, comme le veut la
méthode du dépôt.

**Résultat attendu** : si l'écrémage/balayage atteint ≥ 90 % de l'intégral à ≤ 30 % du coût sur au moins trois
types, alors la lecture rapide est un **problème de contrôleur**, pas de modèle — et Drave peut la démontrer sans
attendre N5. Sinon, le blocage est bien dans le modèle (contexte, mémoire), et le banc le dit.

## 8. Ce qui ne manque pas, et les faux chemins

**Ce qui ne manque pas** :

- le **coût proportionnel à l'activité** (FFN creux, top-2, k-WTA, sortie précoce) — c'est la condition économique
  de l'écrémage ;
- les **blocs hybrides** — un parseur, un AST, un index, un solveur sont des blocs de première classe ;
- la **trace et le rejeu** — aucun autre système ne peut prouver aussi bien *ce qu'il a sauté* ;
- la **prélecture/tampons** — une vraie avance I/O, mesurée, même si ce n'est pas une vision périphérique de
  modèle ;
- le **codec 100 %** et les **71 langues** — la base d'une lecture multilingue, si le décodeur remonte.

**Les faux chemins** :

- **courir après 1 000 mots/minute** : la revue scientifique dit que c'est une illusion ; la cible est
  l'allocation, pas le débit ;
- **ajouter des paramètres** : à 20 000 pas, le student 21,63 M fait **3,381** contre **3,123** pour 11,47 M ; la
  capacité à budget égal donne −8,1 %, mais le prior domine — la structure d'abord ;
- **construire un encodeur visuel avant le texte structuré** : la plupart des documents sont du texte structuré ;
  les parseurs classiques sont moins chers et mesurables ;
- **entraîner un résumeur avant un lecteur** : le décodeur est sous le plancher chrF ; on mesurerait le plancher,
  pas le résumé ;
- **confondre prélecture et vision périphérique** : la première apporte des octets, la seconde des **prédictions** ;
  la tête de prévisualisation manque ;
- **confondre PPL et lecture** : la PPL mesure la fluidité ; le miroir exige la restitution.

## 9. Ce que cela change pour la roadmap

Le programme **R** de [`roadmap.md`](../pilotage/roadmap.md) traduit cette analyse en six phases :

- **R0 — le lecteur v0** : graphe de document, contrôleur classique, banc. **Sans entraînement**, avec le moteur
  existant. C'est la priorité non bloquée.
- **R1 — la fenêtre native** : contexte hiérarchique, curriculum, tokenisation. Dépend de N1/N2.
- **R2 — la mémoire** : gist, entités, store épisodique, relecture. Dépend de N5 et R1.
- **R3 — la restitution** : SFT de lecture, citations. Dépend de N4 et R0.
- **R4 — les blocs structurels** : tableaux, code, maths, vision. Dépend de R0.
- **R5 — la lecture croisée** : multi-documents, retrieval, multilingue. Dépend de R3.

Autrement dit, les **cinq couches** de la § 5 se projettent sur ces six phases : **R0** porte le document, la
politique et le banc ; **R1** la fenêtre ; **R2** la mémoire ; **R3** la restitution ; **R4/R5** les extensions
structurelles et croisées.

Les **fiches de fonctionnalité** sont dans [`backlog/index.md`](../pilotage/backlog/index.md), avec le contrat, la
porte, les contrôles négatifs et ce qui pourrait les rendre fausses. L'état courant et la prochaine action restent
dans [`en-cours.md`](../pilotage/en-cours.md).

## 10. Ce qui pourrait invalider cette analyse

- **Si un modèle natif à 129 octets + un contrôleur classique répond aux questions de document**, alors le contexte
  n'est pas le premier blocage : le contrôleur suffit pour la v0, et R1 peut attendre.
- **Si `z` restitue au-dessus du plancher** (chrF > 39,6) sur des articles tenus à l'écart, alors le gist peut être
  `z`-basé, et R2.1 change de forme.
- **Si la sortie précoce conditionnée par la pertinence** donne une meilleure courbe que la confiance du prochain
  octet, alors la « tête de survol » est le premier changement de modèle qui vaut.
- **Si la sélection aléatoire de régions au même budget égale le contrôleur**, alors le contrôleur ne lit pas : le
  banc est faux, et il faut le refaire.

---

*Sources principales : [`docs/pilotage/roadmap.md`](../pilotage/roadmap.md) (programme R, états A/B/N) ;
[`docs/pilotage/manques.md`](../pilotage/manques.md) (M4, M6, N5, architecture) ;
[`docs/pilotage/en-cours.md`](../pilotage/en-cours.md) (têtes précoces, réflexe) ;
[`docs/theorie/protocole-semantique.md`](protocole-semantique.md) (`z`, chrF) ;
[`reports/rapport-aiguille-topk.md`](../../reports/rapport-aiguille-topk.md) et
[`reports/campagne-benefices/011-09-la-memoire-tient-laiguille-est-retrouvee.md`](../../reports/campagne-benefices/011-09-la-memoire-tient-laiguille-est-retrouvee.md)
(aiguille Qwen) ; [`docs/archive/note-lecteurs-paralleles.md`](../archive/note-lecteurs-paralleles.md) (prélecture) ;
[`docs/methode/miroir.md`](../methode/miroir.md) (règle du miroir).*
