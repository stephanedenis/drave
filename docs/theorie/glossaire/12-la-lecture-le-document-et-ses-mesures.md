# 12. La lecture, le document et leurs mesures

> **Famille 12 du glossaire** (12 familles). Index : [le glossaire](../glossaire.md).

---

## 12. La lecture, le document et leurs mesures

Les termes du **programme R** et du **backlog** : comment un document devient des régions, comment une
politique choisit quoi lire, ce qu'on garde en mémoire, et avec quelles mesures on prouve la
compréhension. Les définitions renvoient aux fiches du backlog, au plan et à l'analyse ; les termes
déjà définis ailleurs sont liés, pas recopiés.

**Lecture rapide (survol, balayage, écrémage, lecture sélective)** — Ensemble des modes de lecture qui
adaptent l'effort au but et au document : **survol** (structure, titres, début et fin), **balayage**
(chercher une cible), **écrémage** (prendre le gist, sauter les détails), **lecture sélective** (ne lire
que l'utile). La revue de Rayner et al. (2016) montre que la vitesse élevée avec compréhension pleine
n'est pas tenable : le levier est l'**allocation**, pas le débit.
**Où** : `docs/theorie/lecture-rapide.md`, programme R de `docs/pilotage/roadmap.md`.
**Réf.** : Rayner et al., *So Much to Read, So Little Time*, 2016.

**Contrôleur de lecture** — Politique qui choisit, pour un but et un budget, la prochaine action de
lecture (survol, balayage, lecture, relecture, arrêt) et sa profondeur. Il transforme un document en
**trajectoire** tracée, rejouable ; il est **classique d'abord**, neuronal ensuite.
**Où** : `docs/pilotage/backlog/R02-controleur-lecture.md`, ligne R0.2.

**Relecture** *(régression de lecture)* — Retour sur un passage mal compris, pour récupérer une
information ou vérifier une contradiction ; à ne pas confondre avec la
relecture adverse d'un document. Elle exige
une mémoire du texte (store de régions) et un déclencheur.
**Où** : `docs/pilotage/backlog/R06-tete-relecture.md`, `R22-memoire-episodique.md`.

**Graphe de document** *(région, offset, provenance, manifeste)* — Représentation d'un document en
**régions typées** (titre, section, paragraphe, tableau, code, maths, figure), avec leur **offset** dans
le fichier, leur parent et leur **provenance**. Le **manifeste** est l'objet sérialisé qui porte ces
régions et survit au rejeu.
**Où** : `docs/pilotage/backlog/R01-graphe-document.md`, ligne R0.1.

**Span** *(span gold)* — Intervalle de texte délimité par deux offsets. Un **span gold** est l'intervalle
de référence qui contient la réponse attendue ; il sert à mesurer l'exactitude et la **citation**.
**Où** : `docs/pilotage/backlog/R03-banc-lecture-rapide.md`, `R32-citations-provenance.md`.

**Closed-book** — Réglage d'évaluation où le modèle répond **sans le document**, de mémoire. C'est le
contrôle négatif du banc de lecture : si le closed-book fait aussi bien que la lecture, le banc ne mesure
pas la lecture.
**Où** : `docs/pilotage/backlog/R03-banc-lecture-rapide.md`, `R21-memoire-travail-gist.md`.

**Gist** *(mémoire de travail, mémoire épisodique)* — Le **gist** est l'état résumé d'un document
(thème, entités, faits) qui tient lieu de mémoire de travail entre les sections. La **mémoire
épisodique** est le store des régions et de leur état, qui permet de revenir sur un passage.
**Où** : `docs/pilotage/backlog/R21-memoire-travail-gist.md`, `R22-memoire-episodique.md`.

**Retrieval** *(recherche, index, BM25)* — Sélection des passages pertinents dans un ou plusieurs
documents avant lecture. Un **index** (lexical ou vectoriel) rend la recherche sous-linéaire ; **BM25**
est le scoreur lexical classique.
**Où** : `docs/pilotage/backlog/R05-tete-balayage.md`, `R51-lecture-croisee.md`.

**Curriculum** *(d'entraînement)* — Ordre de difficulté croissante des exemples pendant l'entraînement
(longueur, contexte, tâche). Dans R1.2, il désigne la recette qui allonge le contexte sans refaire les
négatifs 130–256.
**Où** : `docs/pilotage/backlog/R12-curriculum-contexte.md`.

**SFT** *(supervised fine-tuning ; ajustement supervisé)* — Entraînement supervisé sur des couples
instruction → réponse, pour apprendre un format et un comportement. Le SFT de lecture (R3.1) doit tenir
sur des **documents non vus**, pas seulement mémoriser.
**Où** : `docs/pilotage/backlog/R31-restitution-sft.md`, `N4-usage-sft.md`.

**Distillation** *(professeur → élève)* — Entraîner un petit modèle (**élève**) à imiter les sorties ou
les distributions d'un grand (**professeur**). Le programme N distille Qwen/DeepSeek dans `drave-n0` ; la
porte est l'écart au professeur sur un jeu tenu à l'écart.
**Où** : `docs/pilotage/backlog/N2-distillation.md` ; voir [professeur / élève](entrees/professeur-eleve.md).

**chrF** — Mesure de similarité de chaînes par n-grammes de caractères, utilisée pour la traduction et la
restitution. Elle se lit toujours avec un **plancher** (la surface source contre la référence) : sans
plancher, un chrF de 20 ne dit rien.
**Où** : `docs/pilotage/backlog/R52-multilingue-decodeur.md`, `B10.3-raisonnement-z.md`.

**WER** *(Word Error Rate ; taux d'erreur mot)* — Proportion de mots faux (substitutions, insertions,
suppressions) dans une transcription OCR. C'est une mesure d'entrée pour R4.4 ; la mesure de sortie reste
la **parité de réponse** avec le texte natif.
**Où** : `docs/pilotage/backlog/R44-encodeur-visuel.md`.

**F1** *(F-mesure)* — Moyenne harmonique de la précision et du rappel ; utile quand les réponses sont des
**spans** et que le nombre de mots compte.
**Où** : `docs/pilotage/backlog/R03-banc-lecture-rapide.md`.

**AUC** *(aire sous la courbe ROC)* — Probabilité qu'un score classe un positif avant un négatif ; elle
mesure le classement d'une tête (survol, balayage) indépendamment du seuil.
**Où** : `docs/pilotage/backlog/R04-tete-survol.md`.

**Parseur** *(analyseur syntaxique)* — Programme qui transforme un format (HTML, PDF, DOCX, code, LaTeX)
en structure (arbre, grille, AST). Dans R0.1, un parseur par format émet des **régions** ; il est
classique, pas neuronal.
**Où** : `docs/pilotage/backlog/R01-graphe-document.md`, `R41-bloc-tableaux.md`.

**AST** *(Abstract Syntax Tree ; arbre de syntaxe abstraite)* — Arbre qui représente la structure d'un
programme (expressions, instructions, portées) sans la ponctuation de surface. Il permet de lire du code
par ses dépendances et de l'exécuter.
**Où** : `docs/pilotage/backlog/R42-bloc-code.md`.

**CAS** *(Computer Algebra System ; système de calcul formel)* — Bibliothèque qui manipule des expressions
symboliques (dérivée, simplification, substitution) au lieu de les évaluer numériquement.
**Où** : `docs/pilotage/backlog/R43-bloc-maths.md`.

**OCR** *(Optical Character Recognition ; reconnaissance optique de caractères)* — Conversion d'une image
de texte en texte machine. Dans R4.4, l'OCR est un **bloc externe** ; la porte est la parité de réponse
avec le texte natif, pas le WER seul.
**Où** : `docs/pilotage/backlog/R44-encodeur-visuel.md`.

**Layout** *(mise en page)* — Organisation spatiale d'une page (colonnes, titres, tableaux, figures, ordre
de lecture). C'est l'information que le texte plat perd et que R4.4 doit restaurer.
**Où** : `docs/pilotage/backlog/R44-encodeur-visuel.md`.

**DRVM** *(Drave Model)* — Format natif de modèle du programme N : manifeste, graphe de blocs, payload de
tenseurs, hash. Il remplace GGUF comme format de référence pour `drave-n0`.
**Où** : `docs/pilotage/backlog/N0.3b-parite-ppl.md` ; voir [DRVF](entrees/drvf.md) et [GGUF](entrees/gguf.md).

**Contrôle négatif** — Dispositif qui doit **échouer** si la mesure ne mesure pas ce qu'elle prétend :
closed-book, régions aléatoires, sections mélangées, plancher chrF. Sans lui, un chiffre n'est pas un
résultat.
**Où** : `docs/pilotage/backlog/index.md`, `docs/methode/resultats.md`.

**Graphe de dépendances** *(arête dure, plafond, frontière)* — Représentation des dépendances entre
fiches : une **arête dure** bloque l'artefact d'entrée ; un **plafond** borne le résultat sans bloquer le
travail ; la **frontière** est l'ensemble des items disponibles. À ne pas confondre avec le
plafond de flux ni avec la frontière fidélité/contenu.
**Où** : `docs/pilotage/backlog/dependances.md`.

**Contrat** *(de fiche)* — Ce qu'une fonctionnalité reçoit, rend, coûte et trace, écrit avant le code. À
ne pas confondre avec le contrat d'activation, qui est un format de
flux.
**Où** : `docs/pilotage/backlog/_modele.md`.

**Tableau** *(table de données)* — Grille de cellules indexées par lignes et colonnes, avec en-têtes et
fusions ; elle se lit par un parseur 2D et des opérations classiques (filtre, jointure, agrégat).
**Où** : `docs/pilotage/backlog/R41-bloc-tableaux.md`.

**Tenu à l'écart** *(held-out)* — Jeu d'évaluation dont les documents ne sont jamais vus à
l'entraînement ; c'est la condition pour distinguer l'apprentissage de la mémorisation (24/24 vus, 0/4
tenus).
**Où** : `docs/pilotage/backlog/R31-restitution-sft.md`, `N4-usage-sft.md`.

**Banc de lecture rapide** — Banc qui mesure la **compréhension par unité de calcul** sur plusieurs types
de documents, avec des modes (intégral, écrémage, balayage, sélectif) et des contrôles négatifs
(closed-book, régions aléatoires, sections mélangées).
**Où** : `docs/pilotage/backlog/R03-banc-lecture-rapide.md` ; voir [banc](entrees/banc.md).
