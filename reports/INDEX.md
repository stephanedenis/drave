# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **178 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
| [aiguille-gpt-oss.md](aiguille-gpt-oss.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf |
| [alignement-verne.md](alignement-verne.md) | Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais) |
| [bilan-b11.md](bilan-b11.md) | Bilan B11 — ce qui tient, ce qui ne tient pas |
| [bilan-multi-materiel.md](bilan-multi-materiel.md) | Bilan multi-matériel — CPU, FPGA, GPU |
| [campagne-benefices.md](campagne-benefices.md) | Campagne 24 h — où Drave est à son meilleur, tâche par tâche |
| [fiche-nuit-17-10.md](fiche-nuit-17-10.md) | La nuit du 17 au 18 octobre : la couche commune entrée-sortie, de 2 langues à 448 |
| [rapport-32b-couche-confondant.md](rapport-32b-couche-confondant.md) | Le 32 B : le pont à 0,49 — et le confondant de la couche relative |
| [rapport-8bits.md](rapport-8bits.md) | Drave — 8 bits : la perfection est-elle atteignable ? |
| [rapport-aiguille-topk.md](rapport-aiguille-topk.md) | Rapport — l'attention creuse perd-elle l'information ? (aiguille × `--attn-topk`) |
| [rapport-aiguille.md](rapport-aiguille.md) | L'aiguille dans la botte de foin : où en est la mesure de qualité |
| [rapport-analyse-flux.md](rapport-analyse-flux.md) | Analyse du flux, couche par couche |
| [rapport-architecture-memoire.md](rapport-architecture-memoire.md) | Rapport — architecture mémoire : ce qui va en VRAM, en RAM, et sur le disque |
| [rapport-attention-creuse.md](rapport-attention-creuse.md) | Attention creuse — le trou se referme, et par le haut |
| [rapport-attribution-kv.md](rapport-attribution-kv.md) | Phase 1.4 — l'écart du cache KV int8 est ENTIÈREMENT dû aux clés |
| [rapport-budget-attention-allocation.md](rapport-budget-attention-allocation.md) | Où dépenser le budget d'attention — uniforme ou sur la moitié des couches ? (second ordre) |
| [rapport-budget-decision.md](rapport-budget-decision.md) | Le budget d'une DÉCISION — deux monnaies, et la métrique du plan n'en voit qu'une |
| [rapport-budget-kimi-k3.md](rapport-budget-kimi-k3.md) | Kimi-K3 Q4 : ce qu'un jeton lit vraiment, et ce que ça impose |
| [rapport-c2-recurrence.md](rapport-c2-recurrence.md) | C2 — la récurrence (boucle sur soi) : la boucle existe, elle est bornée… et elle DÉGRADE la lisibilité |
| [rapport-c4-retard.md](rapport-c4-retard.md) | C4 — le prix d'un état en retard : **×633 pour UN pas**, et ce que ça impose à un ordonnanceur |
| [rapport-c8-echelle.md](rapport-c8-echelle.md) | C8 à l'échelle : la courbe monte encore, mais plus de capacité NUIT — la limite est la donnée |
| [rapport-c8-generalisation.md](rapport-c8-generalisation.md) | C8 — la tête réflexe sur des textes JAMAIS VUS : jusqu'à ×5,7 du modèle complet |
| [rapport-c8-inter-langue.md](rapport-c8-inter-langue.md) | C8 — transfert inter-langue : ce que le corpus multilingue dit vraiment (et le piège du corpus PARALLÈLE) |
| [rapport-c8-peripherie.md](rapport-c8-peripherie.md) | C8 — la périphérie : l'entrée entre, la sortie sort, le délai est exact — mais le modèle ne GARDE pas le signal |
| [rapport-c8-sonde-profondeur.md](rapport-c8-sonde-profondeur.md) | C8 — le réflexe : l'état intermédiaire CONTIENT le prochain jeton, c'est la TÊTE qui ne sait pas le lire |
| [rapport-c8-tete-entrainee.md](rapport-c8-tete-entrainee.md) | C8 — une TÊTE ENTRAÎNÉE pour sa profondeur : ×540 sur la tête empruntée |
| [rapport-c8-transfert-corpus.md](rapport-c8-transfert-corpus.md) | C8 — transfert d'un corpus à un AUTRE : la tête lit quand même l'état (÷1 730) |
| [rapport-c9-echange-experts.md](rapport-c9-echange-experts.md) | C9 sur un modèle routé : échanger les choix d'experts ne transfère RIEN d'utilisable |
| [rapport-c9-lateralite.md](rapport-c9-lateralite.md) | C9 — latéralité : l'échange est exact, il ne crée pas de gain, et il récupère un jumeau dégradé à hauteur de sa moyenne |
| [rapport-cache-experts-vram.md](rapport-cache-experts-vram.md) | Rapport — un cache d'experts en VRAM pour Kimi-K3 : mesuré, et pourquoi c'est non |
| [rapport-campagne-parcimonie.md](rapport-campagne-parcimonie.md) | Campagne « parcimonie imposée » — synthèse |
| [rapport-capteur-hebbien.md](rapport-capteur-hebbien.md) | Capteur hebbien — apprendre des logs d'activation |
| [rapport-carte-raisonnement-naturel.md](rapport-carte-raisonnement-naturel.md) | La carte du raisonnement naturel : quatre mesures, trois courbes, deux axes |
| [rapport-cerveau-corrections.md](rapport-cerveau-corrections.md) | Corrections B12 — ce que le stress des sous-agents a changé |
| [rapport-cerveau-modules.md](rapport-cerveau-modules.md) | Rapport — modules cerveau-langage M1–M9 |
| [rapport-chargement-paresseux.md](rapport-chargement-paresseux.md) | Le chargement construisait 2,7 Go de « listes » que personne ne lisait |
| [rapport-coherence-docs-2.md](rapport-coherence-docs-2.md) | Cohérence des documents avec le code — second passage |
| [rapport-coherence-docs-3.md](rapport-coherence-docs-3.md) | Rapport — cohérence de la documentation, troisième passage |
| [rapport-coherence-docs.md](rapport-coherence-docs.md) | Cohérence des documents avec le code — audit |
| [rapport-coherence-vision.md](rapport-coherence-vision.md) | Cohérence des `docs/` avec la vision Drave — révision du 02/10 |
| [rapport-compacite-trace.md](rapport-compacite-trace.md) | Compacité de la trace — le disque paie trois fois le câble |
| [rapport-consolidation-balayage.md](rapport-consolidation-balayage.md) | Le balayage de la consolidation — un optimum INTÉRIEUR de capacité (rang 4) et de pas (3e-4), qui ne composent PAS |
| [rapport-consolidation-c7.md](rapport-consolidation-c7.md) | C7 — la consolidation : le rejeu met bien l'expérience dans les poids (−16,4 % en domaine, **+1,3 % hors domaine**) |
| [rapport-consolidation-structure-partagee.md](rapport-consolidation-structure-partagee.md) | Ce qui se consolide, c'est la STRUCTURE PARTAGÉE — même mémorisation (−22,5 %), transfert −7,4 % ou +1,2 % |
| [rapport-cpu-aer.md](rapport-cpu-aer.md) | Drave — l'architecture « push » (AER) sur CPU |
| [rapport-croisement-push-pull.md](rapport-croisement-push-pull.md) | Croisement push / pull — quand l'architecture événementielle est-elle justifiée ? |
| [rapport-cycle-c2.md](rapport-cycle-c2.md) | C2 — le cycle à deux régions : exact au premier pas, **divergent** ensuite (14,65 → 2 988 en 4 pas) |
| [rapport-cycle-entraine.md](rapport-cycle-entraine.md) | C2 bis — le cycle ENTRAÎNÉ : ×228 au pas 4, mais il dégrade encore (et le moteur le confirme) |
| [rapport-cycle-rapide.md](rapport-cycle-rapide.md) | Le cycle rapide : l'article 1 de l'UDHR dans 399 langues |
| [rapport-decision-par-couche.md](rapport-decision-par-couche.md) | La décision par couche : à 20-56 % de densité, le dense gagne (2 %) ; le push est pour les couches creuses |
| [rapport-decoupage-moe.md](rapport-decoupage-moe.md) | Rapport — découpage des MoE en clusters, pour notre mode d'opération |
| [rapport-decoupage-v41.md](rapport-decoupage-v41.md) | Rapport — Le découpage de V4.1 : la couture exacte, et l'instrument innocenté |
| [rapport-deepseek.md](rapport-deepseek.md) | B9 — DeepSeek pour le langage, GPU pour le modèle natif |
| [rapport-design-H-carte-sorties.md](rapport-design-H-carte-sorties.md) | Dessin H — la carte des points de sortie : la borne monte quand on sort tard, mais le gain atteignable s'effondre |
| [rapport-design-H-profondeur-routee.md](rapport-design-H-profondeur-routee.md) | Dessin H — profondeur routée : la borne de l'oracle vaut ≈ 31 % des jetons, et le chemin court reste derrière le chemin long même là où il est le plus sûr |
| [rapport-design-H-sorties-precoces.md](rapport-design-H-sorties-precoces.md) | Dessin H — les sorties précoces (8 et 4) : la question ouverte est tranchée, et le verdict ne change pas |
| [rapport-dessin-B-poids-creux.md](rapport-dessin-B-poids-creux.md) | Dessin B (poids creux) — le levier reste à trouver : élaguer coûte toujours cher |
| [rapport-dialogue-diabla.md](rapport-dialogue-diabla.md) | Le dialogue réel (DiaBLa) : +40,3 / +44,2 au 1,5 B — mais la référence est une **post-édition**, pas une traduction |
| [rapport-drapeaux-ignores.md](rapport-drapeaux-ignores.md) | Drapeaux et variables « analysés mais jamais appliqués » — audit systématique |
| [rapport-e1-e2-connectome-croissance.md](rapport-e1-e2-connectome-croissance.md) | E1 et E2, re-mesurés : le connectome aléatoire coûte 9 % (pas 1 %), et la croissance n'est PAS pire que le hasard |
| [rapport-e2-croissance.md](rapport-e2-croissance.md) | E2 — la croissance locale ne bat pas la structure tirée au hasard (2,3431 contre 2,3215) |
| [rapport-e4-ratio-signes.md](rapport-e4-ratio-signes.md) | E4 (côté ENTRAÎNEMENT) — le ratio de signes cortical ne paie pas : 2,2729 → 2,3838 → 2,5188 |
| [rapport-e5-distillation.md](rapport-e5-distillation.md) | E5 — distiller le cerveau dans le réflexe : l'accord double (28 % → 51 %), et le texte ne suit toujours pas |
| [rapport-e6-poids-lognormaux.md](rapport-e6-poids-lognormaux.md) | E6 — poids log-normaux : les chiffres corrigés, et les trois chiffres RÉTRACTÉS |
| [rapport-e9-homeostasie.md](rapport-e9-homeostasie.md) | E9 — L'HOMÉOSTASIE SYNAPTIQUE : amortir le changement plastique rend la consolidation MEILLEURE des deux côtés |
| [rapport-elagage-logs.md](rapport-elagage-logs.md) | A6.3 — l'élagage guidé par les logs : aucun neurone ne s'allume jamais, mais 63 % s'allument à peine |
| [rapport-empreinte-memoire.md](rapport-empreinte-memoire.md) | Rapport — l'empreinte mémoire : ce qui réduit vraiment ce qu'il faut charger |
| [rapport-encodage.md](rapport-encodage.md) | Drave — encodage de structure : éliminer la valeur |
| [rapport-engram-etat.md](rapport-engram-etat.md) | Engram de DeepSeek-V4.1 : ce qui est établi, ce qui manque, et pourquoi on s'arrête là |
| [rapport-eparsite.md](rapport-eparsite.md) | Drave — élagage et approche par événement |
| [rapport-execution-v41.md](rapport-execution-v41.md) | Rapport — test d'exécution locale de DeepSeek-V4.1-Flash, avec toutes les optimisations |
| [rapport-fenetre-puits-attention.md](rapport-fenetre-puits-attention.md) | Fenêtre d'attention × puits : jusqu'où la fenêtre est-elle gratuite ? |
| [rapport-gpt-oss-perplexite.md](rapport-gpt-oss-perplexite.md) | Perplexité de gpt-oss : deux bugs réels, une prémisse fausse |
| [rapport-gpu-scores.md](rapport-gpu-scores.md) | Noyau GPU de scores d'attention — le premier des trois du top-k |
| [rapport-gpu-tandem-nvlink.md](rapport-gpu-tandem-nvlink.md) | Le tandem GPU (2 × Quadro RTX 5000, NVLink) : ce qu'il fait, ce qu'il pourrait faire |
| [rapport-gpu-topk-selection.md](rapport-gpu-topk-selection.md) | Rapport — la sélection top-k et la somme sur GPU (noyaux 2 et 3 du plan) |
| [rapport-gpu-topk-tout.md](rapport-gpu-topk-tout.md) | Le top-k GPU : le noyau fusionné gagne jusqu'à ~64 k clés, la chaîne séparée au-delà |
| [rapport-granularite-flux.md](rapport-granularite-flux.md) | Granularité des listes et volume des flux entre unités — mesuré |
| [rapport-grappe-deportee.md](rapport-grappe-deportee.md) | A7.4 — la grappe déportée : le flux ne transporte plus les zéros |
| [rapport-grappe-intra-couche.md](rapport-grappe-intra-couche.md) | A7.3 — la grappe intra-couche : le top-1024 (21 %) rend la même perplexité |
| [rapport-grappes.md](rapport-grappes.md) | Drave — grappes afférentes/efférentes et découpage en sous-modèles |
| [rapport-greffon.md](rapport-greffon.md) | Greffon : plomberie d'apprentissage |
| [rapport-habituation.md](rapport-habituation.md) | L'habituation (soustraire le passé) n'apporte RIEN — le réseau calcule déjà la différence |
| [rapport-harnais.md](rapport-harnais.md) | Drave — harnais de test : qualité et débit variable |
| [rapport-hc-permutation.md](rapport-hc-permutation.md) | Hyper-connexions de V4-Flash : les 16 connexions sont une PERMUTATION |
| [rapport-hebbien-produits.md](rapport-hebbien-produits.md) | A6.1 — les produits hebbiens n'ajoutent presque rien : +0,0045 de R² |
| [rapport-hybride.md](rapport-hybride.md) | Rapport — hybride codec + mémoire, et le contexte |
| [rapport-inference.md](rapport-inference.md) | Inférence complète en Rust — Qwen2.5-0.5B sans GPU, sans BLAS, sans dépendance |
| [rapport-jeux-symboliques.md](rapport-jeux-symboliques.md) | B5/B6 — les jeux symboliques : 112 surfaces, 100 % au niveau 4, 33/33 paires invariantes |
| [rapport-kv-par-couche.md](rapport-kv-par-couche.md) | La quantification du KV par couche : le coût de l'int8 est dans les **premières** couches |
| [rapport-langues-maitres.md](rapport-langues-maitres.md) | B7/B8 — 71 langues pour les jeux, et les livres des maîtres mesurés |
| [rapport-lecteur-multifichiers.md](rapport-lecteur-multifichiers.md) | Rapport — un modèle éclaté se lit comme un seul |
| [rapport-localite-activation.md](rapport-localite-activation.md) | Localité d'activation : ce que PowerInfer apporte, et ce qu'on en garde |
| [rapport-logits-gpu-vs-cpu.md](rapport-logits-gpu-vs-cpu.md) | Rapport — pourquoi le déport des projections change (ou non) la perplexité |
| [rapport-loi-frontiere-fenetre.md](rapport-loi-frontiere-fenetre.md) | La frontière de la fenêtre : pas de loi en N, un régime sûr (la moitié des clés) et un régime imprévisible en dessous |
| [rapport-m7-frequence.md](rapport-m7-frequence.md) | B16 — M7-bis : la fréquence, pas la neuromodulation |
| [rapport-m8-log-normal.md](rapport-m8-log-normal.md) | M8 — le variant log-normal : CAUSE TROUVÉE (le partage des poids), CORRIGÉE, et le moteur innocenté |
| [rapport-materiel-disque-ou-cpu.md](rapport-materiel-disque-ou-cpu.md) | Disque ou CPU ? — ce que la mesure dit d'un deuxième NVMe |
| [rapport-matvec-f32-parallele.md](rapport-matvec-f32-parallele.md) | Rapport — Le produit matrice-vecteur f32 de V4.1 : ×9,34 sur l'attention, sans changer un bit |
| [rapport-memoire-travail-n5.md](rapport-memoire-travail-n5.md) | N5 — la mémoire de travail : le réseau ne l'APPREND pas, la structure la donne (+0,96 contre −2,77) |
| [rapport-minimal.md](rapport-minimal.md) | Drave — test de principe : modèle minimal en ternaire / multi-bits |
| [rapport-mla-experts.md](rapport-mla-experts.md) | Rapport — MLA à rang faible et formats sans noyau : GLM-5.3 et Kimi deviennent calculables |
| [rapport-mode-listes.md](rapport-mode-listes.md) | Drave — « mode listes » : exécuter sans GPU |
| [rapport-mode4-lot-listes.md](rapport-mode4-lot-listes.md) | Mode 4 — le lot en listes : ÷2,3 sur les octets, et ce qu'il coûte |
| [rapport-modele-drave.md](rapport-modele-drave.md) | DÉVELOPPER UN MODÈLE **NATIF DRAVE** — étude, et le plan pour le mesurer |
| [rapport-modele-moteur.md](rapport-modele-moteur.md) | Le modèle produit ici tourne dans Drave — et se découpe |
| [rapport-modele-reel.md](rapport-modele-reel.md) | Drave — le modèle réel expose-t-il ses grappes ? |
| [rapport-modules-famille.md](rapport-modules-famille.md) | C3.2b — un module de restitution par famille : l'indo-européen recopie à 100 % |
| [rapport-morcellement-experts.md](rapport-morcellement-experts.md) | Rapport — peut-on « morceler » un modèle ? L'élagage par fréquence, mesuré |
| [rapport-multilingue.md](rapport-multilingue.md) | B15 — M1 sur 66 langues : invariance et exactitude |
| [rapport-mur-memoire-4bits.md](rapport-mur-memoire-4bits.md) | Le mur mémoire, et ce que les 4 bits achètent vraiment |
| [rapport-n4-dessin-b.md](rapport-n4-dessin-b.md) | N4 — le chemin court entraîné (dessin B) : ÷1,2 à ÷1,9 selon la profondeur, et deux corrections de mesure |
| [rapport-n4-porte-execution.md](rapport-n4-porte-execution.md) | N4 — la porte d'exécution : le chemin court entraîné est mesuré par le MOTEUR (÷1,47 et ÷1,24) |
| [rapport-niah-fragilite.md](rapport-niah-fragilite.md) | Le critère de `porte-indice` ne survit pas à une reconstruction de son entrée |
| [rapport-nli-francais-dur.md](rapport-nli-francais-dur.md) | Le NLI français plus dur que XNLI : DACCORD +26,9, GQNLI +56,7 — et le 1,5 B bat le 3 B |
| [rapport-operateur-negation.md](rapport-operateur-negation.md) | B4.1 — la négation n'est pas une opération portée par l'état |
| [rapport-optimisations-auto.md](rapport-optimisations-auto.md) | Rapport — détection matérielle et configuration automatique |
| [rapport-optimisations.md](rapport-optimisations.md) | Moteur d'événements Rust — les 4 optimisations, et les 3 pièges |
| [rapport-p0-flux.md](rapport-p0-flux.md) | P0 — Le harnais de flux : compter ce qu'on paie, par provenance |
| [rapport-parcimonie-entrainee.md](rapport-parcimonie-entrainee.md) | La parcimonie entraînée — premier banc, et la loi du coût par événement |
| [rapport-parcimonie-imposee.md](rapport-parcimonie-imposee.md) | Parcimonie imposée à l'inférence — la frontière mesurée |
| [rapport-passage-a-l-echelle.md](rapport-passage-a-l-echelle.md) | Passer aux gros modèles : ce qui bloque, chiffré |
| [rapport-passe-complete-13-octobre.md](rapport-passe-complete-13-octobre.md) | Deux passes complètes dans la même nuit — et ce qu'elles ont attrapé |
| [rapport-passe-complete-portes.md](rapport-passe-complete-portes.md) | Passe COMPLÈTE des portes : de 22 à 47 portes — et une porte qui était verte en ne mesurant RIEN |
| [rapport-passe-k3-disque.md](rapport-passe-k3-disque.md) | Où passe le temps d'une passe Kimi-K3 : le disque, et rien d'autre |
| [rapport-pensee-sans-verbaliser.md](rapport-pensee-sans-verbaliser.md) | Rapport — la pensée sans verbaliser : le journal des mesures 77–168 |
| [rapport-pensee-silencieuse.md](rapport-pensee-silencieuse.md) | PENSER SANS VERBALISER — la boucle d'état naïve détruit la prédiction, et verbaliser n'est PAS du gaspillage |
| [rapport-phase3-reparti.md](rapport-phase3-reparti.md) | Phase 3 — le calcul réparti redevient fidèle |
| [rapport-pipeline-m2.md](rapport-pipeline-m2.md) | B14 — M2 dans la chaîne : un rameau, pas un étage |
| [rapport-pipeline-memoire.md](rapport-pipeline-memoire.md) | B17 — M7-bis dans la chaîne : LFU aide la mémoire, pas M8 |
| [rapport-pipeline-semantique.md](rapport-pipeline-semantique.md) | B13 — chaîne sémantique M1 → M5 → M6 → M8 |
| [rapport-placement-bits-kv.md](rapport-placement-bits-kv.md) | Où mettre les bits du cache KV : la courbe complète |
| [rapport-placement-kv-8k.md](rapport-placement-kv-8k.md) | Le placement du KV à 8 k : ×1,93 sur le préremplissage, ×5,8 sur l'attention |
| [rapport-plateau-semantique.md](rapport-plateau-semantique.md) | Rapport — le plateau sémantique, mesuré sur un corpus multilingue réel |
| [rapport-politique-budget-attention.md](rapport-politique-budget-attention.md) | Le budget d'attention a-t-il une bonne taille par texte ? — le coût de la moitié varie de ×180 |
| [rapport-pont-generatif.md](rapport-pont-generatif.md) | Le pont GÉNÉRATIF : le réseau naît, l'attrition le RÉDUIT |
| [rapport-pont-semantique.md](rapport-pont-semantique.md) | Rapport — le pont linguistique-sémantique, mesuré |
| [rapport-pool-tampons.md](rapport-pool-tampons.md) | Le pool de tampons : neutre en temps — et l'hypothèse qui l'avait motivé est réfutée |
| [rapport-portes-p0-p9.md](rapport-portes-p0-p9.md) | Les deux portes, phase par phase (P0 → P9) |
| [rapport-precision.md](rapport-precision.md) | Drave — la sparsité peut-elle acheter de la précision ? |
| [rapport-prefill-par-experts.md](rapport-prefill-par-experts.md) | Rapport — le préremplissage par experts : ce que le regroupement rapporte, mesuré |
| [rapport-prefill-par-lots.md](rapport-prefill-par-lots.md) | Préremplissage par lots : ce que le GEMM apporte vraiment |
| [rapport-prefill-reparti.md](rapport-prefill-reparti.md) | Phase 3.4 — le préremplissage par LOTS sur le fil |
| [rapport-prelire-grappe.md](rapport-prelire-grappe.md) | S4 — le préchargement par grappe : la lecture à la demande rend 29 Mo/s là où la grappe rend 1 230 |
| [rapport-programme-evolutif.md](rapport-programme-evolutif.md) | Programme « journaliser, faire évoluer » — ce que la mesure autorise |
| [rapport-provenance-v41.md](rapport-provenance-v41.md) | DeepSeek-V4.1 : ce que le fichier dit, et ce qu'il ne dit pas |
| [rapport-raid0-nvme.md](rapport-raid0-nvme.md) | Le raid0 de 4 NVMe en service — débits, QPI, et ce que le moteur n'en voit pas |
| [rapport-regle-placement-perte.md](rapport-regle-placement-perte.md) | A8.3 — la règle place et perte choisit le KV comme la main |
| [rapport-restitution.md](rapport-restitution.md) | B18 — restitution canonique : 528/528, mais pas un décodeur |
| [rapport-reutilisation-experts.md](rapport-reutilisation-experts.md) | La réutilisation des experts, mesurée |
| [rapport-routage-experts.md](rapport-routage-experts.md) | Rapport — le routage des experts était faux pour quatre gros modèles sur cinq |
| [rapport-s4-prechargement-moteur.md](rapport-s4-prechargement-moteur.md) | S4 — la prélecture dans le moteur : le calcul ne paie plus les défauts de page |
| [rapport-semantique.md](rapport-semantique.md) | Le protocole sémantique natif — premier passage |
| [rapport-session-2026-09-30.md](rapport-session-2026-09-30.md) | Session du 30/09 — index des chantiers |
| [rapport-sommeil-budget.md](rapport-sommeil-budget.md) | Le budget du sommeil — ce que le rejeu rapporte (÷ croissant en domaine) et ce qu'il coûte (bruité) |
| [rapport-sommeil-deux-nuits.md](rapport-sommeil-deux-nuits.md) | Deux nuits, deux expériences — la première garde son gain, la seconde n'ajoute presque rien |
| [rapport-sommeil-selection.md](rapport-sommeil-selection.md) | La sélection du rejeu — à volume égal, *ce qu'on rejoue* compte moins que *rejouer* |
| [rapport-speculatif-reflexe.md](rapport-speculatif-reflexe.md) | Le réflexe propose, le cerveau vérifie — acceptation 2 à 30 % (le cerveau non entraîné : 0 %) |
| [rapport-sprint-24h.md](rapport-sprint-24h.md) | Sprint 24 h — bilan B12 → B18 |
| [rapport-tableaux-casses.md](rapport-tableaux-casses.md) | Un tableau qui ne rend pas est un tableau qui n'existe pas — 17 lignes, 9 fichiers, et une porte |
| [rapport-tete-garantie.md](rapport-tete-garantie.md) | Rapport — restriction de tête GARANTIE : exacte, et sans gain |
| [rapport-tete-restreinte.md](rapport-tete-restreinte.md) | Rapport — restreindre la tête de sortie : ce qui marche, ce qui ne marche pas |
| [rapport-transport-liste.md](rapport-transport-liste.md) | Phase 3.2 — transporter la LISTE au lieu du vecteur |
| [rapport-travail-reel.md](rapport-travail-reel.md) | Le moteur est-il prêt pour du vrai travail ? |
| [rapport-universaux.md](rapport-universaux.md) | Rapport — base d'universaux typés |
| [rapport-v4-couches-0-1.md](rapport-v4-couches-0-1.md) | V4-Flash, couches 0 et 1 — la première comparaison étage par étage |
| [rapport-v4-hca.md](rapport-v4-hca.md) | Les compresseurs de DeepSeek-V4 (HCA et CSA), validés contre llama.cpp |
| [rapport-v4-reparti.md](rapport-v4-reparti.md) | V4-Flash réparti sur deux nœuds — exact, et ce qu'il coûte |
| [rapport-v4-yarn-compresse.md](rapport-v4-yarn-compresse.md) | V4-Flash : la rotation des couches compressées était le RoPE simple |
| [rapport-v41-couches-brouillon.md](rapport-v41-couches-brouillon.md) | V4.1 — les couches du brouillon sont dans le fichier |
| [rapport-v41-mhc.md](rapport-v41-mhc.md) | V4.1 : la chaîne mHC **retardée**, et les trois égalités vérifiées sur le vrai modèle |
| [rapport-valeur-unaire.md](rapport-valeur-unaire.md) | Drave — éliminer la valeur par répétition d'adresse ? |
| [rapport-vie-quatre-jours.md](rapport-vie-quatre-jours.md) | Quatre jours de suite — deux refusés par le protocole, un qui dégrade |
| [rapport-vision-qwen2vl.md](rapport-vision-qwen2vl.md) | La vision n'est plus bloquée — elle est MESURÉE, et elle a tort |
| [rapport-vitesse-v41.md](rapport-vitesse-v41.md) | Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé |
| [rapport-vram-transfert.md](rapport-vram-transfert.md) | La VRAM : ce qui coûte n'est pas le lien, c'est l'allocation |
| [toutes-langues.md](toutes-langues.md) | Extension à toutes les langues, puis aux grands corpus |
