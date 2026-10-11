# 2026-10-11 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-11.md](2026-10-11.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (7)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 03:57 | `0ab6789b` | M9 livre dans le registre des manques, et 33 portes dans l'etat | `etat-cerveau.md`, `manques.md`, `2026-10-11.md` (+5) |
| 04:41 | `bfbc26fc` | Le noyau creux couvre maintenant TOUT le modele : divise par 3,8 les paires, et 36 % plus LENT | `main.rs`, `model.rs`, `2026-10-11.md` (+14) |
| 04:42 | `b9772404` | Fiche B : le noyau creux couvre les experts (divise par 3,8 les paires) et reste 36 % plus lent — le prochain pas est un noyau, pas un modele | `2026-10-11.md`, `2026-10-11_distribue.md`, `README.md` (+5) |
| 04:57 | `2fa0105a` | Dessin B : le noyau creux ne rattrape le dense qu'a 10 % de poids gardes — un regime ou le modele est detruit (x41 000). A 25 %, deux fois plus lent malgre divise par 3,8 de paires | `etat-cerveau.md`, `2026-10-11.md`, `2026-10-11_apprentissage.md` (+14) |
| 04:59 | `c5cd3f93` | Registre : M9 livre en entier, et le fait desagreable ecrit (le noyau creux ne paie qu'a 10 %, ou le modele est mort) | `manques.md`, `2026-10-11.md`, `2026-10-11_moteur.md` (+4) |
| 05:01 | `d7dada51` | Roadmap : le dessin B porte son etat mesure (le noyau existe, il paie les paires, et il ne paie le temps qu'a 10 %) | `modele-pour-drave.md`, `2026-10-11.md`, `2026-10-11_distribue.md` (+7) |
| 08:11 | `22d9919c` | Reprise : les portes regenerent leurs prerequis de /tmp (tools/_corpus.sh, modele de porte-reparti-moteur) — une seule exception, qui refuse en le disant | `REPRISE.md`, `2026-10-11.md`, `2026-10-11_apprentissage.md` (+32) |

## Chiffres du jour

`10 %` · `25 %` · `36 %` · `÷3,8` · `3,8 paires` · `−36 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Étapes du jour (18)

*Ce que l'agent a consigné en le faisant (lignes `⏵` du journal de session) :*

- **00:20** — Défaut de protocole trouvé : le « meilleur point » annule l'élagage — correction
- **00:20** — Correction du protocole et relance des deux seules mesures faussées
- **00:27** — Commit du croisement E6, de l'instrument d'occupation et des deux corrections de protocole
- **01:28** — Un protocole court suffit-il pour voir l'effet Dale ? (essai à 600 pas)
- **01:30** — Porte de la recette « signes figés » (protocole court, seuil explicite)
- **02:59** — Audit systématique : chaque drapeau du harnais laisse-t-il dans le fichier la trace qu'il annonce ?
- **03:44** — Volet coût d'E1 : ce que 4× moins de poids achètent (estimation sur les paires)
- **03:46** — M9, seconde moitié : rendre la ligne « paires » sensible à l'occupation (inventaire du moteur)
- **03:47** — Agrégation de l'occupation et affichage dans la ligne des paires
- **03:49** — Ligne d'occupation ajoutée au récapitulatif des paires
- **03:52** — Non-régression : `porte-flux` et `porte-budget` (qui lisent la ligne des paires)
- **04:08** — Essai : le noyau creux donne-t-il la même perplexité, et moins de paires ?
- **04:08** — Les experts (1,8 M des 2,3 M de paires) passent par `Vue4` — lecture du chemin pour les rendre creux
- **04:26** — Round 56 : la pièce manquante du dessin B est écrite — exacte, payante en paires, plus lente en temps
- **04:34** — Le noyau creux couvre maintenant TOUT le modèle (÷3,8 paires) — mesure de la vitesse
- **04:41** — Commit : le noyau creux couvre maintenant les experts (÷3,8 paires, −36 % de vitesse)
- **04:43** — Round 57 : le noyau creux couvre tout le modèle — ÷3,8 paires, et 36 % plus lent
- **08:11** — Message actionnable pour la seule porte dont le modèle ne se régénère pas seule

## Sessions actives ce jour

- `d31b3d9b` — Où en est-on (début 2026-10-08 09:11, 71.0 h) → [rapport](sessions/d31b3d9b/rapport.md) · [digest](sessions/d31b3d9b/digest.md)

## Mesures et rapports touchés

- [reports/rapport-dessin-B-poids-creux.md](../reports/rapport-dessin-B-poids-creux.md)

<!-- notes -->

<!-- /notes -->
