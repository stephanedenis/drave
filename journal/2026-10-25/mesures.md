# 2026-10-25 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-25/README.md](README.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (7)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 02:52 | `9a589115` | C3.2c — LE NOMBRE DE TEXTES D'EVALUATION DEVIENT UN PARAMETRE : --eval-textes (3 par defaut). Le 100 % de C3.2b portait sur 3 textes ; C3.2c le mesure sur 8, et la courbe par famille viendra | `2026-10-25/README.md`, `2026-10-25/memoire.md`, `THEMES.md` (+1) |
| 03:20 | `68a9285a` | C3.2c — LE 100 % DE C3.2b ETAIT UN EFFET DES 3 TEXTES : sur 8 textes d'evaluation, la recopie de la famille indo-europeenne est a 14,7 %, pas 100 %. Le controle reste a 0 %. Le chiffre honnete : 14,7 % contre 30 % (reference a 1 langue) et 4,4 % (a 10 langues) — au-dessus de la reference a 10 langues (3,3x), sous celle a 1 langue. C'est un pas, pas une solution | `2026-10-25/README.md`, `2026-10-25/mesures.md`, `README.md` (+2) |
| 04:44 | `ef989038` | DOC — LE BILAN DU 25/10 DIT C3.2 : la page vivante ajoute le resultat au bilan du jour (un module par famille, 4 sur 5 au-dessus de la reference, 14,7 a 100 %) et le journal des mesures du 25 porte le recit (les 3 sous-lignes, la courbe, les deux instruments repares) | `en-cours.md`, `2026-10-25/README.md`, `2026-10-25/docs.md` (+2) |
| 04:46 | `cc3d34e4` | ROADMAP — LA LIGNE C3.2 EST CLOSE : la section disait encore « prochaine action : C3.2c » alors que les trois sous-lignes sont mesures. Elle dit maintenant : aucune, la ligne est close ; la suite (9 familles, comprendre l'indo-europeen a 14,7 %) est hors du plan. La reserve du sino-tibetan (40,5 % avant) est ajoutee | `roadmap.md`, `2026-10-25/README.md`, `2026-10-25/mesures.md` |
| 04:48 | `c35f7448` | CARTE — LA C3 POINTE VERS SON RESULTAT : la ligne C3 ne menait qu'a la synthese 07 et a la garde de tete ; elle mene maintenant aussi au rapport des modules par famille (4 sur 5 au-dessus de la reference). La carte est le point d'entree pour trouver un sujet : elle doit mener au chiffre | `carte.md`, `2026-10-25/README.md`, `2026-10-25/mesures.md` (+1) |
| 04:50 | `5c221b31` | DOC — L'INVENTAIRE LISTE LE RAPPORT C3.2 : docs/README.md enumerait la carte du raisonnement naturel et les mesures, mais pas le rapport des modules par famille. Il y est : 28 familles, le module, la courbe sur 5 familles (4 sur 5 au-dessus de la reference) | `README.md`, `2026-10-25/README.md`, `2026-10-25/mesures.md` |
| 06:37 | `df627001` | README — LA RESTITUTION PAR FAMILLE EST DANS CE QUI EST FAIT : la section « fait, mesure » listait A7, B4 et A8 ; elle ajoute C3.2 (28 familles decoupees, le module par famille, la courbe sur 5 familles — 4 sur 5 au-dessus de la reference, de 14,7 % a 100 %, controle 0 %). Le README dit maintenant tout ce qui est accompli | `README.md`, `2026-10-25/README.md`, `2026-10-25/portes.md` (+1) |

## Chiffres du jour

`14,7 %` · `100 %` · `0 %` · `40,5 %` · `30 %` · `4,4 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Mesures et rapports touchés

- [reports/rapport-modules-famille.md](../reports/rapport-modules-famille.md)

<!-- notes -->
**Le 25 octobre — C3.2 : la restitution par famille.** Le découpage (C3.2a : 28 familles, 362 langues, 12 383
articles), le module par famille (C3.2b : 0 % → 100 % sur 3 textes) et la **courbe sur 5 familles** (C3.2c :
indo-européen 14,7 %, atlantic-congo 94,0 %, austronesian 61,0 %, sino-tibetan 100,0 %, turkic 96,1 %) — **4 familles
sur 5 au-dessus de la référence** à une langue. La difficulté est l'**hétérogénéité interne** de la plus grande famille,
pas la taille du corpus. Deux instruments réparés au passage : le modèle n'était pas sur le GPU, et le LoRA était sur
CPU contre un modèle sur cuda (le piège du 14ᵉ jour, deux fois).

**Les jeux symboliques (B5/B6).** La demande était double : optimiser les couches linguistiques pour la sémantique
des jeux (morpion, échecs, dames, go, cartes), puis bâtir la logique dans le niveau pensée. On a posé un
**contrat RSN-jeu** (jeu + nature + corps canonique + annotation hors empreinte) et quatre couches cumulatives :
surface, normalisation, lexique, grammaire, sémantique. Le corpus de **112 surfaces** est couvert à **50 / 77 /
105 / 110 / 112** ; les **33 paires** équivalentes passent de **9/33** à **33/33** ; **0 collision** sur les 8
groupes négatifs ; la restitution est **112/112** et la perturbation **112/112**. Le lexique permuté perd **20
items** — les phrases, exactement la population qu'il sert ; les étiquettes mélangées tombent à **7/112**.

Côté pensée : le morpion est résolu (valeur **0**, partie parfaite nulle, exact **200/200** sans défaite) ; le
perft des échecs est exact sur six positions jusqu'à la profondeur 4, les **3/3** mats en un sont trouvés (le
statique n'en trouve qu'**1/3**) ; les dames passent le perft **7 · 49 · 302 · 1 469 · 7 361 · 36 768** et la
recherche gagne **20/20** contre le joueur sans recherche ; la politique des cartes fait **79,7 %** contre le
hasard (1 000 donnes, **0** coup illégal sur 52 000). La décision est **invariante 5/5** : la même position
écrite de deux façons donne le même coup.

Le négatif : le MCTS du go, à **60 playouts**, gagne **1/3** contre le hasard. Les règles sont justes (capture,
suicide, ko, score), la force n'est pas établie ; c'est écrit. Le corpus est **construit** par le même code que
celui qu'il teste — le perft, les contrôles négatifs et la restitution sont là pour que ce ne soit pas circulaire.

La porte : [`tools/porte-jeux.sh`](../tools/porte-jeux.sh) (54 tests + mesure rapide).
<!-- /notes -->
