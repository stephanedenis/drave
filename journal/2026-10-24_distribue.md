# 2026-10-24 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-24.md](2026-10-24.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (25)

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
| 15:32 | `976d55e4` | A7.2 + A8.2 — LE RELAIS A CHIFFRE EGAL, ET LA PERTE ENTRE DANS LA REGLE. A7.2 etabli : porte-topologie (92 s, 42.5477) — une couche executee ailleurs rend la meme sortie, le flux coute 1 608 octets/flux, 0,25 Mbit/s, latence <= 20 ms ; reste la grappe intra-couche (A7.3). A8.2 code : choisir_avec_perte + 3 tests — l'int8 tardif (+0,03 %) passe a 1 %, l'int4 tardif (+2,7 %) exige 5 %, la tete 4 bits (+10 %) est refusee a 5 %, l'int4 global (+364 %) jamais : la lecon de la tete devient une regle testee | `en-cours.md`, `roadmap.md`, `placement.rs` (+4) |
| 15:42 | `d116a6f6` | B4.1 — LA NEGATION N'EST PAS PORTEE PAR L'ETAT : l'operateur « Il est faux que : H » sur 1034 paires DACCORD (1,5 B, couche 22) donne un flip de 0,4148 (SOUS le hasard 0,5) et une garde de 0,5852 (au-dessus), quand la reference tient (0,8103). La sonde relit l'etiquette originale sur les paires niees : elle lit la relation de surface, pas l'operation. Controle au hasard propre (0,4566). Premier resultat de B4, NEGATIF — B4.2 devient l'operateur appris | `en-cours.md`, `roadmap.md`, `2026-10-24.md` (+6) |
| 15:56 | `12e5a053` | DOC — LA NAVIGATION PAR FICHIERS : une carte des sujets (docs/carte.md, 83 liens — concepts, chantiers, phases, activites, schemas), le chapitre 7 decompose en 10 parties (5 972 lignes, 179 sections) avec son index qui garde les 26 liens, le glossaire en 11 familles (2 274 lignes), la revue etendue au dossier glossaire, le serveur du site pointe la carte. Verifie : mdserve et le site rendent les tableaux, les liens et les SVG | `AGENTS.md`, `README.md`, `README.md` (+31) |
| 15:57 | `cae7bd41` | DOC — LES TROIS DOSSIERS SE POINTENT : reports/README.md et journal/README.md portent la ligne de navigation (la carte des sujets, l'etat du moment, l'inventaire, l'index des resultats, le journal). docs, reports et journal se lisent maintenant l'un l'autre par des liens de fichiers | `2026-10-24.md`, `2026-10-24_distribue.md`, `README.md` |
| 16:03 | `dd585b60` | B4.2 — LA NEGATION EST APPRENABLE, PAS TRANSFERABLE : une sonde reentrainee sur les paires niees lit la relation basculee a 0,7042 (hasard 0,5 ; controle 0,4952), mais la sonde de l'original ne lit pas le nie (0,4148) et reciproquement (0,3312). L'operateur n'est pas une direction : c'est une GEOMETRIE LOCALE — la lecon du plan (mesure 119). B4.3 : un operateur appris sur une paire d'operations transfere-t-il a une autre ? | `2026-10-24.md`, `2026-10-24_distribue.md`, `operateur-negation-1.5b-l22.json` (+2) |
| 16:31 | `b22b7097` | A8.3 — LA REGLE PLACE ET PERTE EST BRANCHEE : placement::kv_precision choisit la precision du KV par couche selon le budget DRAVE_PERTE_MAX (defaut 1 %) — l'int8 si sa perte mesuree tient (+2,28 % sur les premieres, +0,03 % sur les dernieres), le f32 sinon. La regle rend EXACTEMENT le choix de la main : 30,7286 des deux cotes (contre 30,7660 en f32), memes couches en int8. Deux tests ajoutes (8/8). La lecon de la tete devient la regle du KV | `roadmap.md`, `model.rs`, `placement.rs` (+4) |
| 18:50 | `a4377f9b` | DOC — LE BILAN DU JOUR EN ENTIER : la page vivante dit ce que la journee a etabli — la carte close, B4 close (les cinq chiffres de l'operateur), A7 complete (le relais 42,5477, la grappe exacte a 21 %), A8 opt-in, les DEUX passes 45/47 (toutes les references stables le soir), DiaBLa au 3 B, le 14 B l24. L'heure passe a 19 h | `en-cours.md`, `2026-10-24.md`, `2026-10-24_memoire.md` (+1) |
| 19:03 | `d9547ca3` | A7.4 — LA GRAPPE DEPORTEE : le format du relais passe en version 2 (un masque d'un bit par canal + les valeurs non nulles). Le flux de la grappe coute 4,22x moins que le dense (1 704 o contre 7 196 o), la porte du flux rend les MEMES chiffres (60,8135 / 60,8135), et la version 1 reste lisible. A7 est complete : la couche deportee, la grappe, sa taille, et son transport | `en-cours.md`, `roadmap.md`, `kimi_k3.rs` (+6) |
| 19:07 | `2f2f6be6` | B4 (SUITE) — LA CONCEPTION DU LORA DE LA NEGATION : la question (l'operation dans le poids, pour que l'etat la porte sans sonde), le dispositif (le LoRA rang 8 sur le 1,5 B, les 723 paires niees, les cinq tests de B refaits), le critere (le flip passe le hasard), le cout (1-2 h de GPU, apres la passe) et le risque (le LoRA peut apprendre la surface sans l'operation — controle : une negation differente) | `2026-10-24.md`, `2026-10-24_distribue.md`, `THEMES.md` (+1) |
| 19:15 | `0ebdf5fd` | B4 (SUITE) — LE MODE LORA DANS L'OUTIL : --lora apprend la negation DANS les poids (le LoRA rang 8 du modele, entraine sur les paires niees, la tete oui/non) AVANT de refaire les cinq tests de B. Le modele est gele sauf le LoRA ; une epoque sur les 723 paires | `2026-10-24.md`, `2026-10-24_distribue.md`, `THEMES.md` (+1) |
| 19:18 | `5f9a227a` | B4.6 — LE LORA DE LA NEGATION EST DECLARE : la ligne existe dans la roadmap (le rang 8, les 723 paires niees, le critere : le flip passe le hasard avec le controle au hasard et sur une negation differente). Elle est codee, pas encore mesuree — le GPU est occupe par la passe | `roadmap.md`, `2026-10-24.md`, `2026-10-24_distribue.md` |
| 20:38 | `58db87d5` | ROADMAP — LA LIGNE A7.4 AVAIT 5 CELLULES AU LIEU DE 4 : le lien du rapport etait dans une 5e cellule, et mistune refuse le tableau ENTIER ; la porte des tableaux l'a attrape (1 tableau ne rendait pas). Le lien passe dans la 4e cellule (une virgule au lieu d'une barre). La porte repasse : 583 fichiers, 1 105 liens, chaque tableau a le meme nombre de cellules partout | `roadmap.md`, `2026-10-24.md`, `2026-10-24_distribue.md` |
| 21:24 | `ccf47752` | B4.6 — LE LORA DE LA NEGATION INVERSE LA LECTURE : l'entrainement converge (perte 0,0022) et le modele reste intact (0,8135), mais le flip_sonde est 0,2283 = 1 - garde_sonde (0,7717) — le LoRA apprend la SURFACE (« il est faux que ») comme un marqueur d'inversion, pas l'operation. Negatif de B4.6, coherent avec B4.2 (la geometrie). La reserve est ecrite (le 1 - p peut etre un artefact de la sonde, le controle est le LoRA sur les paires originales) | `en-cours.md`, `roadmap.md`, `2026-10-24.md` (+3) |
| 21:26 | `8dfeb5a5` | B4.6 — LE CONTROLE --lora-original : entrainer le LoRA sur les paires ORIGINALES (sans nier). Si le flip_sonde reste a ~0,41 (le B4.1), le LoRA a appris quelque chose de specifique ; s'il tombe a ~0,23 comme le LoRA nie, c'est la sonde qui rend le complement — la reserve de la fiche est tranchee par ce run | `2026-10-24.md`, `2026-10-24_distribue.md`, `THEMES.md` (+1) |
| 21:34 | `7fdabd19` | B4.6 — LE CONTROLE TRANCHE : le LoRA entraine sur les paires ORIGINALES donne flip_sonde 0,4662 (proche du 0,41 du B4.1), contre 0,2283 pour le LoRA nie — le LoRA nie a bien appris quelque chose de specifique, ce n'est pas la sonde seule. Mais flip_sonde + garde_sonde = 1,0000 dans les DEUX cas : le LoRA retourne la reponse, il ne transfere pas l'operation. Le negatif de B4.6 tient | `2026-10-24.md`, `2026-10-24_distribue.md`, `rapport-operateur-negation.md` |

## Chiffres du jour

`0,4662` · `0,2283` · `1,0000` · `0,0022` · `0,8135` · `0,7717` · `723 paires` · `60,8135` · `21 %` · `42,5477` · `1 %` · `+2,28 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Mesures et rapports touchés

- [reports/07-mesures-couche-commune.md](../reports/07-mesures-couche-commune.md)
- [reports/07/p1.md](../reports/07/p1.md)
- [reports/07/p10.md](../reports/07/p10.md)
- [reports/07/p2.md](../reports/07/p2.md)
- [reports/07/p3.md](../reports/07/p3.md)
- [reports/07/p4.md](../reports/07/p4.md)
- [reports/07/p5.md](../reports/07/p5.md)
- [reports/07/p6.md](../reports/07/p6.md)
- [reports/07/p7.md](../reports/07/p7.md)
- [reports/07/p8.md](../reports/07/p8.md)
- [reports/07/p9.md](../reports/07/p9.md)
- [reports/README.md](../reports/README.md)
- [reports/rapport-analyse-flux.md](../reports/rapport-analyse-flux.md)
- [reports/rapport-decision-par-couche.md](../reports/rapport-decision-par-couche.md)
- [reports/rapport-dialogue-diabla.md](../reports/rapport-dialogue-diabla.md)
- [reports/rapport-grappe-deportee.md](../reports/rapport-grappe-deportee.md)
- [reports/rapport-operateur-negation.md](../reports/rapport-operateur-negation.md)
- [reports/rapport-regle-placement-perte.md](../reports/rapport-regle-placement-perte.md)

<!-- notes -->

<!-- /notes -->
