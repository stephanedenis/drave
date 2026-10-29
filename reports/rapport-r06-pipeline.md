# R0.6 — le pipeline de lecture : 12/20 au pilote, 10/10 refusés, 7/8 au modèle

> **Ligne de roadmap** : R0.6 · **Date** : 2026-10-29 · **Verdict** : ✅ **le contrat est tenu** —
> 20/20 réponses acceptées au pilote dont **12 justes** (0,600), **provenance vérifiée 20/20**,
> **refus 9/10** sur des questions hors sujet, **rejeu identique**, et le **modèle** répond
> **7/8** là où l'extractif n'en donne que **3/8** (paraphrases).
>
> **Dispositif** : `tools/lecture.py` (extractif par défaut, modèle sur demande) ; seuil de refus
> **3,8** ; porte `tools/porte-lecture.sh` (6 contrôles) ; JSON brut
> [`r06-pipeline.json`](r06-pipeline.json) ; spec
> [`pipeline-lecture.md`](../docs/implantation/pipeline-lecture.md).

## La question

R0.1 (le document), R0.2 (le contrôleur), R0.3 (le banc) existent séparément. Le pipeline les
**assemble** : un document, une question, un budget → une réponse **avec sa source**, dans une
trace rejouable. La question de la fiche : le contrat tient-il — budget, provenance, refus,
rejeu — et que vaut l'assemblage sur les trois régimes mesurés ?

## Le dispositif

- **une commande** : `python3 tools/lecture.py --document X --question Q [--budget 0.30]
  [--lecteur extractif|modele]` ; sortie JSON ou texte, la source (région, offset, sha) avec
  la réponse ;
- **le refus** : si le meilleur score BM25 est sous **3,8**, la réponse est « insuffisant » —
  le pipeline ne rend pas un passage au hasard ;
- **la porte** : 6 contrôles — réponse connue, budget tenu, provenance, rejeu, refus,
  closed-book — tous verts ;
- **les trois régimes** : pilote (20 questions main), hors sujet (10 questions), paraphrases
  (8 questions du banc durci).

## Ce qui est mesuré

| régime | mesure | chiffre |
|---|---|---|
| **pilote** (20 questions) | réponses acceptées · justes · provenance | **20/20** · **12/20 = 0,600** · **20/20** |
| **hors sujet** (10 questions) | refus | **9/10 = 0,900** |
| **paraphrases** (8 questions) | extractif · modèle | **3/8** · **7/8** |
| **rejeu** | deux exécutions, même JSON | **identique** |
| **porte** | 6 contrôles | **6/6** |

**Le pipeline fait ce qu'il promet** : il lit dans le budget (2 516 octets sur 3 132 pour la
question de référence), cite sa source (région `r00032`, octets 8015–8339), refuse le hors
sujet, et rejoue à l'identique.

**Et il choisit bien ses lecteurs** : sur les paraphrases, l'extractif ne donne que 3/8 (il est
refusé ou trompé), le **modèle en donne 7/8**. C'est la leçon de R0.3 rendue **utilisable** :
le lexique pour les mots, le modèle pour les paraphrases, et le refus comme aiguillage.

## Le seuil, et pourquoi 1,0 (et pas 3,8)

Les scores BM25 des **réponses justes** du pilote vont de **3,94 à 11,08** ; le seul **faux
positif** hors sujet (« trois » dans « trois octets ») est à **3,56**. Un seuil de **3,8** sépare
les deux sur ce document — et c'est un piège : **mesuré sur les 84 paraphrases, il refuse 32 %
des questions et coûte 6,7 points** (0,269 → 0,202) pour gagner **un** refus sur dix. Le seuil
est donc ramené à **1,0** : il attrape les questions qui ne partagent **rien** avec le document
(score 0,00) et laisse passer les autres. Le faux positif à 3,56 reste — il n'est pas séparable
des vraies réponses par un seuil global. C'est la leçon de R0.5 appliquée : **un seuil absolu ne
se transporte pas**. Exposé (`--seuil`), il se calibre par corpus.

## Le choix automatique de la voie : +11 points sur un corpus de valeurs, −15 sur un corpus mixte

`--lecteur auto` classe la question par sa **forme** (« combien », « quel numéro », « quelle
date » → span ; sinon extractif). Résultat sur les trois jeux :

| jeu | auto | extractif | écart |
|---|---:|---:|---:|
| lexical (249, questions à valeur) | **0,944** | 0,835 | **+0,109** |
| paraphrases (84, à valeur) | **0,333** | 0,274 | **+0,059** |
| pilote (20, mixte) | 0,450 | **0,600** | **−0,150** |

**Sur un corpus qui demande des valeurs, le choix automatique paie** (+11 points sur le
lexical). **Sur un corpus mixte, il coûte** (−15 points sur le pilote). Les cinq désaccords du
pilote disent pourquoi :

- **les nombres en mots** : « combien d'invariants ? » attend « six », le span ne connaît que les
  chiffres et rend « 2 » ;
- **le classement du span** : « combien de pages R0.1 ? » attend « 51 », le span rend « 0.1 »
  (le premier chiffre de la phrase, pas la réponse) — le span hérite du BM25 du **passage**, pas
  d'un score de **span** ;
- **un artefact de contrôle** : « point 7 » attendu, « 7 » rendu — la valeur est juste, la
  comparaison est stricte.

**La leçon, la même que R0.5 mais par un autre chemin** : le choix de la voie dépend du
**corpus**, pas seulement de la forme de la question. Le défaut du pipeline reste l'extractif ;
`--auto` s'active pour un corpus dont on sait qu'il demande des valeurs.

Deux correctifs ont été essayés pour rattraper le pilote — un score de fenêtre et des spans de
nombres en mots — et **les deux ont été rejetés par la mesure** (détail dans la fiche R05) : le
pilote gagne 2 questions, les bancs en perdent 5. Le déficit de l'auto sur un corpus mixte
(−0,150) reste **nommé, pas corrigé**.

## Ce qui pourrait le rendre faux

- **le seuil est calibré sur l'échelle BM25 brute** de ce corpus : un autre document, une autre
  longueur de passages, et 3,8 ne sépare plus rien (la leçon du routeur, R0.5) ;
- **les échantillons sont petits** : 20, 10 et 8 questions ; un cas vaut 0,05 à 0,125 ;
- **le modèle n'a ni provenance ni refus** : il répond toujours, et sa réponse ne se cite pas ;
- **le pilote** mesure le lecteur extractif (0,600), pas le pipeline : le pipeline ne fait que
  l'assembler — c'est déjà le plafond de R0.2 ;
- **le budget en octets** ignore le coût CPU réel (découpage, scoring), qui reste négligeable
  ici (0,02 s).

## Ce que ça change

1. **R0 est utilisable** : une commande, un contrat, une porte. Les mesures de R0.1–R0.3 ne
   sont plus des fiches isolées, elles sont un lecteur.
2. **Le refus est une propriété de sûreté** : un pipeline qui répond toujours est un pipeline
   qui devine ; celui-ci dit « insuffisant » quand il ne sait pas, et propose le modèle.
3. **L'aiguillage extractif/modèle est démontré** là où il compte : 3/8 contre 7/8 sur les
   paraphrases.

## Fichiers

- `tools/lecture.py` — le pipeline (extractif, modèle, refus, provenance, trace).
- `tools/porte-lecture.sh` — la porte à 6 contrôles.
- `docs/implantation/pipeline-lecture.md` — le contrat et les limites.
- `reports/r06-pipeline.json` — les mesures brutes (20 + 10 + 8 questions).
