# La carte de Drave — l'index des sujets

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 175 fichiers / 242 JSON, 53 documents**), chemins archivés
> corrigés (`docs/archive/`), B10–B12 réintégrés dans les cartes. **Les règles d'`AGENTS.md`
> ne changent pas.** Source de vérité : `docs/en-cours.md` (état) et
> `docs/roadmap.md` (plan). *Spécifique : cette page est l'index des sujets ; les blocs
> B10–B12 et les documents orphelins y sont ajoutés.*

> **Le hub des sujets.** Chaque lien mène à **un fichier**. Les autres portes : [la vision](vision.md) ·
> [l'état](en-cours.md) · [la roadmap](roadmap.md) · [l'inventaire](README.md) · [les résultats](../reports/README.md) ·
> [le journal](../journal/README.md) · [l'archive](archive/README.md).

## Où l'on va, où l'on en est

| | |
|---|---|
| [la vision](vision.md) — le bus d'événements, les blocs, l'hybridation, ce qu'elle refuse | |
| [la mission](agent/mission.md) — les deux programmes, l'ordre des priorités | |
| [l'état](en-cours.md) — ce qui est en cours, les chiffres qui comptent, les questions | |
| [la roadmap](roadmap.md) — les lignes A et B, la file « jamais en attente » | |
| [les portes](references-non-regression.md) — les passes complètes, les repères | |
| [le glossaire](glossaire.md) — le vocabulaire non négociable | |

## Les blocs

| le bloc | le concept | les preuves |
|---|---|---|
| **le bus, les flux** | [la vision](vision.md) · [le format de flux](format-flux.md) · [les clusters](format-clusters.md) | [les portes](references-non-regression.md) |
| **le bloc neuronal** | [le format de flux](format-flux.md) · [la modularisation](modularisation.md) | [les mesures](../reports/README.md) |
| **le bloc classique** | [la vision](vision.md) · [la modularisation](modularisation.md) | [les jeux](jeux-symboliques.md) |
| **la langue** | [le protocole sémantique](protocole-semantique.md) · [les jeux symboliques](jeux-symboliques.md) · [la généalogie](genealogie-des-langues.md) · [le banc externe](llm-externe.md) | [B7/B8](../reports/rapport-langues-maitres.md) · [B9](../reports/rapport-deepseek.md) |
| **la pensée** | [la synthèse 05](synthese/05-la-pensee-sans-verbaliser.md) · [la synthèse 08](synthese/08-les-operations.md) | [B4](../reports/rapport-operateur-negation.md) · [B5/B6](../reports/rapport-jeux-symboliques.md) |
| **la sémantique typée (B10/B11)** | [le protocole](protocole-semantique.md) · [les universaux](semantique-universaux.md) | [B10](../reports/rapport-semantique.md) · [B11](../reports/rapport-universaux.md) · [bilan](../reports/bilan-b11.md) |
| **le cerveau-langage (B12)** | [les modules](modules-cerveau-langage.md) | [la fiche](../reports/rapport-cerveau-modules.md) |
| **le matériel et le système** | [l'array NVMe](configuration-nvme-raid-amd.md) · [NUMA](numa-segregation.md) · [le convertisseur](convertisseur.md) · [le contexte long](contexte-long.md) | [les mesures](../reports/bilan-multi-materiel.md) |
| **la mesure** | [la synthèse 06](synthese/06-comment-savoir.md) · [l'organisation](organisation-du-depot.md) | [les portes](references-non-regression.md) |

## Les chantiers

| chantier | état | où il vit |
|---|---|---|
| **A7** la grappe déportée | **fait** — relais 42,5477, grappe 21 %, transport 4,22× | [la roadmap](roadmap.md) |
| **A8** l'ordonnanceur place et perte | **fait, opt-in** | [la roadmap](roadmap.md) |
| **B4** les opérateurs abstraits | **close** — six mesures, le LoRA inverse | [la fiche](../reports/rapport-operateur-negation.md) |
| **B5/B6** les jeux symboliques | **faits** — 112 items, 100 % au niveau 4, pensée 5/5 | [le concept](jeux-symboliques.md) · [la fiche](../reports/rapport-jeux-symboliques.md) |
| **B7/B8** les langues et les maîtres | **faits** — 71 langues, 449/449, livre 10/10, go 10/10 | [le concept](jeux-symboliques.md) · [la fiche](../reports/rapport-langues-maitres.md) |
| **B9** le banc externe | **mesuré** — seuil 9,23–9,96 M, 31,63 M/610 4,40 %, fenêtre, négatif 30 langues | [le concept](llm-externe.md) · [la fiche](../reports/rapport-deepseek.md) |
| **B10** le protocole sémantique | **premier passage** — encodeur convergent (0,426), décodeur négatif (référence complète : 12,7 / 5,3 contre 39,6 ; référence tronquée : 14,0 / 5,4 contre 38,8) | [le protocole](protocole-semantique.md) · [la fiche](../reports/rapport-semantique.md) |
| **B11** la base d'universaux typés | **premier passage** — codec 100 % (79/79, 449/449) ; natif synthétique normalisé 55,7 % (invariance 37,0 %) ; codec + contexte 528/528 (100 %) ; natif contexte suffixé 59,8/40,7 ; **restitution du code 100 %**, surface **33/79** | [la note](semantique-universaux.md) · [la fiche](../reports/rapport-universaux.md) |
| **B13** la chaîne sémantique | **intégration** — M1 528/528 ; M5 contexte 18,7 % vs 12,6 % ; M6 94,3 % ; M8 57,95 % (borne haute) | [la fiche](../reports/rapport-pipeline-semantique.md) · [le code](../tools/cerveau/pipeline_semantique.py) |
| **B12** les modules cerveau-langage | **premier passage** — M1 528/528 ; M2 **98,6 / 93,2** (double dissociation) ; M8 **96,48 %** hors stock ; M5/M6/M7 négatifs ; M9 lésions | [les modules](modules-cerveau-langage.md) · [la fiche](../reports/rapport-cerveau-modules.md) |
| **C1–C7** les sept chantiers | **mesurés** — corpus, traduction, restitution, styles, domaines, documentation, pensée | [l'état](en-cours.md) |

## Les preuves

- [les résultats](../reports/README.md) — une fiche par expérience, les négatifs nommés ;
- [les portes](references-non-regression.md) — **49 portes, 47 vertes, 2 structurelles** (26/10 14 h 30) ;
- [le journal](../journal/README.md) — le récit daté ;
- [les schémas](synthese/schemas/vue-ensemble.svg) — la vue d'ensemble, l'anatomie, les facultés, les modes, la
  pensée, les portes, la couche commune.

## L'archive et la théorie

- **l'archive** : [les plans, notes et études 2026-09/10](archive/README.md) — **facultatif** ;
- **la synthèse** : [l'index](synthese/index.md) — huit chapitres, de la vision à la mesure ;
- **les normes** : [l'organisation](organisation-du-depot.md) · [l'utilisation](utilisation.md) ·
  [l'histoire](histoire.md) · [les relations humaines](relations-humaines.md).
