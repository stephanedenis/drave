# Campagne 24 h — où Drave est à son meilleur, tâche par tâche

> 08/10 21 h → 09/10. Rapport **vivant** : il est mis à jour au fil des étapes.
> File : `tools/campagne-benefices.sh`. Journaux bruts : `/tmp/campagne24/`.
> Plan : `docs/campagne-benefices.md`.
>
> Règle de lecture : chaque chiffre porte ses conditions (corpus, tokenizer,
> charge de fond). La charge a oscillé entre 3 et 18 pendant la campagne
> (entraînements en parallèle) — les mesures **déterministes** (perplexité,
> comptes d'événements) n'en dépendent pas, les **temps** oui, et c'est écrit.

---

## Index des expériences

| # | expérience | date réelle (git) | fichier |
|---|---|---|---|
| 001 · R | Résumé — les cinq résultats qui comptent, et les manques | 2026-10-10 10:18 HAE (`4a8cac9`) | [001-R-resume-les-cinq-resultats-qui-comptent-e.md](campagne-benefices/001-R-resume-les-cinq-resultats-qui-comptent-e.md) |
| 002 · 00 | 0. Le piège qui a failli tout fausser | 2026-10-10 10:18 HAE (`4a8cac9`) | [002-00-le-piege-qui-a-failli-tout-fausser.md](campagne-benefices/002-00-le-piege-qui-a-failli-tout-fausser.md) |
| 003 · 00-bis | 0 bis. Le verdict, famille par famille | 2026-10-10 10:18 HAE (`4a8cac9`) | [003-00-bis-le-verdict-famille-par-famille.md](campagne-benefices/003-00-bis-le-verdict-famille-par-famille.md) |
| 004 · 01 | 1. Le décodage spéculatif : ×1,2, pas ×2 — mesuré avant d'écrire du moteur | 2026-10-10 10:18 HAE (`4a8cac9`) | [004-01-le-decodage-speculatif-1-2-pas-2-mesure.md](campagne-benefices/004-01-le-decodage-speculatif-1-2-pas-2-mesure.md) |
| 005 · 02 | 2. Les deux familles de tâches que Drave ne couvre pas | 2026-10-10 10:18 HAE (`4a8cac9`) | [005-02-les-deux-familles-de-taches-que-drave-ne.md](campagne-benefices/005-02-les-deux-familles-de-taches-que-drave-ne.md) |
| 006 · 03 | 3. La grille de modèles — « ce modèle tourne-t-il, et à quel prix ? » | 2026-10-10 10:18 HAE (`4a8cac9`) | [006-03-la-grille-de-modeles-ce-modele-tourne-t.md](campagne-benefices/006-03-la-grille-de-modeles-ce-modele-tourne-t.md) |
| 007 · 04 | 4. Ce que le dépôt sait déjà, par famille de tâches (avant cette campagne) | 2026-10-10 10:18 HAE (`4a8cac9`) | [007-04-ce-que-le-depot-sait-deja-par-famille-de.md](campagne-benefices/007-04-ce-que-le-depot-sait-deja-par-famille-de.md) |
| 008 · 05 | 5. Les modèles entraînés ici, mesurés DANS le moteur — ce que le routage et la distillation rapportent | 2026-10-10 10:18 HAE (`4a8cac9`) | [008-05-les-modeles-entraines-ici-mesures-dans-l.md](campagne-benefices/008-05-les-modeles-entraines-ici-mesures-dans-l.md) |
| 009 · 07 | 7. Répartir par EXPERTS : ce que coûterait l'unité de travail naturelle | 2026-10-10 10:18 HAE (`4a8cac9`) | [009-07-repartir-par-experts-ce-que-couterait-lu.md](campagne-benefices/009-07-repartir-par-experts-ce-que-couterait-lu.md) |
| 010 · 08 | 8. Les tâches à SORTIE CONTRAINTE : une matrice qu'on ne lit pas | 2026-10-10 10:18 HAE (`4a8cac9`) | [010-08-les-taches-a-sortie-contrainte-une-matri.md](campagne-benefices/010-08-les-taches-a-sortie-contrainte-une-matri.md) |
| 011 · 09 | 9. La mémoire TIENT : l'aiguille est retrouvée à toutes les profondeurs | 2026-10-10 10:18 HAE (`4a8cac9`) | [011-09-la-memoire-tient-laiguille-est-retrouvee.md](campagne-benefices/011-09-la-memoire-tient-laiguille-est-retrouvee.md) |
| 012 · 10 | 10. La génération : TTFT et débit, mesure directe | 2026-10-10 10:18 HAE (`4a8cac9`) | [012-10-la-generation-ttft-et-debit-mesure-direc.md](campagne-benefices/012-10-la-generation-ttft-et-debit-mesure-direc.md) |
| 013 · 10-bis | 10 bis. Quatre tâches, sorties verbatim — et c'est le MODÈLE qui limite, pas le moteur | 2026-10-10 10:18 HAE (`4a8cac9`) | [013-10-bis-quatre-taches-sorties-verbatim-et-cest-l.md](campagne-benefices/013-10-bis-quatre-taches-sorties-verbatim-et-cest-l.md) |
| 014 · 10-ter | 10 ter. La densité d'activation ne dépend PAS de la tâche — la qualité, si | 2026-10-10 10:18 HAE (`4a8cac9`) | [014-10-ter-la-densite-dactivation-ne-depend-pas-de.md](campagne-benefices/014-10-ter-la-densite-dactivation-ne-depend-pas-de.md) |
| 015 · 12 | 12. Le cas extrême : **365,7 Go sur une machine de 125 Go** | 2026-10-10 10:18 HAE (`4a8cac9`) | [015-12-le-cas-extreme-365-7-go-sur-une-machine.md](campagne-benefices/015-12-le-cas-extreme-365-7-go-sur-une-machine.md) |
| 016 · 13 | 13. La tête restreinte, sur deux modèles de plus | 2026-10-10 10:18 HAE (`4a8cac9`) | [016-13-la-tete-restreinte-sur-deux-modeles-de-p.md](campagne-benefices/016-13-la-tete-restreinte-sur-deux-modeles-de-p.md) |
| 017 · 14 | 14. Une mesure à refaire : le lot sur le 30B a mesuré le cache de pages | 2026-10-10 10:18 HAE (`4a8cac9`) | [017-14-une-mesure-a-refaire-le-lot-sur-le-30b-a.md](campagne-benefices/017-14-une-mesure-a-refaire-le-lot-sur-le-30b-a.md) |
| 018 · 16 | 16. Deux pièges de méthode, consignés | 2026-10-10 10:18 HAE (`4a8cac9`) | [018-16-deux-pieges-de-methode-consignes.md](campagne-benefices/018-16-deux-pieges-de-methode-consignes.md) |
| 019 · 17 | 17. L'instrument : le binaire de la campagne était plus VIEUX que ses correctifs | 2026-10-10 10:18 HAE (`4a8cac9`) | [019-17-linstrument-le-binaire-de-la-campagne-et.md](campagne-benefices/019-17-linstrument-le-binaire-de-la-campagne-et.md) |
| 020 · 18 | 18. Le résultat publié SURVIT au correctif d'échelle (sémantique multilingue) | 2026-10-10 10:18 HAE (`4a8cac9`) | [020-18-le-resultat-publie-survit-au-correctif-d.md](campagne-benefices/020-18-le-resultat-publie-survit-au-correctif-d.md) |
| 021 · 19 | 19. La parcimonie imposée, sur 24 réglages : le k-WTA écrase le seuil, encore | 2026-10-10 10:18 HAE (`4a8cac9`) | [021-19-la-parcimonie-imposee-sur-24-reglages-le.md](campagne-benefices/021-19-la-parcimonie-imposee-sur-24-reglages-le.md) |
| 022 · 20 | 20. Contexte et lots : deux réponses, dont une qui n'est pas celle qu'on croit | 2026-10-10 10:18 HAE (`4a8cac9`) | [022-20-contexte-et-lots-deux-reponses-dont-une.md](campagne-benefices/022-20-contexte-et-lots-deux-reponses-dont-une.md) |
| 023 · 21 | 21. Le noyau, re-mesuré : le croisement est là, et il coûte à densité 1 | 2026-10-10 10:18 HAE (`4a8cac9`) | [023-21-le-noyau-re-mesure-le-croisement-est-la.md](campagne-benefices/023-21-le-noyau-re-mesure-le-croisement-est-la.md) |
| 024 · 22 | 22. Les listes ne calculent pas une approximation : les logits sont identiques AU BIT PRÈS | 2026-10-10 10:18 HAE (`4a8cac9`) | [024-22-les-listes-ne-calculent-pas-une-approxim.md](campagne-benefices/024-22-les-listes-ne-calculent-pas-une-approxim.md) |
| 025 · 22-bis | 22 bis. Ce que le nouveau matériel change, d'après ces mesures | 2026-10-10 10:18 HAE (`4a8cac9`) | [025-22-bis-ce-que-le-nouveau-materiel-change-dapres.md](campagne-benefices/025-22-bis-ce-que-le-nouveau-materiel-change-dapres.md) |
| 026 · 23 | 23. Ce qui reste à mesurer (état de la file, 9 octobre 16 h) | 2026-10-10 10:18 HAE (`4a8cac9`) | [026-23-ce-qui-reste-a-mesurer-etat-de-la-file-9.md](campagne-benefices/026-23-ce-qui-reste-a-mesurer-etat-de-la-file-9.md) |
| 027 · 24 | 24. Mémoire épisodique (C6) : ce qui marche, et ce qui ne marche PAS | 2026-10-10 10:18 HAE (`4a8cac9`) | [027-24-memoire-episodique-c6-ce-qui-marche-et-c.md](campagne-benefices/027-24-memoire-episodique-c6-ce-qui-marche-et-c.md) |
| 028 · 25 | 25. Le pont entre deux régions (C9/C10) : combien de fibres, et à quel prix | 2026-10-10 10:18 HAE (`4a8cac9`) | [028-25-le-pont-entre-deux-regions-c9-c10-combie.md](campagne-benefices/028-25-le-pont-entre-deux-regions-c9-c10-combie.md) |
| 029 · 26 | 26. Le réflexe (C8) : un chemin court qui ne sait RIEN, et pourquoi | 2026-10-10 10:18 HAE (`4a8cac9`) | [029-26-le-reflexe-c8-un-chemin-court-qui-ne-sai.md](campagne-benefices/029-26-le-reflexe-c8-un-chemin-court-qui-ne-sai.md) |
| 030 · 27 | 27. OÙ COUPER le modèle ? Le point de coupe est neutre — sauf à cause du lien | 2026-10-10 10:18 HAE (`4a8cac9`) | [030-27-ou-couper-le-modele-le-point-de-coupe-es.md](campagne-benefices/030-27-ou-couper-le-modele-le-point-de-coupe-es.md) |
| 031 · 28 | 28. La greffe d'état (C2/C6) : elle TRANSFÈRE le contenu — ma première conclusion était fausse | 2026-10-10 10:18 HAE (`4a8cac9`) | [031-28-la-greffe-detat-c2-c6-elle-transfere-le.md](campagne-benefices/031-28-la-greffe-detat-c2-c6-elle-transfere-le.md) |
| 032 · 29 | 29. La mémoire QUI SERT : retrieval → injection, de bout en bout | 2026-10-10 10:18 HAE (`4a8cac9`) | [032-29-la-memoire-qui-sert-retrieval-injection.md](campagne-benefices/032-29-la-memoire-qui-sert-retrieval-injection.md) |
| 033 · 30 | 30. Le rappel par le contenu dépend de l'INDICE, pas de la mémoire (8 indices) | 2026-10-10 10:18 HAE (`4a8cac9`) | [033-30-le-rappel-par-le-contenu-depend-de-lindi.md](campagne-benefices/033-30-le-rappel-par-le-contenu-depend-de-lindi.md) |
| 034 · 31 | 31. Clé de FENÊTRE : la prédiction est RÉFUTÉE, et elle confirme la leçon du §24 quater | 2026-10-10 10:18 HAE (`4a8cac9`) | [034-31-cle-de-fenetre-la-prediction-est-refutee.md](campagne-benefices/034-31-cle-de-fenetre-la-prediction-est-refutee.md) |
| 035 · 32 | 32. Budget d'octets par lien (C10) : déclaré, et vérifié sur ce qui PASSE | 2026-10-10 10:18 HAE (`4a8cac9`) | [035-32-budget-doctets-par-lien-c10-declare-et-v.md](campagne-benefices/035-32-budget-doctets-par-lien-c10-declare-et-v.md) |
| 036 · 33 | 33. Pannes de lien (C11) : nommées, avec un code distinct, et sans résultat partiel | 2026-10-10 10:18 HAE (`4a8cac9`) | [036-33-pannes-de-lien-c11-nommees-avec-un-code.md](campagne-benefices/036-33-pannes-de-lien-c11-nommees-avec-un-code.md) |
| 037 · 34 | 34. La porte rouge de répartition : un DÉFAUT DE PORTE, pas un défaut du modèle | 2026-10-10 10:18 HAE (`4a8cac9`) | [037-34-la-porte-rouge-de-repartition-un-defaut.md](campagne-benefices/037-34-la-porte-rouge-de-repartition-un-defaut.md) |
| 038 · 35 | 35. Découverte : le registre des régions (C11) | 2026-10-10 10:18 HAE (`4a8cac9`) | [038-35-decouverte-le-registre-des-regions-c11.md](campagne-benefices/038-35-decouverte-le-registre-des-regions-c11.md) |
| 039 · 36 | 36. Balayage des portes : le piège de fenêtre était LATENT dans une deuxième porte | 2026-10-10 10:18 HAE (`4a8cac9`) | [039-36-balayage-des-portes-le-piege-de-fenetre.md](campagne-benefices/039-36-balayage-des-portes-le-piege-de-fenetre.md) |
| 040 · 37 | 37. E4 — l'équilibre excitation/inhibition : l'hypothèse est VRAIE dans un sens seulement | 2026-10-10 10:18 HAE (`4a8cac9`) | [040-37-e4-lequilibre-excitation-inhibition-lhyp.md](campagne-benefices/040-37-e4-lequilibre-excitation-inhibition-lhyp.md) |
| 041 · 38 | 38. Un drapeau qui ne faisait RIEN dans le chemin réparti (`--ffn-gain`) | 2026-10-10 10:18 HAE (`4a8cac9`) | [041-38-un-drapeau-qui-ne-faisait-rien-dans-le-c.md](campagne-benefices/041-38-un-drapeau-qui-ne-faisait-rien-dans-le-c.md) |
| 042 · 39 | 39. Audit des drapeaux par CHEMIN : une méthode de criblage, et sa portée exacte | 2026-10-10 10:18 HAE (`4a8cac9`) | [042-39-audit-des-drapeaux-par-chemin-une-method.md](campagne-benefices/042-39-audit-des-drapeaux-par-chemin-une-method.md) |
| 043 · 40 | 40. Protocole v7 : la fenêtre d'attention voyage, et le refus disparaît | 2026-10-10 10:18 HAE (`4a8cac9`) | [043-40-protocole-v7-la-fenetre-dattention-voyag.md](campagne-benefices/043-40-protocole-v7-la-fenetre-dattention-voyag.md) |
| 044 · 41 | 41. Protocole v8 : le pilote sait enfin ce que coûte la moitié distante | 2026-10-10 10:18 HAE (`4a8cac9`) | [044-41-protocole-v8-le-pilote-sait-enfin-ce-que.md](campagne-benefices/044-41-protocole-v8-le-pilote-sait-enfin-ce-que.md) |
| 045 · 42 | 42. C10 CLOS : trois budgets, trois codes — octets (6), latence (8), paires (9) | 2026-10-10 10:18 HAE (`4a8cac9`) | [045-42-c10-clos-trois-budgets-trois-codes-octet.md](campagne-benefices/045-42-c10-clos-trois-budgets-trois-codes-octet.md) |
| 046 · 43 | 43. L'instrument de trace est CALIBRÉ : 50 ms injectés, 50,2 ms mesurés | 2026-10-10 10:18 HAE (`4a8cac9`) | [046-43-linstrument-de-trace-est-calibre-50-ms-i.md](campagne-benefices/046-43-linstrument-de-trace-est-calibre-50-ms-i.md) |
| 047 · 44 | 44. La GIGUE d'un pas réparti : 7 ms sur 17,7 — ce qu'un ordonnanceur doit tolérer | 2026-10-10 10:18 HAE (`4a8cac9`) | [047-44-la-gigue-dun-pas-reparti-7-ms-sur-17-7-c.md](campagne-benefices/047-44-la-gigue-dun-pas-reparti-7-ms-sur-17-7-c.md) |
| 048 · 45 | 45. Combien de MESSAGES coûte un pas ? Quatre — et c'est l'en-tête écrit à part | 2026-10-10 10:18 HAE (`4a8cac9`) | [048-45-combien-de-messages-coute-un-pas-quatre.md](campagne-benefices/048-45-combien-de-messages-coute-un-pas-quatre.md) |
| 049 · 46 | 46. Inventaire des drapeaux en chemin RÉPARTI : cinq agissent, trois sont inertes | 2026-10-10 10:18 HAE (`4a8cac9`) | [049-46-inventaire-des-drapeaux-en-chemin-repart.md](campagne-benefices/049-46-inventaire-des-drapeaux-en-chemin-repart.md) |
| 050 · 47 | 47. `--attn-sinks` : le drapeau VIT, mais seulement avec une fenêtre — et « 0 » n'existait pas | 2026-10-10 10:18 HAE (`4a8cac9`) | [050-47-attn-sinks-le-drapeau-vit-mais-seulement.md](campagne-benefices/050-47-attn-sinks-le-drapeau-vit-mais-seulement.md) |
| 051 · R | Annexe — manifeste des journaux | 2026-10-10 10:18 HAE (`4a8cac9`) | [051-R-annexe-manifeste-des-journaux.md](campagne-benefices/051-R-annexe-manifeste-des-journaux.md) |

**Les estampilles écrites dans le corps des textes ne sont pas fiables** : elles ont été
saisies à la main en avançant une horloge supposée, et certaines tombaient **dans le
futur** (jusqu'au 12 octobre 2026). La date fiable est celle de l'en-tête de chaque
fichier, tirée de git. Voir `docs/organisation-du-depot.md` § 4.
