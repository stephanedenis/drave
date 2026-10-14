# État des modules — l'index

> **2026-10-10 10:35 HAE.** Ce fichier est un **index** : pour chaque module du dépôt, sa
> **roadmap** (ce qu'on projette), son **état** (où on en est) et sa **prochaine action**. Le
> détail mesuré est dans `reports/` (une fiche par expérience), les événements dans `journal/`.
> Convention : `docs/organisation-du-depot.md`.

| module | roadmap / plan | état | prochaine action |
|---|---|---|---|
| **Moteur** (`drave-core`) | `docs/roadmap-drave.md`, `docs/roadmap.md`, `docs/plan-modeles-lourds.md` | `docs/manques.md` (M1-M8 : noyau de listes pour experts, noyau GPU creux, lots + hyper-connexions, encodeurs, spéculatif, apprentissage embarqué, qualité des gros modèles, défaut de sauvegarde log-normal) | M8 (le fichier sauvé ne reproduit pas le modèle entraîné) — cause ouverte |
| **Modèle** (dessins entraînables) | `docs/modele-pour-drave.md`, `docs/plan-deepseek41-complet.md`, `docs/plan-mla-vision.md` | `docs/manques.md` (N1-N4) ; `docs/etat-cerveau.md` § 4 | entraîner les dessins **H/I/J** (jamais entraînés) |
| **Cerveau / distribué** | `docs/plan-cerveau-complet.md` (les douze capacités) | **`docs/etat-cerveau.md`** — C1-C12, avec le chiffre qui prouve chacune | C8 : le **chemin court entraîné** est mesuré **et exécuté par le moteur** (dessin B : ÷1,24 à ÷1,47 à profondeur 8, `reports/rapport-n4-porte-execution.md`) ⇒ trancher la **variabilité** entre exécutions (±10 %) et mesurer la **génération libre** ; la **structure de mémoire** (conception et portes : `docs/note-peripherie-c8.md` § 6) · C9 : la variante `--echange experts` (le gain entre vues valides est **nul**, mesuré) · C4 : l'ordonnanceur — la politique est tranchée (on ne réutilise **jamais** un état : ×633 contre ×1,06) |
| **Émulation d'un professeur** | `docs/programme-recherche.md`, `docs/note-un-pont-par-professeur.md`, `docs/note-regle-contrastive.md` | **`docs/etat-emulation-professeur.md`** (méthode, résultats, corrections) | les expériences sont dans `reports/toutes-langues/` (107 fiches) |
| **Biologie → moteur** | `docs/biologie-pour-drave.md` (E1-E9) | `docs/etat-cerveau.md` § 3 : E1, E3, E4, E7, E8 mesurées ; E6 en échec de code ; E2/E5 cadrées | écrire le protocole E2 (croissance des connexions) et E5 (rejeu) |
| **Matériel et système** | `docs/configuration-nvme-raid-amd.md`, `docs/numa-segregation.md`, `docs/plan-gpu-topk.md`, `docs/colab-reparti.md` | `reports/bilan-multi-materiel.md`, `reports/rapport-materiel-disque-ou-cpu.md` | — |
| **Conventions et mémoire du dépôt** | `docs/organisation-du-depot.md`, `docs/references-non-regression.md`, `docs/glossaire.md`, `docs/histoire.md`, `docs/relations-humaines.md` | ce fichier, plus `README.md` (entrée) et `REPRISE.md` (check-list de démarrage) | tenir `journal/AAAA-MM-JJ.md` à chaque round |

**Points d'entrée** : `README.md` (ce qu'est Drave, où est quoi) · `REPRISE.md` (les cinq premières
minutes d'une session, ce qui doit être vert, les pièges) · `docs/references-non-regression.md`
(les repères chiffrés d'une passe de portes) · `docs/organisation-du-depot.md` (où écrire quoi).

## Où sont les chiffres

- **une fiche par expérience** dans `reports/` : `reports/campagne-benefices/` (51 fiches, la
  campagne 24 h du 8-9 octobre et le sprint cerveau du 9-10 octobre), `reports/toutes-langues/`
  (107 fiches, l'extension multilingue), et les rapports d'une seule expérience à la racine de
  `reports/` ;
- **les monolithes d'origine** sont conservés dans `reports/archive/` : rien n'a été supprimé,
  les fiches en sont des extraits **verbatim**.

## La règle de lecture

Un état ne dit pas « c'est fait » : il dit **c'est fait, et voici le chiffre qui le prouve**,
avec le fichier où le vérifier. Quand un chiffre est corrigé, l'ancien reste **à côté** du
nouveau (c'est ainsi que le dépôt garde mémoire de ses erreurs : voir `docs/manques.md` § 4 et
les fiches qui portent une rectification).
