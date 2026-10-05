# Reprise — état du projet et mode d'emploi pour une nouvelle session

> Rédigé à la fin d'une session longue. Tout ce qui suit est **mesuré**, pas
> déduit. Les valeurs de perplexité sont des **références de non-régression** :
> si une modification les change, c'est qu'elle a changé le calcul.
>
> **Nom** : le projet s'appelle **Drave** (binaire `drave`, paquet `drave-core`,
> variables `DRAVE_*`, histoire du renommage dans `docs/histoire.md`). Le dossier
> de travail, lui, s'appelle encore `Qtrinet` — les chemins ci-dessous sont ceux
> qui existent.

---

## 1. En une phrase

`drave-core` est un moteur d'inférence Rust (~13 758 lignes, `std` seul) qui
charge les GGUF **en place** (aucune copie, aucune requantification), exécute les
projections soit en listes d'événements, soit en produit scalaire dense, gère les
MoE, tient une conversation, et déporte au GPU ce qui y gagne. Il fait tourner du
0,5 B au 120 B sur le CPU de cette machine.

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --chat --flux --prompt "Explique le ciel bleu en une phrase." \
    --n 64 --ctx 512 --threads 16 --temp 0
```

---

## 2. Références de non-régression

> **Revérifiées le 30/09 après tous les changements de la journée** (mode lot,
> protocole v4, DRVF v2/v3, plafond R4, tableau de bord) : Qwen ctx 256 =
> **19,3885** et gpt-oss ctx 256 = **15,1757**, `cargo test` **17/17**. La porte
> gpt-oss était la seule que la relecture adversariale n'avait pas pu faire
> tourner (bornes de temps) ; elle est verte.
>
> **Mise à jour du 04/10 (bloc 31) — Kimi-K3 est LÀ, et le levier « experts » est
> chiffré.** Les 1 508,7 Go sont complets (32/32 shards, vérifiés à l'octet).
> Budget par jeton **mesuré** : **86,787 Go** — experts routés 25,830 (29,8 %),
> dense 60,958 (70,2 %). Le dense pèse 2,3× les experts : aucune technique sur
> les experts n'adresse plus de 30 % du trafic d'un jeton.
>
> Le **regroupement par experts** du préremplissage (`--lot N`), qui existait
> sans avoir jamais été mesuré, vaut **×1,58** (Qwen3-30B-A3B, invite de
> 192 jetons, NVMe, 16 fils) et **15,5× moins d'octets d'experts** — mais le
> temps décroche au-delà du lot 2 : c'est le dense qui prend la main.
> `reports/rapport-prefill-par-experts.md`.
>
> **`--lot N > 1` n'est PAS identique au chemin jeton**, et le moteur l'annonce
> maintenant : routage différent sur 7 838/9 312 lignes, génération gloutonne
> divergente au 3e jeton, mais PPL 19,143 contre 19,172, argmax identique
> 191/191, Pearson min 0,99719. Deux compteurs muets du chemin par lots sont
> refermés (« paires experts » tombait à 1 % dès le lot 2), et `forward_lot`
> **refuse** désormais un modèle à experts partagés au lieu d'en calculer un
> autre en silence.
>
> Une hypothèse a été **réfutée** dans le même bloc : la tuile du GEMM 4 bits
> (8 / 16 / 64 → 21,2 / 21,2 / 22,0 s à lot 32) ne change rien. La constante
> reste à 8 ; `DRAVE_TUILE_LOT` est un banc d'essai, pas un réglage.
>
> `--k3-essai` sur les 32 shards redonne **exactement** les sorties obtenues avec
> 25 shards (composition 0-3 : 8,7757 / 5,2909 / 5,2559 / 5,4735) : les shards
> déjà présents portaient les octets définitifs.
>
> **LA RÉFÉRENCE A TOURNÉ (22h57)** : `REF_SANS_REPACK=1 tools/ref_logits_k3` sur
> le modèle complet, 4 jetons → **2 h 48 min 21 s, soit ~42 min par jeton**, à
> **11 % de CPU** (borné par le disque : 1,80 To lus, 451 Go/jeton, 5,2 balayages
> du modèle), RSS 102 Go, **swap 0**. Les **93 couches** `l_out-0`…`l_out-92` sont
> vidées dans `/tmp/refk3-l_out-N.bin`, plus les logits.
>
> **LA COUCHE 0 PASSE (05/10, 02h25).** Trois défauts trouvés par la comparaison,
> aucun par relecture : (1) la **norme L2 par tête sur `q` et `k`**
> (`build_gdn_l2_norm`) n'existait nulle part ; (2) la **banque résiduelle
> s'accumulait entre les jetons** au lieu d'être propre à la passe ; (3) son
> **ORDRE de remise à zéro** — avant l'attention résiduelle, pas après, sinon un
> `res_mix` s'applique là où la référence n'en applique pas. Les trois étaient
> invisibles au jeton 0 seul.
>
> ## **LE PONT LINGUISTIQUE-SÉMANTIQUE EXISTE (06/10, 10h50)** — et il tient en une matrice
>
> **Mission** : émuler en boîte noire le premier niveau abstrait des gros modèles
> (celui où la langue cesse de dominer) pour avoir notre propre pont. Le professeur
> est une boîte noire : `--trace-flux` donne son entrée (couche 0 = la plongée du
> jeton) et sa sortie (couche L = la cible).
>
> **LE TÉMOIN QUI RENVERSE TOUT** : une **simple application linéaire de la
> plongée du jeton** prédit la couche abstraite du professeur à **0,90-0,92** —
> deux fois mieux que la récurrence linéaire (0,47-0,49), et la capacité d'état
> n'y change rien (plate de rang 32 à 256). **Le niveau abstrait est déjà à ~90 %
> déterminé par la plongée du jeton courant.**
>
> **ET LE PONT, jugé sur l'invariance inter-langue, 20 langues d'entraînement →
> 20 langues JAMAIS vues :**
>
> | couche 10 | cos moyen | pire paire |
> |---|---:|---:|
> | professeur | 0,6284 | 0,3281 |
> | **pont linéaire** | **0,7343** (+17 %) | **0,4421** (+35 %) |
>
> **Le pont rend une représentation PLUS invariante que le professeur lui-même**,
> et sa pire paire (0,4421) approche celle du plateau d'un **30 B** (0,471) —
> 60 fois plus gros. **Mécanisme** : une SEULE application linéaire sert toutes les
> langues à la fois, donc elle ne retient que ce qu'elles ont en commun. Un
> projecteur sur le partagé, par moindres carrés — sans récurrence, sans
> rétropropagation, sans oracle. Il fait mieux que l'annulation oracle.
>
> **ET IL TIENT EN UN SEUL NEURONE** — intuition de Stéphane (« un neurone par
> sortie, puis on itère ; l'apprentissage est hyper-rapide au début »), confirmée
> et chiffrée. Le rang du pont EST le nombre de neurones :
>
> | neurones | fidélité au professeur | **invariance** | pire paire |
> |---|---:|---:|---:|
> | **1** | 0,668 | **0,9492** | **0,7762** |
> | 4 | 0,748 | 0,9139 | 0,7769 |
> | 64 | 0,682 | 0,7658 | 0,4842 |
>
> **Un neurone donne 0,9492 d'invariance** contre 0,6284 pour le professeur et
> 0,471 pour le plateau d'un 30 B. Les neurones suivants montent la fidélité
> (0,668 → 0,748) mais font **baisser l'invariance monotonement** : ils ajoutent du
> détail propre à chaque langue. **Compromis net** : copier le professeur demande
> des neurones, le pont brut n'en demande **qu'un**.
>
> **L'artefact rang-1** : `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz`
> (`P` 896×128, `W0` 896×128, `moy` 896), appliqué par
> `tools/applique_pont.py <pont.npz> <trace.drvf>` — `abstrait = (e·W0)·Pᵀ + moy`.
> Vérifié sur grec, hébreu, japonais, thaï (écritures absentes de l'entraînement).
>
> **À LIRE AVANT DE S'EN SERVIR** : plus invariant ≠ meilleur — le pont peut
> **jeter** de l'information propre à la langue que le professeur porte. Le test
> qui le dirait : brancher le pont devant les couches suivantes et mesurer la
> perplexité. **PAS FAIT.** Et le pont n'est pas récurrent. Détail et réserves :
> `reports/rapport-pont-semantique.md`.
>
> ## **ÉTAT AU 06/10 11h05** — corpus, plateau sémantique, et trois négatifs nets
>
> **Corpus ingérés** : l'UDHR (456 langues, **les 30 articles alignés dans
> toutes**, 13 680 unités — `tools/extrait_udhr.py`), Wikipedia **trouvée en
> local** (81 Go, 6 langues, appariables par entité — attention,
> `Panini-Research/data/wikipedia_ingestion/backlog_*.db` porte des **files
> d'URL**, pas du texte), et Gutenberg parallèle (Dumas, Shakespeare,
> Dostoïevski). Détail : `docs/note-ingestion-corpus.md`.
>
> **Le plateau sémantique est mesuré** sur 10 langues / 4 écritures : la
> convergence inter-langue culmine à **35-42 % de la profondeur** puis le modèle
> re-spécialise vers sa sortie. **Un modèle haut de gamme converge mieux** :
> pic 0,693 contre 0,649, et surtout **pire paire 0,471 contre 0,280**.
> `reports/rapport-plateau-semantique.md`, `tools/plateau_multilingue.py`.
>
> **Trois négatifs, tous mesurés, qui définissent le problème** :
> 1. une règle hebbienne différentielle **locale et non ciblée ne transfère pas**
>    — nulle sur un autre texte, nulle sur un autre article, et **négative** sur
>    une langue non vue (0,6027 → 0,5461) ;
> 2. **aucune lecture** ne bat la meilleure couche seule : combiner dilue
>    (0,5867 pour 3 couches, 0,5574 pondéré, contre 0,6027) ;
> 3. donc **l'écart sémantique est dans les POIDS** — ni dans la lecture, ni
>    accessible par une règle sans terme qui récompense l'invariant.
>
> **Le moteur sait maintenant** : appliquer une règle hebbienne différentielle
> (`HebbDiff`, seuil d'événement, forme signée, décroissance), la **mesurer**, la
> **sauver** et la **recharger** (`DRAVE_HEBB_SAUVER` / `DRAVE_HEBB_CHARGER`), et
> la **réfuter proprement**.
>
> **Ce qu'il faudrait pour réduire l'écart** : une règle **contrastive**
> (anti-Hebbien sur le différentiel inter-langue) avec **alignement au niveau du
> jeton** et un **terme de partage**. C'est un travail de conception.
>
> ## **ÉTAT AU 06/10 00h10** — pour reprendre après compactage
>
> **Fait** : Kimi-K3 (1 508,7 Go) tourne en entier, ses logits sont ceux de
> llama.cpp (**top-1 identique 3/3**), et il **engendre** (pas 0 → 1103, pas 1 →
> 3140, les top-1 de la référence). 7,4 min/jeton pour les logits, ×6 plus rapide
> que la référence. Trois des treize points de vérification sont verts.
>
> **Le roadmap est dans `docs/roadmap-drave.md`** : la niche est « la RAM fait
> moins de 15 % du modèle », personne d'autre n'y fonctionne, et cinq chantiers
> sont à ARRÊTER (mesurés).
>
> **Quatre réfutations mesurées, à ne pas refaire** :
> cache d'experts en VRAM (×1,09 — plafond ×1,41) · cache de pages pour garder le
> dense (deux passes : 1 516 430 puis 1 522 584 ms) · copie anonyme pour épingler
> (swape — et `swapon` N'EXISTE PAS ici, lire `/proc/swaps`) · regroupement par
> experts pour le temps (64 → 48 lectures, **aucun gain**).
>
> **Ce qui marche** : le noyau MXFP4 du moteur sur les experts (×3,6 sur le FFN,
> logits identiques) · le dense emprunté en Q8_0 (×1,12, top-1 identique,
> corrélations 0,998) · le regroupement par experts (64 → 48 lectures, gardé).
>
> **QUESTION OUVERTE, à trancher en premier** : la passe complète coûte **2,95 s
> par couple (couche, jeton)** contre **0,75 s à chaud** — quatre fois plus — et
> réduire de 25 % les experts lus ne change rien. Hypothèse non mesurée : la
> **dispersion** (~144 lectures par couple × ~10 ms de déplacement). Le pas pour
> trancher : `majflt` (`/proc/PID/stat`) et le temps d'attente disque sur une
> passe complète.
>
> **La passe tournait sur UN CŒUR SUR 40** (`Percent of CPU: 99 %`). Elle est
> maintenant parallélisée par (expert, jeton), **bit à bit identique** — mais son
> gain n'est **pas établi** (×1,08 à froid, ×0,90 à chaud, dans le bruit des
> mesures de ce bloc).
>
> **Pièges d'instruments, tous rencontrés** : `swapon`, `bc`, `taskset` **ne
> sont pas installés** ici. Un instrument absent ne renvoie pas « non » — lire
> `/proc/swaps`, faire l'arithmétique en `awk`, et vérifier l'expansion d'un
> argument dans `/proc/PID/cmdline` AVANT de lancer trois heures de calcul.
>
> ## **LE MUR EST LE DISQUE (09h10)** — et le prochain chantier est nommé
>
> Le chiffre qui commande tout : le FFN coûte **3,1 s par couple (couche, jeton)**
> dans la passe complète contre **0,37 s** sur 4 couches. Même code, **huit fois
> plus lent** : la passe streame 1,5 To depuis un disque tournant.
>
> 1. Par appel, la passe relit **~59,6 Go de dense Q8_0 + 12,4 Go d'experts
>    partagés**, contre 25,9 Go d'experts routés par jeton. Pour N jetons, le
>    dense est relu N fois.
> 2. **Le dense tient en RAM** (59,6 Go sur 125) — c'est la thèse du plan.
> 3. Ce qui l'empêche : la **déquantification**. Chaque appel alloue et libère
>    ~224 Go de tampons f32, ce qui **évince le cache de pages**.
>
> **Prochain chantier** : emprunter les blocs Q8_0 au lieu de les déquantifier.
> `Gguf::q8_blocks`, `DenseQ8::emprunter_q8` et `dot_q8_source` existent déjà et
> servent tout le reste du moteur. À faire pour les cinq grosses projections du
> KDA (`attn_q/k/v`, `ssm_g`, `attn_output` : 1,88 Go en f32 contre 0,47 Go en
> Q8_0 par couche), puis la MLA et la FFN dense de la couche 0.
>
> **Modèle déjà écrit** : le noyau MXFP4 sur les experts (`DRAVE_K3_MXFP4=1`) —
> ×3,6 sur le FFN poids en cache, sortie **identique au niveau des logits** sur
> le modèle entier (mêmes corrélations à la 6ᵉ décimale, mêmes top-1). Le même
> geste appliqué au dense attaque le DISQUE au lieu de la RAM.
>
> ## **LE MOTEUR ENGENDRE AVEC KIMI-K3 (06h56)** — et chaque pas est celui de la référence
>
> `DRAVE_K3_GEN=N` : préfill puis jetons gloutons, l'état récurrent (convolution,
> delta, cache MLA) **restauré au rechargement de chaque couche**. Deux appels
> successifs, le second ne voyant qu'un jeton nouveau :
>
> ```
> pas 0 : 2 jeton(s) en entrée (1080 s) → argmax 1103 ✅
> pas 1 : 3 jeton(s) en entrée (1578 s) → argmax 3140 ✅
> ```
>
> 1103 et 3140 sont les **top-1 de llama.cpp-k3** aux mêmes positions. Le second
> pas vérifie donc deux choses : le choix est le bon, **et** il vient d'un état
> restauré, pas recalculé.
>
> **« Faire tourner le modèle en local » au sens plein** : 93 couches, 1,5 To de
> poids, 125 Go de RAM, **une seule couche de poids en mémoire** (~2,2 Go) plus
> ~0,6 Go d'états pour les 93 couches. ~18 min par jeton engendré.
>
> **Piège à connaître** : `DRAVE_K3_IMPOSE` et le tableau d'attente. Le premier
> essai a affiché « argmax 1103 ❌ (référence 1309) » — c'était **mon attendu**
> qui était faux (le jeton cible au lieu du top-1 de la référence). Un attendu
> mal écrit fabrique un échec qui n'existe pas.
>
> ## **LA PASSE COMPLÈTE DE KIMI-K3 PASSE (04h28)** — 93 couches, vérifiées
>
> `DRAVE_K3_PASSE=93` calcule **tout le modèle**, une seule couche en mémoire à
> la fois (~2,2 Go au lieu de ~220 Go). `l_out-92` comparé à llama.cpp-k3 :
> corrélations **0,999857 / 0,999900 / 0,999919** sur trois jetons, écarts
> relatifs 1,4 % / 0,5 % / 0,7 % — **et l'écart ne dérive pas avec la
> profondeur**.
>
> **Quatre des treize points du protocole sont verts** (couches 0, 12, 24, 92),
> et le dernier est le modèle entier : 8 points de contrôle dans la banque,
> 68 couches KDA avec convolution et récurrence, 24 MLA à cache latent, 896
> experts dont 16 par jeton, SiTU.
>
> **ET SES LOGITS SONT CEUX DE LA RÉFÉRENCE (05h06)** — passe complète avec la
> tête, comparée aux logits de llama.cpp-k3 : corrélations **0,999802 / 0,999900
> / 0,999924**, **top-1 identique 3/3**, et l'argmax est **le bon jeton** à chaque
> position (275, 1309, 3140 — les cibles). Le critère de la porte de correction
> du dépôt (≥ 0,95 de corrélation, top-1 ≥ 85 %) passe à **100 %** sur le plus
> gros modèle du parc. `DRAVE_K3_TETE=1` rend les logits au format
> `--logits-bin`.
>
> **Coût mesuré : 7,4 minutes par jeton (tête comprise).** La référence met **42 minutes par
> jeton** sur la même machine (bornée par le disque, 1,80 To lus pour 4 jetons) :
> cette passe ne lit que les 16 experts choisis sur 896 et ne repaquette rien —
> **six fois plus rapide que la référence, et vérifiée contre elle.**
>
> `DRAVE_K3_PASSE=N` est le nouvel outil ; `DRAVE_K3_COUCHES=N` reste pour
> vérifier l'enchaînement couche par couche.
>
> **VINGT-CINQ COUCHES, TROIS BANQUES (03h37)** — `DRAVE_K3_COUCHES=25`, banques
> aux couches 0, 12 et 24. Contre `l_out-24` : jetons 0/1/2 à **0,999984 /
> 0,999893 / 0,999866**. **Trois des treize points du protocole sont verts**
> (couches 0, 12, 24), et l'écart **ne croît pas avec la profondeur** : 3,7e-04 à
> la couche 24 contre 3,1e-04 à la couche 0, pour des dynamiques comparables.
>
> **ET LES TREIZE COUCHES PASSENT (03h17)** — `DRAVE_K3_COUCHES=13`, couches 0
> à 12, donc le **franchissement de la banque de la couche 12** avec un `res_mix`
> à deux points de contrôle :
>
> | couche 12 | jeton 0 | jeton 1 | jeton 2 |
> |---|---|---|---|
> | corrélation | 0,990927 → **0,999945** | 0,458801 → **0,999943** | 0,448762 → **0,999102** |
>
> **Deux des treize points de comparaison du protocole sont verts.** Ce qui est
> vérifié d'un coup : enchaînement résiduel, banque et son redémarrage, `res_mix`
> à deux points, état de convolution et récurrence delta transportés entre
> jetons, MoE latent, MLA à cache latent, SiTU.
>
> | couche 0 | jeton 0 | jeton 1 | jeton 2 |
> |---|---|---|---|
> | corrélation | 0,983164 → **0,999979** | 0,790361 → **0,999982** | 0,641780 → **0,999983** |
> | écart max | 1,19e-02 → **3,74e-04** | 1,55e-01 → **2,92e-04** | 1,80e-01 → **3,07e-04** |
>
> **Leçon payée cher** : le test « KDA contre NumPy » passait au vert depuis le
> début — il comparait le code à sa propre transcription. Un test qui partage
> l'erreur de l'implémentation ne teste rien ; c'est la comparaison à un tiers
> qui a trouvé les trois bugs, en deux heures.
>
> Reste : la couche 12 (13 couches enchaînées, une banque franchie) et l'écart
> résiduel de 0,4 % (accumulation f32 sur des poids Q8_0, à confirmer).
>
> **Et le premier jalon de vérification est NÉGATIF** : couche 0, corrélation
> 0,9832 (pos 0) → 0,7904 (pos 1) → 0,6418 (pos 2) ; couche 12, 0,9909 → 0,4588 →
> 0,4488. Le motif est le message : la position 0 est presque juste et tout se
> défait à la position 1, donc le défaut est dans ce qui TRANSPORTE un état — la
> convolution KDA (`d_conv = 4`) ou la récurrence delta-net. Au jeton 0 la
> convolution ne voit que son remplissage, ce qui explique qu'il y soit invisible.
> Second défaut, plus petit : la position 0 est à ~1 % (norme 0,937 fois la
> référence).
>
> **Prochaine action, dans l'ordre** : (1) bissecter couche par couche avec les
> 93 vidages de la référence pour trouver la PREMIÈRE qui décroche ; (2) comparer
> les tenseurs INTERMÉDIAIRES de la couche 0 (entrée et sortie de la convolution,
> au jeton 1) — `ref_logits --tensors` sait filtrer n'importe quel nœud du graphe.
>
> `REF_SANS_REPACK` est né de là : le repaquetage par défaut de llama.cpp
> recopiait les poids en RAM (104 Go résidents + 6,9 Go de swap après **16**
> tenseurs sur 2 573). C'est la première barrière de cette classe — ni
> l'architecture, ni le format : la politique de mémoire du moteur de référence.
>
> **En cours au moment d'écrire** : `llama-cli` (llama.cpp-k3) charge Kimi-K3 et
> génère — la mesure qui dira ce que la référence fait sur cette machine. La
> porte `gpt-oss-120b MXFP4 ctx 256` (attendue 15,6017) a été **arrêtée
> volontairement** pour lui laisser le disque, après avoir échoué par **délai
> dépassé** et non par chiffre faux ; à rejouer.
>
> **Mise à jour du 02/10 — c'est ce bloc qui fait foi** : Qwen2.5-0.5B Q8_0
> ctx 256 = **19,3885** (inchangée) · clusters Qwen3-30B ctx 64 limit 8 =
> **799,8557** · gpt-oss-120b MXFP4 ctx 256 = **15,6017** (**changée** par le
> correctif de routage : le biais `exp_probs_b` ne doit pas entrer dans le softmax
> des poids — `reports/rapport-routage-experts.md`) · `cargo test --release` =
> **49** · protocole **v5**, modes 0–4. Les lignes gpt-oss plus bas qui portent
> encore 15,1757, 15,1667, 15,0757 ou 18,5803 datent d'AVANT ce correctif : à
> revérifier avant de s'en servir comme porte.
>
> **Chemin GPU revérifié le même jour** (personne ne l'avait exercé depuis les
> changements) : gpt-oss avec `DRAVE_GPU=1` donne **15,1667**, la valeur attendue
> du pilote, et `--gpu-banc` retrouve l'exactitude des noyaux — 1,6 ms par ligne
> en warp-par-ligne contre 7,2 ms sur 30 fils CPU, **écart max 1,99e-7**.
>
> **Mise à jour du 02/10 (20h30) — la rotation des couches compressées, et
> l'instrument qui mentait.** llama.cpp ET vLLM appliquent YaRN ×16 (sans mscale)
> à TOUTES les positions dès que `compress_ratio > 0` ; le moteur y appliquait son
> régime retardé (RoPE simple). Correctif fait et **validé par la mesure** contre
> llama.cpp, tenseur par tenseur, à la position 127 : 4,515e-03 d'écart contre
> 5,376e-03 en RoPE simple (corrélation 0,999996 contre 0,999993).
>
> Le premier essai disait l'inverse — parce que la rampe du moteur était calculée
> avec un contexte d'origine de **4 096** au lieu de 65 536 : `Meta::as_f64()` ne
> lit que les flottants et `rope.scaling.original_context_length` est un **u32**
> dans le GGUF. Le défaut prenait la place de la valeur, sans un mot. C'est en
> remontant des écarts aux ANGLES appliqués (rampe mesurée (8, 18) au lieu de
> (15, 25)) que le bug est apparu. Porte V4-Flash : **8430,2968 → 8430,4966**
> (le chiffre bouge à peine à ctx 32, où les deux régimes coïncident presque :
> c'est la comparaison par tenseur qui tranche). Les chiffres V4-Flash antérieurs
> sont à revérifier.
>
> **Mise à jour du 02/10 (23h) — le découpage V4.1 est exact au bit près, et
> « l'instrument qui mentait » ne mentait pas.** Deux énigmes du sprint 12 sont
> fermées.
>
> 1. **Le V4.1 découpé à la couche 20 donnait 514 722,06 au lieu de 1 743
>    713,62.** Cause : la `pre` reçue du pair pour le jeton *p* restait en place
>    au `forward` du jeton *p+1* — le nœud qui commence à la couche 0 amorçait sa
>    chaîne retardée sur les coefficients de la dernière FFN du pair **au jeton
>    précédent**. Mesuré par tenseur : 629 tenseurs divergents, **tous aux
>    positions 1 et 2, aucun à la position 0**. Correctif : `forward` ne consomme
>    la `pre` reçue que si le nœud **reprend au milieu du modèle**
>    (`couche_debut > 0`), et `norme_finale` prend `&mut self` et la **consomme**
>    (elle appartient à la réduction de ce flux-là). Après : écart **0,00e0**, et
>    **953 tenseurs de la passe répartie du pilote + 945 du nœud moteur
>    identiques au bit près** à une passe complète (et 1 591 fichiers de la passe
>    de référence du pilote, dans un second processus, identiques eux aussi —
>    mais ceux-là ne peuvent pas échouer sur la couture ; voir la revue adverse
>    du bloc 13). Le V4-Flash ne pouvait pas le voir : sa réduction finale
>    est apprise, donc `np = 0` chez lui.
> 2. **La référence du harnais (1 743 713,62) différait de `--ppl`
>    (208 411,867).** Ce ne sont pas les mêmes réglages : `--ppl` quantifie les
>    activations sur **16 bits** (32 767 niveaux, sa référence de non-régression),
>    les modes flux sur **8 bits** (127 niveaux, `appliquer_quantification`).
>    Preuve : `--ppl --abits 8` donne **1 743 713,6243** et **2 544 tenseurs
>    identiques au bit près** à la référence du harnais. `--dense` n'y est pour
>    rien (`--ppl --dense` = `--ppl`, 0 tenseur différent). Le premier tenseur qui
>    diverge entre 127 et 32 767 niveaux est `l_last-0-*` — le **MoE** —, pas
>    l'attention, qui est en f32 et n'est pas quantifiée.
>
> **Corrigé aussi** : les émetteurs de LOTS (modes 3 et 4) n'écrivaient pas le
> préfixe v6 `np` que le décodeur lit pour tous les modes — corps décalé de quatre
> octets. Un seul encodeur (`prefixe_premix`) les sert ; mesuré sur deux nœuds
> (Qwen2.5-0.5B Q8_0, 24 jetons, `--lot 4`) : mode 3 = **0,00e0**, mode 4 =
> 4,45e-3 (avec perte, comme son codec : mode 2 = 3,65e-2).
>
> Sprint : [`sprints/13-les-deux-enigmes-du-decoupage-v41.md`](sprints/13-les-deux-enigmes-du-decoupage-v41.md).
>
> **Mise à jour du 02/10 (21h35) — l'engram est VIVANT, et P8 est fermée.**
> L'injection était branchée et vérifiée par tenseur, mais rien n'établissait
> qu'elle ENTRE dans le calcul. `DRAVE_SANS_ENGRAM=1` (déclaré dans `VARS_LUES`,
> annoncé quand il est actif) coupe le bloc : sur la passe complète V4.1, mêmes
> jetons et mêmes réglages, la perplexité passe de **1 743 713,6243** à
> **1 427 298,2128** (22,2 %), la couche 0 reste **identique au bit près** et les
> couches 1 à 39 changent toutes. Les vides `engram_kv`/`engram_sortie`
> disparaissent quand l'interrupteur est actif — le bloc n'a pas tourné. Mesure de
> VIVACITÉ, pas de qualité — et l'ablation GRANDIT avec le contexte (+22,2 % à
> ctx 8, +55,4 % à ctx 32 : 115 521,8693 contre 74 328,5818), ce qui est la
> signature d'une mémoire. **Question ouverte, chiffrée : retirer l'engram AMÉLIORE
> la perplexité sur ces deux fenêtres.** La formule est exclue comme cause (les
> quatre règles sont vérifiées contre la transcription numpy et contre le portage
> publié `mudler/vllm.cpp`, relu le 02/10) ; reste la provenance de la table, du
> `token_map` ou des poids d'injection du fichier Q2. Le masque
> des jetons d'image reste un no-op **décidé** (sans objet en texte, réouverture
> avec un chemin multimodal V4.1).
>
> **Mise à jour du 02/10 (23h) — V4.1 trois fois plus rapide, sans changer un
> bit.** Le poste d'attention valait 12 369,91 ms par jeton parce que son produit
> matrice-vecteur f32 était **mono-fil** ; il est maintenant parallèle **par
> lignes** (chaque ligne garde son ordre de sommation) : **1 324,48 ms/token**,
> et la passe complète de 66-68 s à **22,2 s** — perplexité et 2 544 vides
> **identiques au bit près**, porte V4-Flash 8430,4966 inchangée. De bout en bout
> à ctx 32 : 313,1 s → 152,9 s (×2,05). Nouveau profil : `postes` + une ligne
> « dont attention V4 » (projets q/kv, compresseur, indexeur, scores+somme,
> dé-rotation+sortie groupée) — le calcul d'attention proprement dit ne fait que
> **4,5 %** du poste ; le poste dominant est maintenant `proj+mlp` (lecture
> d'experts). Essayé et **refusé par la mesure** : un cache RAM des experts
> (`DRAVE_EXPERTS_RAM`) est 4 à 21 % PLUS LENT (le noyau cache déjà) — drapeau
> éteint, verdict dans son annonce.
>
> ## ⚠️ 03/10 (02h50) — V4.1 ne prédit pas (V4-Flash, si)
>
> Test fonctionnel : huit répétitions de « The sky is blue. » (39 jetons). Un
> modèle qui fonctionne donne une perplexité de 1 à 2.
>
> | moteur | modèle | PPL |
> |---|---|---|
> | llama.cpp | V4-Flash IQ1_M | **1,844** |
> | Drave | V4-Flash IQ1_M (mêmes identifiants) | **1,875** |
> | Drave | V4.1-Flash Q2, sans engram | **3 677** |
>
> Sur 31 positions : top-1 exact **0/31**, NLL 11,657 nats (uniforme 11,770).
> Tokenizer hors de cause (référence externe `tools/tokenize_llama`, identifiants
> identiques). Le chemin V4 partagé est juste ; le défaut est dans un mécanisme
> propre à V4.1 (chaîne mHC retardée, compresseur des ratios 1 et 2, ou engram).
> **Conséquence de lecture** : tous les chiffres V4.1 du dépôt sont des références
> de non-régression, pas des mesures de qualité. Localisation : bloc 21.
>
> **Mise à jour du 03/10 (00h) — la nuit des optimisations, et pas un chiffre
> changé.** Trois leviers, tous prouvés bit-exacts (5 670 tenseurs comparés au
> total, 0 écart) :
>
> | levier | effet |
> |---|---|
> | matvec f32 parallèle **par lignes** | attention 12 369,91 → 1 324,48 ms/token (×9,34) |
> | `threads_iq` déborné (8 → 20 fils) | `proj+mlp` ctx 32 : 3 530 → 2 432 ms/token |
> | noyau **AVX2** de déquantification Q2_K | `proj+mlp` ctx 32 : 2 432 → 1 834 ms/token |
>
> **Passe V4.1 à ctx 32 : 313,1 s → 88,5 s (×3,54)** ; à ctx 8 : 66-68 s → 10,7 s ;
> découpage à deux nœuds : 0,00e0 en 16,4 s (référence locale 25,6 s, contre 68,0
> en début de nuit). Le profil de V4.1 a maintenant une ligne « dont attention V4 »
> (le calcul d'attention proprement dit ne fait que 4,5 % du poste) et la porte
> V4-Flash reste à **8430,4966**.
>
> **Deux choses essayées et REFUSÉES par la mesure** : un cache RAM des experts
> (+4 % à 4 Go, +21 % à 32 Go — le noyau cache déjà) et le SIMD du produit
> scalaire (il réassocie la somme, donc changerait la référence). Le noyau IQ1_M
> (V4-Flash) ne rend que ×1,07 : son coût est la LECTURE du codebook, pas
> l'arithmétique.
>
> **Revue adverse du bloc 13** : trois chiffres publiés corrigés (953 tenseurs de
> la passe répartie et non 2 544 ; 82 016 octets au retour et non 81 999 ; la
> trame sans préfixe v6 **interbloque** le pair au lieu d'être « fausse et
> muette ») et quatre trous fermés (compteur des octets reçus, `take()` en tête de
> `norme_finale`, refus d'une `pre` sur une trame `debut = 0` et sur un LOT, code
> retour de la porte du découpage). Détail : `sprints/13`.
>
> **Mise à jour du 02/10 (22h) — l'ENGRAM de V4.1 est branché, et une passe avant
> V4.1 COMPLÈTE devient possible.** Le hachage glissant (O(1) par jeton : la
> fenêtre de `max_ngram − 1` suffit), la lecture des 24 rangées de 264 octets dans
> les tables de 101 Go, la projection `wkv` [25 600, 6 144] et l'injection sur les
> `hc` copies sont dans la passe avant, en tête des couches 1 et 14. Vérifié de
> bout en bout (`tools/verifier_v41_engram.py` : adresses recalculées par la
> référence, rangées relues dans la vraie table) : projection à ~1e-5
> (accumulation f32 sur 6 144 termes), injection à ~1e-6. Coût annoncé :
> **6 336 octets par jeton et par table**. La liste des manques de V4.1 est
> désormais **vide** : le modèle des 40 couches tourne, l'indexeur gardant tous les
> blocs, exact sous `indexer.top_k` (512) et refusé au-delà. Le chemin par LOTS,
> lui, refuse maintenant les modèles à hyper-connexions (`--lot > 1`) : son corps
> n'a aucune occurrence de `hc_*`, donc il calculait un autre modèle en silence.
>
> **Mise à jour du 02/10 (20h) — le cache compressé partagé, et une régression
> attrapée par la porte.** Les **34 couches consommatrices** de V4.1 lisent
> maintenant les tampons de leur source (`comp_source`), prouvé par un contrôle
> positif/négatif (sortie de la couche 3 : 1,30 à 2,16 d'écart selon que sa source
> a tourné ; sortie de la source 2 identique au bit). En chemin, une régression :
> la largeur du compresseur calculée par `dims[0] / hidden` donnait **0** aux
> couches CSA de V4-Flash (`1024 / 4096` en entiers) et la porte est tombée de
> **8430,2968** à **5026,4538** — attrapée par la porte du modèle entier, pas par
> les sondes d'une seule couche (le bloc compressé n'y est construit qu'à la
> dernière position, jamais notée). Corrigé, remesuré : **8430,2968**.
>
> **Mise à jour du 02/10 (19h) — le compresseur de V4.1, ratios 1 et 2.** Les
> **couches sources** (celles qui possèdent leurs tenseurs de compresseur : 2, 8,
> 14, 20) tournent et sont vérifiées contre une référence numpy écrite depuis le
> noyau `fused_save_compress_norm` : pool `comp_brut` à ~5e-07, norme + RoPE de
> bloc à ~5e-06 sur une dynamique de 1,2 à 2,6 (arrondi f32). La couche 20
> (ratio 1, **sans porte ni `ape`**) publie bien un bloc par jeton, la couche 2
> (ratio 2) un bloc par groupe de deux. L'indexeur de V4.1 (clés tirées du latent
> du compresseur principal) n'est pas porté : le moteur garde tous les blocs —
> exact sous `indexer.top_k` (512), refusé au-delà — et le dit. Les **34 couches
> consommatrices** (partage du cache compressé) sont refusées avec ce motif.

> La chaîne **mHC retardée** de V4.1 est implémentée et vérifiée sur le fichier de
> **365,7 Go** : la copie 0 du premier raccord est **exacte** (0,000e+00), les 24
> mélanges et la réduction finale (pas de tête apprise) tiennent à ~1e-7, recalculés
> en numpy hors du moteur (`tools/verifier_v41_mhc.py`,
> `reports/rapport-v41-mhc.md`). `cargo test --release` = **59**. Deux manques
> annoncés pour V4.1 étaient **faux** (la référence d'exécution existe : vLLM) et
> sont remplacés par la liste réelle des manques. Nouveau drapeau :
> `--tete-partielle`. Trois bugs de configuration corrigés au passage
> (`n_expert` relu en GGUF-seul, `rms_norm_eps` ignoré, YaRN déclaré dans le JSON
> et non lu).

> **Mise à jour du 03/10 — la porte de correction tient à ctx 512, et le stockage
> explique deux fausses pistes.** (1) À ctx 512 (511 prédictions, chemin par
> défaut, référence llama.cpp sur la même fenêtre) : corrélation moyenne
> **0,989879**, min 0,941811, top-1 **475/511 (93,0 %)**, PPL 6,2612 contre
> 6,0030 (+4,3 %). **L'accord s'améliore avec la position** (0,98534 → 0,98934 →
> 0,99142) : aucune dérive de rotation, de blocs ni de fenêtre. (2) Le coût par
> jeton passe de 2,50 s (ctx 64) à **2,58 s (ctx 512)** : ce que les blocs 23-24
> prenaient pour une croissance (jusqu'à « 60 s/jeton à ctx 1 024 ») était le
> **disque dur** qui portait le modèle. (3) **Chiffre corrigé** : le gain de
> `DRAVE_SIMD_DOT` est **×1,18 sur la passe, ×1,37 sur `proj+mlp`** (A/B
> entrelacé) et non ×2,06/×3,05 comme publié d'abord — le run de référence
> tournait pendant qu'un processus survivant d'un `timeout` occupait les cœurs.
> (4) Granularité des listes : **elle route, elle ne compresse pas**
> (`reports/rapport-granularite-flux.md`).

Corpus : `/tmp/wt2_txt.txt` = 20 000 premiers octets de `data/wikitext2_test.txt`.
**Régénérable** (à refaire si `/tmp` a été vidé) :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
head -c 20000 data/wikitext2_test.txt > /tmp/wt2_txt.txt
# les identifiants DOIVENT venir du tokenizer du modèle — jamais croisés
drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
    --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_qwen.txt
drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf \
    --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_oss.txt
```

