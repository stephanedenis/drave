# 2026-10-04 — Documentation, état, conventions

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (21)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:23 | `5ddd1d95` | K3 : ce qui est vérifié sans supposition, et le point de méthode sur le chemin de la référence | `verification-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 00:42 | `faba8e54` | ref_logits : REF_UBATCH, pour forcer le chemin AUTORÉGRESSIF de la référence | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 01:33 | `ec0bdf17` | Sprint 31 : la suite — deux bugs trouvés par la comparaison, et la leçon de méthode | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 02:30 | `34989f97` | K3 : LA COUCHE 0 PASSE — le troisième bug était l'ORDRE de remise à zéro de la banque | `kimi_k3.rs`, `README.md`, `MANIFEST.md` (+2) |
| 02:31 | `fc97db55` | Docs : la couche 0 de Kimi-K3 passe, et la leçon du test qui partageait l'erreur | `REPRISE.md`, `verification-kimi-k3.md`, `README.md` (+3) |
| 03:17 | `416ec43e` | K3 : LES TREIZE COUCHES PASSENT, banque franchie comprise | `verification-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 03:18 | `64131908` | REPRISE : les treize couches de K3 passent, banque comprise | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 03:19 | `a0ebc984` | Sprint 31, fin de bloc : Kimi-K3 vérifié sur treize couches | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 03:38 | `b26bf56b` | REPRISE : vingt-cinq couches de K3, trois banques, trois points verts | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 03:38 | `70c62bae` | K3 : VINGT-CINQ COUCHES, TROIS BANQUES — trois des treize points sont verts | `verification-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 04:29 | `53da1593` | REPRISE : la passe complète de Kimi-K3 passe — 93 couches, 7,2 min/jeton | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 05:07 | `ecb01d4f` | Sprint 31 : Kimi-K3 entier, logits vérifiés, 7,4 min/jeton | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 05:08 | `046a04aa` | K3 : l'écart résiduel est caractérisé, pas supposé — pente nulle, 0,25 % de la dynamique | `verification-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 05:38 | `3f55d710` | K3 : l'état récurrent survit à la libération de sa couche, et la génération gloutonne est branchée | `kimi_k3.rs`, `main.rs`, `README.md` (+3) |
| 06:06 | `190f523a` | K3 : le cache MLA se RESTAURE par affectation — la génération tombait après le 1er pas | `kimi_k3.rs`, `README.md`, `MANIFEST.md` (+2) |
| 08:59 | `1aec3455` | K3 : le mur est le disque, et le prochain chantier est nommé précisément | `verification-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 09:00 | `896365a0` | REPRISE : le mur est le disque, prochain chantier nommé (emprunter le dense Q8_0) | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 11:41 | `9aff2cd6` | K3 : le dense emprunté donne x1,12 et des logits conformes — et le cache de pages NE le garde pas | `verification-kimi-k3.md`, `kimi_k3.rs`, `README.md` (+3) |
| 23:01 | `120fab56` | docs : le roadmap — où Drave est à son meilleur, et ce qu'il faut arrêter | `roadmap-drave.md`, `README.md`, `MANIFEST.md` (+3) |
| 23:51 | `64d694f1` | REPRISE : l'état au 06/10 00h10, pour reprendre après compactage | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 23:51 | `e7ac6f63` | K3 : la passe tournait sur UN CŒUR SUR 40 — parallélisée, et une question laissée ouverte | `verification-kimi-k3.md`, `kimi_k3.rs`, `README.md` (+3) |

## Chiffres du jour

`0,25 %` · `93 couches`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)

<!-- notes -->

<!-- /notes -->
