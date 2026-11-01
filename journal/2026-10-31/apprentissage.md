# 2026-10-31 — Règles locales, hebbien, modulateurs, distillation

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (1)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 16:38 | `660c479c` | N2 — LA HIÉRARCHIE NE PAIE PAS SUR LA DISTILLATION NON PLUS (2,9935 CONTRE 2,9927, TROIS GRAINES) | `en-cours.md`, `README.md`, `distribue.md` (+4) |

## Chiffres du jour

`2,9935` · `2,9927`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — Continue session work (début 2026-10-31 17:17, 5.4 h) → [rapport](../sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md) · [digest](../sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md)
- `0f3b6070-57ce-4642-b9ec-3b3956f75978` — Regarde l'image /tmp/qa/check1.png avec (début 2026-10-31 18:02, 0.0 h) → [rapport](../sessions/0f3b6070-57ce-4642-b9ec-3b3956f75978/rapport.md) · [digest](../sessions/0f3b6070-57ce-4642-b9ec-3b3956f75978/digest.md)
- `163d631a-6528-4324-b7b3-6487d24feeb5` — — (début 2026-10-31 17:39, 0.0 h) → [rapport](../sessions/163d631a-6528-4324-b7b3-6487d24feeb5/rapport.md) · [digest](../sessions/163d631a-6528-4324-b7b3-6487d24feeb5/digest.md)
- `22e518ee-81b8-4081-ae1b-f0d7a777a1d7` — Compléter les autres sessions avant le backlog (début 2026-10-31 11:13, 0.2 h) → [rapport](../sessions/22e518ee-81b8-4081-ae1b-f0d7a777a1d7/rapport.md) · [digest](../sessions/22e518ee-81b8-4081-ae1b-f0d7a777a1d7/digest.md)
- `bc3c0b97-cae0-4773-921d-ef27c8285461` — Cohérence de la documentation et recommandations (début 2026-10-27 08:56, 104.7 h) → [rapport](../sessions/bc3c0b97-cae0-4773-921d-ef27c8285461/rapport.md) · [digest](../sessions/bc3c0b97-cae0-4773-921d-ef27c8285461/digest.md)
- `df1b1098-d54e-4763-bfc2-2a8cc1498cec` — Tu es relecteur visuel de (début 2026-10-31 17:52, 0.0 h) → [rapport](../sessions/df1b1098-d54e-4763-bfc2-2a8cc1498cec/rapport.md) · [digest](../sessions/df1b1098-d54e-4763-bfc2-2a8cc1498cec/digest.md)
- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 5.0 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)
- `fe3c05f0-834b-44f2-8739-501865d652c1` — Lecture de en-cours.md et choix de tâche (début 2026-10-31 17:35, 5.1 h) → [rapport](../sessions/fe3c05f0-834b-44f2-8739-501865d652c1/rapport.md) · [digest](../sessions/fe3c05f0-834b-44f2-8739-501865d652c1/digest.md)

## Mesures et rapports touchés

- [reports/rapport-n2-distillation.md](../../reports/rapport-n2-distillation.md)

<!-- notes -->
### N2 — le budget, les quatre sources, et le mètre faussé

La journée avait commencé par deux négatifs nets sur la hiérarchie. En reprenant N2 l'après-midi,
la question était simple : le dispositif reconstruit hier n'avait vu que **20,48 Mo** d'un seul
corpus en **5 000 pas** — que donne-t-il à budget plein, **41 Mo, 20 000 pas**, et à quatre
sources ?

Douze distillations, trois graines, deux cartes. Le budget paie : **2,8527** contre **2,9355**
(−0,0828), du même ordre que la chaîne historique. Les quatre sources coûtent : **3,7591** sur le
protocole (+0,91) et **3,4350** à quotas égaux (+0,58) — l'anglais du manifeste (82,5 %) explique
la moitié de la perte, pas toute. Le curriculum 129 gagne **0,0416** à 129 et **0,0056** à 128 :
réel, marginal.

Puis un chiffre n'a pas collé. Pendant l'entraînement, l'évaluation rapide affichait **2,39** ; à
la fin, sur 128 fenêtres, **2,86**. Un demi-point, ce n'est pas du bruit. Les huit premières
fenêtres — celles du compteur 0, d'où part le protocole — donnaient **2,42**, et la toute première
**1,16**. Trop beau. L'enquête a trouvé la cause : **la validation n'est pas tenue à l'écart**.
`corpus_fr_val.txt` est la queue de `corpus_fr.txt`, sa tête est l'entraînement — et le corpus
empile des documents qui se recopient : **32,8 %** des fenêtres du protocole sont **verbatim**
dans l'entraînement (42 sur 128), **23,5 %** des fenêtres d'entraînement y apparaissent plus d'une
fois.

Ce qui change tout : **2,7078 et 2,6998 sont mesurés sur ce même jeu**. Sur fenêtres propres, le
meilleur élève est à **2,9795** (la base à 3,2450, le témoin de 5 000 pas à 3,0534). La porte
< 2,5 n'a jamais été une mesure de généralisation, et le prochain levier de N2 n'est pas un
réglage d'entraînement : c'est le corpus — dédupliquer, séparer par document, puis remesurer.
<!-- /notes -->