Le mode `--tokenize --fichier` **vérifie la réversibilité** (texte reconstruit
identique à la source) — les deux tokenizers la passent sur ce corpus.

| modèle | commande (abrégée) | perplexité attendue |
|---|---|---|
| Qwen2.5-0.5B Q8_0 | `--dense --limit 512` | **19,3885** |
| Qwen2.5-0.5B Q4_0 | `--q4 --limit 512` | **21,0110** |
| Qwen2.5-0.5B Q8_0, 6 bits | `--dense --bits-attn 6 --bits-ffn 6 --limit 512` (ctx 256) | **19,5633** ← bat l'int8 (19,8059), mais de moins loin qu'annoncé : la valeur **19,3045** qui figurait ici n'est PAS reproductible avec cette commande (re-mesuré le 30/09, deux fois) |
| Qwen2.5-0.5B Q8_0, 4 bits | `--dense --q4 --limit 512` | **23,1323** |
| Qwen2.5-1.5B Q4_K_M | `--q4 --limit 256` | **12,9228** |
| Qwen2.5-VL-7B Q4_K_M | défaut, `--limit 128` | **10,9947** |
| Qwen3-30B-A3B MoE | `--dense --limit 128` | **7,6139** |
| gpt-oss-120b MXFP4 | `--dense --limit 64`, ids_oss | **20,8361** (63 jetons) |
| gpt-oss-120b MXFP4 | `--dense --limit 512`, ids_oss | **15,6017** (510 jetons, deux fenêtres) — était 15,1757 avant le correctif de routage du 02/10 |
| gpt-oss-120b MXFP4 | `--ppl-texte`, `--limit 512` (mêmes jetons) | **15,0757** (509 jetons) — *avant* le correctif de routage du 02/10 |
| gpt-oss-120b MXFP4 | `--dense --ctx 512 --limit 512`, ids_oss | **18,5803** (511 jetons, une fenêtre) — *avant* le correctif de routage du 02/10 |
| gpt-oss-120b MXFP4, YaRN | `DRAVE_YARN=1`, `--ctx 512 --limit 512` | **174,3375** ← le YaRN statique du modèle (mesure d'avant le correctif de routage) |

> **gpt-oss : les anciens chiffres (39,8 puis 129,9) sont périmés.** Ils ont été
> mesurés avec deux bugs depuis corrigés : le biais `attn_output` ignoré et la
> fenêtre glissante appliquée aux 36 couches au lieu d'une sur deux. Le détail
> est dans `reports/rapport-gpt-oss-perplexite.md` ; la **référence externe**
> (llama.cpp, mêmes identifiants, sans BOS) donne 38,37 à 63 jetons et 169,67 à
> 511 en mode YaRN — notre moteur fait **mieux**, parce qu'il sait éteindre
> YaRN, qui coûte ici un facteur 9.

Toujours `--ctx 256 --abits 16 --threads 16`, et **jamais croiser les fichiers
d'identifiants** : nourrir un modèle avec le découpage d'un autre donne une
perplexité qui ne mesure que l'absurdité de l'entrée (42 127 mesuré ainsi).
Un garde-fou le détecte maintenant (identifiant ≥ vocabulaire = erreur franche).

---

## 2bis. La cible a changé (03/10) : Kimi-K3, et le tokenizer kimi

> **Les modèles périmés sortent du chemin critique** (DeepSeek-V4-Flash : acquis
> conservés, portes archivées) au profit des **meilleurs modèles ouverts**, en
> particulier ceux qui ne tiennent pas en local. La cible est **Kimi-K3** :
> 1 508,7 Go en Q4, 93 couches, 896 experts dont **16 par jeton**, 1 M de
> contexte, attention **hybride** (KDA delta-net 3 couches sur 4 + MLA), MoE
> **latent**, attention résiduelle inter-couches, SiTU. Détails :
> `docs/plan-kimi-k3.md` et `docs/architecture-kimi-k3.md`. **Un jeton lit ~35 Go
> de poids** (2,3 % du modèle) : c'est le sujet.
>
> **Deux défauts silencieux corrigés avant même de faire tourner le modèle**
> (`tools/porte-tokenizer-kimi.sh`, référence officielle en pur Python) :
> le motif `kimi` n'était pas implémenté (nos identifiants divergeaient sur les
> chiffres et le chinois — **Kimi-K2.7 était touché aussi**), et le découpage par
> casse enjambait les majuscules (« HelloWorld » d'un morceau). 11 textes sur 11
> identiques à l'officiel, 69 tests verts, gpt-oss inchangé.
>
> **Référence exécutable** : `llama.cpp` amont connaît `kimi-k3` — une seconde
> copie est construite (`llama.cpp-k3/`) et `tools/ref_logits_k3` est lié contre
> elle. La porte de correction est donc **possible** sur cette classe, ce qui
> n'était pas le cas pour V4.1.

## 3. Ce qui est implémenté et vérifié

| domaine | état |
|---|---|
| Formats lus **en place** | Q4_K, Q6_K, Q4_0, Q8_0, MXFP4, F16, F32 |
| MoE | routeur + biais de routeur, biais par expert, top-k, expert partagé, tranches contiguës |
| Architectures | q/k-norm (Qwen3), `post_attention_norm` (gpt-oss), sinks appris, fenêtre glissante, YaRN (défaut **off**), RoPE simple et partiel (conventions **NEOX** et **NORM**), `head_dim` déclaré |
| Trois attentions | dense (Qwen/gpt-oss), MLA latente (GLM/Kimi, `attn_kv_a_mqa`), **MLA V4** (`attn_kv`, une tête normée en entier, seconde RMS par tête, valeurs = clés, dé-rotation, sortie groupée `attn_output_a/b`) |
| Hyper-connexions | DeepSeek-V4/V4.1 : résidu en `hc` copies (4), mélanges `pre`/`post`/`comb` par couche, **Sinkhorn** (20 itérations), mélange de tête optionnel. Validé contre llama.cpp à **1e-7** (`reports/rapport-v4-couches-0-1.md`) |
| Exécution bornée | `--couches a:b` : exécute une plage de couches pour comparer à la référence avant que le reste du modèle existe. Le manque retiré est **annoncé**, jamais silencieux |
| États injectés | `DRAVE_ETAT_ENTREE=<fichier REFD>` : démarre la boucle de couches avec le résidu qu'a produit **llama.cpp** (`l_last-<k-1>`), pour valider **une seule couche** quand la précédente n'est pas encore implémentée |
| Attention V4 compressée | **HCA** (ratio 128) faite et validée : valeur + porte par jeton, `ape` de rang, softmax **par canal** sur les 128 jetons du bloc, norme, RoPE de bloc (base 160 000, position du premier jeton), puis fenêtre brute + blocs complets (`n_visible = (pos+1)/ratio`). **CSA** (ratio 4) refusé explicitement (P5) |
| Tête de sortie | `output.weight` si non lié (bug corrigé), sinon `token_embd` |
| Tokenizers | Qwen2 **et** o200k (gpt-4o), tous deux lus du GGUF, sélectionnés par `tokenizer.ggml.pre` |
| Échantillonnage | température, top-k 40, top-p, **pénalité de répétition** (`--rep-penalty`, fenêtre `--hist`) |
| Génération | **sortie en flux** (`--flux`), **session multi-tours** (`--session`), arrêt sur fin de tour |
| Encodages | listes d'événements (push), dense int8 par ligne, dense 4 bits par bloc, **6 bits empaqueté par bloc** |
| GPU | noyaux PTX + API pilote, tête et projections opt-in (`DRAVE_GPU=1`) |
| Outils | `--ppl`, `--plan` (placement), `--tokenize`, `--bits N` (simulation de précision) |
| Mesure | `--ppl-texte F` (identifiants du tokenizer du modèle), `--depuis N` (ne noter qu'à partir du jeton N, contexte ancré — les mêmes jetons deviennent comparables à 512, 1 024, 4 096… de contexte), `--ppl-profil` (perte par tranche de 256 positions), `--logits-bin F` (logits bruts), `--harmony*` (habillage harmony), `--swa-pattern N`, `--sans-fenetre` |
| Rotation | **YaRN à retardement** : RoPE simple tant que `--ctx` ne dépasse pas **4 ×** `rope.scaling.original_context_length` (16 384 pour gpt-oss), **interpolation YaRN seule au-delà** (la température `mscale` est la moitié nuisible : divise la perplexité par 8,9 à 512 jetons). `DRAVE_YARN=1` = YaRN complet des références, `DRAVE_YARN_NON=1` (ou `--sans-yarn`) = jamais, `DRAVE_YARN_MSCALE=0/1` = température seule. La trace `[config] rotation` dit lequel est actif |
| Budget de contexte | `--plan --ctx N` : KV f32/int8/int4, relecture par jeton, décodage selon les bandes passantes, coût du préremplissage séquentiel, portée du YaRN |
| Référence externe | `tools/ref_logits` (llama.cpp, mêmes identifiants, sans BOS) + `tools/compare_logits.py` |
| **Flux mesuré** | le rapport de `--ppl` donne les **paires** (poids × activation) par provenance — **attention / experts / partagé** — et les scores : c'est ce qui dit *où* passe le flux, donc ce qu'on peut déporter, découper ou simplifier. Les **événements** ne comptent que le chemin en listes (poids non nuls) ; les paires comptent tout ce qui est payé, y compris les chemins **déquantifiés (IQ)** et **MLA f32** qui n'affichaient que des zéros (`reports/rapport-p0-flux.md`) |

**Vérifications externes déjà faites** (elles ont trouvé les bugs) : déquantification
Q4_K/Q6_K comparée à une référence F16 des mêmes poids ; tokenizer o200k comparé
à `/tokenize` ; perplexités recoupées avec `llama-perplexity` ; **logits comparés
un à un à llama.cpp** sur les mêmes identifiants (corrélation 0,999976 au premier
jeton, top-1 identique sur 63 positions, |ΔNLL| médian 0,076) ; tokenizer o200k
comparé à `llama-tokenize` sur 4 424 jetons (0 écart).

---

## 4. Pièges de l'environnement (tous rencontrés)

| piège | solution |
|---|---|
| **CUDA 13 : les symboles non versionnés du pilote échouent** (`cuMemAlloc` → erreur 201 alors que le contexte est courant) | utiliser partout les `_v2` |
| `nvcc` refuse gcc 15/16 (conflit d'en-têtes glibc) | compiler en **PTX avec clang**, le pilote compile à la volée |
| Python/numpy lent | `LD_PRELOAD=/usr/lib64/libopenblas.so.0` |
| 16 fils **battent** 32 sur ce moteur | ne pas sursouscrire la barrière tournante ; `--threads 16` |
| Épinglage NUMA | **perd** (23,2 → 25,5 s sur le 30 B) ; `--pin` déconseillé |
| Déport GPU | rentable seulement au-delà de **8 Mo** par matrice ; la tête n'est **pas** déportée (noyau non coalescé, 23 → 159 ms) |
| Charge de fond de la machine | fait varier les durées du simple au double : entrelacer les A/B, préférer les métriques déterministes |
| **Le support du modèle change tout** (03/10) : V4-Flash vivait sur `WDC WD120EFGX`, un **disque ROTATIONNEL** (`/home/stephane/Data13TB`), et le cache de pages est partagé. Un jeton lit **2,669 Go de poids** → **13,3 s/jeton** à 200 Mo/s. Rejoué sur NVMe, le même protocole passe de 1 027,7 s à **567,1 s** (×1,81) et le débit devient **plat** | mesurer sur une copie NVMe (`/home/stephane/FastNVMe/modeles-lourds/v4flash-iq1m/`, 86,9 Go, vérifiée) ; dire sur quel support chaque chiffre a été obtenu |
| Un `read_bytes` lu **une fois** ne prouve rien (instantané ≠ intervalle) | échantillonner `/proc/<pid>/io` **pendant toute la passe** et rapporter au temps |
| Les boucles d'analyse CLI sont **triplées** | un drapeau en **dernière** position était ignoré ; `--pin` et `--moe-topk` absents d'un des modes. Vérifier le mode visé |

---

## 5. Règles de méthode (chacune a coûté une erreur)

1. **Mesurer avant de conclure.** Le croisement push/pull était annoncé à 10 %,
   il est à 22 %. Dérouler un noyau « évident » n'a rien donné : le chemin était
   au mur mémoire, pas mal écrit.
2. **La double quantification est le piège le plus cher** : +12 % de perplexité
   sur Q4_0, et une simulation de précision qui annonçait 19,96 là où le format
   réel donne 19,30.
3. **Une hypothèse se teste, elle ne se défend pas.** Trois ont été réfutées cette
   session : cache KV pour l'attention (c'était la vectorisation), rotary partiel
   pour gpt-oss (185 → 1 095), YaRN (184,9 contre 39,8 sans).
4. **Vérifier quel chemin est actif** avant de déboguer un chiffre : la trace
   `[config]` au chargement dit quelles particularités ont été reconnues.
5. **Ne pas conclure sur 255 jetons** : l'écart peut être du bruit ; 510 minimum.
6. **Ne pas laisser un dépôt cassé** pour finir une refactorisation : revenir au
   dernier état valide est une option honorable.
7. **Mesurer avant de LANCER** (03/10, bloc 23). Une passe de 1 024 jetons sur
   V4-Flash a été lancée sans mesurer le coût au contexte visé : **60 s par jeton**,
   soit 17 heures — arrêtée après 25 minutes et 6 positions. Une passe de 4 jetons
   au contexte visé coûte une minute et donne le budget. Coût par jeton mesuré :
   **3,2 s à ctx 32** (attention 1,19 s, proj+mlp 2,04 s) — et il croît avec le
   contexte, alors que llama.cpp fait la même passe de 1 024 jetons en 4 minutes.
8. **Un drapeau qui ne fait rien doit être dit.** `--dense` est **inerte pour
   V4-Flash** : PPL identique au chiffre près, durées identiques, et le compteur
   « dont en listes » reste à 0,0 M — le modèle passe par le chemin dense de toute
   façon. Deux blocs durant, il a été cru « aligné sur llama.cpp » : c'était une
   supposition, pas une mesure.
9. **Une optimisation qui change une sortie dit ce qu'elle change** (03/10,
   bloc 24, chiffres CORRIGÉS au bloc 26). `DRAVE_SIMD_DOT=1` vectorise le produit
   scalaire des experts (AVX2+FMA, quatre accumulateurs) : **×1,18 sur la passe**
   V4-Flash et **×1,37 sur `proj+mlp`** (mesure entrelacée : 157,8 → 133,9 s ;
   1 472 → 1 078 ms/token) — et **+0,15 %** de perplexité, corrélation 0,9981
   contre notre propre chemin scalaire. Les premiers chiffres publiés (×2,06 et
   ×3,05) venaient d'un run de référence pollué par un processus survivant. Le drapeau s'annonce au premier appel et reste
   **opt-in** (l'activer par défaut déplacerait 8430,4966 et les autres
   références). Le chemin par défaut, lui, reste **bit à bit** celui d'avant.
10. **Une mesure sous charge non vérifiée n'est pas une mesure.** Un A/B a donné
   319 s contre 78 s pour le même travail : un processus `drave` avait survécu au
   `timeout` du shell (`timeout` tue le shell, pas son enfant). Vérifier
   `pgrep -x drave` avant de conclure.

---

## 6. Les huit chantiers : où ils en sont

| # | chantier | état | mesure |
|---|---|---|---|
| 1 | protocole de perplexité longue | **fait** | `--depuis N` note les mêmes jetons à contexte variable ; `--depuis 256 --ctx 256` redonne exactement la fenêtre 2 historique (21,565) |
| 2 | seuil de rotation YaRN | **fait, seuil à 4 × la longueur déclarée** | comparaison appariée (mêmes 512 jetons) : contexte 128→1536, RoPE simple 39,52/49,79/49,93/298,56 contre interpolation 42,13/82,02/82,15/578,86 → le simple gagne partout. **Au-delà du seuil** (5 120 jetons, corpus de 17 k maintenant disponible) : simple **9,6986** contre interpolation seule **1 269,1777** → le seuil de 4 096 était **trop bas**, puis celui de 1,25 × mesuré insuffisant ; le moteur ne bascule qu'à **4 × la longueur déclarée** (16 384 pour gpt-oss) — `docs/contexte-long.md` §5.quater. Au-delà (131 k) : non mesuré |
| 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** contre +494 % pour llama.cpp — meilleur que la référence, et 1 M tient en int4 (9,7 Go). Prix caché : la passe coûte 864 s (f32) / 1 144 (int8) / 1 461 (int4), la déquantification par élément — c'est ce que le noyau GPU de E4 supprime |
| 4 | préremplissage par lots | **fait, −20 % et attribué** | tuilage, **attention groupée dans le lot** et **tête en lot** (`logits_lot`) : Qwen ctx 512, **17,1 s → 13,6 s (−20 %)** à perplexité égale (13,1368 → 13,1359) ; gpt-oss ctx 256, ≈ 50 s → **34,4 s** (13,7205 partout). Postes : projections ÷2,6, FFN/wo ÷1,43, attention par lots encore **×1,7** (5,59 contre 3,24 ms/jeton), tête inchangée (5,47 contre 5,63 — noyau lié au calcul, pas à la mémoire). Au passage : pointeur gras sur les sommes par bloc (lot > 90 → blocage muet) corrigé et verrouillé par un test — voir `reports/rapport-prefill-par-lots.md` |
| 5 | échelles par bloc pour `DenseQ8` | **fait, hypothèse réfutée** | 23,696 contre 23,612 : les échelles par bloc n'apportent rien ; l'avantage du 6 bits est son coût (25 % d'octets en moins à qualité égale) |
| 6 | boucles CLI unifiées | **fait** | `struct Options` + `analyser` ; trois drapeaux de plus trouvés ignorés (`--attn-topk`, `--qk-topk`, `--sans-yarn` en inférence) et un bug de pas de lecture corrigé |
| 7 | noyaux GPU | **fait, quatre formats** | warp par ligne : tête **Q8_0** (1,6 ms contre 7,3 CPU, écart 2e-7), **MXFP4** (0,1 ms, écart **0,00e0** — bit à bit), **Q4_K** (0,5 contre 1,2 ms, 4e-7), **Q6_K** (3,6 contre 8,3 ms sur la tête liée de 191 Mo, 3,3e-7 ; ×5 sur un tenseur de 11 Mo). **Tête Q6_K branchée** dans le moteur : `DRAVE_GPU=1 DRAVE_GPU_TETE=1` → 7,58 → **3,60 ms/jeton**, perplexité identique (13,6877). Reste le cache d'experts chauds en VRAM : la mesure d'activation (`rapport-localite-activation.md`) dit qu'un préchargement statique ne paie pas sur SiLU |
| 8 | suite du plan 1 M | **fait pour E4/E5** | **E4 KV déporté en VRAM** : noyaux `attn_kv_*` (tuiles de 32 clés, softmax en ligne, recombinaison + puits), miroir du cache **paginé** (capacité doublée à la demande : 0,05 Go de VRAM à ctx 1 M après 512 jetons) et `DRAVE_GPU_KV=1` — à 1 M de clés l'attention passe de 968 ms à **13,2 ms** par couche (int4, ×73) et, dans le moteur à 4 096 de contexte, de **22,2 à 3,3 ms/jeton** (−38 % de bout en bout) à perplexité identique (12,2177 → 12,2175). **E5 attention creuse** : mesurée (`--attn-topk 256` : 234,9 contre 298,6). MLA et vision restent non testables (aucun modèle MLA ici ; le projecteur `mmproj` est là mais rien ne lit les patchs) |

### Mesures du tour « huit chantiers » (toutes commitées)

| mesure | valeur |
|---|---|
| noyau GPU Q8_0 warp (tête Qwen 0.5B, 144,6 Mo) | **1,6 ms** contre 7,3 ms CPU (×4,6), écart 2e-7 |
| noyau GPU MXFP4 warp (expert gpt-oss, 4,4 Mo) | **0,1 ms** contre 7,5 ms CPU (×75), écart **0,00e0** |
| noyau GPU Q4_K warp (Qwen 1.5B, 7,7 Mo) | 0,5 ms contre 1,2 ms CPU (×2,2), écart 4e-7 |
| noyau GPU Q6_K warp (tête liée Qwen 1.5B, 191,4 Mo) | **3,6 ms** contre 8,3 ms CPU 16 fils (23,2 → 53,6 Go/s), écart 3,3e-7 |
| noyau GPU Q6_K warp (ffn_down Qwen 1.5B, 11,3 Mo) | **0,3 ms** contre 1,5 ms CPU (×5), écart 7,1e-7 |
| tête Q6_K déportée (Qwen 1.5B Q4_K_M, ctx 256, 510 jetons) | 7,58 → **3,60 ms/jeton** ; bout en bout 44,4 → 41,4 s (−7 %) ; lot 512 : 36,0 → 34,0 s ; **perplexité identique** (13,6877 / 13,6864) |
| préremplissage par lots (Qwen, ctx 512) | lot 1 = **17,1 s** · lot 512 = **13,6 s** → **−20 %** (perplexité 13,1368 → 13,1359) |
| préremplissage par lots (gpt-oss, ctx 256, MoE groupé) | ≈ 50 s à lot 1 · **34,4 s** à lot 256 (13,7205 dans tous les cas) |
| tête de sortie en lot | **aucun gain** (5,47 contre 5,63 ms/jeton) : noyau lié au calcul — il faut AVX2 ou le GPU |
| attente du pool après panique d'un worker | **échoue en clair** au lieu de boucler (constaté : 10 min d'attente active) |
| KV int8, échelles par bloc | +1,5 % (512 jetons) et +3,4 % (4 591) — était +7,1 % et +5,2 % |
| KV int4, échelles par bloc | +219 % (512) et +287 % (4 591) — était +384 % et +450 % |
| KV à 8 192 jetons (longueur de la référence llama.cpp) | f32 **14,2339** · int8 **14,6667 (+3,0 %)** contre +0,8 % chez llama.cpp · int4 **66,0369 (+364 %)** contre +494 % chez llama.cpp |
| porte gpt-oss selon l'ouverture du pilote | sans `DRAVE_GPU` : **15,1757** · avec `DRAVE_GPU=1` : **15,1667** — l'écart vient du déport automatique des projections Q8_0 (> 8 Mo), pas d'une régression |
| attention creuse (gpt-oss, ctx 2 048) | sans restriction 298,56 · **top-256 : 234,88** · fenêtre 512 : 3 269,34 |
| KV déporté en VRAM, 1 M de clés (une couche, `--banc-kv`) | f32 165,8 → **13,6 ms** (×12) · int8 510,6 → 15,0 (×34) · int4 968,5 → **13,2 ms (×73)**, écarts 1e-5 à 1e-4 |
| KV déporté dans le moteur (`DRAVE_GPU_KV=1`, ctx 4 096) | attention **22,16 → 3,29 ms/jeton** (÷6,7) · balayage 219,4 → **136,2 s** · perplexité 12,2177 → 12,2175 |
| attention déportée dans le PRÉREMPLISSAGE par lots (ctx 4 096, lot 512) | **261,6 → 93,7 s (×2,8)**, perplexité **identique** (12,2175) |
| dépaquetage vectorisé du noyau (1 M de clés) | f32 13,6 → **7,0 ms** (308 Go/s) · int8 15,0 → **6,5** · int4 13,2 → **7,4 ms** |
| cache d'experts MXFP4 en VRAM (gpt-oss, 32 jetons) | 5,12 → **5,43 jetons/s (+6 %)**, 53,5 % de succès — verdict : ne pas activer par défaut |
| cache KV CPU paginé (ctx 1 M, 512 jetons écrits) | **0,03 Go** alloués au lieu de 25,77 Go, perplexité inchangée |
| aiguille v2 (12 sondes) | **12/12 trouvées** : 1,5B 512/2048, 30B 2048, gpt-oss 4096, profondeurs 0,1/0,5/0,9 |
| KV déporté, ctx 512 (point de croisement) | attention 2,91 (CPU) contre 3,22 ms (GPU) : le noyau ne paie qu'au-delà de ~4 000 clés |
| miroir VRAM paginé (capacité doublée à la demande) | à **ctx 1 M** : cache CPU 25,77 Go contre **0,05 Go** de VRAM pour 512 jetons écrits (l'allocation d'un bloc exigeait 25,77 Go et refusait) ; perplexité 13,1369 inchangée |
| rotation, comparaison appariée | RoPE simple gagne à TOUTES les longueurs mesurées : 128 à 1 536 (39,5 → 298,6), 5 120 (**9,70 contre 1 269,18**), 16 384 (**35,18 contre 1 133,02**) |

### Ce qu'il faut faire ensuite, dans l'ordre

État au moment d'écrire : les huit chantiers de la campagne précédente sont clos
(voir le tableau du §6), et la campagne « six nouveaux chantiers » a livré
l'aiguille v2, le dépaquetage vectorisé du noyau d'attention, les experts MXFP4
en VRAM, l'attention par lots déportée et la pagination des deux caches KV. Ce
qui reste est classé par rentabilité mesurée.

1. **Fusionner la chaîne du top-k déporté.** Elle gagne déjà à 16 k (attention
   19,58 → **7,59 ms/jeton**, balayage −24 %), mais coûte 8 lancements et 17
   transferts par couche et par jeton : un seul noyau par ligne (descente radix +
   collecte + somme, les k scores en partagé) doit ramener les 8 lancements à 2 et
   supprimer le tampon `nh × n × 4` que le plan déclarait « trop ». Critère :
   dépasser le CPU dès 4 000 clés. Détail : `docs/plan-gpu-topk.md`, § « La
   prochaine étape n'est pas un noyau de plus ».
2. **Noyau de la tête Q8_0.** Le chemin CPU de la tête par lots est **lié au
   calcul** (5,5 ms/jeton pour Qwen 0.5B, le lot n'y change rien). Deux voies :
   un noyau AVX2 (le déport GPU Q8_0 existe déjà : 15,6 → 6,2 ms/jeton sur
   gpt-oss). C'est le premier consommateur après le FFN.
3. **Second GPU.** 16 Go dorment. Le cache d'experts MXFP4 (13,2 Mo par expert,
   4 608 experts chez gpt-oss) et le KV à 1 M le rempliraient utilement ; il faut
   un second contexte CUDA et une règle de répartition.
4. ~~**Rotation au-delà de 5 120 jetons.**~~ **MESURÉ À 16 k** : RoPE simple
   **35,18** contre **1 133,02** en interpolation seule, et le seuil est passé à
   **4 ×** la longueur déclarée (16 384, la plus grande longueur mesurée).
4. ~~**MLA et vision.**~~ **TOUS DEUX FAITS.** MLA : modèle synthétique + référence
   numpy, écart **5,2e-7**. Vision : chaîne COMPLÈTE et démontrée de bout en bout
   — image → patchs → 32 couches (rotation 2-D **conforme à la source** ggml,
   fenêtre locale d'après clip.cpp) → `v.post_ln` → projecteur (64 groupes ×
   3 584) → injection dans le modèle de texte → **152 064 logits**. Tranches
   validées contre numpy : patchs 5,4e-7, projecteur 1,7e-6, une couche 1,8e-6.
   Réserves NOMMÉES : la permutation colonne-majeur des couches fenêtrées
   (constatée dans la source, pas implémentée), et l'absence de référence locale
   pour la qualité (libmtmd d'ollama bloqué sur `tokenize`, cinq hypothèses
   testées). Tout est dans `docs/plan-mla-vision.md`.

5. **Top-k dans le noyau d'attention.** `--attn-topk 256` AMÉLIORE la perplexité
   (234,88 contre 298,56 à 2 048) mais repasse aujourd'hui par le CPU : le noyau
   GPU ne le gère pas.
6. ~~Experts MXFP4 dans le préremplissage par lots~~ **MESURÉ, À NE PAS FAIRE
   TEL QUEL** : le cache LRU donne +6 % en décodage (5,12 → 5,43 jetons/s,
   53,5 % de succès, 10,64 Go montés) — le chemin CPU des experts est déjà AVX2
   et le coût par expert est faible. Il faudrait supprimer les trois lancements
   et copies par expert, ou grouper les projections.
7. **Mesure de qualité à contexte long** (`reports/rapport-aiguille.md`) :
   étendre la grille à 8 192 et 16 384, plusieurs codes par sonde, et croiser avec
   `--attn-topk`.

### Les variables d'environnement, et leurs pièges

| variable | ce qu'elle fait | le piège |
|---|---|---|
| `DRAVE_GPU=1` | ouvre le pilote CUDA (`gpu::instance`) | **c'est elle qui commande tout** ; sans elle, les autres ne font RIEN et rien ne le dit |
| `DRAVE_GPU_TETE=1` | déporte la tête (Q8_0 ou Q6_K) | inutile sans `DRAVE_GPU` |
| `DRAVE_GPU_KV=1` | tient le cache KV en VRAM et y calcule l'attention | inutile sans `DRAVE_GPU` ; au-dessous de ~4 000 clés le CPU gagne (lancements + recopies) |
| `DRAVE_GPU_TOPK=1` | calcule le top-k de l'attention (`--attn-topk`) en VRAM : scores, seuil radix, collecte des k indices, softmax + Σ w·V | inutile sans `DRAVE_GPU` **et** `DRAVE_GPU_KV` ; exige `nkv × rep = nh` et `k ≤ 1 024` ; tout refus d'un noyau retombe sur le CPU. Perplexité identique à 5e-4 près (9,4162 contre 9,4167 à ctx 2 048), mais **pas encore de gain de temps à 2 048 clés** : six lancements et cinq recopies par couche et par jeton (la fusion des quatre passes est à faire) |
| `DRAVE_GPU_EXPERTS=1` | cache LRU des experts MXFP4 en VRAM | inutile sans `DRAVE_GPU` ; budget par `DRAVE_GPU_EXPERTS_GO` (défaut 8) |
| `DRAVE_KV_BITS=8` ou `4` | quantifie le cache KV (défaut f32) | le 4 bits coûte +364 % de perplexité à 8 192 |
| `DRAVE_KV_K_F32=1` | garde les CLÉS en f32 (valeurs quantifiées) | mesuré : à 8 192, **64 %** de la taille f32 (5,125 octets par élément, échelles comprises) pour +0,023 %, contre +3,04 % pour l'int8 complet (28 % de la taille) — l'écart int8 vient des clés à 99 % (`reports/rapport-attribution-kv.md`) |
| `DRAVE_KV_V_F32=1` | garde les VALEURS en f32 | +3,01 % : ne sert à rien, l'erreur ne passe pas par là |
| `DRAVE_KV_K_F16=1` | clés en **f16** (2 octets/valeur, précision relative) | **le meilleur réglage mesuré** : à 8 192 jetons, clés f16 + valeurs int8 = **+0,018 %** pour **39 % de la taille f32** — contre +0,023 % pour les clés f32 (64 % de la taille) et +3,04 % pour l'int8 complet (28 %) |
| `DRAVE_DUMP_COUCHES=<préfixe>` | écrit en f32 brut l'état résiduel et les intermédiaires (`hc_attn_pre`, `qr`, `qr_norm`, `q_norm`, `kv_norm`, `attn_derope`, `attn_out`, `l_last`), **par couche et par position** — à comparer avec `REF_DUMP` de `tools/ref_logits` via `tools/compare_etats.py` |
| `DRAVE_TRACE_BLOCS=1` | trace DRVF **v3** : valeurs i8, échelle f16 par bloc de 32 | 45 079 930 o contre 66 370 408 en v2 (−32 %), rejeu 19,4029 contre 19,3885 (+0,074 %) |
| `DRAVE_FLUX_VERIF=1` | vérifie l'écart entre l'activation calculée et celle que la trace impose | 1,5e-5 en v2 ; **muet dès que `--lot > 1`** (le rejeu par lots passe par `flux_lot`) |
| `DRAVE_HARMONY_TRACE=1` | trace les fenêtres du découpage « harmony » (gpt-oss) | diagnostic |
| `DRAVE_VISION_TEXTE=<gguf>` | modèle de texte qui reçoit le vecteur d'image | 152 064 logits démontrés de bout en bout |
| `DRAVE_Q8_BLOCS=1` | échelles par bloc de 32 pour `DenseQ8` | **hypothèse réfutée** : 23,696 contre 23,612 — aucun gain |
| `DRAVE_SANS_EMPRUNT=1` | reconstruit les matrices au lieu de les emprunter au GGUF | outil de diagnostic (le lecteur « en place » est le défaut) |
| `DRAVE_YARN_RAMPE=0` | force l'interpolation PURE de YaRN (rampe nulle) | mesure du §6.2 : le RoPE simple gagne partout |
| `DRAVE_BANC_KV_UNIT`, `_KUNIT`, `_K0`, `_V1`, `_GRAD`, `_DEBUG` | variantes du **banc KV** (`--banc-kv`) : valeurs unitaires, clés nulles, dégradé | outil de mesure, pas des réglages de production |
| `DRAVE_DEBUG_FLUX=1` | le nœud moteur imprime ce qu'il reçoit (n, positions, octets) | diagnostic du mode lot |
| `DRAVE_KV_F16=1` | arrondit clés/valeurs en f16 avant quantification | mesuré : aucun effet (hypothèse réfutée) |
| `DRAVE_YARN=1` / `DRAVE_YARN_NON=1` / `DRAVE_YARN_MSCALE=0` | force / interdit / règle la rotation | le défaut ne bascule qu'à **4 ×** la longueur déclarée (16 384 pour gpt-oss, `docs/contexte-long.md` §5.quater) |
| `DRAVE_BANC_KV_GPU_SEUL=1` | saute la référence CPU du banc de KV | à 1 M elle coûte 3 à 16 minutes |

Une porte de non-régression se mesure **sans** `DRAVE_GPU` : la variable déporte à
elle seule les projections Q8_0 de plus de 8 Mo, ce qui change le chiffre de
0,06 % (15,1757 → 15,1667 sur gpt-oss).

## 6bis. Session « Drave » — le calcul réparti tient debout

Tout est mesuré, tout est commité. Détail complet dans `docs/roadmap.md` (phases
0 à 3) et les rapports cités.

**Le découpage en deux nœuds est fidèle** (`reports/rapport-phase3-reparti.md`) :
écart local/réparti **0,00e0** — 144,8289 des deux côtés à 40 jetons, et
**9,5146 des deux côtés à 1 024 jetons** (1 023 flux : le dernier jeton n'a rien
à prédire, il n'est plus envoyé), le banc
réparti prenant le temps du calcul local (19,7 contre 19,4 ms par jeton). Il a
fallu deux corrections dans `Model::forward`, et la première ne suffisait pas :

1. la boucle partait de `0` au lieu de `couche_debut..couche_fin` : le pilote
   calculait les 24 couches, envoyait l'état FINAL, et le pair les recalculait
   toutes par-dessus (`forward_lot` et `forward_mla`, eux, respectaient la plage) ;
2. la norme finale était appliquée DEUX fois (le nœud moteur normait parce que sa
   plage allait jusqu'à la dernière couche, puis le pilote normait). La règle est
   maintenant portée par un drapeau explicite, `flux_brut`.

**Le protocole de flux est en v5** (`docs/format-flux.md`) : en-tête de **79
octets** avec version, mode et le **contrat d'activation complet** (niveaux, seuil,
top-k, renorm, les sept top-k par projection, attn/qk/moe top-k) — deux nœuds
réglés différemment calculaient deux choses différentes en silence (0,69 d'écart
mesuré, et un serveur en `--topk-q 900` contre un client en `--topk-q 4` divergeait
sans un mot). Un pair d'une autre version est refusé en le disant. Les modes sont
dense, listes, blocs et **lot** ; `--flux-serveur` accepte `hôte:port`, et
`colab/` (notebook + `tools/preparer_colab.sh`) porte la recette de la phase 3.4.

**Ce que coûte le transport** (`reports/rapport-transport-liste.md`) :

| | octets par flux | écart local/réparti |
|---|---|---|
| dense f32 | 3 663 | **0,00e0** |
| listes à échelle par bloc, seuil 0,01 | 1 608 | 2,7e-2 |
| échelles par bloc, seuil 0,01 | 2 268 | 2,7e-2 |

`TCP_NODELAY` a divisé l'attente du pair par six (**97,6 → 16,1 ms** par jeton,
soit 1,01× le calcul local) : le banc réparti prend maintenant le temps du calcul
local, à logits identiques. Et avec un relais retardateur
(`tools/proxy_latence.py`), la formule du coût est mesurée :
**attente ≈ calcul distant + 3,2 × latence par message** — 1,01× le calcul local à
0 ms, 1,99× à 5 ms, 4,89× à 20 ms, fidélité intacte (0,00e0) dans les trois cas.
Le seuil de rentabilité (phase 3.3) est donc une affaire de latence, pas de débit :
0,25 Mbit/s suffisent. Un aller-retour Colab de 60 ms donnerait ~8 jetons/s
contre ~60 en local.

**Phase 1.4 attribuée** (`reports/rapport-attribution-kv.md`) : l'écart du cache
KV int8 (+3,0 % à 8 192) vient **entièrement des clés** — clés f32 + valeurs int8
donne +0,023 %, clés int8 + valeurs f32 donne +3,01 %. Réglage utilisable tout de
suite : `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` (75 % de la taille f32 pour +0,02 %).

**Une hypothèse réfutée** : transmettre l'entrée NORMÉE au lieu du résidu brut
passait l'écart de 0,00e0 à **5,61e0** en mode dense — la connexion résiduelle a
besoin du résidu lui-même. Drapeau retiré, réfutation écrite.

### Session « autonomie jusqu'à 15h » — ce qui s'ajoute (12h → 15h)

**Le préremplissage par lots sur le fil est FAIT** (mode 3 du protocole) : N états
d'un coup au lieu d'un flux par jeton. Vérifié : 256 jetons en 4 lots de 64 →
**écart 0,00e0** (18,0851 = 18,0851) ; en UN lot de 917 583 octets → **0,00e0**
aussi. C'était le bloqueur de la phase 3.4 ; `colab/` contient maintenant le
notebook prêt à ouvrir, `tools/preparer_colab.sh` fait le dépôt en un fichier
(`git bundle`, 4,5 Mo — il n'y a pas de dépôt distant) et vérifie l'empreinte du
modèle.

**Le protocole est en version 5** et le contrat d'activation transporte
niveaux, seuil, top-k, renorm, les sept top-k par projection, attn/qk/moe top-k :
un serveur lancé avec `--topk-q 900` et un client avec `--topk-q 4` donnent quand
même 0,00e0 — les réglages du client gagnent. En version 3 ils divergeaient en
silence.

**Le format de trace est en version 2 par défaut et 3 en option** :

| | v1 | v2 (défaut) | v3 (`DRAVE_TRACE_BLOCS=1`) |
|---|---|---|---|
| trace dense 512 jetons | 132 396 736 o | 66 370 408 o | **45 079 930 o** |
| rejeu `--flux-forcer` | 19,3885 | 19,3885 | 19,4029 (+0,074 %) |

La v2 (indices par écarts) est SANS PERTE ; la v3 (valeurs i8, échelle f16 par
bloc de 32) est avec perte. Le rejeu annonce ses comptes — `24 576 listes
servies, 0 manquantes` — et c'est ce qui a démasqué un FAUX POSITIF : mon premier
« rejeu v3 = 19,3885 » lisait en fait la perplexité du calcul normal, la trace
n'étant pas chargée du tout (l'écrivain décalait le fichier de huit octets).

**L'audit des drapeaux** (`reports/rapport-drapeaux-ignores.md`, délégué) : 110
options passées au crible, **46 ignorées dans au moins un mode**. Corrigés :
les top-k (ci-dessus), `--keep` en `--ppl` (prouvé : 1929,3230 identique avant),
`--ffn-gain` en `--infer`, `--threads` en FS/PR/BM, `--hebb-q`/`--hebb-out`,
`--plan` sans `--ctx` (annonçait 512 au lieu de 32 768), la précédence de fenêtre,
le pas de 2 du mode par défaut (`--dense --threads 4` annonçait 30 fils),
`--trace-flux` en inférence (muet), les modes multiples (silencieux). Restent :
`--banc-vision` (ne reçoit aucune `Options`), `--bits` du noyau GPU, et la
recommandation de fond — un `--options-actives` qui imprime les réglages
réellement en vigueur.

### Créneau 15h07 → 18h00 : le mode 4, et la frontière KV confirmée

**Le protocole est en version 5** avec un cinquième mode : le **mode 4 « lot en
listes »**. Chaque état d'un lot est encodé comme le mode 2 et auto-délimité par
ses trois tailles (`a_j · n_blocs_j · longueur_j`). Mesuré, 256 jetons, lots de 16,
seuil 0,01 : **1,5 ko par jeton au lieu de 3,5** (÷2,3) pour un écart de 3,03e-2 —
sous le critère (1,5 × les 2,74e-2 du mode 2 par jeton). Plan :
`docs/plan-mode4-lot-listes.md`.

Trois choses apprises en le faisant : la construction de l'en-tête est maintenant
UNE fonction (`tete_flux`) pour les trois émetteurs (sa duplication avait produit
l'en-tête d'un octet trop long) ; le serveur ne traitait que le mode 3 dans sa
branche lot, donc un flux de listes paniquait ; et le refus d'un mode inconnu est
devenu IMMÉDIAT, avant tout octet de corps. **17 tests**, dont quatre sur le mode 4
(état forgé, deux états, préfixe incohérent, flux à zéro élément).

**La frontière du cache KV tient à 4 096 comme à 8 192** : clés f16 + valeurs int8
= +0,011 % et +0,018 %, int8/int8 = +2,25 % et +3,04 %. Les clés f16 font aussi
bien que les clés f32 pour moitié moins d'octets. ⚠️ Interaction : le miroir VRAM
suppose une disposition homogène, donc les variantes d'attribution le DÉSACTIVENT —
à très long contexte avec `DRAVE_GPU_KV=1`, garder les clés en f32.

**Le noyau GPU de top-k** (phase 1.1) est spécifié et chiffré dans
`docs/plan-gpu-topk.md` : le chemin GPU est conditionné à `attn_topk == 0`
(`model.rs:3150`), donc le mode creux retombe sur le CPU où il coûte 968 ms par
couche à 1 M de clés contre 13,2 ms avec le miroir. Trois noyaux, six étapes, leur
critère d'exactitude — c'est le prochain chantier, et il n'a pas été bâclé faute de
temps : il est écrit.

### Créneau 17h41 → 19h41 (sprint 1) : le top-k GPU, du banc au moteur

**Les trois noyaux du plan sont écrits, mesurés et relus.** Le top-k de l'attention
ne retombait plus sur le CPU par nécessité : `model.rs:3150` interdisait le miroir
VRAM dès que `attn_topk > 0`.

| étape | ce qui est fait | mesure |
|---|---|---|
| 1 · scores | `attn_scores` (déjà là au début du sprint) | écart **1,6–2,3e-7**, **26,7–40×** le CPU (re-mesure sur clés distinctes : l'ancien 1,03e-7 venait d'un banc dégénéré) |
| 2 · sélection | `attn_topk_histo` (4 passes d'octets) + `attn_topk_compte` + `attn_topk_ecrit` | **même ensemble que le CPU** 14/14 lignes, différence symétrique 0 à 4 k / 65 k / 262 k / **1 M** clés ; collecte **0,95 ms** contre 1 653 ms de tri CPU à 1 M (×1 744) |
| 3 · somme | `attn_topk_somme` (softmax sur les k + puits, Σ w·V, indices lus en VRAM) | écart **1,0–4,8e-7** (critère 1e-6) · temps GPU **constant : 0,07 ms** de 4 k à 262 k clés |
| 4 · moteur | branche `DRAVE_GPU_TOPK=1` dans `forward`, repli CPU sur tout refus | PPL **9,4162** contre **9,4167** (CPU) à ctx 2 048 · 13,1355 contre 13,1358 à ctx 8 192 |
| 5 · 1 M | chaîne complète sans relecture des scores | **3,90 ms** pour 14 lignes × 1 M clés, contre 539,9 ms d'attention complète CPU (×138) et 13,2 ms en VRAM — **0,3×** le complet (critère : ≤ 2×) |

⚠️ **Le gain de TEMPS dans le moteur n'est pas encore là**, et c'est mesuré :

| contexte alloué | jetons | clés vues (moy.) | attention CPU | attention GPU top-k | balayage |
|---|---|---|---|---|---|
| 2 048 | 511 | 255 | **4,21 ms/jeton** | 7,68 | 18,1 / 20,4 s |
| 8 192 | 511 | 255 | **6,35 ms/jeton** | 7,36 | 19,2 / 19,7 s |
| **16 384** | 4 095 | **2 047** | 19,58 ms/jeton | **7,59 ms/jeton** | **203,7 / 155,5 s (−24 %)** |

⚠️ Le nombre de clés notées dépend du nombre de JETONS (`n = pos + 1`), pas du
contexte alloué : les deux premières lignes valent pour ~255 clés, la troisième
pour ~2 047. Ce qui est établi : à 255 clés le CPU gagne, à 2 047 le déport gagne
(attention −61 %, balayage −24 %, perplexité identique à 2e-5) — **le croisement
en clés est donc entre 255 et 2 047**, plus haut que celui de l'attention complète
(~4 000), à cause du coût fixe : **8 lancements et 17 transferts par couche et par
jeton** (dont 8 copies DtoH bloquantes). Une grille propre demande de faire varier
le nombre de jetons à contexte fixé (17 434 disponibles ; ~20 min par passe à
16 384 jetons). Le prochain sprint doit donc **fusionner** — descente radix,
collecte et somme dans un seul noyau, tampons hôtes réutilisés — pas ajouter un
noyau.

**Quatre défauts attrapés, chacun par un moyen différent** — c'est la leçon du
créneau :
1. le **banc était dégénéré** (même clé à toutes les positions : tous les scores
   d'une ligne égaux, donc la descente radix ne choisissait jamais entre deux
   seaux) — trouvé en RELISANT le banc, pas en le faisant échouer ;
2. le **puits était ajouté par chaque fil** dans le noyau 3 alors que chaque fil
   ne tient qu'une somme partielle : dénominateur ×45,7, sortie 55× trop petite à
   k = 1 — trouvé par le BANC en une ligne ;
3. une **relecture adversariale** (sous-agent) a trouvé 7 défauts de plus, dont un
   bloquant : le garde de réallocation de la collecte était piloté par les
   dimensions au lieu des capacités, donc un échec d'allocation au milieu du `||`
   laissait un pointeur 0 pour l'appel suivant. Corrigés, avec en plus une fuite
   VRAM (`kv_assurer`), trois capacités périmées, quatre copies DtoD non
   vérifiées, une boucle infinie latente et un `rep` tronqué ;
4. une SECONDE relecture adversariale, sur le branchement dans le moteur, a
   trouvé **un faux résultat silencieux dans un noyau plus ancien** :
   `attn_kv_recombine` lisait `sinks[warp]` (tête DANS le groupe KV) alors que la
   sortie est écrite par tête GLOBALE — sur gpt-oss, `DRAVE_GPU_KV=1` donnait donc
   à la tête `kvh×rep + w` le puits de la tête `w`, jusqu'à 4,65 logit d'écart
   (facteur 105 sur le drainage). **Mesuré avant/après** : perplexité gpt-oss ctx
   256 `DRAVE_GPU=1 DRAVE_GPU_KV=1` = **17,6531 AVANT** contre **15,1786 APRÈS**
   (référence CPU 15,1757 ; Qwen n'a pas de puits, donc la porte de 19,3885 ne
   pouvait pas le voir). Deux lignes de correction. La relecture a aussi listé 12
   autres points, dont cinq corrigés dans la foulée : garde du noyau 3 testé
   APRÈS sept lancements, couverture de la collecte non vérifiée alors que la
   copie qui le permet est déjà payée, unités de capacité mélangées
   (`sinks_cap`/`out_cap` en éléments d'un côté, en octets de l'autre), compteur
   d'événements incohérent entre les deux chemins, `DRAVE_GPU_TOPK=0` qui
   ACTIVE.

**Un audit de documentation** (second sous-agent) a corrigé quatre chiffres périmés
ou mal sourcés, dont la ligne « 65 536 » du rapport des scores (7,4 ms / 8,9×,
mesurée AVANT le découpage en tranches → 2,36 ms / 26,7×) et le compteur de lignes
Rust (12 171 → **13 480** en fin de sprint, un seul chiffre dans tout le dépôt).

Portes du sprint, mesurées sur le binaire final : **Qwen2.5-0.5B Q8_0 ctx 256 =
19,3885** · **gpt-oss-120b MXFP4 ctx 256 = 15,1757** · `cargo test --release` =
**17/17** · `--banc-topk` toujours vert de n = 1 à n = 1 000 000.

### Sprint 2 (19h49 → 21h49) : la chaîne du top-k fusionnée en UN noyau

**Le croisement avec le CPU tombe de ~255-2 047 clés à ~300 clés**, et le déport
devient franchement gagnant : c'est le sprint qui rend l'attention creuse déportée
utilisable.

| # | livrable | mesure |
|---|---|---|
| 1 | `attn_topk_tout` : descente radix + collecte + somme en UN noyau par ligne (256 compteurs, k indices et k poids en partagé, aucun indice ne quitte la VRAM) | **2 lancements au lieu de 8** · plus de tampon `nh × n × 4` |
| 2 | seuil de bascule avec la chaîne, **mesuré** | noyau 4 plus rapide jusqu'à 131 072 clés (0,13 contre 0,22 ms à 4 k), la chaîne au-delà (1,35 contre 1,58 à 262 k) |
| 3 | grille PROPRE (une seule variable : le nombre de jetons) | CPU 4,26 → 38,84 ms/jeton de 255 à 4 095 clés · **GPU plat 4,53 → 4,97** · croisement ~300 clés · **7,8× à 4 095 clés** |
| 4 | perplexité | identique à 2e-5 à chaque point (13,1355/13,1358 · 9,4162/9,4167 · 12,2265/12,2267) |
| 5 | gpt-oss (seul modèle à puits), ctx 1024 | pruning +2,66 % (CPU) et +2,90 % (GPU) — **même effet des deux côtés** |
| 6 | filets | NaN si la collecte ne remplit pas les k places (AVANT la somme), bornes sur les écritures partagées, `k > n` / `n ≥ 2^24` / k > 1024 / 4 bits refusés |

**Trois défauts trouvés par la revue adverse autonome** : une COURSE bloquante
(aucune barrière entre la lecture du préfixe et la remise à zéro de la passe
suivante — prouvée dans le PTX, écriture partagée hors bornes en aval) ; le CPU et
le GPU ne départageaient PAS les ex æquo de la même façon (`select_nth_unstable_by`
n'est pas stable) alors que la documentation l'affirmait ; `shCle` mort (4 ko de
partagé par bloc), `k > n` accepté, comptages en `float` non bornés.

**Et un filet de sécurité qui ne retenait rien** : le NaN-poisen était écrit puis
écrasé par la somme, et les indices non remplis servaient à LIRE la VRAM avant lui
(mesuré en sabotant la collecte : CUDA_ERROR_ILLEGAL_ADDRESS). Corrigé — le filet
sort avant la somme, et le sabotage redevient un refus propre. **Un garde-fou non
testé est une décoration.**

✅ **Doute instruit** (`reports/rapport-logits-gpu-vs-cpu.md`) : le déport des
projections donne des logits **IDENTIQUES au CPU sur un modèle dense**
(Qwen2.5-0.5B : écart moyen |ΔNLL| = 0,0000, perplexité 17,4315 des deux côtés) et
les décale de **0,038 nat** sur gpt-oss (MxFP4, 128 experts top-8), avec le même
jeton sur **497 des 511 positions** (les 14 divergences portent les plus grands
écarts, jusqu'à 1,37 nat). Les noyaux GPU sont donc exacts ; ce qui diffère,
c'est le **routage des experts** — un top-8 est une opération discrète, qu'un écart
de 1e-7 sur un logit de routeur peut faire basculer. Hypothèse fortement étayée par
le contraste dense/MoE, à démontrer en comparant les routages eux-mêmes. Le miroir
KV, lui, ne pèse que 0,25 %.

### Sprint 7 (05h39 → 07h39) : clôture de la nuit — le livelock du contexte

**Un défaut bloquant trouvé par accident, et corrigé.** Une sonde d'aiguille a duré
23 minutes au lieu de 75 s : son invite faisait 4 731 jetons pour un `--ctx 4608`.
Le moteur ne refusait pas la demande — **il bouclait sans fin** (`KvCache::assurer`,
`model.rs:1117` : `while cap < besoin { cap = (cap * 2).min(self.ctx) }`, où `cap`
plafonne à `ctx`). Le même défaut avait été corrigé côté GPU au **sprint 1**
(`kv_assurer`, commit `47ce9b7`) ; le chemin CPU était resté.

Correctif : la capacité est plafonnée au contexte déclaré, `Model::generate`
**tronque l'invite en réservant la place de la génération** et la boucle de décodage
**s'arrête** quand le contexte est plein — en le disant à chaque fois.

⚠️ **Le premier correctif était faux, et la relecture de clôture l'a prouvé** :
tronquer à `ctx` exactement laissait le décodage appeler `forward(pos = ctx)`, dont
l'assertion tombait — un **SIGABRT** (exit 134) là où je croyais « rendu la main en
312 s » (mon script de vérification ne lisait pas le code de sortie). Corrigé, et
re-vérifié **en lisant le code de sortie** : ctx 256 avec une invite de 306 jetons →
troncature annoncée, **exit 0** ; contexte plein → « génération arrêtée à 255
jetons », **exit 0**. L'invariant `pos < ctx` est désormais gardé dans
`KvCache::ecrire` (au-delà, l'écriture partait dans le bloc de la tête KV suivante),
et `--infer --topk`, `--ppl-reparti --ids` sont bornés. **18 tests.**

### Ce que la nuit a établi (sprints 2 à 6)

| # | résultat | mesure |
|---|---|---|
| 1 | **Noyau fusionné du top-k** : descente radix + collecte + somme en UN noyau par ligne | 8 lancements → 2 · tampon `nh × n × 4` supprimé · écart 7,2e-7 (avec puits) et 8,4e-7 (sans) |
| 2 | **Le déport du top-k gagne** | attention plate 4,5–5,0 ms/jeton de 255 à 4 095 clés · croisement ~300 clés · ×7,8 à 4 095 clés |
| 3 | **Le préremplissage déporté** | prompt de 3 961 jetons : **286,6 → 63,8 s** (×4,5) · perplexité 9,4335 / 9,4337 (écart relatif 2,1e-5) |
| 4 | **Le déport des projections est EXACT sur un modèle dense** | logits bit à bit identiques (|ΔNLL| moyen 0,0000) ; sur un MoE, 0,038 nat de décalage et 497/511 top-1 identiques → routage des experts (hypothèse) |
| 5 | **Le noyau fusionné gagne au décodage, jusqu'à 16 k clés** | GPU plat, CPU 4,26 → 38,84 ms/jeton · k = 1 024 suffit à 8 192 clés (12,5 %) |
| 6 | **L'attention creuse à 6 % n'est PAS moins fiable que l'attention complète** | neuf fenêtres contiguës, mêmes invites : **dense 8/9, k = 256 8/9**, et les échecs ne sont pas les mêmes fenêtres (dense rate la 3e, k = 256 rate la 1re) — le succès dépend de la divergence chaotique du décodage, pas du budget d'attention |
| 7 | **Six artefacts qui promettaient ce qu'ils ne faisaient pas** | garde-fou jamais déclenché · échantillon lu comme un accord global · grep qui ne suit pas la chaîne d'appels · décalage de fenêtre remis à zéro · section annoncée dans un commit mais absente · **script de vérification qui ne lisait pas le code de sortie** (le correctif du livelock a été cru bon alors qu'il finissait en SIGABRT) |

### La frontière du cache KV, mesurée en entier

| réglage | octets/élément | % du f32 | écart |
|---|---|---|---|
| clés f16 · valeurs int8 | 3,125 | **39 %** | **+0,018 %** ← le meilleur point |
| clés f32 · valeurs int8 | 5,125 | 64 % | +0,023 % |
| clés f32 · valeurs int4 | 4,625 | 58 % | +0,46 % |
| clés f16 · valeurs int4 | 2,625 | 33 % | +0,61 % |
| int8 · int8 | 2,25 | 28 % | +3,04 % |
| int4 · int4 | 1,25 | 16 % | +364 % |

Réglage recommandé : **`DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1`** — 2,5× plus petit que le
f32 pour deux centièmes de pour cent. Détail et reproduction :
`reports/rapport-placement-bits-kv.md`.

⚠️ **Mais le temps change le conseil** (mesuré au banc à 262 144 clés) : les clés
f16 coûtent **2,3× le temps CPU** des clés f32 (162 contre 70 ms par passe), et le
miroir VRAM — qui ramène l'attention à 1,7 ms par passe — **exige une disposition
homogène**, donc toute variante d'attribution le désactive. Par régime : clés f16
à contexte court ou moyen sur CPU ; **int8/int8 homogène** dès qu'on veut le miroir
ou qu'on est à très long contexte. Et l'aiguille v2 retrouve **9/9** sondes dans
les trois variantes, int8/int8 compris : la tâche est plus robuste que la
perplexité ne le suggère.

### Le mode lot gagne sur les deux tableaux

Chronométré sur 256 jetons, machine au repos : **116,7 ms par jeton** en flux simple
contre **16,6 ms en un seul lot** (7×, par le produit matrice-matrice), et **18×**
sur un lien à 20 ms par message (2,6 s contre 47,6 s). `reports/rapport-prefill-reparti.md`.

### Hygiène et garde-fous ajoutés depuis (13h)

- **`--options-actives`** : un tableau de bord qui imprime, APRÈS toutes les
  affectations, les réglages que le moteur utilise vraiment (niveaux, seuil,
  top-k, fenêtre, lot, cache KV avec sa variante…). C'est la réponse au défaut le
  plus coûteux du dépôt — un drapeau qui ne fait rien. Branché dans les quatre
  modes principaux.
- **Un drapeau inconnu est signalé** : `--keeep 0.05` était avalé en silence.
- **Règle R4 dans le code** : les trois modes qui allouent sur une taille lue dans
  l'en-tête refusent au-delà de 256 Mo — un pair pouvait demander ~15 To.
- **Les tests du protocole** : taille d'en-tête et version verrouillées,
  aller-retour des paires à échappement (écart de 255 compris), refus des corps
  tronqués, aller-retour dense par la vraie mise en trame, refus d'un lot géant.
  Le test de troncature a immédiatement trouvé une garde manquante dans le
  décodeur.
- **Six défauts de la première relecture adversariale corrigés** : compteur de
  listes manquantes aveugle en rejeu par lots, clés de trace incohérentes selon
  `--lot`, pair factice qui ne lisait pas le mode lot, modes sparse ignorés en
  silence avec `--lot > 1`, panique du client sur un refus du pair, `--limit 1` qui
  affichait NaN.
- **Huit de la seconde**, qui attaquait les correctifs eux-mêmes : le tableau de
  bord `--options-actives` s'exécutait AVANT les affectations en perplexité (il
  montrait donc l'état d'avant — pire que rien), la règle R4 ne couvrait pas
  `n_blocs` (16 Gio alloués sur une trame de 83 octets), le décodeur de paires
  allouait sur le `n` du fil (12 Gio avant de dire « tronqué »), une trame forgée
  hors dimension TUAIT le nœud (SIGABRT), l'envoi paniquait encore sur un pair
  fermé, `-keep` (un seul tiret) était avalé, `--flux-forcer` ignoré en inférence,
  `--banc-mla` muet sur la trace.
- **Dix-sept tests** : onze sur le protocole et le plafond — taille d'en-tête et
  version verrouillées, aller-retour des paires à échappement, refus des corps
  tronqués, deux trames FORGÉES envoyées dans une vraie socket (indice hors
  dimension, 100 millions de blocs, cumul au-delà des 256 Mo), quatre sur le mode 4
  (état forgé, deux états, préfixe incohérent, liste vide acceptée en modes 1/2).

### Les prochains chantiers, dans l'ordre

0. **Noyau GPU de top-k** (phase 1.1) : le seul poste de la feuille de route qui
   demande du travail GPU *neuf* ; les deux Quadro sont libres et le cadre existe
   (`gpu/compiler.sh`, `drave_gpu.cu`, sm_75). Vient ensuite le **second GPU**
   (16 Go dormants : cache d'experts MXFP4 et KV à 1 M paginé).
1. ~~Préremplissage par LOTS sur le fil~~ **FAIT** (mode 3), et ~~lot en listes~~
   **FAIT AUSSI** (mode 4 : 1,5 ko par jeton au lieu de 3,5).
2. **Clés du cache KV** : `DRAVE_KV_K_F16=1` (clés en f16, 3,125 octets par
   élément contre 2,25 en int8/int8 et 8 en f32) donne **+0,057 %** à contexte 256
   là où l'int8/int8 coûte +2,15 % — la campagne à 8 192 jetons est en cours ;
   reste à confirmer, puis à choisir la politique par défaut.
3. **Transport** : le mode « blocs » perd encore un peu de fidélité ; l'écart
   **décroît** avec la longueur (13,7 % à 64 jetons, 1,3 % à 1 024) — chercher
   pourquoi il ne descend pas plus vite.
4. Le reste des phases 1 et 2 de `docs/roadmap.md` (noyau GPU de top-k,
   ordonnanceur de placement, flux de poids depuis le NVMe).

---

## 7. Carte du dépôt

```
drave-core/src/
  engine.rs     pool de fils, barrière, accumulateurs, noyau dense int8
  model.rs      chargement, forward, attention, MoE, génération, YaRN, sinks
  list.rs       encodages (PushMat, DenseQ4/6/8), noyaux AVX2, sources empruntées
  gguf.rs       lecteur GGUF, dequantification, vues en place
  tokenizer.rs  BPE byte-level, motifs qwen2 et gpt-4o
  gpu.rs        API pilote CUDA (sans crate), noyaux PTX
  main.rs       modes : inférence, perplexité, plan, tokenize
gpu/drave_gpu.cu + .ptx    noyaux, compilés par clang
tools/ref_logits.cpp         référence llama.cpp : mêmes identifiants, sans BOS
tools/compare_logits.py      comparaison position par position (NLL, top-1, corrélation)
tools/harmony_canonique.py   montage harmony canonique (analysis puis final)
reports/rapport-travail-reel.md      ce que le moteur sait faire, tests réels
reports/rapport-gpt-oss-perplexite.md  les deux bugs de gpt-oss et la référence externe
docs/contexte-long.md                budget 1 M : KV, préremplissage, rotation
docs/convertisseur.md                plan de chargement, résultats négatifs
reports/rapport-passage-a-l-echelle.md   modèle de coût, faisabilité par modèle
journal/                             sessions archivées automatiquement
```

Le journal s'archive à chaque commit (`tools/archive_sessions.py` +
`tools/session_report.py`, crochet git et crontab horaire).

---

## 8. Premier pas suggéré pour la nouvelle session

```bash
# 1. l'état est-il vert ? (Qwen ne doit pas bouger : les corrections de cette
#    session ne touchent que les modèles à biais de sortie et à fenêtre par couche)
cd drave-core && cargo build --release && cargo test --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt \
    --ctx 256 --abits 16 --threads 16 --limit 512 --dense   # attendu 19,3885

# 2. si /tmp a été vidé, régénérer le corpus et les identifiants (§2)

# 3. gpt-oss : le chiffre de contrôle de cette session (≈ 45 s de chargement,
#    ~100 s pour 510 jetons). SANS `DRAVE_GPU` : la variable ouvre le pilote, et le
#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le
#    chiffre devient 15,1667 (même calcul, ordre de sommation du noyau GPU).
./target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf \
    --ppl /tmp/ids_oss_512.txt --ctx 256 --dense --threads 16 --limit 512  # attendu 15,6017
#    (15,1757 avant le correctif de routage du 02/10 ; DRAVE_GPU=1 donne un écart
#    du même ordre que les 0,06 % mesurés alors — non re-mesuré depuis.)

# 4. puis §6.b : la rotation ne bascule plus qu'au-delà de 4 × la longueur
#    d'origine déclarée (16 384 pour gpt-oss) — mesuré, voir docs/contexte-long.md §5.quater

# 5. le calcul réparti (§6bis) : deux nœuds, 12 couches chacun, et le même chiffre
#    des deux côtés. Le nœud moteur doit être lancé AVANT le pilote.
cd ..   # racine du dépôt
(./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
     --flux-serveur 45999 --ctx 256 > /tmp/serveur.log 2>&1 &)
sleep 3
./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
    --ppl-reparti 127.0.0.1:45999 --couches-locales 12 --limit 40 --ctx 256
# attendu : « écart : 0.00e0 » en mode dense (le transport f32 est exact)

# 6. le contrôle qui attrape les fautes de banc : `tools/pair_factice.py` parle le
#    protocole sans charger de modèle et DIT ce qu'il reçoit (tailles, modes,
#    réglages). C'est lui qui a montré un flux de 919 canaux là où le modèle en a
#    896 — mon compteur divisait par le nombre de jetons notés, pas de flux envoyés.
python3 tools/pair_factice.py 45760 896 &
./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
    --ppl-reparti 127.0.0.1:45760 --couches-locales 12 --limit 4 --ctx 256
```

## Sprint 08 — un modèle éclaté se lit comme un seul (11:13 → 13:13)

```bash
# Un dossier qui contient commun.gguf + cluster-XX.gguf + mapping.tsv EST un
# modèle : aucune option nouvelle. Inventaire par les seuls en-têtes :
./drave-core/target/release/drave /home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters --tensors
# attendu : 9 fichiers · 1587 tenseurs · 18,55 Go · en-têtes lus en ~0,4 s

# Un GGUF découpé en shards s'ouvre par n'importe lequel de ses morceaux :
./drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf --tensors
# attendu : 3 fichiers · 1328 tenseurs · 86,90 Go (= la somme des fichiers)

# Portes : Qwen 19,3885 · cargo test 24 verts.
./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt \
    --ctx 256 --abits 16 --threads 16 --limit 512 --dense
```

# L'ÉPREUVE décisive : le modèle éclaté rend le MÊME chiffre que l'original.
# (mêmes jetons, même contexte, chemin par jeton)
./drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf \
    --ppl /tmp/ids_qwen.txt --ctx 64 --limit 64 --dense --threads 12 --lot 1   # 15,2789
./drave-core/target/release/drave /home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters \
    --ppl /tmp/ids_qwen.txt --ctx 64 --limit 64 --dense --threads 12 --lot 1   # 15,2789
# et par lots (--lot 64) : 15,2736 — l'écart connu entre les deux ordres de sommation
```

# Les fichiers sont MAPPÉS : 3,3x plus rapide et 3x moins de mémoire qu'une
# lecture complète (9,32 s / 6,35 Go contre 30,68 s / 19,20 Go sur Qwen3-30B,
# perplexité identique). `DRAVE_MMAP=0` revient à la lecture complète.

# Un NŒUD PARTIEL ne charge que ses clusters : 2,36 Go pour un huitième des
# experts, contre 6,33 Go pour le modèle entier.
DRAVE_CLUSTERS=0 ./drave-core/target/release/drave \
    /home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters \
    --ppl /tmp/ids_qwen.txt --ctx 64 --limit 8 --dense --threads 8 --lot 1
```

**Ouvert** : la SOMME des contributions entre nœuds (le nœud partiel saute les
experts absents, mais rien n'additionne encore ce que deux nœuds calculent) ; les
biais d'experts en clusters (gpt-oss en a, refusés explicitement) ; le
rééquilibrage des clusters par charge et non par nombre d'experts.

## Inventaire des modèles lourds (01/10 midi)

```bash
# Lit les EN-TÊTES seuls (le plus gros fichier fait 366 Go) et confronte les
# poids annoncés par les descripteurs GGUF aux tailles annoncées par HuggingFace.
tools/inventaire_modeles_lourds.sh
```

| modèle | architecture | fichiers | tenseurs | poids lus | annoncé HF |
|---|---|---|---|---|---|
| DeepSeek-V4.1-Flash-Q2 | `deepseek41` | 1 | 1 046 | 365,70 Go | 365,7 Go |
| GLM-5.3-UD-IQ1_S | `glm-dsa` | 6 | 1 809 | 216,71 Go | 216,7 Go |
| Kimi-K2.7-Code-UD-IQ1_M | `deepseek2` | 8 | 1 096 | 303,90 Go | 303,9 Go |
| DeepSeek-V4-Flash-UD-IQ1_M | `deepseek4` | 3 | 1 328 | 86,90 Go | 86,9 Go |
| MiniMax-H3 | `?` | 1 | 532 | 11,42 Go | 11,4 Go |

**984 Go de concordance** : c'est la vérification la plus large de la table des
types ggml. Aucune de ces architectures n'a de `forward` dans le moteur — c'est
le chantier d'après.

```bash
# La table des types ggml, confrontée à libggml elle-même (41 types, 0 divergence)
tools/verifier_table_types.sh
```

## Session d'analyse — l'empreinte mémoire de DeepSeek-V4.1 (01/10, 10 h 47 → 18 h)

Rapport complet : [`reports/rapport-empreinte-memoire.md`](reports/rapport-empreinte-memoire.md).
Traces conservées : `/home/stephane/FastNVMe/artefacts/traces/session-01-10/`.

### Le résultat qui change tout

Décomposition des 365,7 Go de V4.1 : **engram 203,4 Go (55,6 %)** · experts
152,9 Go (41,8 %) · attention 5,4 Go · embeddings et tête 2,0 Go.

`blk.N.engram_embd.weight` fait **101,4 Go par couche** (2 couches), de forme
`[384 006 168, 264]` en I8 — mais **ce n'est pas un tenseur de poids, c'est une
table de hachage de n-grammes**. Une session de 10 000 jetons n'en touche que
**17 276 entrées, soit 4,6 Mo**. Ratio : 1 pour 22 000.

**Empreinte réelle : 50 à 80 Go au lieu de 365,7 Go**, dont 0,4 Go d'engram.

```bash
# L'empreinte se chiffre sur une trace de routage réelle :
DRAVE_TRACE_EXPERTS=/tmp/routage.txt ./drave-core/target/release/drave \
    /home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2 \
    --ppl /tmp/ids_30b_wiki.txt --ctx 2048 --limit 2048 --dense --threads 10 --lot 1
python3 tools/analyse_empreinte.py /tmp/routage.txt      # courbes par couche
```

### Les pistes mesurées, et leur verdict

| piste | verdict | chiffre |
|---|---|---|
| **engram mmappé** | **à faire** | 203 Go → 0,4 Go chargés |
| **tête restreinte à la langue** | **à faire** | −30 % de trafic ; top-1 français dans 99,2 % des cas |
| **cache d'experts 25 %** | à faire | 80 % des appels servis en mémoire |
| découpage plus fin que l'expert | impossible | seuil à 5 % : perplexité ×287 |
| grappes par langue | non | Jaccard entre langues 0,75–0,90, référence interne 0,805 |
| dictionnaire token → experts | non | Jaccard du même token : 0,06 aux couches médianes |
| pré-remplissage du cache par langue | non | le cache atteint son régime en 32 jetons |
| allocation du cache par couche | non | gain maximal +1,2 % |

### Deux découvertes de structure

- **Le miroir** : les couches extrêmes sont 4,6× plus liées au token que les
  médianes (Jaccard 0,259 contre 0,056). Mais les couches symétriques (0/47) ne
  partagent rien (0,030).
- **Une périodicité de 12 couches** : Jaccard 0,323 à écart 12, 0,210 à écart 24,
  **0,035 pour tout autre écart**. Le modèle a 4 blocs de 12 couches qui
  réutilisent les mêmes experts — mais ce sont des tenseurs différents, donc
  aucune économie de stockage directe.

### Rejouer notre propre journal

Les 28 sessions du `journal/` (59 Mo, 2,5 M jetons) ont été tokenisées et routées
pour voir si **notre** usage change l'empreinte. Réponse : non, il se comporte
comme le français générique (58,1 experts pour 90 % contre 59,3). Mais la
**langue** la change :

| langue du contenu | 90 % des appels sur | Go d'experts (V4.1) |
|---|---|---|
| français | 46,3 % | 71 |
| **anglais** | **34,8 %** | **53** |

**18 Go d'écart** — et le code et la technique sont massivement anglais.

Cache d'engram pour notre usage : **388 Mo couvrent l'intégralité du journal**
(1 470 860 entrées sur 384 M, soit 0,38 % de la table de 101 Go). Le vocabulaire
du journal fait 19 228 tokens (12,66 %), confirmant le plafond mesuré.

```bash
# Rejouer le journal à travers le modèle
cat $(ls -tr journal/sessions/*/digest.md) > /tmp/corpus/journal.txt
./drave-core/target/release/drave <clusters> --tokenize --fichier /tmp/corpus/journal.txt \
    --sortie /tmp/corpus/journal.ids
DRAVE_TRACE_EXPERTS=/tmp/routage_journal.txt ./drave-core/target/release/drave <clusters> \
    --ppl <ids> --ctx 4096 --limit 4096 --dense --threads 10 --lot 1
```

### Analyse STATIQUE des poids (pas des traces)

`tools/analyse_experts_statique.py` déquantifie les experts (Q4_K, Q6_K, Q8_0,
F32, F16) et compare **ce qu'ils sont**, pas ce qu'ils font.

| question | réponse mesurée |
|---|---|
| des experts jumeaux à fusionner ? | **non** — similarité intra-couche max 0,04–0,19, médiane ~0,00 |
| des sources creuses ? | **non** — 78 % des colonnes portent 80 % du poids |
| la périodicité de 12 est-elle dans les poids ? | **oui** — corrélation 0,27–0,39 à écart 12, ~0,00 ailleurs |
| peut-on fusionner deux couches du cycle ? | **non** — aucun expert ne dépasse 0,5 (max 0,49) |

**La périodicité est structurelle, pas seulement fonctionnelle** — et elle est
**bornée aux couches 6–39** (trois cycles de 12) : 0/12 = 0,001, 30/42 = 0,003.

```bash
python3 tools/analyse_experts_statique.py \
    /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf \
    --couches 0,6,12,24,36,47 --lignes 8
```

**Seule piste ouverte** : une décomposition conjointe des quatre couches d'un
cycle. 35 % de variance partagée à extraire, **rang inconnu** — donc pas compté
comme un résultat.

### Architecture mémoire : VRAM, RAM, disque

Rapport : [`reports/rapport-architecture-memoire.md`](reports/rapport-architecture-memoire.md).

Débits **mesurés** : VRAM **84,9 Go/s** (noyau `warp par ligne`) · RAM **20,9 Go/s**
(CPU 30 fils) · NVMe aléatoire 5,5 Go/s · PCIe 3.0 ×16 ~12 Go/s. **Le noyau GPU
est 4× plus rapide que le CPU** — le déport n'est pas marginal.

| niveau | capacité | contenu |
|---|---|---|
| VRAM | 30,2 Go | commun 8,0 + **22,2 Go d'experts chauds** (2 227) |
| RAM | 102 Go | jusqu'à 10 247 experts — 90 % des appels dans **71 Go** |
| NVMe | 828 Go | le reste + **engram mmappé** |

**Noyaux manquants, par ordre de gain** : attention MLA (−194 ms/jeton : 5,40 Go
par jeton, premier poste, **pas déportable aujourd'hui**) · IQ2_XXS/Q2_K
(−86 ms). Cumul 499 → ~210 ms par jeton.

**Le KV qu'on oublie** : à 1 M de contexte, **96,6 Go en F16** — plus que les
71 Go d'experts. En int8 : 48,3 Go. **Sa quantification est une condition, pas une
optimisation** : au-delà de 0,77 M de jetons en F16, il n'y a plus de place pour
les experts. Le seuil de bascule VRAM (KV contre experts) est ~100 K jetons.

```bash
# Le banc qui donne les débits (sans DRAVE_GPU, il rend « GPU absent »)
DRAVE_GPU=1 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --gpu-banc
# attendu : CPU 20,9 Go/s · GPU ligne par fil 41,9 · GPU warp par ligne 84,9
```

### Topologie matérielle et affinités

Relevé : NVMe (02:00.0), **les deux GPU** (03:00.0, 04:00.0) et les CPU 0-9 sont
sur le **NUMA node 0**. **NVLink présent entre les GPU : 25,78 Go/s** (2× le
PCIe). **Pas de FPGA.**

| mesure | résultat |
|---|---|
| NUMA, calcul pur | 13,8 (node 0) vs 14,2 (node 1) Go/s — **bruit** |
| NUMA, lecture NVMe | 22,41 vs 21,45 Go/s — **4 %** |
| **10 cœurs, 10 fils** | 14,7 Go/s |
| **10 cœurs, 20 fils (paires HT)** | **18,7 Go/s — +27 %** |
| 10 cœurs, 30 fils | 15,0 Go/s — régression |
| 20 cœurs, 20 fils | **22,5 Go/s** |
| 20 cœurs, 40 fils (HT) | 18,9 Go/s — rien, et très bruité |

**La règle** : l'hyperthreading n'apporte rien quand on a tous les cœurs (la
bande passante sature), mais **+27 % quand on n'en a que dix**. Un nœud restreint
doit donc prendre ses **paires HT** (`0-9,20-29`), pas dix cœurs secs. Trois fils
par cœur est une régression.

**Corrigé dans le moteur** : `engine::coeurs_physiques()` lit
`/sys/devices/system/cpu/cpu*/topology/` au lieu des threads logiques — le défaut
passe de **30 à 20 fils**. Porte Qwen inchangée (19,3885), 32 tests verts.

**FPGA Stratix V** : branché en USB seulement (625 Mo/s), et **aucun cas d'usage**
— le mur n'est pas le calcul (0,6 ms par couche contre 10,9 ms de lecture, un
rapport de 18×). À réévaluer si une charge de calcul dense apparaît, et en PCIe.

```bash
# Les mesures d'affinité
taskset -c 0-19 env DRAVE_GPU=1 ./drave-core/target/release/drave \
    models/Qwen2.5-0.5B-Q8_0.gguf --gpu-banc --threads 20   # 22,5 Go/s
taskset -c 0-9,20-29 env DRAVE_GPU=1 ./drave-core/target/release/drave \
    models/Qwen2.5-0.5B-Q8_0.gguf --gpu-banc --threads 20   # 18,7 Go/s (10 cœurs + HT)
```

## Session d'implémentation — détection matérielle et configuration automatique

Nuit du 01/10 au 02/10. Rapports :
[`reports/rapport-optimisations-auto.md`](reports/rapport-optimisations-auto.md) et
[`reports/rapport-tete-restreinte.md`](reports/rapport-tete-restreinte.md).

### Ce qui est implémenté

| brique | ce qu'elle décide | mesure qui la justifie |
|---|---|---|
| `materiel.rs` | cœurs physiques, paires HT, NUMA, caches, GPU, NVLink, disques | `available_parallelism` rend 40 threads pour 20 cœurs |
| `--materiel` | le plan complet, **avec la raison de chaque ligne** | chaque règle porte son chiffre |
| threads par défaut | **20** (cœurs physiques) | 20 cœurs = 22,5 Go/s · 10 = 14,3 · 40 = 18,9 |
| cache KV | f32 tant qu'il tient dans **un tiers** de la RAM, int8 au-delà | 90 Ko/jeton en F16 sur V4.1 ⇒ 96,6 Go à 1 M |
| cache d'experts VRAM | VRAM libre − 2 Go − le commun | VRAM 84,9 Go/s contre RAM 22,5 |
| épinglage HT | si la machine a moins de 8 cœurs | 10 cœurs + HT = 18,7 contre 14,7 secs |
| prélecture | `madvise(WILLNEED)` après le routage | **sans effet mesuré** (0,3 %) — conservée, pas comptée |

Vérifié en vrai : `--materiel` sur V4.1 donne **384 experts de 9,95 Mo**, et à 1 M
de jetons il bascule le KV en 8 bits avec sa raison (« 94,4 Go en F16, soit 81 %
de la RAM libre »).

### Ce qui a été mesuré puis RETIRÉ

**La tête à restriction garantie** : trois voies, aucune ne tient.

| voie | résultat |
|---|---|
| restriction simple | +10,5 à +15 %, mais **la sortie change** |
| borne de Cauchy-Schwarz | exacte, **ne conclut jamais** (5 à 20× trop haute) |
| sparsité de l'entrée | densité 5,1 % ⇒ perplexité **×107** |

**On ne peut pas garantir l'argmax en lisant moins que tout.** `--tete-restreinte`
reste, comme **génération contrainte** assumée, refusée en perplexité.

### Le mmap, toutes tailles

| modèle | taille | temps | RSS |
|---|---|---|---|
| Qwen3-30B en clusters | 18,55 Go | 0,46 s | 72 Mo |
| DeepSeek-V4-Flash (3 shards) | 86,90 Go | 0,07 s | 35 Mo |
| **DeepSeek-V4.1-Flash** | **365,70 Go** | **0,08 s** | **47 Mo** |

### L'engram : 16 ms par entrée sur le disque mécanique

La sonde le chiffre : 10 000 entrées de 264 octets lues en 169 s depuis le
mécanique, soit **16 936 µs chacune** — un seek. Un jeton lit ~4 n-grammes × 2
couches : **128 ms par jeton** rien qu'en accès à la table.

D'où la copie de V4.1 sur le NVMe (`/home/stephane/FastNVMe/modeles-lourds/`,
exception documentée à la politique de stockage) : 698 Go libres, et un NVMe fait
0,07 ms par page au lieu de 16 ms.

```bash
# Le plan, avec ses raisons, sans charger de modèle
./drave-core/target/release/drave <modele-ou-dossier> --materiel --ctx 1048576
# La sonde d'engram (lecture parallèle, mémoire résidente affichée)
./drave-core/target/release/drave <modele-v4.1> --sonder-engram 20000
```


---

## Session « routage, MLA et formats » (01/10 22 h → 02/10) — ce qui était faux, et ce qui bloque encore

### Les portes, revérifiées

| porte | valeur | état |
|---|---|---|
| Qwen2.5-0.5B Q8_0 ctx 256 (dense) | **19,3885** | inchangée |
| Qwen3-30B en clusters ctx 64, 8 jetons | **799,8557** | inchangée |
| gpt-oss-120b MXFP4 ctx 256 | **15,6017** | **changée** (15,1757 avant) — voir ci-dessous |
| `cargo test --release` | **48** | 41 avant |
| `tools/portes_formats.sh` | **17 formats × 2 blocs** | tous exacts contre libggml |
| V4-Flash, 43 couches | **8 430,2968** à ctx 32 (4 jetons notés) | le modèle de la famille V4 tourne en entier — les trois régimes d'attention (brute, HCA, CSA + indexeur) dans la même passe. `tools/portes.sh` le vérifie |

**Pourquoi gpt-oss a changé.** Le moteur mettait le biais du routeur dans le
softmax des poids ; llama.cpp le met dans la **sélection** seulement
(`build_moe_ffn` : `weights = probs[selected]`, où `probs = softmax(logits)`
sans biais). L'ancien chiffre était auto-cohérent mais faux. Détail et
vérification : `reports/rapport-routage-experts.md`.

### Le routage des experts : quatre conventions, pas une

`expert_gating_func` existe dans les GGUF et n'était pas lu. Le moteur applique
maintenant la bonne convention par modèle — softmax (Qwen3), **sigmoïde**
(Kimi-K2.7, GLM-5.3), **racine de softplus** (DeepSeek-V4) — plus
`expert_weights_scale` (1,5 · 2,5 · 2,827), qui était purement absent, et le
routage **par table** (`ffn_gate_tid2eid`, I32) des 3 premières couches de
V4-Flash. `--config` montre la convention retenue ET sa provenance :

```bash
./target/release/drave <modele.gguf> --config     # 50 ms, sans charger le modèle
```

### La MLA à rang faible : trouvée fausse, puis validée

Le premier essai était **faux** : corrélation des logits −0,04 avec llama.cpp,
même jeton prédit à toutes les positions, perplexité 42,6 M contre 4 286. La
cause est une **asymétrie de disposition** entre les deux remontées KV :

| tenseur | déclaration llama.cpp | dimension rapide |
|---|---|---|
| `attn_k_b` | `{qk_nope, kv_lora, nh}` | la **sortie** (`qk_nope`) |
| `attn_v_b` | `{kv_lora, v, nh}` | l'**entrée** (`kv_lora`) |

Les écrire toutes deux « sortie rapide » donne des valeurs fausses de la bonne
forme. Après correction : **corrélation 0,999024**, **top-1 3/3**, perplexité
5 966 contre 4 286 (3 jetons froids).

**Mais la validation s'arrête là.** Sur 7 jetons notés, l'écart de NLL à
llama.cpp est de +0,009 à la position 0, +0,372 à la position 1, +0,611 à la
position 2, puis **+4,070 à la position 3** et redescend ensuite (perplexité
4 807,76 contre 890,4559). Un saut à une position précise n'est pas une
accumulation d'arrondis : un mécanisme s'enclenche. Première piste testée et
écartée : la quantification des activations lisait le tampon entier au lieu de
la tranche utile — corrigé, écart inchangé. Le prochain pas est outillé :
`ref_logits --tensors 'ffn_moe_out-3'` contre `DRAVE_DEBUG_MLA=1`, à la
position 3.

Ce qui a permis de le trouver, et qu'il faut réutiliser : `ref_logits` accepte
maintenant `--tensors REGEX` (il imprime les tenseurs nommés du graphe llama.cpp
pendant l'évaluation) et le moteur accepte `DRAVE_DEBUG_MLA=1` (mêmes grandeurs).
La comparaison a montré que `q_a`, `q_a_norm`, `c_kv`, `k_rope`, `q_rope`
concordaient à 1 % ; `kqv_out-0` a donné l'écart ; et la position 0 l'explique
en une ligne — à la position 0 l'attention n'a qu'une clé, donc `kqv_out = v_0`,
c'est-à-dire `wv_b` seul.

**Ce qui reste ouvert sur ce chemin** : la vitesse (l'attention MLA est en
scalaire et sans SIMD : ~20 s par jeton sur GLM-5.3 à cause des reconstructions
`k_nope`/`v` refaites pour chaque position), et l'absence de noyau IQ (la
déquantification domine le coût des experts).

### Ce que le moteur sait calculer, et ce qu'il ne sait pas

`--config` le dit avant toute panne. Au 02/10 :

| modèle | poids | calculable |
|---|---|---|
| Qwen3-30B-A3B, Qwen3-235B-A22B | 30 / 235 G | **oui** |
| gpt-oss-120b | 117 G | **oui** |
| GLM-5.3 (glm-dsa) | 754 G | **oui**, et validé contre llama.cpp (corrélation 0,999) |
| Kimi-K2.7 (deepseek2) | 1 026 G | **oui** (calculé : 161 s de chargement, 73 s/jeton) — non validé |
| GLM-5.3-Flash | 321 G | non — hyper-connexions |
| DeepSeek-V4-Flash / V4.1 | 284 / 755 G | non — hyper-connexions, index, sortie à rang faible |

**Aucun modèle DeepSeek-V4 n'a jamais été exécuté ici.** Tous les chiffres
publiés à leur sujet (empreinte, périodicité, miroir, sonde engram) viennent
d'analyses **statiques** des tenseurs. C'est écrit dans le message de refus du
moteur depuis cette session, pour que la distinction ne se perde pas.

### Formats : huit de plus, et un bug de facteur 2

Q5_K, Q5_0, Q5_1, Q3_K, IQ3_XXS, IQ1_S, IQ4_XS sont déquantifiés et comparés à
libggml **au bit près** ; l'échelle E8M0 de MXFP4 donnait des poids **deux fois
trop petits** (corrigé, test unitaire). Les formats de super-bloc sans noyau
(Q2_K, Q3_K, Q5_K, IQ1_S, IQ1_M, IQ2_XXS, IQ3_XXS, IQ4_XS) sont lus par
déquantification puis produit en f32 : juste par construction, plus lent qu'un
noyau dédié, et c'est ce qui rend GLM-5.3 et Kimi chargeables.

```bash
tools/portes_formats.sh          # 17 formats × 2 blocs, contre libggml
tools/extraire_tables_ggml.sh verifier   # les grilles IQ embarquées = celles de ggml
```

---

## Bilan de la session « routage, MLA et formats » (01/10 22 h → 02/10 07 h)

**16 commits.** Ce qui a changé, dans l'ordre d'importance :

1. **Le routage des experts était faux pour quatre gros modèles sur cinq.** Le
   moteur n'avait qu'un booléen là où les GGUF déclarent quatre conventions
   (`expert_gating_func`), et il ne lisait ni `expert_weights_scale` (1,5 · 2,5 ·
   2,827) ni `hash_layer_count` (la table `ffn_gate_tid2eid` de V4-Flash). Une
   seule implémentation les porte maintenant, partagée par le jeton seul et le
   lot ; quatre tests unitaires les encodent. Porte gpt-oss : 15,1757 → 15,6017,
   changement justifié par `build_moe_ffn` de llama.cpp (le biais ne départage
   que la sélection).
2. **Six déquantificateurs de plus** (Q5_K, Q5_0, Q5_1, Q3_K, IQ3_XXS, IQ1_S,
   IQ4_XS) et **un bug de facteur 2** trouvé dans MXFP4 (échelle E8M0 mélangée
   avec la grille doublée). 18 formats lisibles, 17 vérifiés contre libggml.
3. **L'attention MLA à rang faible**, qui débloque GLM-5.3 (754 G) et
   Kimi-K2.7 (1 026 G) — jamais calculés ici avant cette session. Deux bugs de
   disposition trouvés par comparaison à llama.cpp : `wv_b` rangé à l'envers de
   `wk_b` (corrélation −0,04 → **0,999024**) et l'indexation de tranche dans le
   lot parallèle.
4. **Trois tenseurs lus nulle part** : l'expert partagé (2D, jamais calculé !),
   le biais de sélection `exp_probs_b`, et la table `tid2eid`.
5. **`verifier_architecture` + `--config`** : le moteur dit en 50 ms, sans
   charger le modèle, ce qu'il sait calculer et ce qui manque — au lieu de mourir
   sur « tenseur blk.3.attn_q.weight absent », qui accuse le fichier.

**Chantier 2 de la feuille de route (tête garantie) : clos, et clos par une
mesure.** `--tete-garantie` est implémenté et **exact** (mêmes jetons générés
avec et sans), mais la borne de Cauchy-Schwarz vaut **12,6×** le logit maximal
sur les poids réels (18,0381 contre 1,4283), le raffinement par blocs de 32
n'apporte rien (12,4×), et la boucle finit par calculer **151 936 lignes sur
151 936**. Gain nul. Il n'existe pas, sur ces poids, de borne qui distingue les
lignes hors liste avant de les avoir lues : le seul gain réel reste
`--tete-restreinte` (×7), qui change la sortie. Détail :
[`reports/rapport-tete-garantie.md`](reports/rapport-tete-garantie.md).

**Chantiers 3 et 4 de la feuille de route.**

- **(3) accès mmappé à la table d'engram** : fait (`--sonder-engram`), mesuré
  sur le NVMe — une entrée de 264 octets coûte 17 276 entrées pour 10 000 jetons,
  soit 4,6 Mo touchés sur 203 Go adressés.
- **(4) chargeur d'experts à lecteurs parallèles** : mesuré sur fichier **froid**
  (fadvise DONTNEED, zones distinctes, 120 blocs de 4 Mo) — **×0,78 sur le
  disque mécanique et ×0,88 sur le NVMe**. Le parallélisme ne sert à rien ici :
  en défaut de page, le readahead du noyau sature déjà le périphérique avec un
  seul flux séquentiel, et sur le mécanique il s'ajoute aux déplacements de tête.
  Cinquième mesure de prélecture du dépôt, cinquième résultat nul — mais la
  première dont on connaît la raison. Outil :
  `tools/mesurer_lecture_experts.py`.

**Ce qui reste ouvert, par ordre de valeur :**

| chantier | où c'en est |
|---|---|
| l'écart MLA qui saute à la position 3 | mesuré (+4,07 nats), outillé, non expliqué |
| hyper-connexions (GLM-5.3-Flash, V4 x2) | non implémentées |
| attention par index (DSA) au-delà de `index_topk` | non implémentée |
| noyaux IQ | remplacés par déquantification + produit f32 (juste, lent) |
| vitesse MLA | ~190 s/jeton sur GLM-5.3, attention scalaire |


---

## Test d'exécution de DeepSeek-V4.1-Flash (02/10)

365,71 Go sur le NVMe. **Ce qui tourne est mesuré** : en-têtes 63,8 ms, `--config`
74 ms, plan matériel complet, sonde engram 10 000 entrées en 219-524 ms avec
**120 Mo de RSS pour 365,7 Go adressés**. **La passe avant est refusée en 0,33 s**
avec la liste exacte de ce qui manque, établie d'après `llama.cpp/src/models/deepseek4.cpp` :
hyper-connexions (4 copies de l'état + Sinkhorn), sortie à rang faible groupée
(`o_groups = 8`), dé-rotation de sortie + puits par tête, et **trois attentions
compressées CSA/HCA** selon `compress_ratios`. L'engram, lui, n'est pas un
obstacle : llama.cpp ne le calcule pas non plus.
Détail et estimation d'effort : [`reports/rapport-execution-v41.md`](reports/rapport-execution-v41.md).


---

## Plan pour exécuter DeepSeek-V4.1 (02/10)

[`docs/plan-deepseek41-complet.md`](docs/plan-deepseek41-complet.md) — neuf phases,
chacune avec une **porte** (commande + résultat attendu), un interdit et un budget.
Trois faits vérifiés le 02/10 le structurent :

1. **llama.cpp ne connaît pas `deepseek41`** (`unknown model architecture`) : il
   n'existe aucune référence externe pour V4.1 ;
2. **llama.cpp exécute V4-Flash** (`deepseek4`, 1 325 tenseurs chargés,
   NLL 11,737 sur un jeton froid) — c'est donc **V4-Flash le banc d'essai**, avec
   les mêmes mécanismes (hyper-connexions, MLA, compresseur, indexeur, table) et
   86,9 Go qui tiennent en RAM ;
3. **V4.1-Flash-Q2 n'a pas les tenseurs `output_hc_*`** alors qu'il déclare
   `hc_mult = 4` : fichier incomplet ou converti à tort — question de provenance à
   trancher avant d'écrire du code (phase P7).

**Le plan est écrit dans le vocabulaire de Drave, pas dans celui de llama.cpp** :
V4.1 est fait de flux qui sont déjà des listes — les 6 experts sur 384
(`--trace-experts`), la table `tid2eid` des 3 premières couches, la sélection de
blocs du compresseur (`attn_compressor_gate`), les **2 048 candidats** de
l'indexeur CSA, les **24 connexions pondérées** du mélange hyper-connexions, et
les adresses d'engram. Trois de ces flux n'existent dans aucun moteur connu, et
les tracer est notre apport. Chaque phase a donc **deux portes** : la correction
(comparaison à llama.cpp sur V4-Flash) **et** Drave (événements par jeton, trace
rejouée à l'identique, découpage en grappes, flux lisible par un outil).

Premier écart à combler, et il passe avant la conformité des logits : une passe
de V4.1 afficherait aujourd'hui **« 0 événements »**, parce que le chemin MLA et
le chemin experts-IQ travaillent en f32 dense.

Le contrôle d'architecture est la liste vivante du chantier : il perd une ligne
par phase franchie (`--config` le montre en 74 ms, sans charger le modèle).
