# 2026-10-24 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-24.md](2026-10-24.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (10)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 08:13 | `3c9665f1` | A1.5 — LA DECISION PAR COUCHE : la table (densites 20,1 a 56,3 %, croisement 22 %) et la verification — PPL identique (28,4015) entre le push et le dense, le dense 2 % plus rapide (9,2 contre 9,4 s a 255 jetons) ; la table predit le dense pour 23 couches sur 24, la mesure suit. Correction du « ~10 % » perime dans l'analyse du flux | `en-cours.md`, `roadmap.md`, `2026-10-22_moteur.md` (+5) |
| 08:43 | `7a956534` | B1.6 — LE CORPUS DIALOGUE TROUVE : DiaBLa (Bawden et al. 2021), 144 dialogues spontanes FR/EN, 4 910 paires avec les post-editions humaines ; extraction tools/corpus_diabla.py ; la mesure au 7 B est en file (GPU occupe par le 32 B). B1.5 (la prose scientifique) : la recherche ne trouve que des comparables, la ligne reste bloquee et nommee | `roadmap.md`, `2026-10-22_moteur.md`, `2026-10-24.md` (+4) |
| 08:46 | `fcabe8e9` | B2.8 — LE CORPUS NATUREL PLUS DUR TROUVE : DACCORD (1 034 paires FR de contradictions), RTE3-FR (2 x 800) et GQNLI-FR (300), plus durs que XNLI (Skandalis et al., LREC-COLING 2024) ; la mesure est en file, le GPU etant occupe par le 32 B | `roadmap.md`, `2026-10-22_moteur.md`, `2026-10-24.md` (+2) |
| 09:26 | `b3847e8b` | B1.6 MESURE — LE DIALOGUE REEL AVEC SA RESERVE : DiaBLa +40,3/+44,2 contre OpenSubtitles +27,0/+30,4 au meme 1,5 B — mais la reference DiaBLa est une post-edition (biais vers la machine) : c'est une borne haute, pas un septieme registre ; les references independantes sont a recuperer (le GitHub du corpus) | `en-cours.md`, `roadmap.md`, `2026-10-22_moteur.md` (+8) |
| 09:29 | `0b976d08` | B1.6 — LES REFERENCES INDEPENDANTES DE DIABLA TROUVEES : le GitHub du corpus porte les traductions de reference (raw-corpus/*.ref) et le masque eval-filter ; 4 981 paires alignees, verifiees ; la mesure au 1,5 B est lancee — elle dira si l'ecart avec les sous-titres venait du registre ou du biais de la post-edition | `2026-10-22_moteur.md`, `2026-10-24.md`, `2026-10-24_distribue.md` (+1) |
| 09:39 | `8e77f0f6` | B1.6 TRANCHE — LE DIALOGUE SPONTANE AVEC SES REFERENCES INDEPENDANTES : DiaBLa +35,0/+39,3 (4 981 paires alignees par l'eval-filter) contre +40,3/+44,2 en post-edition et +27,0/+30,4 pour les sous-titres, au meme 1,5 B. Le biais de la post-edition est de +5, pas +13 ; le dialogue spontane reste plus facile que les sous-titres et la carte gagne sa ligne | `en-cours.md`, `roadmap.md`, `2026-10-22_moteur.md` (+5) |
| 09:55 | `87f58e8a` | B1.6/B2.7 — LES DEUX BLOCAGES GPU NOMMES : le 7 B sur DiaBLa (15,2 Go de poids sur 15,55, la marge des activations manque) et le 14 B a la couche 24 (quatre tentatives) buttent sur la VRAM de 16 Go, pas sur le protocole. Les trois points a profondeur fixe et les deux references du dialogue suffisent aux conclusions | `roadmap.md`, `2026-10-22_moteur.md`, `2026-10-24.md` (+3) |
| 10:33 | `39a74aeb` | DOC — LA VISION ET LA PAGE VIVANTE ACTUALISEES : la politique de placement existe (placement.rs, choisir, 4 tests) et le KV l'applique, la tete a montre sa limite (le 4 bits qui tient coute +10 % de PPL) ; les six registres et le dialogue spontane sont mesures, reste la prose scientifique (bloquee) | `en-cours.md`, `vision.md`, `2026-10-22_moteur.md` (+3) |
| 15:00 | `1d70ecb7` | FIX — LE LIEN VERS LA CARTE ETAIT CASSE : depuis docs/synthese/, le chemin est ../../reports/ (deux niveaux), pas ../reports/ (un niveau). La revue de documentation l'a signale et c'est corrige | `05-la-pensee-sans-verbaliser.md`, `2026-10-24.md`, `2026-10-24_mesures.md` |
| 15:26 | `36b91baa` | REVISION — LA RAISON D'ETRE, LA STRATEGIE ET LE PLAN. La structure bat la taille n'est plus une hypothese : la sonde est plate des le 1,5 B (0,7256/0,7269/0,7189), le pont plafonne a 0,87, le 14 B est dernier a 50 % (0,4833) — dix fois la taille pour +0,001. Les refus sont ecrits (apprendre des flux +0,0045, le 4 bits de la tete +10 %, la course a l'echelle). La strategie passe de « mesurer l'echelle » a « exploiter la structure » : A7 la grappe deportee, B4 les operateurs abstraits, A8 l'ordonnanceur place et perte. Vision, mission, roadmap, README, AGENTS et page vivante reecrits | `AGENTS.md`, `README.md`, `mission.md` (+6) |

## Chiffres du jour

`50 %` · `+10 %` · `0,7256` · `0,7269` · `0,7189` · `0,4833` · `0,001` · `0,0045` · `15,2 Go` · `16 Go` · `4981 paires` · `1034 paires`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Mesures et rapports touchés

- [reports/README.md](../reports/README.md)
- [reports/rapport-analyse-flux.md](../reports/rapport-analyse-flux.md)
- [reports/rapport-decision-par-couche.md](../reports/rapport-decision-par-couche.md)
- [reports/rapport-dialogue-diabla.md](../reports/rapport-dialogue-diabla.md)

<!-- notes -->

<!-- /notes -->
