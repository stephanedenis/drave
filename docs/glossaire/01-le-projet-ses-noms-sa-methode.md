# 1. Le projet, ses noms, sa méthode

> **Famille 1 du glossaire** (11 familles). Index : [le glossaire](../glossaire.md).

---

## 1. Le projet, ses noms, sa méthode

**A/B (écart A/B)** — Comparaison de deux exécutions ne différant que par un
réglage, sur le même texte et les mêmes jetons. Le dépôt en fait la règle quand un
chiffre absolu n'est pas reproductible : « seul l'écart A/B fait foi »
(`docs/plan-gpu-topk.md:99`). **Où** : `--attn-topk` contre sans top-k,
`docs/contexte-long.md:557-567`.

**Banc (bench)** — Dispositif de mesure isolé qui fait tourner une seule partie du
moteur sur des données choisies, pour que la bonne réponse soit connue d'avance.
Le dépôt en a plusieurs : `--banc-kv`, `--banc-mla`, `--banc-topk`, `--banc-vision`,
`--gpu-banc` (`drave-core/src/main.rs`). Un banc qui passe ne prouve pas qu'il
mesure ce qu'on croit : `docs/sprints.md:69-73`.

**Boxing** — Règle des sprints : 2 h chronométrées, on s'arrête quand la boîte est
pleine même si c'est presque fini, et ce qui reste va au planning suivant.
`docs/sprints.md:6-17`. **Où** : `tools/sprint.sh`.

**CDC** *(polysémie)* — Dans le corpus, **deux sens** :
1. **cahier des charges** : le document d'origine du projet, `Qtrinet-bootstrap.md`,
   qui imposait l'inférence ternaire sur FPGA, « 100 % logique, sans DSP »
   (`docs/histoire.md:11`) ;
2. **Clock Domain Crossing** : traversée de domaines d'horloge sur le FPGA,
   contrainte tenue sans perte de fréquence (`reports/bilan-multi-materiel.md:68`).
Lire le contexte avant de traduire. **Réf.** : pour le second sens, voir la
documentation Intel « Stratix V Device Handbook », section Clocking.

**Couche / Étage** *(polysémie volontairement levée)* — Dans Drave, **deux mots pour deux choses** :
1. **couche** = **couche de neurones** d'un réseau (couche 1, 2, …) : une unité de calcul traversée par l'état.
   C'est le sens des mesures « la langue est lisible dès la couche 1 »
   (`reports/07-mesures-couche-commune.md`) ;
2. **étage** = **niveau d'architecture** du projet : l'**étage 1** est la couche commune entrée-sortie (lire et
   produire toutes les langues, dialectes, styles), l'**étage 2** est le module de pensée abstraite
   (`docs/agent/mission.md`, `AGENTS.md`).

Le nom historique « **couche commune entrée-sortie** » (et le fichier
`reports/07-mesures-couche-commune.md`) désigne l'**étage 1** : le lire comme « étage », jamais comme une couche de
neurones. **Règle** : dans `docs/`, on écrit « **étage** » pour l'architecture et « **couche** » pour les neurones ;
dans `reports/`, les textes anciens gardent « couche commune », à traduire par « étage entrée-sortie » à la lecture.

**Créneau long** — Unité de travail de 3 h, entre le sprint (2 h) et la journée
(8 h) ; produit deux à trois chantiers (`docs/sprints.md:58-63`).

**Definition of done (engagement de fin de sprint)** — Liste non négociable pour
fermer un sprint « vert » : `cargo test --release` passe, les portes de
non-régression sont intactes, tout est commité, la machine est rendue, tout chiffre
annoncé a sa source (`docs/sprints.md:33-46`).

**Drave** — Nom du projet depuis le 30/09/2026 : *stream of logs*, « le flux des
listes », et en français la drave, ces billots confiés à la rivière. Le mot porte
trois propriétés : ça coule, ça se répartit, ça se surveille
(`docs/vision.md:260-273`, `docs/histoire.md:18-24`). **Où** : crate `drave-core`,
binaire `drave`, variables `DRAVE_*`, noyaux `drave_gpu.*`.

**Écart (0,00e0)** — Différence entre le résultat d'une exécution locale et celui
d'une exécution découpée ou transportée. `0,00e0` signifie « aucun écart
représentable » : c'est le critère de fidélité du transport dense
(`docs/roadmap.md:55`, `docs/format-flux.md:185`).

