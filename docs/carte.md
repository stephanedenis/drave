# La carte de Drave — l'index des sujets

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 185 fichiers / 252 JSON, 54 documents**), chemins archivés
> corrigés (`docs/archive/`), B10–B12 réintégrés dans les cartes. **Les règles d'`AGENTS.md`
> ne changent pas.** Source de vérité : `docs/en-cours.md` (état) et
> `docs/roadmap.md` (plan). *Spécifique : cette page est l'index des sujets ; les blocs
> B10–B12 et les documents orphelins y sont ajoutés.*

> **Le hub des sujets.** Un lien, **un fichier**. Les autres portes : [la vision](vision.md) ·
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
| **A7.26** cache mixte 3 prompts | **compromis** — accord moyen 84,19 %, décrochage à 75 sur le train | [la fiche](../reports/rapport-kv-cache-multi.md) |
| **A7.25** balayage seuils | **64 confirmé** — 237/92,6 %, les autres seuils sont pires | [la fiche](../reports/rapport-kv-cache-seuils.md) |
| **A7.24** seuil f32 32 | **négatif** — divergence au 41ᵉ, accord 16,41 % | [la fiche](../reports/rapport-kv-cache-mixte-32.md) |
| **A7.23** seuil f32 128 | **négatif** — divergence au 215ᵉ, accord 83,98 %, moins bon que le seuil 64 | [la fiche](../reports/rapport-kv-cache-mixte-128.md) |
| **A7.22** fenêtre f32 glissante | **négatif** — divergence au 77ᵉ, accord 32,42 %, pire que le mixte | [la fiche](../reports/rapport-kv-cache-fenetre.md) |
| **A7.21** cache mixte 256 | **compromis** — accord 92,58 %, divergence au 237ᵉ | [la fiche](../reports/rapport-kv-cache-mixte-256.md) |
| **A7.20** cache KV mixte | **positive** — 128/128 identiques, mémoire 62,5 % | [la fiche](../reports/rapport-kv-cache-mixte.md) |
| **A7.19** cache KV int8 bloc | **négatif** — divergence au 41ᵉ, accord 32,81 %, pire que par canal | [la fiche](../reports/rapport-kv-cache-int8-bloc.md) |
| **A7.18** cache KV int8 128 | **négatif** — accord 60,94 %, divergence au 77ᵉ jeton | [la fiche](../reports/rapport-kv-cache-int8-128.md) |
| **A7.17** cache KV int8 64 | **positive** — 64/64 identiques avec `CacheInt8` stocké | [la fiche](../reports/rapport-kv-cache-int8-64.md) |
| **A7.16** cache KV int8 stocké | **positive** — 32/32 identiques avec un vrai cache int8 | [la fiche](../reports/rapport-kv-cache-int8.md) |
| **A7.15** 64 jetons K/V int8 | **positive** — 64/64 identiques, accord 1,0 | [la fiche](../reports/rapport-kv-gen-64.md) |
| **A7.14** génération K/V int8 | **positive** — 16/16 jetons identiques, accord 1,0 | [la fiche](../reports/rapport-kv-gen.md) |
| **A7.13** K/V int8 512 | **positive** — ΔPPL 0,0 sur 511 jetons et 24 couches | [la fiche](../reports/rapport-kv-ppl-long.md) |
| **A7.12** PPL K/V int8 | **positive** — PPL 2,6792016 → 2,6792004, Δ −1,17e-6 sur 24 couches | [la fiche](../reports/rapport-kv-ppl.md) |
| **A7.11** attention KV int8 | **stable** — argmax 97,66 %, corrélation 0,99998, ratio 0,266 | [la fiche](../reports/rapport-kv-attention.md) |
| **A7.10** KV int8 | **compromis** — 4× moins d'octets, diff max 0,0155, 25,5 Mio pour 4 096 jetons | [la fiche](../reports/rapport-kv-int8.md) |
| **A7.9** cache KV | **négatif** — 24 couches 24 580 o/jeton, 96 Mio pour 4 096 jetons ; garder côté serveur | [la fiche](../reports/rapport-kv-reseau.md) |
| **A7.8** int8 par canal | **compromis** — ratio 36–39 %, argmax 1,0, KL ~1e-3 ; lossy mais décision stable | [la fiche](../reports/rapport-couche-int8-canal.md) |
| **A7.7** hidden int8 | **négatif** — 34,6 % du volume mais argmax 0,83–0,93, KL 0,12–0,37 ; bf16 meilleur | [la fiche](../reports/rapport-couche-int8.md) |
| **A7.6** couche à distance | **mesuré** — logits bit-à-bit 3/3, ΔPPL 0, RTT 4,052 ms, 4 105 o/jeton ; sparse 1,027× | [la fiche](../reports/rapport-couche-distante.md) |
| **A7.5b** seuil réseau | **mesuré** — sparse 1 672 o vs 7 416, gain 1,94× à 0 ms, 1,006× à 100 ms, seuil −0,60 ms | [la fiche](../reports/rapport-seuil-reseau.md) |
| **A7.5** grappe réseau | **mesuré** — 4,44× moins d'octets, fidélité 100 %, 0,125 ms loopback | [la fiche](../reports/rapport-grappe-reseau.md) |
| **B26** M6 conflit | **nul** — 94,95 %, conflit 0, commutation 0 ; sélecteur sans compétition | [la fiche](../reports/rapport-m6-conflit2.md) |
| **B25** M8 rejeu | **négatif** — M8 exact 0, rejeu 0, hybride 0 sur 6 codes tenus | [la fiche](../reports/rapport-m8-rejeu.md) |
| **B24** routeur confiance | **partiel** — typo 63,7 % (+7,5) mais espaces 34,2 % (−7,5) ; oracle 79,45 % | [la fiche](../reports/rapport-routeur-confiance.md) |
| **C3.2e** sous-familles autres | **mesuré** — uralic 46,7→100 %, benue 88 %, austro 60,3 %, afro ouest 53,5 % | [la fiche](../reports/rapport-sous-familles-autres.md) |
| **C3.2d** sous-familles IE | **mesuré** — 54,6–100 % ; l'IE à 14,7 % est un effet de composition | [la fiche](../reports/rapport-ie-sous-familles.md) |
| **C3.2c** 9 familles | **mesuré** — 7/9 > 30 %, moyenne 69,5 %, contrôle 0 ; indo-européen 14,7 %, uralic 46,7 % | [la fiche](../reports/rapport-familles-9.md) |
| **B23** routeur M1→M2 | **partiel** — espaces 41,8 % vs 11,6 % ; typo 56,2 % < M2 68,3 % ; collision de lexique | [la fiche](../reports/rapport-routeur-m1-m2.md) |
| **B22** M2 typos | **niche robuste** — M2 62–80 % contre M1 24–45 % sur 4 types de typos | [la fiche](../reports/rapport-m2-typo.md) |
| **B21** M9 dose | **dose** — M3 0/4/8/12/12 tautologique ; M5 +4,25 pts de l'ordre 2 ; sham nul | [la fiche](../reports/rapport-m9-dose.md) |
| **B19** M2 secours | **typos** — M2 71,2/76,7 sur typo contre M1 36,6 ; phrase M1 86,6 vs M2 0 ; niche, pas secours général | [la fiche](../reports/rapport-m2-secours.md) |
| **B18** restitution canonique | **involution** — 528/528 rendus et relus, 0 échec ; codec, pas décodeur | [la fiche](../reports/rapport-restitution.md) |
| **B17** mémoire LFU | **filtre** — LFU 9,28 % suffixe vs FIFO 5,03 % ; M8 couverture 70,75 %, lookup 100 %, généralisation 0 | [la fiche](../reports/rapport-pipeline-memoire.md) |
| **B16** M7-bis LFU | **fréquence** — LFU +23,1 pts répétés, +4,25 suffixe, +8,7 nouveaux ; LFU+récence = LFU ; contexte négatif | [la fiche](../reports/rapport-m7-frequence.md) |
| **B14** M2 dans la chaîne | **rameau** — M1 100 %, M2 93,4/93,6 %, aucun étage ne consomme M2 ; M5 plateau 18,70 % vs 12,60 % | [la fiche](../reports/rapport-pipeline-m2.md) |
| **B15** M1 multilingue | **66 langues** — 528/528 ; 26/26 variantes et 15/15 interlangues invariantes ; contrôle permuté 0/90 % | [la fiche](../reports/rapport-multilingue.md) |
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
