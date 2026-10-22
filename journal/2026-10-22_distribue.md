# 2026-10-22 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-22.md](2026-10-22.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (11)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 08:33 | `298cbccb` | MESURE 124 — CONTRE DES CIBLES FIGEES, LE PLAN TRANSFERE : 0,324 / 0,273 / 0,216 en moyenne de deux graines (hasard 0,125 ; avant 0,205 / 0,216 / 0,165), meme signe aux deux decoupages ; seul h1 est solide (z ~ 2,0), h2/h3 dans le bruit de 88 items. Le probleme des mesures 120-123 etait l'objectif (cibles mouvantes), pas l'information | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+8) |
| 10:38 | `b2973375` | MESURE 126 — UN PONT LINEAIRE REND LE RAISONNEMENT INDEPENDANT DE LA LANGUE : 2000 chaines appariees FR/EN, pont ridge EN->FR ; la sonde FR lit l'etat EN ponte a 1,00/0,91/0,68/0,52/0,46 (2 a 6 entites) contre 0,04-0,08 sans pont, controle a paires melangees au hasard. La geometrie est alignable par une petite structure : la tete bien faite = un etat qui compose + un pont qui le rend commun | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+8) |
| 10:41 | `71b610a3` | MESURE 127 — LE PONT EST STRUCTUREL, PAS LEXICAL : la relation taille donne 1,00/0,85/0,67/0,56/0,44, superposable a l'ordre (1,00/0,91/0,68/0,52/0,46) ; controle a paires melangees au hasard. Un meme pont sert deux relations : l'alignement est structurel, pas lexical | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+6) |
| 10:44 | `6d12827a` | MESURE 128 — LE PONT N'EST PAS PROPRE A UNE LANGUE : FR/ES donne 1,00/0,92/0,72/0,56/0,50, superposable a FR/EN (1,00/0,91/0,68/0,52/0,46) ; controle a paires melangees au hasard. Le pont est une petite structure portable, calculee par paire de langues | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+7) |
| 10:47 | `61ae843a` | MESURE 129 — LE PONT NON LINEAIRE ECHOUE : un MLP EN->FR ne depasse pas le hasard (0,04-0,17) contre 0,46-1,00 pour le pont lineaire ; controle au hasard. Avec ~250 paires par longueur, la capacite non lineaire sur-apprend : l'alignement est une petite structure lineaire, pas un reseau | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+6) |
| 10:52 | `d8d1a681` | MESURE 131 — LE PONT EST LANGUE-GENERAL (4 LANGUES) : FR/DE donne 1,00/0,94/0,74/0,65/0,52, comme FR/EN et FR/ES ; controle a paires melangees au hasard. L'alignement tient sur quatre langues indo-europeennes, dont une a ordre des mots different | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+6) |
| 11:10 | `2ac0c08a` | MESURE 136 — LE PONT MULTI-TACHES N'ALIGNE TOUJOURS PAS LE PLAN : 0,136 (hasard 0,125) malgre les paires de plan dans l'entrainement ; sans pont 0,250. Ajouter des paires de plan ne suffit pas : il faut aligner les cibles, ou entrainer le plan dans le modele | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+6) |
| 16:39 | `f36d4c3a` | MESURE 143 — LE REGISTRE PARLE (TED2020) : marge +39,8 (EN->FR) et +40,7 (FR->EN) au 7 B, +37,7/+38,3 au 3 B, plancher 23,7-25,1. Le parle prepare passe au-dessus de la presse (+38,6) ; seul le dialogue spontane reste a couvrir | `en-cours.md`, `2026-10-21.md`, `2026-10-22.md` (+7) |
| 16:45 | `52cf7041` | MESURE 144 — L'ENTRAINEMENT MULTILINGUE N'ALIGNE PAS NON PLUS : sonde FR->EN 0,042 (hasard 5%), pont 0,451 contre 0,810 fige ; la supervision de la tache, meme bilingue, n'apprend pas l'alignement. Il faut un objectif contrastif entre paires FR/EN | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+5) |
| 17:00 | `3ecb5f11` | MESURE 145 — LE REGISTRE TECHNIQUE (WIKIMATRIX MINE) : marge +41,0 (EN->FR) et +46,0 (FR->EN) au 7 B, plancher 32,1/34,2 ; les plus hautes des cinq registres, mais la reference est minee (plancher haut, chrF possiblement gonfle). La carte couvre juridique, presse, litteraire, parle prepare et technique | `en-cours.md`, `2026-10-21.md`, `2026-10-22.md` (+7) |
| 17:26 | `2d10c895` | MESURE 148 — LE DIALOGUE SPONTANE (OPENSUBTITLES) : marge +32,3 (EN->FR) et +33,6 (FR->EN) au 7 B, plancher 17,2 (le plus bas) ; le dialogue est le plus dur apres le litteraire. La carte des six registres est complete | `en-cours.md`, `2026-10-21.md`, `2026-10-22.md` (+7) |

## Chiffres du jour

`5%` · `0,042` · `0,451` · `0,810` · `0,136` · `0,125` · `0,250` · `250 paires` · `0,324` · `0,273` · `0,216` · `0,205`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Mesures et rapports touchés

- [reports/07-mesures-couche-commune.md](../reports/07-mesures-couche-commune.md)
- [reports/README.md](../reports/README.md)

<!-- notes -->

<!-- /notes -->
