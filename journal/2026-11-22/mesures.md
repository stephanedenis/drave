# 2026-11-22 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (8)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:16 | `06bf2cc2` | 100 M — LA LEÇON OPÉRATIONNELLE : LE CHECKPOINT UTILE EST CELUI DE 3 000 PAS (0,882), LE 30 K SERT DE CONTRÔLE NÉGATIF ; LA PRÉDICTION POUR LA DONNÉE 10× EST ÉCRITE D'AVANCE (MOTS > 0,90, RÉPÉTITION ≤ 5, PPL < 2,0) | `en-cours.md`, `README.md`, `memoire.md` (+5) |
| 01:23 | `3590e78b` | BANC 612 — LE 100 M (3 000 PAS) SUR LES 602 PHRASES DU GOLD GELÉ : 0,755 DE MOTS VALIDES, RÉPÉTITION 3, ZÉRO NON-UTF-8, 127,5 OCTETS/S ; LE BANC DE STYLE (0,882) EST PLUS FACILE QUE LE GOLD — LA COMPARAISON DES TROIS CHECKPOINTS EST LE PROCHAIN PAS | `en-cours.md`, `README.md`, `memoire.md` (+10) |
| 01:28 | `deedbb18` | BANC 612 — LE TÉMOIN 30 K : 0,763 CONTRE 0,755 AU 3 K SUR LES PHRASES RÉELLES (LA CONTINUITÉ), MAIS 29 SORTIES NON-UTF-8 CONTRE 0 (LA DÉRIVE) ; LE BANC DE STYLE (0,501 CONTRE 0,882) MESURE LA CRÉATIVITÉ — DEUX MESURES, DEUX VÉRITÉS | `en-cours.md`, `README.md`, `memoire.md` (+8) |
| 02:06 | `bbddfefa` | DIAGNOSTIC 16/11 RELU — LA NUIT LE CONFIRME ET LE CHIFFRE : LE 100 M SUR 1 GO PLAFONNE À 0,76 (LA BORNE VALIDE « 100-150 M SUR 3-6 GO »), « MOTS VALIDES » EST FAIBLE (LE HASARD FAIT 0,711), LA PRIORITÉ EST LA DONNÉE, PAS LA TAILLE | `en-cours.md`, `README.md`, `modele.md` (+6) |
| 02:11 | `2146d526` | CORPUS — L'INVENTAIRE : 137 GO DANS DATA/, ET LE PALIER 1 (3,44 GO, CORPUS_WIKI_FR_PALIER1) EXISTE DÉJÀ ; LE VERROU N'EST PAS LA DONNÉE, C'EST LE NETTOYAGE (DÉDUP, LICENCE, RECETTE) — LA PRÉDICTION POUR LE RUN SUR 3,44 GO EST ÉCRITE D'AVANCE | `en-cours.md`, `README.md`, `distribue.md` (+10) |
| 02:20 | `96ef8dbc` | PALIER 1 — LE RUN DU 100 M SUR LES 3,44 GO EST LANCÉ (ETA 04 H 40) : 27 TOKENS/PARAMÈTRE AU LIEU DE 30, L'HYPOTHÈSE ÉCRITE D'AVANCE (MOTS > 0,85, RÉPÉTITION ≤ 5, NON-UTF-8 ≈ 0, PPL < 2,5) ET LES TROIS RAISONS DE POUVOIR LA RENDRE FAUSSE | `en-cours.md`, `README.md`, `distribue.md` (+9) |
| 04:46 | `5b1b9fe0` | PALIER 1 FRANCHI — LE 100 M SUR 3,44 Go DONNE 0,854 DE MOTS VALIDES SUR LE GOLD 612 : LE MEILLEUR RÉSULTAT DU NATIF (LE 1 Go : 0,755 ; LE 30 k : 0,763) ; 3 HYPOTHÈSES SUR 4 TIENNENT (RÉPÉTITION 2, NON-UTF-8 13 CONTRE 29, MOTS > 0,85), LA PPL MANQUE (3,073 CONTRE < 2,5) — LE CORPUS EST PLUS DUR, PAS COMPARABLE | `en-cours.md`, `README.md`, `distribue.md` (+10) |
| 04:49 | `ab8ef491` | SYNTHÈSE — LE PALIER 1 EST FRANCHI : LE 100 M SUR 3,44 Go DONNE 0,854 (LE MEILLEUR DU NATIF), RÉPÉTITION 2, 13 NON-UTF-8 CONTRE 29 ; LA DONNÉE ÉTAIT LE VERROU, COMME PRÉVU — LA PPL (3,073) N'EST PAS COMPARABLE (CORPUS PLUS DUR) | `en-cours.md`, `README.md`, `distribue.md` (+10) |

## Chiffres du jour

`3,44 Go` · `0,854` · `3,073` · `1 Go` · `0,755` · `0,763` · `0,711` · `0,501` · `0,882`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 516.3 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)

## Mesures et rapports touchés

- [reports/rapport-100m-30k.md](../../reports/rapport-100m-30k.md)
- [reports/rapport-100m-palier1.md](../../reports/rapport-100m-palier1.md)
- [reports/rapport-banc-612.md](../../reports/rapport-banc-612.md)
- [reports/rapport-corpus-disponibles.md](../../reports/rapport-corpus-disponibles.md)
- [reports/rapport-natif-exploitable.md](../../reports/rapport-natif-exploitable.md)
- [reports/rapport-nuit-21-22.md](../../reports/rapport-nuit-21-22.md)

<!-- notes -->

<!-- /notes -->
