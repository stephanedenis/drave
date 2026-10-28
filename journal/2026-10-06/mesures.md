# 2026-10-06 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (52)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:10 | `1a42f81e` | Signal précoce : plus de langues AIDENT (+23 % d'avantage), contrairement à ma mesure antérieure | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 00:22 | `06134457` | Courbe de dose complète : elle NE sature PAS — le gain marginal par langue augmente | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 00:24 | `a96b5538` | Dimensionnement de l'analyse finale, mesuré — et décision de ne PAS optimiser | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 00:51 | `99a89ecf` | Signal précoce sur le panel STRATIFIÉ : l'écart de transfert était un artefact | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 01:43 | `cf54f8b5` | Mon seuil de couche par défaut était TROP STRICT — la profondeur forcée paie | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 01:53 | `dad554e1` | Optimum du seuil de couche : 0,25, et c'est un maximum INTÉRIEUR | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 03:17 | `e85847a6` | Plateau sur 392 langues : le 'sous-ensemble partagé' s'effondre de 678 à 48 canaux | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 03:18 | `2bdae7e9` | LIVRABLE PHASE 2 : le pont sur 301 langues — fid TEST 0,7430, invariance 0,9827 | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 04:00 | `43adee16` | Le piège du droit d'exécution, trois fois — corrigé à la racine | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 04:01 | `644cf5c3` | Restriction ou pas : comparaison complète, et correction de mon invariant | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 04:18 | `00b65d41` | Le plateau du professeur est à la couche 8, pas 10 — ma cible était mal choisie | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 04:27 | `9070ecf1` | Romeo : le pont TRANSFÈRE sur du texte littéraire (0,6660 anglais -> 0,5802 français) | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 04:38 | `e89dbe3e` | Couche 8 contre couche 10 : la correction de cible PAIE (+0,0213 sur le transfert) | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 04:42 | `6b4a75ef` | Audit de cohérence : deux affirmations périmées pointées dans mes propres rapports | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 04:43 | `75d590a6` | Audit (suite) : le TITRE du rapport génératif promettait ce que son corps réfute | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 04:44 | `47152fd7` | Audit (fin) : les deux mêmes incohérences étaient dans recapitulatif.md | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 05:11 | `0ccef36c` | PIÈGE : l'invariance sur Wikipedia ne veut rien dire (segments non appariés) | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 05:15 | `4e12ea69` | CORRECTION : la 'richesse' n'est PAS dans le nombre de canaux actifs | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 07:36 | `e8ae5a28` | Domaine ou langue ? testé — et l'expérience est INCOMPLÈTE, je le signale | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 07:39 | `b7fcce9a` | Signal précoce : la couche 8 gagne aussi au niveau des UNITÉS (+0,0381) | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 07:41 | `0b91cb0c` | La pire paire (dzo) : hypothèse de longueur testée et RÉFUTÉE | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 07:44 | `37429ed9` | Les langues éloignées partagent une NORME plus grande, pas une densité différente | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 08:12 | `338d1948` | Le pont ne sert pas toutes les langues également — et la fidélité EST le témoin constant | `README.md`, `MANIFEST.md`, `digest.md` (+4) |
| 08:55 | `e036749c` | Le réservoir ne sert presque à rien : l'entrée SEULE fait mieux, sans un neurone | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 09:20 | `b2e5631f` | Couche 8 contre couche 10 au niveau des unités : +0,0495 de fidélité | `README.md`, `MANIFEST.md`, `digest.md` (+6) |
| 09:28 | `b15a6048` | Contrôle de capacité : l'entrée gagne par nature, sans que ce soit tranché | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:41 | `4de5b2f1` | Le §29 n'est PAS un artefact d'alignement — mesuré, et Wikipedia transfère mieux | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 10:30 | `c36bb6bb` | Introspection du bloc : trois erreurs, dont un chiffre de tête qui ne disait pas ce qu'il semblait | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 10:40 | `c660fde3` | Correction du §29 : le réservoir n'était pas inutile, il était TROP PETIT | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 12:17 | `d15c870f` | La courbe ne plafonne pas (800 neurones → 0,6821) et baisser le gain est RÉFUTÉ | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 13:18 | `ce3b05d1` | Jalon : 392 langues tracées aux couches 8 ET 10, zéro échec | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 13:39 | `f30b14b9` | Croissance vectorisée sur les langues : 28 s → 1,76 s par neurone, identité bit à bit | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 13:48 | `817ca1bb` | Couche 8 contre couche 10 à 392 langues : 41 sur 41 s'améliorent, ZÉRO régresse | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 15:27 | `6b1cad40` | Deuxième œuvre parallèle (Crime et Châtiment, en-es) et généralisation du test domaine/langue | `README.md`, `MANIFEST.md`, `digest.md` (+5) |
| 15:50 | `f6d40c8b` | Fidélité et invariance tirent en sens opposé quand le réseau grandit | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 16:11 | `5ad2f09e` | Ajuster la lecture SOUS CONTRAINTE d'invariance : +0,042 d'invariance pour 0,008 de fidélité | `README.md`, `MANIFEST.md`, `digest.md` (+4) |
| 16:41 | `a3abff2d` | Croissance + attrition à 392 langues : 182 neurones, TEST 0,6340, invariance 0,8659 | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 16:46 | `d355fec2` | La contrainte d'invariance déplace la courbe, elle ne supprime pas la tension | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 17:16 | `61248ebc` | La contrainte d'invariance fonctionne DANS la croissance, à 16-20 pour 1 | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 18:13 | `75cc1b7e` | Domaine ou langue : enfin testable, et la réponse est 'à égalité' | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 18:22 | `8be5966e` | Le garde-fou du §30 a attrapé une SECONDE occurrence du même bug | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 19:45 | `83cd4256` | LA question du §41 est tranchée : notre sortie ÉCRASE la distinction contenu/langue | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 20:05 | `c3de2df4` | Réécrire l'objectif : la structure du professeur EST atteignable, mais l'objectif à deux curseurs est NON CONVEXE | `README.md`, `MANIFEST.md`, `digest.md` (+4) |
| 20:26 | `603b7a69` | La piste 'le moindres carrés néglige les petites composantes' est RÉFUTÉE par sa prémisse | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 20:47 | `a41a27b7` | Le rétrécissement est réel (3,4x) mais n'est pas la cause ; et la cible du §58 n'est pas stable | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 21:29 | `120d50c5` | Le remède est trouvé mais n'est pas déployable — et un piège de méthode | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 21:41 | `7414653c` | Cinquième remède écarté : le sous-espace du contenu appris ne se TRANSFÈRE pas | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 21:52 | `33d40182` | Le centrage de l'entrée : premier levier de la série à la fois efficace ET déployable | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 22:45 | `09291d7c` | Deux leviers DÉPLOYABLES qui se combinent : le rapport passe de 1,46 à 3,06 | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 23:38 | `3b50b1ac` | Le discriminant fonctionne : rapport 6,96 (64 % de la cible) — et la frontière est tracée | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 23:50 | `97fc5ea1` | OÙ ENTRE LA LANGUE : dans l'entrée, pas dans le réservoir — et le réservoir l'AMPLIFIE | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 23:51 | `f9186a3c` | Glossaire : §10.10, le vocabulaire de la mesure contenu/langue | `glossaire.md`, `README.md`, `MANIFEST.md` (+2) |

## Chiffres du jour

`64 %` · `0,6340` · `0,8659` · `0,042` · `0,008` · `41 s` · `28 s` · `1,76 s` · `0,6821` · `0,0495` · `0,0381` · `0,0213`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)

## Mesures et rapports touchés

- [reports/rapport-plateau-semantique.md](../../reports/rapport-plateau-semantique.md)
- [reports/rapport-pont-generatif.md](../../reports/rapport-pont-generatif.md)
- [reports/rapport-toutes-langues.md](../../reports/rapport-toutes-langues.md)
- [reports/recapitulatif.md](../../reports/recapitulatif.md)

<!-- notes -->

<!-- /notes -->
