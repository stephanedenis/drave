# 2026-10-30

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-10-30/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**21 commits** · **0 session(s)** · **7 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 1 | [distribue.md](distribue.md) |
| docs | 5 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 6 | [mesures.md](mesures.md) |
| modele | 3 | [modele.md](modele.md) |
| moteur | 1 | [moteur.md](moteur.md) |
| portes | 4 | [portes.md](portes.md) |

## Sessions DSH

Aucune session indexée pour ce jour ; voir
[l'index des sessions](../README.md#sessions).

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:04 | `da038e34` | R13.2 + A8.0 — VOCAB 1024 PERD 3,9 % À OCTETS ÉGAUX ; PORTE-INDICE ROUGE QUALIFIÉE |
| 00:06 | `336a2271` | ÉTAT — DATE ALIGNÉE SUR LE COMMIT DU 30 |
| 08:34 | `733232ff` | R06 v5 — LA CALIBRATION COÛTE ~50 GOLDS, LES POIDS APPRIS N'AJOUTENT RIEN, LE PILOTE EST COMPLÉTÉ |
| 08:41 | `720d7e7d` | N3.5f — POSITION VÉRIFIÉE PAS À PAS, DÉSYNC REFUSÉE (CODE 4) ; PORTE 76 |
| 08:42 | `2640e017` | B10 — L'OBJECTIF MOT LÈVE LE DÉCODEUR (32,5, PLANCHER 33,7) MAIS LE `z` NE PORTE QUE 2,6 POINTS |
| 08:53 | `c766ef93` | R13.3 — ANGLAIS 100 MO : LE BPE PERD 4,2/6,6 % À OCTETS ÉGAUX |
| 08:58 | `daabf6be` | A8.0 — 19/33 : PORTE-PANNES ÉPINGLÉE À 33,0156 ; AUDIT FINAL DES 14 RESTANTES |
| 09:03 | `e3747c3f` | B10 — LE DÉCODEUR MOT BAT LE PLANCHER SUR JW (26,7 CONTRE 17,1), MAIS LE `z` NE PORTE QUE 1,9 POINT |
| 09:16 | `ecb67fe9` | B10 — LE CONTRASTIF NE FAIT PAS LIRE `z` : 32,6 DE CHRF (INCHANGÉ), ÉCART `z` 1,45 CONTRE 2,57 |
| 10:04 | `8664cc67` | SCHÉMA — ÉTAT AU 30/10 09 h 25 : A8.0 19 PORTES, B10.2BIS CLOSE, R13 |
| 10:34 | `43a46d7e` | DOCWATCH — L'ÉTAT EN WBS INLINE, LE GANTT DANS LA ROADMAP, LE SVG SUPPRIMÉ |
| 10:46 | `f9132a68` | N3.6 — PONT, PLACEMENT ET SEUIL COMPOSENT DANS LE SERVICE |
| 11:08 | `da725e8a` | SESSIONS — LE PLAN AVANT L'ÉTAT : LINTER, MODÈLE, PORTE 78 |
| 12:58 | `b19ab8b7` | LA CASCADE À CONFIANCE EST PUBLIÉE : DEUX FICHIERS DATÉS, UN SEUIL REPRODUCTIBLE, 0,894 OUT-OF-SAMPLE |
| 13:00 | `10a05c30` | SESSIONS — MIGRATION DOUCE : 3 PLANS À CONFIRMER, STRICT ROUGE, EN-COURS RECALÉ |
| 13:02 | `ac60b79a` | ÉTAT — WBS 13:00, B11.10 4/4 |
| 13:06 | `277103ff` | A8.3d — LE LOT N'EST PAS LES THREADS : L'ÉCART DE 1,90 % SURVIT À 1 THREAD |
| 13:19 | `68590bf0` | LE GRAPHE CONFRONTE L'INDEX, L'ÉTAT POINTE LA FRONTIÈRE — SIX STATUTS DIVERGENTS CORRIGÉS |
| 13:25 | `842e1770` | SESSIONS — LES TROIS PLANS CONFIRMÉS : PÉRIMÈTRES, FICHIERS, HEARTBEAT 13:05 |
| 13:30 | `21a361f9` | R13.4 — DEUX GRAINES : BPE512 DANS LE BRUIT, BPE1024 PERD 4,09 % |
| 13:32 | `b33b56ab` | LA CARTE DE DÉCISION DES CHANTIERS — LA PROFONDEUR DE DÉPENDANCE COMME AXE, LES SOURCES NOMMÉES |

## Le récit de la journée (écrit à la main)

<!-- notes -->
**Session `8156fdcb` — le coût de la calibration, et le pilote complété.**

La cascade à confiance calibrée (R06 v4) égalait l'oracle, mais elle exige des golds. Combien ?
La courbe le dit : **~50 questions** suffisent sur le lexical (0,906 à k=49, contre 0,911 au
maximum), **~25** sur les paraphrases (0,399 à k=25, contre 0,415). Le plateau est atteint tôt —
la calibration est bon marché.

Et les **poids appris** ne valent pas mieux que les poids fixés : identiques sur le lexical,
**pires** sur les paraphrases (0,366 contre 0,415) — une logistique sur 25 à 42 exemples
sur-apprend. Les poids fixés (0,5 couverture + 0,3 accord + 0,2 dispersion) restent.

Le **pilote** est complété : le modèle y donne 0,400 contre 0,600 pour l'extractif — le pilote
est un corpus mixte du côté lexical, cohérent avec la loi « le corpus décide du lecteur ».

La recette de déploiement du programme R est complète : 50 golds → le seuil → la cascade à
confiance, à ~1 point de l'oracle, 12 % d'appels modèle sur un corpus lexical, 85 % sur un
corpus de paraphrases.

**La politique est publiée.** La cascade à confiance n'était qu'un réglage de séance (un seuil
tapé sur la ligne de commande). Elle devient une **politique** : `tools/calibrer.py` transforme
un banc en fichier daté (banc, empreinte du corpus gelé, n, seuil, taux), `lecture.py --cascade
--calibration` le lit, et `--verifie` recalcule le seuil à l'identique. Sur un découpage
indépendant, la cascade égale encore l'oracle sur le lexical (0,894) et bat les deux choix fixes
sur les paraphrases (0,366 contre 0,341 et 0,317).

**Le graphe ne ment plus par omission.** Le backlog s'écrit deux fois (la fiche, puis l'index) :
six statuts avaient divergé — R05 et R06 annoncées « spécifiées » alors qu'elles ont cinq
versions mesurées, A8.3 absente de l'index. `verifie_backlog.py` confronte désormais les deux,
et l'état ne recopie plus les statuts : il pointe la **frontière** du graphe et ne garde que les
**bloquants externes** — la seule chose que le graphe ne peut pas dire.

**La carte de décision, et l'arrimage des écrans.** Trois vues avaient échoué à aider la
décision : le WBS d'états (ni dépendances ni sources), le Gantt (étalé en jours alors qu'on
décide par périodes courtes), le graphe d'items (37 nœuds, dense). La nouvelle carte place les
quatre chantiers en couloirs et la **profondeur de dépendance** en axe vertical — jamais le
temps : en haut, la frontière (11 items, encadrés en vert) ; en dessous, ce qu'elle débloque ;
en bas, les **sources de blocage** nommées (Colab, FPGA, VRAM, corpus). Elle se régénère par
`tools/carte_decisions.py`.

Et une convention pour l'humain : le **premier item** de la liste de tâches d'un écran TUI porte
`Session <id> — <rôle>`, le même id que le titre du bloc d'`en-cours` et que le champ `Session`
du plan. Trois supports, une identité — écrite dans `continuite.md` § 4.
<!-- /notes -->
