# 2026-10-13 — Attention, fenêtre, puits

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-13.md](2026-10-13.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (8)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:12 | `6ea04a92` | Le critere de porte-indice ne survit pas a une reconstruction de son entree : 2 fenetres sur 5 passent (1,21x et 1,69x mieux que le hasard), 3 echouent (jusqu'a 2,13x pire) — le critere est marginal par construction | `etat-cerveau.md`, `references-non-regression.md`, `2026-10-13.md` (+5) |
| 03:58 | `317d3351` | La frontiere de la fenetre n'a pas de loi en N : garder la moitie des cles coute <=2 % sur TROIS textes (+0,5/+1,9/+0,8), garder le quart coute +5 a +49 % (facteur 9 selon le texte) | `etat-cerveau.md`, `2026-10-13.md`, `2026-10-13_outils.md` (+4) |
| 05:35 | `2427a44e` | Frontiere de la fenetre : SEPT textes au lieu de trois — N/2 tient partout (+0,5 a +2,1 %) et N/4 va de +2,8 a +49,2 % (facteur 17,6) | `2026-10-13.md`, `2026-10-13_portes.md`, `rapport-loi-frontiere-fenetre.md` |
| 06:06 | `f53e86c3` | Les deux facons de depenser la moitie des cles se valent : fenetre 1024 pure (+0,5 a +2,1 %) et fenetre 512 + 512 puits (+0,3 a +2,1 %) sur les sept memes textes — le partage fenetre/drain est un parametre d'implementation, pas de qualite | `2026-10-13.md`, `2026-10-13_docs.md`, `THEMES.md` (+1) |
| 06:08 | `4a15e65d` | Plan 6.7 : les deux facons de depenser la moitie des cles se valent (fenetre pure ou fenetre + puits) — le partage est un parametre d'implementation | `etat-cerveau.md`, `2026-10-13.md`, `2026-10-13_attention.md` |
| 13:43 | `d4e40d95` | porte-indice : le controle apparie est fait, et il TUE l'effet — l'indice reel tombe a 482 jetons contre 459 pour le temoin (et 315 contre 1 sur la fenetre qui passait le hasard) : ce que la porte mesurait n'est pas porte par le sens de la question | `etat-cerveau.md`, `2026-10-13.md`, `2026-10-13_modele.md` (+4) |
| 16:22 | `df58cbe2` | Fenetre d'attention : la loi moyennee — a N=4096, N/2 coute +0,9 % (etendue 1,0 pt) et N/4 +4,1 % (1,5 pt), alors qu'a N=2048 le quart allait de +2,8 a +49,2 % : meme la DISPERSION depend de N et du texte | `2026-10-13.md`, `2026-10-13_memoire.md`, `rapport-loi-frontiere-fenetre.md` (+1) |
| 16:24 | `84bc1b2a` | Journal du 13/10 : la passe a 37/39, la loi moyennee de la fenetre, et deux pieges mesures (--attn-sinks 0 qui n'est pas neutre, et mon propre pkill) | `2026-10-13.md`, `2026-10-13_attention.md`, `2026-10-13_moteur.md` (+1) |

## Chiffres du jour

`+0,9 %` · `+4,1 %` · `+49,2 %` · `482 jetons` · `+2,1 %` · `2 %` · `+49 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Mesures et rapports touchés

- [reports/rapport-loi-frontiere-fenetre.md](../reports/rapport-loi-frontiere-fenetre.md)
- [reports/rapport-niah-fragilite.md](../reports/rapport-niah-fragilite.md)

<!-- notes -->

<!-- /notes -->
