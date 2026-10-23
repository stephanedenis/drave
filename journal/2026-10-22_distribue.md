# 2026-10-22 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-22.md](2026-10-22.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (15)

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
| 17:33 | `7c1c2d0d` | MESURE 149 — LE CONTROLE DU CONTRASTE : avec des paires melangees, la sonde FR->EN monte quand meme a 0,505 (correct : 0,742) ; l'entrainement bilingue aligne deja en grande partie, le bon appariement ajoute +24. Le contraste correct n'est pas la cause unique | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+6) |
| 19:12 | `8dd24946` | MESURE 159 — LE TECHNIQUE A REFERENCE HUMAINE (JRC-ACQUIS) : marge +36,4 (EN->FR) et +34,9 (FR->EN), au niveau du juridique (~+35) et non du mine (+41/+46) ; la WikiMatrix gonflait par sa reference minee. La carte des registres a une reference humaine pour le technique | `en-cours.md`, `2026-10-21.md`, `2026-10-22.md` (+6) |
| 19:47 | `4aff99b9` | MESURE 164 — LE TRAIN COMPLET XNLI : 13 394 paires hors domaine, sonde 0,586 (163 : 0,592), pont 0,773 (163 : 0,751), tete 0,456/0,534. Le domaine compte plus que le volume : plus de donnees d'ailleurs n'ameliorent pas l'inference in-domain | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+6) |
| 20:17 | `a0b348e7` | MESURE 165 — LA PROSE TECHNIQUE (MULTIUN) : marge +33,2 (EN->FR) et +32,9 (FR->EN), plancher 30,4-33,0 ; plus dure que le juridico-technique (JRC +36,4/+34,9) et que le juridique (+35,3). La WikiMatrix minee (+41/+46) reste le cas du gonflement ; la carte des registres est complete | `en-cours.md`, `2026-10-21.md`, `2026-10-22.md` (+5) |

## Chiffres du jour

`13394 paires` · `0,586` · `0,592` · `0,773` · `0,751` · `0,456` · `0,534` · `0,505` · `0,742` · `5%` · `0,042` · `0,451`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Mesures et rapports touchés

- [reports/07-mesures-couche-commune.md](../reports/07-mesures-couche-commune.md)
- [reports/README.md](../reports/README.md)

<!-- notes -->

<!-- /notes -->
