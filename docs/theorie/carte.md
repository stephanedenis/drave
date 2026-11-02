# La carte de Drave — l'index des sujets

> **Le hub des sujets.** Un lien, **un fichier**. Les autres portes : [la vision](vision.md) ·
> [l'état](../pilotage/en-cours.md) · [la roadmap](../pilotage/roadmap.md) · [l'inventaire](../README.md) · [les résultats](../../reports/README.md) ·
> [le journal](../../journal/README.md) · [l'archive](../archive/README.md).

## Où l'on va, où l'on en est

| | |
|---|---|
| [la vision](vision.md) — le bus d'événements, les blocs, l'hybridation, ce qu'elle refuse | |
| [la mission](../methode/mission.md) — les deux programmes, l'ordre des priorités | |
| [l'état](../pilotage/en-cours.md) — ce qui est en cours, les chiffres qui comptent, les questions | |
| [la roadmap](../pilotage/roadmap.md) — les chantiers A, B, N, R et la file « jamais en attente » | |
| [la lecture rapide](lecture-rapide.md) · [le backlog](../pilotage/backlog/index.md) — 14 techniques, 5 couches, une fiche par fonctionnalité | |
| [les portes](../pilotage/references-non-regression.md) — les passes complètes, les repères | |
| [le glossaire](glossaire.md) — le vocabulaire non négociable | |

## Les blocs

| le bloc | le concept | les preuves |
|---|---|---|
| **le bus, les flux** | [la vision](vision.md) · [le format de flux](../implantation/format-flux.md) · [les clusters](../implantation/format-clusters.md) | [les portes](../pilotage/references-non-regression.md) |
| **le bloc neuronal** | [le format de flux](../implantation/format-flux.md) · [la modularisation](../methode/modularisation.md) | [les mesures](../../reports/README.md) |
| **le bloc classique** | [la vision](vision.md) · [la modularisation](../methode/modularisation.md) | [les jeux](jeux-symboliques.md) |
| **la langue** | [le protocole sémantique](protocole-semantique.md) · [les jeux symboliques](jeux-symboliques.md) · [la généalogie](genealogie-des-langues.md) · [le banc externe](../implantation/llm-externe.md) | [B7/B8](../../reports/rapport-langues-maitres.md) · [B9](../../reports/rapport-deepseek.md) |
| **la pensée** | [la synthèse 05](synthese/05-la-pensee-sans-verbaliser.md) · [la synthèse 08](synthese/08-les-operations.md) | [B4](../../reports/rapport-operateur-negation.md) · [B5/B6](../../reports/rapport-jeux-symboliques.md) |
| **la sémantique typée (B10/B11)** | [le protocole](protocole-semantique.md) · [les universaux](semantique-universaux.md) | [B10](../../reports/rapport-semantique.md) · [B11](../../reports/rapport-universaux.md) · [bilan](../../reports/bilan-b11.md) |
| **le cerveau-langage (B12)** | [les modules](modules-cerveau-langage.md) | [la fiche](../../reports/rapport-cerveau-modules.md) |
| **le matériel et le système** | [l'array NVMe](../implantation/configuration-nvme-raid-amd.md) · [NUMA](../implantation/numa-segregation.md) · [le convertisseur](../implantation/convertisseur.md) · [le contexte long](../implantation/contexte-long.md) | [les mesures](../../reports/bilan-multi-materiel.md) |
| **la mesure** | [la synthèse 06](synthese/06-comment-savoir.md) · [l'organisation](../methode/organisation-du-depot.md) | [les portes](../pilotage/references-non-regression.md) |

## Les chantiers

| chantier | état | où il vit |
|---|---|---|
| **A7** la grappe déportée | **fait** — relais 42,5477, grappe 21 %, transport 4,22× | [la roadmap](../pilotage/roadmap.md) |
| **A8** l'ordonnanceur place et perte | **fait, opt-in** | [la roadmap](../pilotage/roadmap.md) |
| **B4** les opérateurs abstraits | **close** — six mesures, le LoRA inverse | [la fiche](../../reports/rapport-operateur-negation.md) |
| **B5/B6** les jeux symboliques | **faits** — 112 items, 100 % au niveau 4, pensée 5/5 | [le concept](jeux-symboliques.md) · [la fiche](../../reports/rapport-jeux-symboliques.md) |
| **B7/B8** les langues et les maîtres | **faits** — 71 langues, 449/449, livre 10/10, go 10/10 | [le concept](jeux-symboliques.md) · [la fiche](../../reports/rapport-langues-maitres.md) |
| **B9** le banc externe | **mesuré** — seuil 9,23–9,96 M, 31,63 M/610 4,40 %, fenêtre, négatif 30 langues | [le concept](../implantation/llm-externe.md) · [la fiche](../../reports/rapport-deepseek.md) |
| **B10** le protocole sémantique | **premier passage** — encodeur convergent (0,426), décodeur négatif (référence complète : 12,7 / 5,3 contre 39,6 ; référence tronquée : 14,0 / 5,4 contre 38,8) | [le protocole](protocole-semantique.md) · [la fiche](../../reports/rapport-semantique.md) |
| **B11** la base d'universaux typés | **premier passage** — codec 100 % (79/79, 449/449) ; natif synthétique normalisé 55,7 % (invariance 37,0 %) ; codec + contexte 528/528 (100 %) ; natif contexte suffixé 59,8/40,7 ; **restitution du code 100 %**, surface **33/79** | [la note](semantique-universaux.md) · [la fiche](../../reports/rapport-universaux.md) |
| **A7.5–A7.26** cache KV et grappe réseau | **campagne** — 22 mesures, du cache int8 aux seuils ; voir les fiches | [l'index](../../reports/INDEX.md) |
| **B24–B27** routeur, M8, M6 | **partiels/négatifs** — confiance, rejeu, conflit, moteur ; voir les fiches | [l'index](../../reports/INDEX.md) |
| **C3.2e** sous-familles autres | **mesuré** — uralic 46,7→100 %, benue 88 %, austro 60,3 %, afro ouest 53,5 % | [la fiche](../../reports/rapport-sous-familles-autres.md) |
| **C3.2d** sous-familles IE | **mesuré** — 54,6–100 % ; l'IE à 14,7 % est un effet de composition | [la fiche](../../reports/rapport-ie-sous-familles.md) |
| **C3.2c** 9 familles | **mesuré** — 7/9 > 30 %, moyenne 69,5 %, contrôle 0 ; indo-européen 14,7 %, uralic 46,7 % | [la fiche](../../reports/rapport-familles-9.md) |
| **B23** routeur M1→M2 | **partiel** — espaces 41,8 % vs 11,6 % ; typo 56,2 % < M2 68,3 % ; collision de lexique | [la fiche](../../reports/rapport-routeur-m1-m2.md) |
| **B22** M2 typos | **niche robuste** — M2 62–80 % contre M1 24–45 % sur 4 types de typos | [la fiche](../../reports/rapport-m2-typo.md) |
| **B21** M9 dose | **dose** — M3 0/4/8/12/12 tautologique ; M5 +4,25 pts de l'ordre 2 ; sham nul | [la fiche](../../reports/rapport-m9-dose.md) |
| **B19** M2 secours | **typos** — M2 71,2/76,7 sur typo contre M1 36,6 ; phrase M1 86,6 vs M2 0 ; niche, pas secours général | [la fiche](../../reports/rapport-m2-secours.md) |
| **B18** restitution canonique | **involution** — 528/528 rendus et relus, 0 échec ; codec, pas décodeur | [la fiche](../../reports/rapport-restitution.md) |
| **B17** mémoire LFU | **filtre** — LFU 9,28 % suffixe vs FIFO 5,03 % ; M8 couverture 70,75 %, lookup 100 %, généralisation 0 | [la fiche](../../reports/rapport-pipeline-memoire.md) |
| **B16** M7-bis LFU | **fréquence** — LFU +23,1 pts répétés, +4,25 suffixe, +8,7 nouveaux ; LFU+récence = LFU ; contexte négatif | [la fiche](../../reports/rapport-m7-frequence.md) |
| **B14** M2 dans la chaîne | **rameau** — M1 100 %, M2 93,4/93,6 %, aucun étage ne consomme M2 ; M5 plateau 18,70 % vs 12,60 % | [la fiche](../../reports/rapport-pipeline-m2.md) |
| **B15** M1 multilingue | **66 langues** — 528/528 ; 26/26 variantes et 15/15 interlangues invariantes ; contrôle permuté 0/90 % | [la fiche](../../reports/rapport-multilingue.md) |
| **B13** la chaîne sémantique | **intégration** — M1 528/528 ; M5 contexte 18,7 % vs 12,6 % ; M6 94,3 % ; M8 57,95 % (borne haute) | [la fiche](../../reports/rapport-pipeline-semantique.md) · [le code](../../tools/cerveau/pipeline_semantique.py) |
| **B12** les modules cerveau-langage | **premier passage** — M1 528/528 ; M2 **98,6 / 93,2** (double dissociation) ; M8 **96,48 %** hors stock ; M5/M6/M7 négatifs ; M9 lésions | [les modules](modules-cerveau-langage.md) · [la fiche](../../reports/rapport-cerveau-modules.md) |
| **C1–C7** les sept chantiers | **mesurés** — corpus, traduction, restitution, styles, domaines, documentation, pensée | [l'état](../pilotage/en-cours.md) |

## Les preuves

- [les résultats](../../reports/README.md) — une fiche par expérience, les négatifs nommés ;
- [les portes](../pilotage/references-non-regression.md) — **49 portes, 47 vertes, 2 structurelles** (26/10 14 h 30) ;
- [le journal](../../journal/README.md) — le récit daté ;
- [les schémas](synthese/schemas/vue-ensemble.svg) — la vue d'ensemble, l'anatomie, les facultés, les modes, la
  pensée, les portes, la couche commune.

## L'archive et la théorie

- **l'archive** : [les plans, notes et études 2026-09/10](../archive/README.md) — **facultatif** ;
- **la synthèse** : [l'index](synthese/index.md) — huit chapitres, de la vision à la mesure ;
- **les normes** : [l'organisation](../methode/organisation-du-depot.md) · [l'utilisation](../pilotage/utilisation.md) ·
  [l'histoire](histoire.md) · [les relations humaines](../methode/relations-humaines.md).
