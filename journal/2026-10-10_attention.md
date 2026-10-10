# 2026-10-10 — Attention, fenêtre, puits

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-10.md](2026-10-10.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (18)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 05:44 | `892acfd` | C6 : clé de FENÊTRE — la prédiction est RÉFUTÉE, et elle confirme le §24 quater | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+3) |
| 07:27 | `dee9e58` | Balayage des portes : le piege de fenetre etait LATENT dans porte-topologie aussi | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+3) |
| 08:02 | `031dbc4` | E4 (suite) : le gain d'entree generalise, mais sa MAGNITUDE depend de la fenetre | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+3) |
| 08:24 | `c54c6fa` | attn-topk : pas de defaut (il agit a contexte long) · attn-window : un vrai trou, correction REVERTEE | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 08:33 | `e6f7b6b` | attn-window en reparti : un REFUS explicite, pas un resultat faux et silencieux | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+4) |
| 08:44 | `dd66191` | PROTOCOLE v7 LIVRE : la fenetre d'attention voyage, le refus disparait, tout est vert | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+3) |
| 09:32 | `484a4ef` | CORRECTION : le v7 transporte la fenetre, mais le PILOTE ne l'applique pas — ma conclusion du round 28 etait hative | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:35 | `712a8b4` | Les trois lignes manquantes : le pilote applique enfin la fenetre, et la mesure le confirme | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+3) |
| 09:40 | `dd95fa9` | --attn-sinks : ecrit dans les trois chemins, transporte par le v7… et LU NULLE PART | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 09:41 | `639b007` | Journal : la section 46 bis (--attn-sinks ecrit partout, lu nulle part) manquait — l'ancre du premier essai ne correspondait pas | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 10:07 | `85cf49c` | --attn-sinks : le refus etait FAUX (le compteur EST lu, branche a fenetre) — le drapeau vit, et le zero n'existait pas | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+5) |
| 10:19 | `531e760` | Fenetre x puits d'attention : +2,0 % de perplexite pour divide 2,67 les cles notees (512 jetons) | `etat-cerveau.md`, `2026-10-10.md`, `README.md` (+4) |
| 10:39 | `024e509` | Fenetre x puits : la pente en N mesuree — gratuit a 512 jetons, +40 % a 2 048 | `etat-cerveau.md`, `2026-10-10.md`, `2026-10-10_attention.md` (+13) |
| 10:57 | `b4f1589` | Fenetre x puits a 2 048 : MA conclusion du §4 etait bornee par la grille — avec 512 puits, +0,33 % | `etat-cerveau.md`, `2026-10-10.md`, `2026-10-10_attention.md` (+14) |
| 11:10 | `499400e` | Carte fenetre x puits : la case donne aussi le TEMPS et le debit (tok/s) | `2026-10-10.md`, `2026-10-10_apprentissage.md`, `2026-10-10_attention.md` (+14) |
| 11:42 | `62c9da5` | Carte fenetre x puits : secondes corrigees, et les points d'entree nommes dans l'index | `etat.md`, `organisation-du-depot.md`, `2026-10-10.md` (+9) |
| 12:04 | `7b0ba27` | Fenetre x puits : le prix REEL en temps mesure — diviser les cles par 4 ne rend que +12 % de debit | `2026-10-10.md`, `2026-10-10_apprentissage.md`, `2026-10-10_attention.md` (+15) |
| 12:05 | `9cb184d` | Etat : le prix en temps de la fenetre est consigne (div 4 de cles = +12 % de debit, pas x4) | `etat-cerveau.md`, `2026-10-10.md`, `2026-10-10_attention.md` (+6) |

## Chiffres du jour

`+12 %` · `+0,33 %` · `+40 %` · `512 jetons` · `+2,0 %` · `−6,7 %` · `−1,4 %` · `256 jetons` · `÷2,67` · `2048 jetons` · `10,4046` · `10,3703`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Étapes du jour (36)

*Ce que l'agent a consigné en le faisant (lignes `⏵` du journal de session) :*

