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
| 01 · R | Résumé — les cinq résultats qui comptent, et les manques | 2026-10-09 06:34 HAE (`4836fc8`) | [01-R-resume-les-cinq-resultats-qui-comptent-e.md](campagne-benefices/01-R-resume-les-cinq-resultats-qui-comptent-e.md) |
| 02 · 00 | 0. Le piège qui a failli tout fausser | 2026-10-08 21:32 HAE (`89ae2c3`) | [02-00-le-piege-qui-a-failli-tout-fausser.md](campagne-benefices/02-00-le-piege-qui-a-failli-tout-fausser.md) |
| 03 · 00-bis | 0 bis. Le verdict, famille par famille | 2026-10-08 22:16 HAE (`8343f82`) | [03-00-bis-le-verdict-famille-par-famille.md](campagne-benefices/03-00-bis-le-verdict-famille-par-famille.md) |
| 04 · 01 | 1. Le décodage spéculatif : ×1,2, pas ×2 — mesuré avant d'écrire du moteur | 2026-10-08 22:16 HAE (`8343f82`) | [04-01-le-decodage-speculatif-1-2-pas-2-mesure.md](campagne-benefices/04-01-le-decodage-speculatif-1-2-pas-2-mesure.md) |
| 05 · 02 | 2. Les deux familles de tâches que Drave ne couvre pas | 2026-10-08 21:32 HAE (`89ae2c3`) | [05-02-les-deux-familles-de-taches-que-drave-ne.md](campagne-benefices/05-02-les-deux-familles-de-taches-que-drave-ne.md) |
| 06 · 03 | 3. La grille de modèles — « ce modèle tourne-t-il, et à quel prix ? » | 2026-10-08 21:32 HAE (`89ae2c3`) | [06-03-la-grille-de-modeles-ce-modele-tourne-t.md](campagne-benefices/06-03-la-grille-de-modeles-ce-modele-tourne-t.md) |
| 07 · 04 | 4. Ce que le dépôt sait déjà, par famille de tâches (avant cette campagne) | 2026-10-08 21:47 HAE (`f7bb054`) | [07-04-ce-que-le-depot-sait-deja-par-famille-de.md](campagne-benefices/07-04-ce-que-le-depot-sait-deja-par-famille-de.md) |
| 08 · 05 | 5. Les modèles entraînés ici, mesurés DANS le moteur — ce que le routage et la distillation rapportent | 2026-10-09 02:31 HAE (`1530bee`) | [08-05-les-modeles-entraines-ici-mesures-dans-l.md](campagne-benefices/08-05-les-modeles-entraines-ici-mesures-dans-l.md) |
| 09 · 07 | 7. Répartir par EXPERTS : ce que coûterait l'unité de travail naturelle | 2026-10-08 21:57 HAE (`1e11cc7`) | [09-07-repartir-par-experts-ce-que-couterait-lu.md](campagne-benefices/09-07-repartir-par-experts-ce-que-couterait-lu.md) |
| 10 · 08 | 8. Les tâches à SORTIE CONTRAINTE : une matrice qu'on ne lit pas | 2026-10-08 22:03 HAE (`6379e49`) | [10-08-les-taches-a-sortie-contrainte-une-matri.md](campagne-benefices/10-08-les-taches-a-sortie-contrainte-une-matri.md) |
| 11 · 09 | 9. La mémoire TIENT : l'aiguille est retrouvée à toutes les profondeurs | 2026-10-08 22:04 HAE (`2d57177`) | [11-09-la-memoire-tient-laiguille-est-retrouvee.md](campagne-benefices/11-09-la-memoire-tient-laiguille-est-retrouvee.md) |
| 12 · 10 | 10. La génération : TTFT et débit, mesure directe | 2026-10-08 22:04 HAE (`2d57177`) | [12-10-la-generation-ttft-et-debit-mesure-direc.md](campagne-benefices/12-10-la-generation-ttft-et-debit-mesure-direc.md) |
| 13 · 10-bis | 10 bis. Quatre tâches, sorties verbatim — et c'est le MODÈLE qui limite, pas le moteur | 2026-10-08 22:49 HAE (`d82f01a`) | [13-10-bis-quatre-taches-sorties-verbatim-et-cest-l.md](campagne-benefices/13-10-bis-quatre-taches-sorties-verbatim-et-cest-l.md) |
| 14 · 10-ter | 10 ter. La densité d'activation ne dépend PAS de la tâche — la qualité, si | 2026-10-08 23:03 HAE (`a8a4cdd`) | [14-10-ter-la-densite-dactivation-ne-depend-pas-de.md](campagne-benefices/14-10-ter-la-densite-dactivation-ne-depend-pas-de.md) |
| 15 · 12 | 12. Le cas extrême : **365,7 Go sur une machine de 125 Go** | 2026-10-08 23:27 HAE (`8db69e8`) | [15-12-le-cas-extreme-365-7-go-sur-une-machine.md](campagne-benefices/15-12-le-cas-extreme-365-7-go-sur-une-machine.md) |
| 16 · 13 | 13. La tête restreinte, sur deux modèles de plus | 2026-10-08 23:27 HAE (`8db69e8`) | [16-13-la-tete-restreinte-sur-deux-modeles-de-p.md](campagne-benefices/16-13-la-tete-restreinte-sur-deux-modeles-de-p.md) |
| 17 · 14 | 14. Une mesure à refaire : le lot sur le 30B a mesuré le cache de pages | 2026-10-08 23:27 HAE (`8db69e8`) | [17-14-une-mesure-a-refaire-le-lot-sur-le-30b-a.md](campagne-benefices/17-14-une-mesure-a-refaire-le-lot-sur-le-30b-a.md) |
| 18 · 16 | 16. Deux pièges de méthode, consignés | 2026-10-08 23:38 HAE (`bab38c7`) | [18-16-deux-pieges-de-methode-consignes.md](campagne-benefices/18-16-deux-pieges-de-methode-consignes.md) |
| 19 · 17 | 17. L'instrument : le binaire de la campagne était plus VIEUX que ses correctifs | 2026-10-09 01:55 HAE (`69cf405`) | [19-17-linstrument-le-binaire-de-la-campagne-et.md](campagne-benefices/19-17-linstrument-le-binaire-de-la-campagne-et.md) |
| 20 · 18 | 18. Le résultat publié SURVIT au correctif d'échelle (sémantique multilingue) | 2026-10-08 23:54 HAE (`baeb2c6`) | [20-18-le-resultat-publie-survit-au-correctif-d.md](campagne-benefices/20-18-le-resultat-publie-survit-au-correctif-d.md) |
| 21 · 19 | 19. La parcimonie imposée, sur 24 réglages : le k-WTA écrase le seuil, encore | 2026-10-08 23:56 HAE (`dedeba5`) | [21-19-la-parcimonie-imposee-sur-24-reglages-le.md](campagne-benefices/21-19-la-parcimonie-imposee-sur-24-reglages-le.md) |
| 22 · 20 | 20. Contexte et lots : deux réponses, dont une qui n'est pas celle qu'on croit | 2026-10-09 00:06 HAE (`f9ca016`) | [22-20-contexte-et-lots-deux-reponses-dont-une.md](campagne-benefices/22-20-contexte-et-lots-deux-reponses-dont-une.md) |
| 23 · 21 | 21. Le noyau, re-mesuré : le croisement est là, et il coûte à densité 1 | 2026-10-09 01:55 HAE (`69cf405`) | [23-21-le-noyau-re-mesure-le-croisement-est-la.md](campagne-benefices/23-21-le-noyau-re-mesure-le-croisement-est-la.md) |
| 24 · 22 | 22. Les listes ne calculent pas une approximation : les logits sont identiques AU BIT PRÈS | 2026-10-09 01:55 HAE (`69cf405`) | [24-22-les-listes-ne-calculent-pas-une-approxim.md](campagne-benefices/24-22-les-listes-ne-calculent-pas-une-approxim.md) |
| 25 · 22-bis | 22 bis. Ce que le nouveau matériel change, d'après ces mesures | 2026-10-09 07:33 HAE (`838c511`) | [25-22-bis-ce-que-le-nouveau-materiel-change-dapres.md](campagne-benefices/25-22-bis-ce-que-le-nouveau-materiel-change-dapres.md) |
| 26 · 23 | 23. Ce qui reste à mesurer (état de la file, 9 octobre 16 h) | 2026-10-09 15:55 HAE (`505ed18`) | [26-23-ce-qui-reste-a-mesurer-etat-de-la-file-9.md](campagne-benefices/26-23-ce-qui-reste-a-mesurer-etat-de-la-file-9.md) |
| 27 · 24 | 24. Mémoire épisodique (C6) : ce qui marche, et ce qui ne marche PAS | 2026-10-09 22:30 HAE (`7d7837e`) | [27-24-memoire-episodique-c6-ce-qui-marche-et-c.md](campagne-benefices/27-24-memoire-episodique-c6-ce-qui-marche-et-c.md) |
| 28 · 25 | 25. Le pont entre deux régions (C9/C10) : combien de fibres, et à quel prix | 2026-10-09 23:20 HAE (`00b021f`) | [28-25-le-pont-entre-deux-regions-c9-c10-combie.md](campagne-benefices/28-25-le-pont-entre-deux-regions-c9-c10-combie.md) |
| 29 · 26 | 26. Le réflexe (C8) : un chemin court qui ne sait RIEN, et pourquoi | 2026-10-09 23:39 HAE (`f8ac10e`) | [29-26-le-reflexe-c8-un-chemin-court-qui-ne-sai.md](campagne-benefices/29-26-le-reflexe-c8-un-chemin-court-qui-ne-sai.md) |
| 30 · 27 | 27. OÙ COUPER le modèle ? Le point de coupe est neutre — sauf à cause du lien | 2026-10-09 23:48 HAE (`22d6151`) | [30-27-ou-couper-le-modele-le-point-de-coupe-es.md](campagne-benefices/30-27-ou-couper-le-modele-le-point-de-coupe-es.md) |
| 31 · 28 | 28. La greffe d'état (C2/C6) : elle TRANSFÈRE le contenu — ma première conclusion était fausse | 2026-10-10 03:39 HAE (`b5d5fe9`) | [31-28-la-greffe-detat-c2-c6-elle-transfere-le.md](campagne-benefices/31-28-la-greffe-detat-c2-c6-elle-transfere-le.md) |
| 32 · 29 | 29. La mémoire QUI SERT : retrieval → injection, de bout en bout | 2026-10-10 04:20 HAE (`089c52a`) | [32-29-la-memoire-qui-sert-retrieval-injection.md](campagne-benefices/32-29-la-memoire-qui-sert-retrieval-injection.md) |
| 33 · 30 | 30. Le rappel par le contenu dépend de l'INDICE, pas de la mémoire (8 indices) | 2026-10-10 04:56 HAE (`b21f715`) | [33-30-le-rappel-par-le-contenu-depend-de-lindi.md](campagne-benefices/33-30-le-rappel-par-le-contenu-depend-de-lindi.md) |
| 34 · 31 | 31. Clé de FENÊTRE : la prédiction est RÉFUTÉE, et elle confirme la leçon du §24 quater | 2026-10-10 05:44 HAE (`892acfd`) | [34-31-cle-de-fenetre-la-prediction-est-refutee.md](campagne-benefices/34-31-cle-de-fenetre-la-prediction-est-refutee.md) |
| 35 · 32 | 32. Budget d'octets par lien (C10) : déclaré, et vérifié sur ce qui PASSE | 2026-10-10 05:48 HAE (`203872a`) | [35-32-budget-doctets-par-lien-c10-declare-et-v.md](campagne-benefices/35-32-budget-doctets-par-lien-c10-declare-et-v.md) |
| 36 · 33 | 33. Pannes de lien (C11) : nommées, avec un code distinct, et sans résultat partiel | 2026-10-10 05:56 HAE (`619b940`) | [36-33-pannes-de-lien-c11-nommees-avec-un-code.md](campagne-benefices/36-33-pannes-de-lien-c11-nommees-avec-un-code.md) |
| 37 · 34 | 34. La porte rouge de répartition : un DÉFAUT DE PORTE, pas un défaut du modèle | 2026-10-10 07:21 HAE (`c43425e`) | [37-34-la-porte-rouge-de-repartition-un-defaut.md](campagne-benefices/37-34-la-porte-rouge-de-repartition-un-defaut.md) |
| 38 · 35 | 35. Découverte : le registre des régions (C11) | 2026-10-10 07:25 HAE (`b1b63b0`) | [38-35-decouverte-le-registre-des-regions-c11.md](campagne-benefices/38-35-decouverte-le-registre-des-regions-c11.md) |
| 39 · 36 | 36. Balayage des portes : le piège de fenêtre était LATENT dans une deuxième porte | 2026-10-10 07:27 HAE (`dee9e58`) | [39-36-balayage-des-portes-le-piege-de-fenetre.md](campagne-benefices/39-36-balayage-des-portes-le-piege-de-fenetre.md) |
| 40 · 37 | 37. E4 — l'équilibre excitation/inhibition : l'hypothèse est VRAIE dans un sens seulement | 2026-10-10 07:39 HAE (`d104da6`) | [40-37-e4-lequilibre-excitation-inhibition-lhyp.md](campagne-benefices/40-37-e4-lequilibre-excitation-inhibition-lhyp.md) |
| 41 · 38 | 38. Un drapeau qui ne faisait RIEN dans le chemin réparti (`--ffn-gain`) | 2026-10-10 08:09 HAE (`719ab85`) | [41-38-un-drapeau-qui-ne-faisait-rien-dans-le-c.md](campagne-benefices/41-38-un-drapeau-qui-ne-faisait-rien-dans-le-c.md) |
| 42 · 39 | 39. Audit des drapeaux par CHEMIN : une méthode de criblage, et sa portée exacte | 2026-10-10 08:10 HAE (`39d32f3`) | [42-39-audit-des-drapeaux-par-chemin-une-method.md](campagne-benefices/42-39-audit-des-drapeaux-par-chemin-une-method.md) |
| 43 · 40 | 40. Protocole v7 : la fenêtre d'attention voyage, et le refus disparaît | 2026-10-10 08:44 HAE (`dd66191`) | [43-40-protocole-v7-la-fenetre-dattention-voyag.md](campagne-benefices/43-40-protocole-v7-la-fenetre-dattention-voyag.md) |
| 44 · 41 | 41. Protocole v8 : le pilote sait enfin ce que coûte la moitié distante | 2026-10-10 09:01 HAE (`e22dbd7`) | [44-41-protocole-v8-le-pilote-sait-enfin-ce-que.md](campagne-benefices/44-41-protocole-v8-le-pilote-sait-enfin-ce-que.md) |
| 45 · 42 | 42. C10 CLOS : trois budgets, trois codes — octets (6), latence (8), paires (9) | 2026-10-10 09:10 HAE (`4767b22`) | [45-42-c10-clos-trois-budgets-trois-codes-octet.md](campagne-benefices/45-42-c10-clos-trois-budgets-trois-codes-octet.md) |
| 46 · 43 | 43. L'instrument de trace est CALIBRÉ : 50 ms injectés, 50,2 ms mesurés | 2026-10-10 09:11 HAE (`4367099`) | [46-43-linstrument-de-trace-est-calibre-50-ms-i.md](campagne-benefices/46-43-linstrument-de-trace-est-calibre-50-ms-i.md) |
| 47 · 44 | 44. La GIGUE d'un pas réparti : 7 ms sur 17,7 — ce qu'un ordonnanceur doit tolérer | 2026-10-10 09:12 HAE (`d09f78c`) | [47-44-la-gigue-dun-pas-reparti-7-ms-sur-17-7-c.md](campagne-benefices/47-44-la-gigue-dun-pas-reparti-7-ms-sur-17-7-c.md) |
| 48 · 45 | 45. Combien de MESSAGES coûte un pas ? Quatre — et c'est l'en-tête écrit à part | 2026-10-10 09:15 HAE (`656a65f`) | [48-45-combien-de-messages-coute-un-pas-quatre.md](campagne-benefices/48-45-combien-de-messages-coute-un-pas-quatre.md) |
| 49 · 46 | 46. Inventaire des drapeaux en chemin RÉPARTI : cinq agissent, trois sont inertes | 2026-10-10 09:39 HAE (`63203d7`) | [49-46-inventaire-des-drapeaux-en-chemin-repart.md](campagne-benefices/49-46-inventaire-des-drapeaux-en-chemin-repart.md) |
| 50 · 47 | 47. `--attn-sinks` : le drapeau VIT, mais seulement avec une fenêtre — et « 0 » n'existait pas | 2026-10-10 10:07 HAE (`85cf49c`) | [50-47-attn-sinks-le-drapeau-vit-mais-seulement.md](campagne-benefices/50-47-attn-sinks-le-drapeau-vit-mais-seulement.md) |
| 51 · R | Annexe — manifeste des journaux | 2026-10-09 15:34 HAE (`8015c64`) | [51-R-annexe-manifeste-des-journaux.md](campagne-benefices/51-R-annexe-manifeste-des-journaux.md) |

**Les estampilles écrites dans le corps des textes ne sont pas fiables** : elles ont été
saisies à la main en avançant une horloge supposée, et certaines tombaient **dans le
futur** (jusqu'au 12 octobre 2026). La date fiable est celle de l'en-tête de chaque
fichier, tirée de git. Voir `docs/organisation-du-depot.md` § 4.
