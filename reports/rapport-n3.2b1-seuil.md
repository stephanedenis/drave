# N3.2b1 — le service décide par seuil de confiance

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ✅ **N3.2b1 tenu** — le
> service calcule le chemin court (profondeur 1) **et** le chemin plein, et garde le jeton court
> si sa confiance atteint `seuil=`. Les compteurs le prouvent : **12/0**, **0/12**, **11/1**
> selon le seuil. Ce n’est **pas** encore un saut de calcul : les deux chemins sont calculés ;
> c’est la **décision**. N3.2b2 (cache continu) reste.
>
> **Dispositif** : `tools/porte-n3-seuil.sh`, petit `drave-n0` synthétique (graine 7,
> 132 528 paramètres, 2 blocs), service `--drvm-serve` ; données
> [`n3.2b1-seuil.json`](n3.2b1-seuil.json).

## Ce qui est mesuré

| seuil | choix anticipés | choix pleins | texte |
|---:|---:|---:|---|
| **0** | **12** | **0** | celui du chemin court |
| **1** | **0** | **12** | celui du chemin plein |
| **0,01** | **11** | **1** | mixte, **déterministe** |

Les textes des seuils 0 et 1 sont **différents** ; le 0,01 est stable sur deux appels.

## Le contrôle négatif

- **Seuil 0** : tout court — la borne basse.
- **Seuil 1** : tout plein — la borne haute.
- **0,01** : 11/1 — le seuil **sépare** les jetons, il ne bascule pas tout.
- **Deux appels à 0,01** : identiques — la décision n’est pas un tirage.

## Ce qui pourrait le rendre faux

- **Aucun saut de calcul** : le court et le plein sont calculés ; le service ne gagne pas de temps.
- **Seuil calibré** sur ce petit modèle : 0,01 peut ne pas transférer.
- **Un prompt**, une graine.
- **La confiance est la softmax max** ; elle n’est pas calibrée en probabilité.

## Ce que ça change

N3.2b1 est **fait** : la décision à seuil est branchée et comptée. N3.2b2 (cache continu pour
sauter réellement le calcul) et la composition avec pont/placement restent.

## Fichiers

- `drave-core/src/native.rs` — `generer_seuil`, `pas_profondeur`, service `seuil=`.
- `tools/porte-n3-seuil.sh` — la porte.
- `reports/n3.2b1-seuil.json` — les mesures.
- `reports/rapport-n3.2b1-seuil.md` — cette fiche.