- **05:13** — C6 : je teste la clé de FENÊTRE — l'expérience qui découle du mécanisme k-WTA identifié
- **05:24** — La référence reproduit exactement (50 et 1006) — j'attends les fenêtres 4, 16, 64
- **05:33** — Prédiction RÉFUTÉE : la fenêtre détruit le bon indice (50 → 653) sans aider le mauvais
- **07:25** — Round 13 : je cherche le même piège de fenêtre dans les autres portes qui comparent entier et réparti
- **07:25** — Je balaie les portes : lesquelles comparent un entier à un réparti (le piège de fenêtre) ?
- **07:28** — Round 13 livré : le piège de fenêtre était latent dans une 2ᵉ porte — balayage fait, règle écrite
- **07:56** — E4 : le gain d'entrée se généralise-t-il ? Je teste sur un second modèle et une autre fenêtre
- **07:57** — L'effet généralise (Q4_0 : −6,7 %) mais il DIMINUE avec la fenêtre (256 jetons : −1,4 %) — je verrouille
- **08:10** — L'audit donne des CANDIDATS — je mesure si `--act-topk` et `--attn-topk` agissent en réparti
- **08:10** — La plupart des candidats sont couverts par un helper — reste `--attn-window` : je mesure
- **08:11** — Round 22 : la mesure vide d'hier — je regarde la SORTIE COMPLÈTE d'un candidat (`--attn-window`)
- **08:16** — `--attn-topk` agit à 512 jetons (mon hypothèse était bonne) ; `--attn-window` reste inerte — test en LOCAL
- **08:18** — Deuxième vrai trou : `--attn-window` AGIT en local (13,1→21,6) mais PAS en réparti — je le câble
- **08:26** — La cause est trouvée : le pilote applique la fenêtre, le nœud NON → 195,6 contre 50,4. Je REFUSE au lieu de calculer faux
- **08:45** — Round 28 livré : **protocole v7** — la fenêtre d'attention voyage, le refus disparaît, tout est vert
- **09:32** — Contradiction : la fenêtre ne change RIEN en réparti — ma conclusion du round 28 était hâtive ; je vérifie le câblage
- **09:32** — Round 42 : les trois lignes manquantes — assigner la fenêtre dans le pilote et mesurer avant/après
- **09:36** — Round 42 livré : les trois lignes manquantes — le pilote applique enfin la fenêtre
- **09:39** — Round 44 : `--attn-sinks` est inerte en réparti — l'est-il aussi en LOCAL (le moteur le lit-il) ?
- **09:40** — `--attn-sinks` est inerte **des deux côtés** — je cherche s'il est lu dans le calcul
- **09:40** — Découverte : `Model.attn_sinks` est **écrit partout et lu nulle part** — le drapeau ne peut rien faire
- **09:41** — Round 44 livré : `--attn-sinks` — écrit partout, transporté par le v7, **lu nulle part**
- **09:41** — Round 45 : `--attn-sinks` ne peut rien faire — je le REFUSE explicitement (un endroit, trois chemins)
- **09:53** — Alerte méthodologique : `attn_sinks` semble LU quelque part (ligne 7472) — je vérifie avant de figer un refus fondé sur une prémisse fausse
- **09:53** — Correction en cours : `attn_sinks` EST lu (branche à fenêtre) — je retire le refus fondé sur une prémisse fausse et je mesure
- *(+11 autres étapes — voir les rapports de session)*

## Sessions actives ce jour

- `d31b3d9b` — Où en est-on (début 2026-10-08 09:11, 56.4 h) → [rapport](sessions/d31b3d9b/rapport.md) · [digest](sessions/d31b3d9b/digest.md)

## Mesures et rapports touchés

- [reports/rapport-campagne-benefices.md](../reports/rapport-campagne-benefices.md)
- [reports/rapport-fenetre-puits-attention.md](../reports/rapport-fenetre-puits-attention.md)

<!-- notes -->
` … `
<!-- /notes -->
