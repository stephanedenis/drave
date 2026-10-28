# 2026-10-04

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-10-04/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**35 commits** · **1 session(s)** · **6 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| attention | 1 | [attention.md](attention.md) |
| docs | 21 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| modele | 5 | [modele.md](modele.md) |
| moteur | 4 | [moteur.md](moteur.md) |
| portes | 3 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` | Continue avec REPRISE.md | 2026-09-28 14:46 | 222.5 h | [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:20 | `430657fe` | K3 : la référence PORTE bien l'état — essai de discrimination, et le drapeau est au bon endroit |
| 00:23 | `5ddd1d95` | K3 : ce qui est vérifié sans supposition, et le point de méthode sur le chemin de la référence |
| 00:42 | `faba8e54` | ref_logits : REF_UBATCH, pour forcer le chemin AUTORÉGRESSIF de la référence |
| 01:33 | `ec0bdf17` | Sprint 31 : la suite — deux bugs trouvés par la comparaison, et la leçon de méthode |
| 02:30 | `34989f97` | K3 : LA COUCHE 0 PASSE — le troisième bug était l'ORDRE de remise à zéro de la banque |
| 02:31 | `fc97db55` | Docs : la couche 0 de Kimi-K3 passe, et la leçon du test qui partageait l'erreur |
| 03:17 | `416ec43e` | K3 : LES TREIZE COUCHES PASSENT, banque franchie comprise |
| 03:18 | `64131908` | REPRISE : les treize couches de K3 passent, banque comprise |
| 03:19 | `a0ebc984` | Sprint 31, fin de bloc : Kimi-K3 vérifié sur treize couches |
| 03:38 | `b26bf56b` | REPRISE : vingt-cinq couches de K3, trois banques, trois points verts |
| 03:38 | `70c62bae` | K3 : VINGT-CINQ COUCHES, TROIS BANQUES — trois des treize points sont verts |
| 03:56 | `18b123c9` | K3 : la passe complète, une couche en mémoire à la fois — les 93 couches deviennent calculables |
| 04:29 | `53da1593` | REPRISE : la passe complète de Kimi-K3 passe — 93 couches, 7,2 min/jeton |
| 04:29 | `1de57c96` | K3 : LA PASSE COMPLÈTE DE 93 COUCHES PASSE — le modèle entier, vérifié contre llama.cpp |
| 04:31 | `2698f892` | K3 : la TÊTE sur la passe complète — les logits, critère de la porte de correction |
| 05:06 | `e15dc6b3` | K3 : LES LOGITS DU MODÈLE ENTIER — top-1 identique 3/3, et c'est le bon jeton |
| 05:07 | `291469ee` | REPRISE : les logits du modèle entier, top-1 identique 3/3 |
| 05:07 | `ecb01d4f` | Sprint 31 : Kimi-K3 entier, logits vérifiés, 7,4 min/jeton |
| 05:08 | `046a04aa` | K3 : l'écart résiduel est caractérisé, pas supposé — pente nulle, 0,25 % de la dynamique |
| 05:38 | `3f55d710` | K3 : l'état récurrent survit à la libération de sa couche, et la génération gloutonne est branchée |
| 06:06 | `190f523a` | K3 : le cache MLA se RESTAURE par affectation — la génération tombait après le 1er pas |
| 06:56 | `0a96bb30` | Docs : le moteur engendre avec Kimi-K3, et un attendu mal écrit fabrique un échec qui n'existe pas |
| 06:56 | `78174074` | K3 : LE MOTEUR ENGENDRE, ET CHAQUE PAS EST CELUI DE LA RÉFÉRENCE |
| 08:22 | `71bc6e2f` | K3 : le noyau MXFP4 du moteur sur les experts — x3,6 sur le FFN, et l'échelle d'activation qui manquait |
| 08:57 | `da8ebb26` | K3 : le noyau MXFP4 est vérifié sur le modèle entier — et son gain s'effondre là où il faudrait |
| 08:59 | `1aec3455` | K3 : le mur est le disque, et le prochain chantier est nommé précisément |
| 09:00 | `896365a0` | REPRISE : le mur est le disque, prochain chantier nommé (emprunter le dense Q8_0) |
| 10:43 | `baff04a1` | Cache d'experts en VRAM pour K3 : mesuré, plafond x1,41, verdict x1,09 — non |
| 11:41 | `9aff2cd6` | K3 : le dense emprunté donne x1,12 et des logits conformes — et le cache de pages NE le garde pas |
| 18:22 | `c61cadae` | K3 : le dense emprunté s'ANNONCE, et l'arène résidente est réfutée (elle swape) |
| 23:01 | `120fab56` | docs : le roadmap — où Drave est à son meilleur, et ce qu'il faut arrêter |
| 23:07 | `8e6945bb` | K3 : le regroupement par experts dans la couche — 64 lectures deviennent 51 |
| 23:35 | `d5d0af9e` | K3 : le regroupement par experts MARCHE (64 → 48 lectures) mais ne rapporte pas de temps |
| 23:51 | `64d694f1` | REPRISE : l'état au 06/10 00h10, pour reprendre après compactage |
| 23:51 | `e7ac6f63` | K3 : la passe tournait sur UN CŒUR SUR 40 — parallélisée, et une question laissée ouverte |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