**Fait · mesuré · projeté · déduit** — Étiquettes de confiance du dépôt. *Mesuré* :
chiffre obtenu sur cette machine, commande citée ; *projeté* : extrapolé d'un
modèle ou d'une limite matérielle ; *déduit* : conséquence d'une autre mesure. Le
bilan multi-matériel les distingue colonne par colonne (`reports/bilan-multi-materiel.md:33-40`).

**Harnais (harness)** — Petit montage de test autonome, souvent en Python, qui
enveloppe un composant pour le mesurer ou le comparer à une référence. Exemples :
harnais de perplexité (`src/bpe_np.py`, `src/transformer_np.py`), harnais MLA
(`tools/mla_synthetique.py`, `--banc-mla`), harnais de vision (`tools/vision_ref.py`).
Voir `reports/rapport-harnais.md`.

**Journal de session** — Historique horodaté de tout ce qui a été mesuré, archivé
automatiquement à chaque commit (`tools/archive_sessions.py`, hook git + tâche
horaire). Le journal est la mémoire brute : il n'est **pas** réécrit lors des
renommages (`docs/histoire.md:38-43`, `docs/programme-recherche.md:206-208`).
**Où** : `journal/`.

**Jeton** *(token)* — Unité de **tokenisation** d'un modèle : le découpage technique (octets, caractères, morceaux
de mots) que le modèle calcule. C'est une unité **propre au tokeniseur**, variable d'un modèle et d'une écriture à
l'autre, et **elle ne porte pas le sens** à elle seule. **Ne jamais** l'employer pour la représentation sémantique
neutre (voir **RSN**) : on n'écrit pas « jeton sémantique », « jeton de sens », « jeton neutre ». Les mesures qui
comptent des jetons (bits/token, tokens coûteux, perplexité) sont des **diagnostics d'instrument**, pas des mesures
de sens. **Où** : `tools/marqueur_bruit.py`, `tools/seuil_bruit.py`, toute mesure de perplexité.

**Mesure entrelacée · machine au calme** — Protocole : mesurer les configurations
comparées en alternance, parce que la charge de fond (bureau, autres projets) fait
varier le temps mural de 30 % ; et préférer les mesures déterministes (perplexité,
comptes d'événements) aux mesures de temps (`docs/programme-recherche.md:201-205`,
`reports/rapport-campagne-parcimonie.md:8-10`).

**Non-régression (porte de non-régression)** — Valeur de référence qu'une
modification ne doit pas dégrader. Les portes du dépôt sont : Qwen2.5-0.5B à
contexte 256 = **19,3885** ; gpt-oss à contexte 256 = **15,6017** ; Qwen3-30B en
clusters = **799,8557** ; le banc réparti dense = **0,00e0**
(`docs/sprints.md:38-41`, `docs/plan-gpu-topk.md:101`). **Où** : `tools/portes.sh`,
`cargo test --release`.

**Porte de correction** — Comparaison à une référence **externe** (llama.cpp ou une
implémentation numpy indépendante) qui sert à corriger le moteur, jamais de but.
« La conformité à llama.cpp est une porte de correction, pas le but : le but est de
conduire des flux » (`docs/plan-modeles-lourds.md:83-85`,
`docs/plan-deepseek41-complet.md:9`). **Depuis le 03/10 (bloc 23) elle a des critères
mesurés**, et un outil qui rend le verdict au lieu d'une impression
(`tools/compare_logits.py --porte`, branché dans `tools/portes.sh`) : corrélation des
logits **par position** ≥ 0,95 au minimum et ≥ 0,98 en moyenne, top-1 identique
≥ 85 %, perplexité à moins de 10 % — ce dernier critère **seulement au-delà de 64
prédictions**, parce que sur une fenêtre de 4 jetons le même moteur diverge de 25 %
et sur 63 prédictions de 6,4 % (mesuré sur V4-Flash,
`docs/plan-deepseek41-complet.md:385-430`). **La perplexité seule n'est pas
l'instrument** : sur une fenêtre courte elle amplifie le chaos au lieu de mesurer la
fidélité.

