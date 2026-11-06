# Les rapports — données intermédiaires et références

> **Ce dossier porte les résultats et les données de nos travaux**, jamais la documentation de référence
> (elle est dans [`docs/`](../docs/)). Les fiches courantes sont citées depuis le tableau de bord
> [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md).

> **Navigation** : [la carte des sujets](../docs/theorie/carte.md) · [l'état du moment](../docs/pilotage/en-cours.md) ·
> [l'inventaire des docs](../docs/README.md) · [le journal](../journal/README.md).
>
> **Contexte** : la fiche [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) est un **hub** de
> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par
> partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).

## Les fiches courantes

| fichier | ce qu'il porte |
|---|---|
| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | **B13** — la POS à **83,83 %** (R2a/R3/R2b), F1 **0,6181**, attachement inchangé |
| [`rapport-pos-anglais.md`](rapport-pos-anglais.md) | **B13** — le diagnostic POS anglais (A25) : 5 causes, 3 règles mesurées |
| [`rapport-fiabilite-produit.md`](rapport-fiabilite-produit.md) | **B13** — fiabilité hors gold : 0 plantage, contrat non versionné, 2 `UnicodeEncodeError` |
| [`rapport-robustesse-produit.md`](rapport-robustesse-produit.md) | **B13** — robustesse produit : surrogate et non-str fermés, 8 tests |
| [`rapport-produit-bloc-l.md`](rapport-produit-bloc-l.md) | **B13** — audit de fiabilité (A24) : temps, contrat, 18 correctifs |
| [`rapport-outillage-index.md`](rapport-outillage-index.md) | **B13** — outillage : `--aide` sans écriture, index 625 → **677** |
| [`rapport-file-taches.md`](rapport-file-taches.md) | **B13** — la file des 29 tâches : 8 autonomes, 11 en coordination, 10 bloquées ; 18 périmées |
| [`rapport-produit-v0.md`](rapport-produit-v0.md) | **B13** — le premier produit : **`drave` v0** (analyser/evaluer/rejouer), porte produit, 6 tests |
| [`rapport-autotest-parallele.md`](rapport-autotest-parallele.md) | **B13** — l'autotest parallèle : **183/183 en 1 min 54** (×2,4), mêmes verdicts |
| [`rapport-pensee-v12.md`](rapport-pensee-v12.md) | **B13** — **222/222 (1,0000)**, couverture **0,9289**, 17 spans inatteignables |
| [`rapport-dev-test-v10.md`](rapport-dev-test-v10.md) | **B13** — dev/test v10 : dev 152/152, test 68/68, l'exact est saturé |
| [`rapport-pensee-v11.md`](rapport-pensee-v11.md) | **B13** — les 2 régressions : exact **221/221**, couverture **0,9247**, 18 spans |
| [`rapport-pensee-v10.md`](rapport-pensee-v10.md) | **B13** — le `-ée` et la garde DET : **220/220**, couverture **0,9205** |
| [`rapport-pensee-v9.md`](rapport-pensee-v9.md) | **B13** — la garde PRON : exact **219/219 (1,0000)**, couverture **0,9163**, F1 **0,5822**, dev 152/152, test 67/67 |
| [`rapport-topk-v8.md`](rapport-topk-v8.md) | **B13** — le top-k : `prec = s` expliquait 32/35 échecs ; **211/239** |
| [`rapport-audit-r1r3.md`](rapport-audit-r1r3.md) | **B13** — audit A19 : **+17 net** (24 gains, 7 régressions), R3a inerte |
| [`rapport-spans-v7.md`](rapport-spans-v7.md) | **B13** — les 43 spans (A17) : causes, règles |
| [`rapport-pensee-r1r3.md`](rapport-pensee-r1r3.md) | **B13** — R1/R2/R3 : exact **212/212 (1,0000)**, couverture **0,887**, F1 **0,5763** ; 27 spans |
| [`rapport-dev-test-v7.md`](rapport-dev-test-v7.md) | **B13** — dev/test en v7 : dev **133/134**, test **62/62**, trois découpages, écart ≤ 1 cas |
| [`rapport-coherence-fiches-v7.md`](rapport-coherence-fiches-v7.md) | **B13** — la cohérence des 7 fiches v2→v7 : **23 écarts**, 4 critiques, corrections listées |
| [`rapport-pensee-couverture-v7.md`](rapport-pensee-couverture-v7.md) | **B13** — couverture 0,8201 |
| [`rapport-pensee-attachement-parfait.md`](rapport-pensee-attachement-parfait.md) | **B13** — l'attachement **187/187 (1,0000)** sur les spans prédits, fr 1,0 / en 1,0, dev 126/126, test 61/61 ; le rendement reste 0,7824 |
| [`rapport-pensee-couverture-v5.md`](rapport-pensee-couverture-v5.md) | **B13** — couverture : 187 labels, exact 186/187 |
| [`rapport-gold-split.md`](rapport-gold-split.md) | **B13** — le gold dev/test : **test 0,9814**, dev 0,9811, la règle « régler sur dev, accepter si test ne baisse pas » |
| [`rapport-pensee-segmentation-v4.md`](rapport-pensee-segmentation-v4.md) | **B13** — la segmentation d'abord : F1 **0,4539** (602), exact **157/160**, couverture **160/239**, 183/183 |
| [`rapport-pensee-par-langue.md`](rapport-pensee-par-langue.md) | **B13** — l'attachement par langue : fr 0,9658, en 1,000, mais **28 labels/88 cibles en anglais**, **183/183** |
| [`rapport-gold-anglais.md`](rapport-gold-anglais.md) | **B13** — le gold anglais est sain (0 span faux) ; l'échec anglais est la **segmentation** (60/94 spans) |
| [`rapport-spans-chunker.md`](rapport-spans-chunker.md) | **B13** — les 94 spans : le chunker seul en couvre 0 ; deux règles en récupèrent **84** (prix : faux positifs) |
| [`rapport-audit-v2.md`](rapport-audit-v2.md) | **B13** — l'audit A8 de la v2 : 43 valeurs reproduites, 2 arrondis, 1 prose (46→45) |
| [`rapport-replis-cible.md`](rapport-replis-cible.md) | **B13** — les replis A10 : 145/145 par 3 règles étroites, **borne haute non intégrée** |
| [`rapport-multicibles.md`](rapport-multicibles.md) | **B13** — les multi-cibles A13 : 43/96 GP, exact_any 143/145 |
| [`rapport-cache-chunker.md`](rapport-cache-chunker.md) | **B13** — la validation A11 du cache : ×11,0 à 160 tokens, égalité 612/612, cache falsifié détecté |
| [`rapport-pensee-attachement-v3.md`](rapport-pensee-attachement-v3.md) | **B13** — l'attachement v3 : exact **0,9724**, noms 1,0, R2/R3/R4, **181/181** |
| [`rapport-echecs-v2.md`](rapport-echecs-v2.md) | **B13** — les 8 échecs qualifiés, 5 règles chiffrées (A9) |
| [`rapport-cache-chunker-applique.md`](rapport-cache-chunker-applique.md) | **B13** — le cache appliqué : **×139** en chunker, ×1 en défaut (S domine), sortie identique, **181/181** |
| [`rapport-contrat-s.md`](rapport-contrat-s.md) | **B13** — le contrat `s/v1` : ce que S doit fournir (API, cibles typées, langue), écarts mesurés |
| [`rapport-cout-chunker.md`](rapport-cout-chunker.md) | **B13** — le coût du chunker : O(n²) confirmé, cache ×11,6 à 160 tokens |
| [`rapport-coherence-fiches.md`](rapport-coherence-fiches.md) | **B13** — la cohérence des 11 fiches : 8 justes, 3 divergences réelles (corrigées) |
| [`rapport-pensee-attachement-v2.md`](rapport-pensee-attachement-v2.md) | **B13** — l'attachement v2 : exact **0,9448**, top-k strict **0,9724**, modèle appris rejeté, **180/180** |
| [`rapport-audit-attachement.md`](rapport-audit-attachement.md) | **B13** — l'audit A1 : 14/14 valeurs reproduites, écart 0 |
| [`rapport-topk-diagnostic.md`](rapport-topk-diagnostic.md) | **B13** — le diagnostic A2 : 57 échecs qualifiés, 3 correctifs (F1 +45) |
| [`rapport-classement-appris.md`](rapport-classement-appris.md) | **B13** — le classement appris A3 : 142/145, **non significatif** face à 137, rejeté |
| [`rapport-audit-attachement.md`](rapport-audit-attachement.md) | **B13** — l'audit A1 : 14/14 valeurs reproduites, écart 0 ; 3 JSON sur 5 sont des instantanés, **178/178** |
| [`rapport-pensee-lexique-elargi.md`](rapport-pensee-lexique-elargi.md) | **B13** — le lexique élargi : exact 0,8082 → **0,8483**, **174/174** |
| [`rapport-pensee-spans.md`](rapport-pensee-spans.md) | **B13** — les spans perdus : 48 REL, 33 SUB, 12 GP, **169/169** |
| [`rapport-pensee-echecs-attachement.md`](rapport-pensee-echecs-attachement.md) | **B13** — les 127 échecs : 94 span, 33 → 32 cible, **166/166** |
| [`rapport-pensee-candidats-verbes.md`](rapport-pensee-candidats-verbes.md) | **B13** — les candidats verbes : top-k 0,3264 → **0,4686**, tête 0,7655, **165/165** |
| [`rapport-pensee-cible-proximite.md`](rapport-pensee-cible-proximite.md) | **B13** — la cible par proximité : exact 0,0042 → **0,0544** (×13), top1 0,3975, **164/164** |
| [`rapport-pensee-passifs-sans-par.md`](rapport-pensee-passifs-sans-par.md) | **B13** — les passifs sans par : le chunker 3/3, le générateur S ignore, **163/163** |
| [`rapport-drvm-n01.md`](rapport-drvm-n01.md) | **N** — DRVM N0.1 : 6/6, le payload corrompu est refusé, **149/149** |
| [`rapport-n2-fenetre.md`](rapport-n2-fenetre.md) | **N2/R1** — la fenêtre 128→1 024 : la PPL baisse là où la fenêtre sert (3,2545→2,9950 à 1 000 octets ; 3,2459→2,9449 à 2 000) ; à courte longueur l'ordre s'inverse ; chaque modèle sature à sa fenêtre ; N2.ac + RoPE 512 bat 200 k pas |
| [`rapport-n2-distillation-native.md`](rapport-n2-distillation-native.md) | **N2** — l'erratum de la distillation : rien à parité stricte (−0,03/−0,01/−0,004), +0,14–0,18 = repondération ; la paire propre paie −0,06 |
| [`rapport-ocr-cegep-64.md`](rapport-ocr-cegep-64.md) | **D** — le corpus CEGEP à 64 documents est contaminé : DOC2 (val) est un quasi-doublon du train ; le corpus propre reste à **62 documents** |
| [`rapport-ocr-pdf-restants.md`](rapport-ocr-pdf-restants.md) | **D** — les 8 `.PDF` restants : 4 documents, 49 pages, 3 doublons — la limite est mesurée |
| [`rapport-pensee-fusion-reparee.md`](rapport-pensee-fusion-reparee.md) | **L** — la fusion réparée : par niveau (neuronal POS/syntagmes, heuristique pragmatique) — 0,9309 / 0,8226 / 0,8784 / 0,9954, le maximum des deux |
| [`rapport-s-corpus-reel.md`](rapport-s-corpus-reel.md) | **S** — le corpus réel : GN+GV 8,5 % CEGEP (mélange 9,1 %), 65,5 % propre (9,1 %) ; plancher du mélange ; banque 200 phrases / 355 candidats |
| [`rapport-pensee-vrais-absents.md`](rapport-pensee-vrais-absents.md) | **B13** — les vrais absents : 5 phrases, 0 lien, **140/140** |
| [`rapport-pensee-pieges.md`](rapport-pensee-pieges.md) | **B13** — les questions pièges : 29/34, le si est une convention, **132/132** |
| [`rapport-pensee-gold-342.md`](rapport-pensee-gold-342.md) | **B13** — le gold complet : 522 phrases, POS 0,7586, tête 0,3807, **110/110** |
| [`rapport-pensee-anaphore-bilan.md`](rapport-pensee-anaphore-bilan.md) | **B13** — le bilan de l'anaphore : 27/30, CV 0,847, huit mesures, **109/109** |
| [`rapport-pensee-oubli.md`](rapport-pensee-oubli.md) | **B13** — la mémoire courte : Q × 0,9/10, 20/20, 10,0 pas, **71/71** |
| [`rapport-pensee-look-tardif.md`](rapport-pensee-look-tardif.md) | **B13** — le look tardif : à l'épisode 3000, v final 0,54, 20/20, 8,0 pas, **70/70** |
| [`rapport-pensee-un-look.md`](rapport-pensee-un-look.md) | **B13** — un seul look : 1/4000, v final 0,44, 20/20, 8,0 pas, **69/69** |
| [`rapport-pensee-ultra-rare.md`](rapport-pensee-ultra-rare.md) | **B13** — l'information ultra-rare : utile 0,1 %, 4 looks, v final 0,44, 20/20, **68/68** |
| [`rapport-pensee-tres-rare.md`](rapport-pensee-tres-rare.md) | **B13** — l'information très rare : utile 1 %, v final 0,54, 20/20, 8,0 pas, **67/67** |
| [`rapport-pensee-rare.md`](rapport-pensee-rare.md) | **B13** — l'information rare : utile 10 %, v final 0,8, 20/20, 8,0 pas, **66/66** |
| [`rapport-pensee-asym.md`](rapport-pensee-asym.md) | **B13** — la fiabilité asymétrique : 0,9/0,5, v final 0,44, 20/20, 8,0 pas, **65/65** |
| [`rapport-pensee-intra.md`](rapport-pensee-intra.md) | **B13** — le régime intra-épisode : bascule à chaque look, v final 0,48, 20/20, 8,0 pas, **64/64** |
| [`rapport-pensee-rapide.md`](rapport-pensee-rapide.md) | **B13** — la bascule très fréquente : 1/10, v final 0,28, 20/20, 9,4 pas, **61/61** |
| [`rapport-pensee-frequent.md`](rapport-pensee-frequent.md) | **B13** — la bascule fréquente : 1/50, v final 0,78, 20/20, 8,0 pas, **60/60** |
| [`rapport-pensee-chaotique.md`](rapport-pensee-chaotique.md) | **B13** — l'alternance aléatoire : bascule 1/500, v final 0,12, 20/20, **59/59** |
| [`rapport-pensee-alternance.md`](rapport-pensee-alternance.md) | **B13** — les ruptures répétées : 0,9/0,1 alternés, v final 0,14, 20/20, **58/58** |
| [`rapport-pensee-rupture.md`](rapport-pensee-rupture.md) | **B13** — la rupture : 90 % d'erreur, v final 0,12, 20/20, 8,0 pas, **57/57** |
| [`rapport-pensee-derive.md`](rapport-pensee-derive.md) | **B13** — la fiabilité qui dérive : v final 0,56, 20/20, 8,0 pas, **54/54** |
| [`rapport-pensee-phase-graines.md`](rapport-pensee-phase-graines.md) | **B13** — la phase sur 5 graines : 5/5 buts, 10–14 pas, 376–422 états-Q, **41/41** |
| [`rapport-pensee-phase.md`](rapport-pensee-phase.md) | **B13** — la période qui change : 3 puis 2 pas, A* 28 nœuds, politique but/10, **40/40** |
| [`rapport-pensee-graines.md`](rapport-pensee-graines.md) | **B13** — la robustesse sur 5 graines : 5/5 bruits, 5/5 stables, **33/33** |
| [`rapport-pensee-audit.md`](rapport-pensee-audit.md) | **B13** — l'audit des mesures : 15/15 cohérentes, la politique minute ne transfère pas au bruit, **31/31** |
| [`rapport-pensee-correction.md`](rapport-pensee-correction.md) | **B13** — la mesure corrigée : bug de `seule_minute`, 4 politiques à but/8, 4 fiches corrigées, **30/30** |
| [`rapport-pensee-sans-none.md`](rapport-pensee-sans-none.md) | **B13** — la politique sans None : 56 états-Q, elle tourne 200 pas, **29/29** |
| [`rapport-pensee-professeur.md`](rapport-pensee-professeur.md) | **B13** — le professeur complet : 56 états-Q, il échoue seul, **28/28** |
| [`rapport-pensee-mlp.md`](rapport-pensee-mlp.md) | **B13** — le MLP : 60 poids, l'imitation échoue seule, **27/27** |
| [`rapport-pensee-reseau.md`](rapport-pensee-reseau.md) | **B13** — le réseau linéaire : 12 poids, l'imitation échoue seule, **26/26** |
| [`rapport-pensee-shaping.md`](rapport-pensee-shaping.md) | **B13** — le reward shaping : 56 états-Q, la politique seule échoue encore, **25/25** |
| [`rapport-pensee-minute-entrainee.md`](rapport-pensee-minute-entrainee.md) | **B13** — la Q-table entraînée/minute : 60 états-Q, politique seule échoue, **24/24** |
| [`rapport-pensee-sto-seule.md`](rapport-pensee-sto-seule.md) | **B13** — la politique seule sur le bruit : 8–10 pas, 1–3 essais, 15/15 buts, **19/19** |
| [`rapport-pensee-stochastique.md`](rapport-pensee-stochastique.md) | **B13** — la porte stochastique : 80 %, 30 nœuds/but, sonde 7, **18/18** |
| [`rapport-pensee-seule.md`](rapport-pensee-seule.md) | **B13** — la politique seule : 8 pas, 15/15 buts sans A*, **17/17** |
| [`rapport-pensee-courbe.md`](rapport-pensee-courbe.md) | **B13** — la courbe : 15/15 buts (50–800 épisodes × 3 graines), 30 nœuds, Q 52–83, **16/16** |
| [`rapport-pensee-porte-apprise.md`](rapport-pensee-porte-apprise.md) | **B13** — la porte apprise : Q-table 67 états, 30 nœuds/but, sonde 7, **15/15** |
| [`rapport-pensee-gold-linguistique.md`](rapport-pensee-gold-linguistique.md) | **L/R0.7** — le gold 360 : POS 0,772, exact 0,190/tête 0,510, **attachement tête 1,0/0,966/0,932** (59 ambiguës), pragmatique 1,0/1,0/0,994/0,889 ; neuronal réel refusé |
| [`rapport-bloc-linguistique.md`](rapport-bloc-linguistique.md) | **R0.7** — le bloc linguistique : 9 niveaux, heuristique/neuronal, **398 langues** à 0,9687, activation 51–76 % |
| [`rapport-n2-propre.md`](rapport-n2-propre.md) | **N2.h1** — corpus dédupliqué (**0 %** de fuite) : la chaîne propre vaut **3,09** en domaine, pas 2,85 ; **16,7** sur de la littérature jamais vue |
| [`rapport-n2-diversite.md`](rapport-n2-diversite.md) | **N2.h2** — la diversité française divise la PPL hors dépôt par **4,3** (16,7 → 3,86) pour **+0,17** en domaine |
| [`rapport-n2-longueur.md`](rapport-n2-longueur.md) | **N2.h3** — le verrou de longueur est la **position apprise** : 14,46 → **3,25** à 256 octets ; au-delà, c'est la fenêtre locale |
| [`rapport-n2-capacite.md`](rapport-n2-capacite.md) | **N2.h5** — la capacité (21,65 M) paie **−0,06** en domaine mais ne couvre pas : littérature et longueur inchangées |
| [`rapport-n2-combine.md`](rapport-n2-combine.md) | **N2.h4** — les deux leviers se composent : **3,47** en domaine, **4,10** hors dépôt, **3,49** à 256 octets |
| [`rapport-n2-budget.md`](rapport-n2-budget.md) | **N2.d** — le budget plein paie **2,9355 → 2,8527**, les 4 sources coûtent **+0,91**, et **la validation est contaminée à 32,8 %** (PPL propres **2,9795**) |
| [`rapport-native-prof30k.md`](rapport-native-prof30k.md) | **N2.21** — professeur 30k, lr 3e-6 : PPL **2,823**, dégradation, arrêté |
| `rapport-native-prof20k-6.md` (fiche non écrite) | **N2.23** — professeur 20k, lr 3e-6 : PPL **2,753**, arrêté |
| [`rapport-native-prof20k-8.md`](rapport-native-prof20k-8.md) | **N2.25** — lr 1e-6 : PPL **2,758**, arrêté |
| [`rapport-native-8b-warm.md`](rapport-native-8b-warm.md) | **N2.29** — 8 blocs réchauffés : PPL **2,866**, arrêté |
| [`rapport-native-8b.md`](rapport-native-8b.md) | **N2.28** — 8 blocs : PPL **4,838**, arrêté |
| [`rapport-native-ctx130-2.md`](rapport-native-ctx130-2.md) | **N2.35** — contexte 130 : PPL **2,7149**, négatif |
| [`rapport-native-ctx129-2.md`](rapport-native-ctx129-2.md) | **N2.34** — 129, 10 000 pas de plus : PPL **2,712**, arrêté |
| [`rapport-native-ctx129.md`](rapport-native-ctx129.md) | **N2.33** — contexte 129 : PPL **2,6998**, nouveau meilleur |
| [`rapport-native-ctx130.md`](rapport-native-ctx130.md) | **N2.32** — contexte 130 : PPL **2,786**, arrêté |
| [`rapport-native-ctx136.md`](rapport-native-ctx136.md) | **N2.31** — contexte 136 : PPL **2,974**, arrêté |
| [`rapport-native-ctx160.md`](rapport-native-ctx160.md) | **N2.30** — contexte 160 : PPL **3,804**, arrêté |
| [`rapport-native-ctx256.md`](rapport-native-ctx256.md) | **N2.27** — contexte 256 : PPL **5,675**, arrêté |
| [`rapport-native-local.md`](rapport-native-local.md) | **N2.26** — têtes locales : PPL **2,763**, dégradation |
| [`rapport-native-plafond.md`](rapport-native-plafond.md) | **N2 synthèse** — plafond **2,708**, six essais, porte 2,5 non atteinte |
| [`rapport-native-prof20k-7.md`](rapport-native-prof20k-7.md) | **N2.24** — T=4 : PPL **2,852**, arrêté |
| `rapport-native-prof30k-2.md` (fiche non écrite) | **N2.22** — professeur 30k, lr 1e-5 : PPL **2,828**, arrêté |
| [`rapport-native-prof20k-5.md`](rapport-native-prof20k-5.md) | **N2.19** — 30 000 pas : PPL **2,708**, précision **72,80 %** |
| [`rapport-native-prof20k-4.md`](rapport-native-prof20k-4.md) | **N2.18** — 30 000 pas : PPL **2,714**, précision **72,62 %** |
| [`rapport-native-prof20k-3.md`](rapport-native-prof20k-3.md) | **N2.17** — 30 000 pas : PPL **2,726**, précision **72,34 %** |
| [`rapport-native-prof20k-2.md`](rapport-native-prof20k-2.md) | **N2.16** — 20 000 pas de plus : PPL **2,755**, plateau, tête 3 **72,17 %** |
| [`rapport-native-prof20k.md`](rapport-native-prof20k.md) | **N2.14** — professeur 20k : PPL **2,787**, précision **71,30 %** |
| [`rapport-native-prof10k-2.md`](rapport-native-prof10k-2.md) | **N2.13** — 20 000 pas de plus : PPL **2,876**, précision **70,00 %** |
| [`rapport-native-prof10k.md`](rapport-native-prof10k.md) | **N2.12** — professeur 10k : PPL **2,910** contre **3,082**, tête 3 **69,97 %** |
| [`rapport-native-distillation-50k.md`](rapport-native-distillation-50k.md) | **N2.11** — 50 000 pas : PPL **3,082**, plateau ; tête 3 **68,70 %** |
| [`rapport-native-professeur-30k.md`](rapport-native-professeur-30k.md) | **N2.20** — professeur 30 000 pas : **0,794 bit/octet**, PPL **1,734** |
| [`rapport-native-professeur-20k.md`](rapport-native-professeur-20k.md) | **N2.15** — professeur 20 000 pas : **0,904 bit/octet**, PPL **1,869** |
| [`rapport-native-professeur-10k.md`](rapport-native-professeur-10k.md) | **N2.10** — professeur 10 000 pas : **1,073 bit/octet**, PPL **2,104** |
| [`rapport-native-professeur.md`](rapport-native-professeur.md) | **N2.2** — professeur byte-level 23,76 M : **1,236 bit/octet**, PPL **2,355** |
| [`rapport-native-sft.md`](rapport-native-sft.md) | **N4.6** — SFT minimal : **24/24** vus, **0/4** tenus |
| [`rapport-native-consignes.md`](rapport-native-consignes.md) | **N4.8** — consignes courtes : **0/40** sur mots tenus |
| [`rapport-native-best-2.md`](rapport-native-best-2.md) | **N0.15/N4.7** — meilleur **2,6998** servi : parité native, **650 ms** |
| [`rapport-native-best-service.md`](rapport-native-best-service.md) | **N4.5** — meilleur student **2,708** servi : 53 octets, **589 ms** |
| [`rapport-native-service-auth.md`](rapport-native-service-auth.md) | **N4.4** — service durci : **401/200**, corps 64 Ko, n ≤ 256 ; pas de SFT |
| [`rapport-native-service-rust.md`](rapport-native-service-rust.md) | **N4.3** — service Rust natif avec cache : **611 ms**, 53 octets |
| [`rapport-native-service.md`](rapport-native-service.md) | **N4.2** — service local HTTP : `/sante`, `/generer`, 69 octets, pas de production |
| [`rapport-native-21m-20k.md`](rapport-native-21m-20k.md) | **N2.9** — 21,63 M, 20 000 pas : PPL **3,381**, pire que 11,47 M (**3,123**) |
| [`rapport-native-distillation-20k.md`](rapport-native-distillation-20k.md) | **N2.8** — 20 000 pas : PPL **3,123** contre **3,295**, précision **67,96 %**, gap **+0,768** |
| [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) | les mesures de la couche commune / la synthèse de la nuit |
| [`fiche-nuit-17-10.md`](fiche-nuit-17-10.md) | les mesures de la couche commune / la synthèse de la nuit |
| [`alignement-verne.md`](alignement-verne.md) | l'alignement phrase à phrase du *Tour du monde*, validé aux ancres |
| [`INDEX.md`](INDEX.md) | **A7.5–A7.26** — 22 fiches de cache KV et de grappe réseau ; l'index exhaustif |

## Les données brutes

L'index **exhaustif** des JSON est [`INDEX.md`](INDEX.md) ; les fichiers sont dans ce dossier. Les
principaux agrégats sont :

- [`jeux-mesures.json`](jeux-mesures.json) — 112 surfaces, couverture par niveau, contrôles, pensée ;
- [`jeux-langues-mesures.json`](jeux-langues-mesures.json) — 71 langues, invariance, permutation, notation ;
- [`jeux-maitres-mesures.json`](jeux-maitres-mesures.json) — 17 principes, échecs, dames, go, cartes ;
- [`deepseek-mesures.json`](deepseek-mesures.json) · [`deepseek-mesures-300.json`](deepseek-mesures-300.json) ·
  [`deepseek-natif-300.json`](deepseek-natif-300.json) — le banc externe et la distillation à l'échelle ;
- [`cerveau-mesures.json`](cerveau-mesures.json) — la batterie M1–M9 ;
- [`restitution-mesures.json`](restitution-mesures.json) · [`hybride-mesures.json`](hybride-mesures.json) ·
  [`universaux-mesures.json`](universaux-mesures.json) · [`semantique-mesures.json`](semantique-mesures.json) —
  les blocs B10–B12.

Les JSON de campagne (`traduction-*`, `kfold-*`, `contamination-*`, `pont-*`, `xnli-*`, `plan-*`,
`registre-*`) sont décrits dans la fiche de la mesure correspondante ; [`INDEX.md`](INDEX.md) donne le
titre de chaque fiche.

## Les autres fiches

L'index **exhaustif** et **généré** est [`INDEX.md`](INDEX.md) : une ligne par fiche, triée par nom.
Les fiches qui ne sont pas dans « Les fiches courantes » sont des fiches de campagne, de mesure ou
d'histoire ; on les ouvre par leur **verdict**, pas en entier.

> Les JSON ajoutés après coup sont dans le dossier ; leur description est dans la fiche de la
> mesure correspondante (`reports/INDEX.md` donne le titre de chaque fiche).