**Porte (de décision)** — Un chiffre, mesuré sur cette machine, qui décide de
continuer ou d'abandonner une branche ; « une porte non franchie arrête la
branche — pas de poursuite par inertie » (`docs/programme-recherche.md:134-135`,
`:210`). Exemples : *Porte A* (une variante bat le modèle de base de ≥1 % de
perplexité), *Porte C* (apprendre un fait à l'inférence sans oubli catastrophique).

**Porte Drave** — Épreuve propre au projet, opposée à la porte de correction :
nombre d'événements par jeton non nul, trace écrite puis **rejouée à l'identique**,
découpage en grappes qui donne la même perplexité, flux nouveau lisible par un
outil d'analyse (`docs/plan-deepseek41-complet.md:134-141`). Depuis le 03/10
(bloc 22), « rejouée à l'identique » est **défini et vérifié** : aucune liste
manquante **et** écart de perplexité ≤ 1e-5 (mesuré : 4,5e-06 sur V4-Flash, 1,6e-06
sur Qwen ; `docs/plan-deepseek41-complet.md:347-351`). L'écart ne peut pas être nul :
la trace porte des activations déjà quantifiées, que le rejeu requantifie.

**Qtrinet** — Premier nom du projet, du nom d'un réseau ternaire sur un cluster de
cartes **Stratix V** ; le cahier des charges d'origine, `Qtrinet-bootstrap.md`, est
conservé tel quel comme pièce datée. Les variables `QT_*` ne font plus rien : le
moteur prévient au lieu de laisser croire qu'une option est active
(`docs/histoire.md:11`, `:46-60`).

**Rapport** — Document de `reports/` consignant une campagne : commande exacte,
chiffres, erreurs trouvées, réserves. Un rapport porte ses propres corrections,
souvent en tête (bandeau « État ») ou en sections « CORRIGÉ »
(`reports/rapport-compacite-trace.md:13-18`).

**Rejeu** — Réinjection d'une trace enregistrée dans le moteur
(`--flux-forcer <trace>`) : les activations calculées sont remplacées par celles du
fichier, et si le résultat est identique, « une liste suffit à continuer le
calcul » (`docs/roadmap.md:196-213`, `docs/format-flux.md:6-8`).

**Relire · relecture adverse · relecture déléguée** — Trois niveaux de relecture.
La relecture *adverse* cherche activement à casser une affirmation ; la relecture
*déléguée* est confiée à un autre agent et compte comme une tâche du sprint.
« Trois relectures adversariales ont trouvé 28 défauts sur un créneau, presque tous
par lecture » (`docs/sprints.md:69-73`, `reports/rapport-coherence-vision.md:3-6`).

**Représentation sémantique neutre (RSN)** — L'objet échangé entre le **module pré-linguistique** (texte → sens)
et le **module post-linguistique** (sens → texte) : une **structure multi-niveaux** (graphémique/phonologique,
morphologique, syntaxique, sémantique, discursif/pragmatique), **indépendante de la langue de surface**, annotée de
son bruit (confiance, ambiguïtés, langues probables). Ses éléments sont des **unités de sens**, jamais des **jetons**
(voir **Jeton**) : le jeton est le porteur technique du modèle, la RSN est ce que l'architecture vise. **Où** :
`tools/pont_abstrait.py` (le pont actuel), `docs/synthese/07-modeles-alternatifs-entree-sortie.md` § « La
représentation neutre n'est pas un jeton ».

**Rétrospective** — Partie de la cérémonie de fin de sprint : *garder* / *changer* /
*doute*. « Une rétro qui ne change rien n'est pas une rétro : chaque "changer" doit
devenir une action du sprint suivant » (`docs/sprints.md:27-29`).

**Session · sprint** — Une session (journée) peut contenir plusieurs sprints
(2 h chacun) ; un index de session est écrit dans
`reports/rapport-session-*.md` (`docs/sprints.md:56-65`).

**Trace (de flux)** — Enregistrement, couche par couche et jeton par jeton, des
neurones actifs (indice + valeur) et de leur échelle. La trace est à la fois le
journal d'exécution, la matière du rejeu, le contrat d'échange réseau et la donnée
d'analyse (`docs/format-flux.md:1-18`). **Où** : `--trace-flux`.

**Verdict négatif** — Résultat qui ferme une piste, consigné comme les autres.
Exemples : le cache d'experts MXFP4 en VRAM (+6 %, « à ne pas activer par défaut »,
`docs/contexte-long.md:355-366`), l'épinglage NUMA (« mesuré, perdant »,
`docs/convertisseur.md:236-242`), le lot dense sur la tête de sortie (« ne gagne
rien », `reports/rapport-prefill-par-lots.md:131-136`).

---

